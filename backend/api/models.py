from django.db import models

# Create your models here.
class ChatHistory(models.Model):
    chat_history = models.TextField(blank=True, default="")

    def __str__(self):
        return f"{self.pk}"