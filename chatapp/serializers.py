from rest_framework import serializers
from .models import Document, Chat


class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ['id', 'file', 'extracted_text', 'uploaded_at']
        read_only_fields = ['id', 'uploaded_at']


class ChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields = ['id', 'user_message', 'bot_response', 'created_at']
        read_only_fields = ['id', 'created_at']