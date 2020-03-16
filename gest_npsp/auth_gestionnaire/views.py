from django.shortcuts import render, redirect
from django.views.generic import TemplateView 
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import HttpResponseRedirect


# Create your views here.

def LoginPageView(request = '', **kwargs):
    if request.method == 'POST':
        username = request.POST.get('username_gest')
        password = request.POST.get('password_gest')

        user = authenticate(request, username=username, password=password)
        if user is not None:           
            login(request, user)
            return render(request, 'gestionnaire/ajouter_client.html', context = None)
        else:
            messages.info(request, 'Email ou mot de passe incorrecte !')
    
    return render(request, 'gestionnaire/login.html', context = None)

def LogoutPageView(request):
    logout(request)
    return HttpResponseRedirect('/gestionnaire/')
    #return render(request, 'gestionnaire/login.html', context = None)
