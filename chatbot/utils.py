"""
Utility: AI response generation + Tanglish support.
Works in demo mode without an API key.
With ANTHROPIC_API_KEY set, uses Claude AI.
"""
import json
import os


def get_language_system_prompt(language):
    prompts = {
        'en': (
            "You are a helpful, friendly AI assistant called NeuralChat. "
            "Respond clearly and concisely in English."
        ),
        'ta': (
            "நீங்கள் NeuralChat என்ற AI உதவியாளர். "
            "தமிழிலேயே மட்டும் பதில் சொல்லுங்கள். "
            "தெளிவாகவும் இயல்பாகவும் பேசுங்கள்."
        ),
        'tg': (
            "You are NeuralChat, a friendly AI assistant who responds in Tanglish — "
            "Tamil words written in English letters mixed naturally with English. "
            "Example style: 'Vanakkam! Naan ungalukku help pannuven. Enna theriyanum sollu!' "
            "Use Tamil words like: nalla, romba, seri, paaru, theriyuma, aamam, illai, "
            "enna, epdi, yaar, enga, ippo, apram, vanakkam, nandri, santhosham. "
            "Keep it casual, warm, and fun."
        ),
    }
    return prompts.get(language, prompts['en'])


def generate_ai_response(user_message, language='en', chat_history=None):
    """
    Generate AI response. Uses Claude API if key is set, else demo mode.
    """
    api_key = os.environ.get('ANTHROPIC_API_KEY', '')
    if api_key and api_key.startswith('sk-ant'):
        try:
            return _call_claude_api(user_message, language, chat_history or [], api_key)
        except Exception:
            pass
    return _demo_response(user_message, language)


