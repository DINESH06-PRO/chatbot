from django.contrib import admin
from .models import Chat, Message


class MessageInline(admin.TabularInline):
    model = Message
    extra = 0
    readonly_fields = ('timestamp',)


@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'language', 'created_at', 'updated_at')
    list_filter = ('language', 'user')
    search_fields = ('user__username', 'title')
    inlines = [MessageInline]


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('chat', 'user_message', 'timestamp')
    search_fields = ('user_message', 'ai_response')
    readonly_fields = ('timestamp',)
