from django.shortcuts import render
import string
import random   
from inscription.models import TypeClient, Client
from commande.models import CommandeModel, DetailsCommandeModel
from medicament.models import Medicament, TypeMedicament
from others.models import ContactModel

def password():
    return ''.join([random.choice(string.digits + string.ascii_letters) for i in range(0, 10)])

def gestionnaire_dashboard_page(request = '', **kwargs):
    if request.user.is_authenticated:
        return render(request, 'gestionnaire/dashboard.html', context=None)
    else:
        return render(request, 'gestionnaire/login.html', context = None)        

def gestionnaire_ajoutclient_page(request = '', **kwargs):
    if request.user.is_authenticated:
        typeClient = TypeClient.objects.all()
        return render(request, 'gestionnaire/ajouter_client.html', {'typeClient': typeClient, 'pwd': password()})
    else:
        return render(request, 'gestionnaire/login.html', context = None) 

def gestionnaire_gererclient_page(request = '', **kwargs):
    if request.user.is_authenticated:
        clients = Client.objects.all()        
        return render(request, 'gestionnaire/gerer_client.html', {'clients': clients})
    else:
        return render(request, 'gestionnaire/login.html', context = None) 

def deleteclient(request, id):
    if request.user.is_authenticated:
        client = Client.objects.get(id=id)
        client.delete()
        clients = Client.objects.all()       
        return render(request, 'gestionnaire/gerer_client.html', {'clients': clients})
    else:
        return render(request, 'gestionnaire/login.html', context = None) 

def valider_commande(request, id):
    if request.user.is_authenticated:
        commande = CommandeModel.objects.filter(id=id).update(etat_commande=1)
        details_commande = DetailsCommandeModel.objects.all()
        commande = CommandeModel.objects.all()
        return render(request, 'gestionnaire/commandes.html', {'commandes': commande, 'details': details_commande})
    else:
        return render(request, 'gestionnaire/login.html', context = None) 

def gestionnaire_commandes_page(request = '', **kwargs):
    """commandes = CommandeModel.objects.filter(etat_commande=0)        
    resultat = {}
    i = -1
    for c in commandes:
        i = i + 1
        details_cde = DetailsCommandeModel.objects.filter(id_commande = c.id)
        #print(details_cde[i])
        qte_totale = 0
        res = {}
        for d in details_cde:    
                    
            medicament = Medicament.objects.get(id = details_cde[i].id)
            type_medicament = TypeMedicament.objects.get(id = medicament.id).libelle
            drug = medicament.libelle_produit
            qte = details_cde[i].quantite_med
            aux = {}
            aux["medicament"] = drug
            aux["type"] = type_medicament
            aux["qte"] = qte
            res[d.id] = aux
            qte_totale = qte_totale + qte
        aux = {}
        aux["medicaments"] = res
        aux["quantite_totale"] = qte_totale
        resultat[c.id] = aux
    #print(Resultat)"""
    if request.user.is_authenticated:
        details_commande = DetailsCommandeModel.objects.all()
        commande = CommandeModel.objects.all()
        return render(request, 'gestionnaire/commandes.html', {'commandes': commande, 'details': details_commande})
    else:
        return render(request, 'gestionnaire/login.html', context = None) 

def gestionnaire_itineraire_page(request = '', **kwargs):
    if request.user.is_authenticated:
        return render(request, 'gestionnaire/maps.html', context=None)
    else:
        return render(request, 'gestionnaire/login.html', context = None)

def gestionnaire_messages_page(request = '', **kwargs):
    if request.user.is_authenticated:
        contacts = ContactModel.objects.all()
        return render(request, 'gestionnaire/messages.html', {'contacts': contacts})
    else:
        return render(request, 'gestionnaire/login.html', context = None)

def itineraire_page(request = '', **kwargs):
    return render(request, 'gestionnaire/itineraire.html', context=None)