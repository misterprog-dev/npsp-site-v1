from django.shortcuts import render
from django.views.generic import TemplateView
from commande.models import CommandeModel, DetailsCommandeModel
from medicament.models import Medicament, TypeMedicament
from inscription.models import Client

def passer_commande_page(request = '', **kwargs):
    if request.method == 'POST':
        products = request.POST.getlist('products')
        quantities = request.POST.getlist('quantities')
        date_livraison = request.POST.get('date_livraison')

        client = Client.objects.get(email = request.user.email)
        #print(client)
        commande = CommandeModel(client = client, date_livraison = date_livraison)
        commande.save()

        #On enregistre les détails de la commande du client
        id_commande = CommandeModel.objects.get(client = client, etat_commande = 0)
        #print(id_commande)
        
        for i in range(len(products)):
            id_med = Medicament.objects.get(id = products[i])
            qtite = quantities[i]
            details = DetailsCommandeModel(id_commande = id_commande, id_medicament = id_med, quantite_med = qtite)
            details.save()                        

        medicaments = Medicament.objects.all()
        return render(request, 'commandes/passer_commande.html', {'medicaments': medicaments, 'message':'Commande validée avec succès !!!!'})
    else:
        medicaments = Medicament.objects.all()
        return render(request, 'commandes/passer_commande.html', {'medicaments': medicaments})


def gerer_commande_page(request, **kwargs):
    details = DetailsCommandeModel.objects.all()
    commandes = CommandeModel.objects.all()
    return render(request, 'commandes/gerer_commande.html', {'details': details, 'commandes': commandes})

def supp_commande(request, id):
    details = DetailsCommandeModel.objects.filter(id_commande=id)
    details.delete()
    commandes = CommandeModel.objects.filter(id=id)
    commandes.delete()

    details = DetailsCommandeModel.objects.all()
    commandes = CommandeModel.objects.all()
    return render(request, 'commandes/gerer_commande.html', {'details': details, 'commandes': commandes})

def historique_commande_page(request, **kwargs):
    details = DetailsCommandeModel.objects.all()
    commandes = CommandeModel.objects.all()
    return render(request, 'commandes/historique_commande.html', {'details': details, 'commandes': commandes})