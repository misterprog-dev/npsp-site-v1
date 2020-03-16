from django.contrib import admin
from .models import CommandeModel, DetailsCommandeModel

@admin.register(CommandeModel)
class CommandeModelAdmin(admin.ModelAdmin):
    list_display = ('client','date_commande', 'date_livraison', 'date_livraison', 'etat_commande', 'date_commande')
    ordering = ('client', )
    search_fields = ('date_livraison', 'date_commande')

@admin.register(DetailsCommandeModel)
class DetailsCommandeAdmin(admin.ModelAdmin):
    list_display = ('id_commande', 'id_medicament','quantite_med',)
    ordering = ('id_commande', 'id_medicament', 'quantite_med')
    search_fields = ('id_medicament', 'quantite_med')