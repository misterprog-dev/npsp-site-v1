from django.db import models
import uuid

#Models typeMedicament
class TypeMedicament(models.Model):
    libelle = models.CharField(max_length=300, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


#Models Medicament
class Medicament(models.Model):
    UNITE = (
        ('g', 'gramme'),
        ('mg', 'milligramme'),
    )
    code_produit = models.CharField(max_length=300, unique=True)
    libelle_produit = models.CharField(max_length=300)
    dosage = models.IntegerField()
    unite = models.CharField(max_length=5, choices=UNITE)
    type_medicament = models.ForeignKey(TypeMedicament, on_delete=models.CASCADE, default=None,)
    kilo_paquet = models.DecimalField(max_digits=15, decimal_places=10, default = 1.0000000000)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['code_produit']
