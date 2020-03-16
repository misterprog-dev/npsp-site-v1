from django.contrib import admin
from .models import TypeMedicament, Medicament

@admin.register(TypeMedicament)
class TypeMedicamentAdmin(admin.ModelAdmin):
    list_display = ('libelle', 'created_at', 'updated_at',)
    ordering = ('libelle', )
    search_fields = ('libelle',)

@admin.register(Medicament)
class MedicamentAdmin(admin.ModelAdmin):
    list_display = ('code_produit', 'libelle_produit', 'dosage', 'unite', 'type_medicament', 'kilo_paquet', 'created_at', 'updated_at')
    ordering = ('code_produit', 'libelle_produit' )
    search_fields = ('code_produit', 'libelle_produit')