def _call_claude_api(user_message, language, chat_history, api_key):
    import urllib.request
    import urllib.error

    messages = []
    for h in chat_history[-6:]:
        messages.append({"role": "user", "content": h['user_message']})
        if h.get('ai_response'):
            messages.append({"role": "assistant", "content": h['ai_response']})
    messages.append({"role": "user", "content": user_message})

    payload = json.dumps({
        "model": "claude-sonnet-4-20250514",
        "max_tokens": 1024,
        "system": get_language_system_prompt(language),
        "messages": messages,
    }).encode('utf-8')

    req = urllib.request.Request(
        'https://api.anthropic.com/v1/messages',
        data=payload,
        headers={
            'Content-Type': 'application/json',
            'x-api-key': api_key,
            'anthropic-version': '2023-06-01',
        },
        method='POST',
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        data = json.loads(resp.read().decode('utf-8'))
        return data['content'][0]['text']


def _demo_response(user_message, language):
    """Smart demo responses in all three languages."""
    msg = user_message.lower().strip()

    # ── English ──────────────────────────────────────────
    if language == 'en':
        if any(w in msg for w in ['hello', 'hi', 'hey']):
            return ("Hello! 👋 I'm NeuralChat AI, your intelligent assistant.\n\n"
                    "I can help you with questions, writing, analysis, coding, and much more.\n"
                    "What would you like to explore today?")
        if 'how are you' in msg:
            return "I'm running perfectly and ready to help! 😊 What's on your mind?"
        if any(w in msg for w in ['what can you do', 'help', 'capabilities']):
            return ("Here's what I can help you with:\n\n"
                    "• 💬 Answer any question\n"
                    "• ✍️ Writing & editing\n"
                    "• 🐍 Code (Python, JS, etc.)\n"
                    "• 📊 Analysis & research\n"
                    "• 🌐 English, Tamil & Tanglish\n\n"
                    "Just ask me anything!")
        if any(w in msg for w in ['thank', 'thanks']):
            return "You're welcome! 😊 Happy to help anytime. What else can I do for you?"
        if any(w in msg for w in ['bye', 'goodbye']):
            return "Goodbye! 👋 Come back anytime. Have a great day!"
        if 'tamil' in msg:
            return ("Tamil (தமிழ்) is one of the world's oldest classical languages, "
                    "spoken by over 80 million people worldwide. It has a rich literary "
                    "tradition dating back more than 2,000 years.\n\n"
                    "Switch to Tamil mode (🇮🇳 TA) to chat in Tamil!")
        if 'tanglish' in msg:
            return ("Tanglish is Tamil written in English letters — super popular among "
                    "Tamil speakers online and in text messages!\n\n"
                    "Example: 'Vanakkam! Naan ungalukku help pannuven.'\n\n"
                    "Switch to Tanglish mode (✨ TG) to try it!")
        if any(w in msg for w in ['who are you', 'what are you']):
            return ("I'm NeuralChat AI — a multilingual chatbot built with Django and "
                    "powered by Claude AI.\n\n"
                    "I support English 🇺🇸, Tamil 🇮🇳, and Tanglish ✨.\n\n"
                    "To unlock full AI responses, set your ANTHROPIC_API_KEY.")
        return (f"You asked: \"{user_message}\"\n\n"
                "I'm running in demo mode right now. To get full AI-powered responses:\n\n"
                "1. Get a free API key at console.anthropic.com\n"
                "2. Set environment variable: ANTHROPIC_API_KEY=sk-ant-...\n"
                "3. Restart the server\n\n"
                "Until then, I can still answer greetings and common questions! 😊")

    # ── Tamil ─────────────────────────────────────────────
    elif language == 'ta':
        if any(w in msg for w in ['hello', 'hi', 'வணக்கம்', 'vanakkam']):
            return ("வணக்கம்! 👋 நான் NeuralChat AI.\n\n"
                    "நான் உங்களுக்கு கேள்விகளுக்கு பதில் சொல்வேன், "
                    "எழுத்து வேலைகளில் உதவுவேன், மற்றும் பல.\n\n"
                    "என்ன கேட்கணும்?")
        if 'எப்படி இருக்கீங்க' in msg or 'how are you' in msg:
            return "நான் நலமாக இருக்கிறேன், நன்றி! 😊 உங்களுக்கு என்ன உதவி வேண்டும்?"
        if any(w in msg for w in ['help', 'உதவி', 'என்ன செய்வீர்']):
            return ("நான் இவற்றில் உதவ முடியும்:\n\n"
                    "• கேள்விகளுக்கு பதில் சொல்வேன்\n"
                    "• தமிழில் எழுத உதவுவேன்\n"
                    "• குறியீடு எழுத உதவுவேன்\n"
                    "• ஆராய்ச்சியில் உதவுவேன்\n\n"
                    "என்ன வேண்டும் சொல்லுங்கள்!")
        if any(w in msg for w in ['நன்றி', 'thanks', 'thank']):
            return "நன்றி! 😊 வேறு ஏதாவது கேட்கணுமா?"
        if any(w in msg for w in ['bye', 'போகிறேன்', 'சரி']):
            return "போய் வாருங்கள்! 👋 மீண்டும் பேசுவோம்!"
        return (f"நீங்கள் கேட்டது: \"{user_message}\"\n\n"
                "நான் இப்போது demo mode-ல் இயங்குகிறேன். "
                "முழு AI திறனுக்கு ANTHROPIC_API_KEY அமைக்கவும்.\n\n"
                "ஆனால் எளிய கேள்விகளுக்கு பதில் சொல்ல முடியும்! 😊")

    # ── Tanglish ──────────────────────────────────────────
    else:
        if any(w in msg for w in ['hello', 'hi', 'hey', 'vanakkam']):
            return ("Vanakkam! 👋 Naan NeuralChat AI.\n\n"
                    "Naan ungalukku kelvikku pathil solluven, "
                    "writing help pannuven, code debug pannuven — romba things pannuven!\n\n"
                    "Enna theriyanum? Sollu da!")
        if 'eppadi irukkinga' in msg or 'how are you' in msg or 'eppadi iruka' in msg:
            return "Romba nalla iruken, nandri! 😊 Neenga eppadi irukinga? Enna help venum?"
        if any(w in msg for w in ['help', 'udhavi', 'enna pannuva']):
            return ("Paaru, naan ungalukku romba things help pannuven:\n\n"
                    "• Kelvikku pathil solluven 💬\n"
                    "• Tamil, English, Tanglish-la pesuvom 🌐\n"
                    "• Code help pannuven 🐍\n"
                    "• Writing help pannuven ✍️\n\n"
                    "Enna venum sollu, pannuven!")
        if any(w in msg for w in ['nandri', 'thanks', 'thank']):
            return "Ayyo nandri vendam da! 😊 Ungalukku help panradhu ennakku santhosham!"
        if any(w in msg for w in ['bye', 'poitu vara', 'seri da']):
            return "Seri da, poitu va! 👋 Apparam pesuvom. Take care!"
        if 'tamil' in msg:
            return ("Tamil — romba pழைய, romba azhagana language da! 🙏\n\n"
                    "2000+ years history iruku. 80 million people pesuvanga worldwide.\n\n"
                    "Tamil mode (🇮🇳 TA) switch pannitu Tamil-la pesi paaru!")
        return (f"Neeyum sonna: \"{user_message}\"\n\n"
                "Ippo naan demo mode-la iruken da. "
                "Full AI power vekka:\n\n"
                "1. console.anthropic.com-la free key edhu\n"
                "2. ANTHROPIC_API_KEY set pannu\n"
                "3. Server restart pannu\n\n"
                "Apram nee yedha keteelum full answer solluven! 😊")
