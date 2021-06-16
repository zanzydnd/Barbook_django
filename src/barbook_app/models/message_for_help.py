from django.db import models


class Message(models.Model):
    message_text = models.TextField(max_length=300)
    author_email = models.EmailField()
    created_at = models.DateTimeField(auto_now=True)
    still_relevant = models.BooleanField(default=True)
    author_name = models.CharField(max_length=200, null=True)

    class Meta:
        db_table = "help_message"
        verbose_name = "Сообщение поддержке"
        verbose_name_plural = "Сообщения поддержке"
