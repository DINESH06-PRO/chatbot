from django.urls import path
from . import views

urlpatterns = [
    # Auth
    path('',        views.login_view,  name='home'),
    path('login/',  views.login_view,  name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('logout/', views.logout_view, name='logout'),

    # Chat UI
    path('chat/', views.chat_view, name='chat'),

    # JSON APIs
    path('api/send/',           views.send_message_api,    name='send_message_api'),
    path('api/delete/<int:chat_id>/', views.delete_chat_api, name='delete_chat_api'),
    path('api/delete-all/',     views.delete_all_chats_api, name='delete_all_chats_api'),
    path('api/messages/<int:chat_id>/', views.get_chat_messages_api, name='get_chat_messages_api'),
]
