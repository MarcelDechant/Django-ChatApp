from django.db import models
from django.db.models.fields import DateField
from datetime import date
from django.conf import settings

# Create your models here.

class Chat(models.Model):
    created_at = models.DateField(default=date.today)

class Message(models.Model):
    text = models.CharField(max_length=500)
    created_at = DateField(default=date.today)
    #chat = Chat Klasse verknüpfen
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name='chat_message_set', default=None, blank=True, null=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='author_message_set')
    # => settings.AUTH_USER_MODEL => Klasse des aktuellen Users > Default Funktionalität von Django
    # => on_delete=models.CASCADE => wenn ein nutzer aus dem System gelöscht wird, werden auch alle Daten die 
    #    mit diesem Nutzers verknüpft sind, gelöscht. 
    # => related_name='author_message_set' => Information welche die Datenbank benötigt. Da es sich um zwei verknüpfte Objekte handelt 
    #    > author welcher der User ist und die Message
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='receiver')