from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import ContactModel

@login_required
def HomePageView(request = '', **kwargs):
    return render(request, 'index.html', context=None)

@login_required
def AboutPageView(request = '', **kwargs):
    return render(request, 'about.html', context=None)

@login_required
def show_contact_form(request = '', **kwargs):
    return render(request, 'contact.html', context=None)

@login_required
def add_contact(request = '', **kwargs):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        contact = ContactModel(nom=name, email=email, sujet=subject, message=message)
        contact.save()
        
        return render(request, 'contact.html', {'message_succes':'Votre message a été envoyé avec succès !'})
    
    return render(request, 'contact.html', {'message_echec':"Echec de l'envoi du message !"})   
