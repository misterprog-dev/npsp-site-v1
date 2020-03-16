from django.db import models
import uuid

class ContactModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text='Unique ID for client contact', editable=False)
    nom = models.CharField(max_length=50, blank=True)
    email = models.EmailField(max_length=50,)
    sujet = models.CharField(max_length=150, blank=True)
    message = models.TextField()   