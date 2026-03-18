# Generated migration for NeuralChat AI chatbot
# This file is pre-built. Just run: python manage.py migrate

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Chat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='New Chat', max_length=255)),
                ('language', models.CharField(
                    choices=[('en', 'English'), ('ta', 'Tamil'), ('tg', 'Tanglish')],
                    default='en',
                    max_length=5,
                )),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='chats',
                    to=settings.AUTH_USER_MODEL,
                )),
            ],
            options={
                'ordering': ['-updated_at'],
            },
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_message', models.TextField()),
                ('ai_response', models.TextField(blank=True, default='')),
                ('timestamp', models.DateTimeField(default=django.utils.timezone.now)),
                ('chat', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='messages',
                    to='chatbot.chat',
                )),
            ],
            options={
                'ordering': ['timestamp'],
            },
        ),
    ]
