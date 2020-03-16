from django.conf import settings
from django.contrib import admin
from .models import Gestionnaire, TypeClient, Client

@admin.register(Gestionnaire)
class GestionnaireAdmin(admin.ModelAdmin):
    list_display = ('nom', 'prenom', 'email', 'contact', 'commune',)
    ordering = ('nom', )
    search_fields = ('nom', 'prenom', 'email', 'commune')

@admin.register(TypeClient)
class TypeClientAdmin(admin.ModelAdmin):
    list_display = ('libelle',)
    ordering = ('libelle', )
    search_fields = ('libelle',)

# @admin.register(Adresse)
# class AdresseAdmin(admin.ModelAdmin):
#     list_display = ('ville', 'location')
#     ordering = ('ville', )
#     search_fields = ('libelle',)

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('nom', 'prenom', 'email', 'contact', 'ville', 'x', 'y')
    ordering = ('nom', 'prenom', )
    search_fields = ('nom', 'prenom', 'ville')
    
