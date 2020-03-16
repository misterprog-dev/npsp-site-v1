from django.shortcuts import render
from django.contrib.auth.models import User
from django.views.generic import TemplateView 
from .models import Client, TypeClient

import string
import random
import bcrypt

def get_hashed_password(pwd):
    return bcrypt.hashpw(pwd.encode('utf-8'), bcrypt.gensalt())

def check_password(pwd, hashed_password):
    return bcrypt.checkpw(pwd.encode('utf-8'), hashed_password.encode('utf-8'))

def validate_inscription_client(request = '', **kwargs):
    nom = request.POST.get("nom")
    prenom = request.POST.get("prenom")
    typeclient = TypeClient.objects.all().get(id=request.POST.get("typeclient"))
    email = request.POST.get("email")
    contact = request.POST.get("contact")
    service_time = request.POST.get("service_time")
    pwd = get_hashed_password(request.POST.get("password"))
    password = bcrypt.hashpw(pwd, bcrypt.gensalt())
    ville = request.POST.get("ville")
    x = request.POST.get("x")
    y = request.POST.get("y")

    #On le met dans la liste des users pour l'authentification
    user = User.objects.create_user(email, email, password)
    user.last_name = prenom
    user.first_name = nom
    user.save()

    client = Client(nom = nom, prenom=prenom, type_client=typeclient, email=email,contact=contact, service_time = service_time, password = password, ville=ville, x=x, y=y )
    client.save()

    typeClient = TypeClient.objects.all()
    pwd = ''.join([random.choice(string.digits + string.ascii_letters) for i in range(0, 10)])
    
    return render(request, 'gestionnaire/ajouter_client.html', 
                    {'message_inscription':'Inscription effectuée avec succès !', 
                    'typeClient':typeClient,
                    'pwd': pwd})
