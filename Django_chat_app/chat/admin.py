from django.contrib import admin
from .models import Chat, Message


class MessageAdmin(admin.ModelAdmin):
    fields = ('chat', 'text', 'created_at', 'author', 'receiver') #Felder die den Messages angezeigt werden sollen
    list_display = ('chat', 'text', 'created_at', 'author', 'receiver') # Spaltenüberschrift
    search_fields = ('text',) # Fügt ein Textfeld hinzug und filtert Nachrichten mit dem entsprechenden Text


# Register your models here.
admin.site.register(Message, MessageAdmin)
admin.site.register(Chat)
