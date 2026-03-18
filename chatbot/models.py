from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Chat(models.Model):
    LANGUAGE_CHOICES = [
        ('en', 'English'),
        ('ta', 'Tamil'),
        ('tg', 'Tanglish'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chats')
    title = models.CharField(max_length=255, default='New Chat')
    language = models.CharField(max_length=5, choices=LANGUAGE_CHOICES, default='en')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_at']

    def __str__(self):
        return f"{self.user.username} - {self.title[:40]}"


class Message(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name='messages')
    user_message = models.TextField()
    ai_response = models.TextField(blank=True, default='')
    timestamp = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['timestamp']

    def __str__(self):
        return f"[{self.timestamp.strftime('%Y-%m-%d %H:%M')}] {self.user_message[:50]}"
