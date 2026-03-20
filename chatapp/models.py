from django.db import models

class Document(models.Model):
    file = models.FileField(upload_to='docs/')
    extracted_text = models.TextField(blank=True)

class Chat(models.Model):
    user_message = models.TextField()
    bot_response = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)