from django.urls import path
from .views import upload_document, chat, chat_ui

urlpatterns = [
    # API Routes
    path('upload/', upload_document, name='upload_document'),
    path('chat/', chat, name='chat_api'),

    # Frontend UI
    path('', chat_ui, name='chat_ui'),
]