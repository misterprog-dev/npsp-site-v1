from django.shortcuts import render, redirect
from django.views.generic import TemplateView 
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import HttpResponseRedirect

def LoginPageView(request = '', **kwargs):
    if request.method == 'POST':
        username = request.POST.get('email_cust')
        password = request.POST.get('password_cust')
        print(username + " " + password) 

        user = authenticate(request, username=username, password=password)
        print(user)
        if user is not None:           
            login(request, user)
            return HttpResponseRedirect('/home/')
        else:
            messages.info(request, 'Email ou mot de passe incorrecte !')
    
    return render(request, 'login.html', context = None)

def LogoutPageView(request = ''):
    logout(request)
    return HttpResponseRedirect('/')
