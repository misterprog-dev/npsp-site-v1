from django.db import models
import uuid
from django import forms
from medicament.models import Medicament
from inscription.models import Client

class CommandeModel(models.Model):
    client = models.ForeignKey(Client, to_field='id',
                                 on_delete=models.CASCADE, default=None, ) 
    date_commande = models.DateTimeField(auto_now_add=True)
    date_livraison = models.DateField(default=None)
    #delay = models.BigIntegerField()
    etat_commande = models.PositiveSmallIntegerField(default=0,)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) 

    def save(self, *args, **kwargs):
        #self.delay = 
        super(CommandeModel, self).save(*args, **kwargs)

class DetailsCommandeModel(models.Model):
    id_commande= models.ForeignKey(CommandeModel, on_delete=models.CASCADE)
    id_medicament = models.ForeignKey(Medicament, on_delete=models.CASCADE)
    quantite_med = models.DecimalField(max_digits=10,
                                 help_text="La quantité en carton", max_length=20, decimal_places=2, default=0.0) 
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) 
                                    