"""
Views for NeuralChat AI — Authentication + Chat API
"""
import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.utils import timezone

from .models import Chat, Message
from .utils import generate_ai_response


# ─── Authentication ─────────────────────────────────────────────────────────

def signup_view(request):
    if request.user.is_authenticated:
        return redirect('chat')

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        email    = request.POST.get('email', '').strip()
        password1 = request.POST.get('password1', '')
        password2 = request.POST.get('password2', '')

        errors = []
        if len(username) < 3:
            errors.append('Username must be at least 3 characters.')
        elif User.objects.filter(username=username).exists():
            errors.append('Username already taken.')
        if not email:
            errors.append('Email is required.')
        elif User.objects.filter(email=email).exists():
            errors.append('Email already registered.')
        if len(password1) < 8:
            errors.append('Password must be at least 8 characters.')
        elif password1 != password2:
            errors.append('Passwords do not match.')

        if errors:
            return render(request, 'chatbot/signup.html', {
                'errors': errors, 'username': username, 'email': email
            })

        user = User.objects.create_user(username=username, email=email, password=password1)
        login(request, user)
        return redirect('chat')

    return render(request, 'chatbot/signup.html')


def login_view(request):
    if request.user.is_authenticated:
        return redirect('chat')

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('chat')
        return render(request, 'chatbot/login.html', {
            'error': 'Invalid username or password.', 'username': username
        })

    return render(request, 'chatbot/login.html')


def logout_view(request):
    logout(request)
    return redirect('login')


# ─── Chat ────────────────────────────────────────────────────────────────────

@login_required
def chat_view(request):
    user_chats = Chat.objects.filter(user=request.user).order_by('-updated_at')

    active_chat = None
    chat_messages = []
    chat_id = request.GET.get('chat_id')
    if chat_id:
        try:
            active_chat = Chat.objects.get(id=int(chat_id), user=request.user)
            chat_messages = active_chat.messages.order_by('timestamp')
        except (Chat.DoesNotExist, ValueError):
            return redirect('chat')

    return render(request, 'chatbot/chat.html', {
        'user_chats': user_chats,
        'active_chat': active_chat,
        'chat_messages': chat_messages,
    })


# ─── APIs ────────────────────────────────────────────────────────────────────

@login_required
@require_POST
def send_message_api(request):
    try:
        data = json.loads(request.body)
        user_message = data.get('message', '').strip()
        language     = data.get('language', 'en')
        chat_id      = data.get('chat_id')

        if not user_message:
            return JsonResponse({'error': 'Message cannot be empty.'}, status=400)
        if language not in ('en', 'ta', 'tg'):
            language = 'en'

        # Get or create chat
        if chat_id:
            try:
                chat = Chat.objects.get(id=int(chat_id), user=request.user)
                chat.language = language
                chat.save(update_fields=['language'])
            except (Chat.DoesNotExist, ValueError):
                return JsonResponse({'error': 'Chat not found.'}, status=404)
        else:
            title = user_message[:60] + ('…' if len(user_message) > 60 else '')
            chat = Chat.objects.create(user=request.user, title=title, language=language)

        # Recent history for context
        history = list(
            chat.messages.order_by('-timestamp')[:6].values('user_message', 'ai_response')
        )
        history.reverse()

        # Generate response
        ai_response = generate_ai_response(user_message, language, history)

        # Save message
        msg = Message.objects.create(
            chat=chat,
            user_message=user_message,
            ai_response=ai_response,
        )
        Chat.objects.filter(id=chat.id).update(updated_at=timezone.now())

        return JsonResponse({
            'success': True,
            'chat_id': chat.id,
            'chat_title': chat.title,
            'ai_response': ai_response,
            'timestamp': msg.timestamp.strftime('%I:%M %p'),
        })

    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON.'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@login_required
@require_POST
def delete_chat_api(request, chat_id):
    try:
        chat = get_object_or_404(Chat, id=chat_id, user=request.user)
        chat.delete()
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@login_required
@require_POST
def delete_all_chats_api(request):
    try:
        Chat.objects.filter(user=request.user).delete()
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@login_required
def get_chat_messages_api(request, chat_id):
    try:
        chat = get_object_or_404(Chat, id=chat_id, user=request.user)
        messages_data = [
            {
                'id': m.id,
                'user_message': m.user_message,
                'ai_response': m.ai_response,
                'timestamp': m.timestamp.strftime('%I:%M %p'),
            }
            for m in chat.messages.order_by('timestamp')
        ]
        return JsonResponse({
            'success': True,
            'chat_id': chat.id,
            'chat_title': chat.title,
            'language': chat.language,
            'messages': messages_data,
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
