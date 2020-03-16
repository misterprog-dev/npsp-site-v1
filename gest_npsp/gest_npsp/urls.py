"""gest_npsp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.views.generic import TemplateView
from inscription import views as insc_view
from commande import views as cde_view
from others import views as others_view
from statistique.views import StatistiquePageView
from authentification import views as auth_custo_view
from auth_gestionnaire import views as auth_gest_view
from livraison import views as livraison_view
from gestionnaire import views as gestionnaire_view

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    #CLient
    url(r'^$', auth_custo_view.LoginPageView, name="login_customer"),
    url(r'^logout_customer/', auth_custo_view.LogoutPageView, name="logout_customer"),
    url(r'^home/', others_view.HomePageView, name="index"),
    url(r'^contact/', others_view.show_contact_form , name="contact"),
    url(r'^send_contact/', others_view.add_contact,  name="send_contact"),
    url(r'^about/', others_view.AboutPageView, name="about"),
    
    url(r'^passer_commande/', cde_view.passer_commande_page, name="passer_commande"),  
    url(r'^gerer_commande/', cde_view.gerer_commande_page, name="gerer_commande"),  
    url(r'^supp_commande/(?P<id>.*)', cde_view.supp_commande, name="supp_commande"),  
    url(r'^historique_commande/', cde_view.historique_commande_page, name="historique_commande"),  

    # url(r'^planning/', PlanningPageView.as_view(), name="planning"),
    # url(r'^statistique/', StatistiquePageView.as_view(), name="statistique"),     

    # url(r'^validate_commande_client/', cde_view.validate_commande_client, name="validate_commande_client"),
    # url(r'^valider_commande_page/', cde_view.show_valider_commande_page, name="valider_commande_page"),  
    # url(r'^validate_commande_client_livraison/', cde_view.validate_commande_client_livraison, name="validate_commande_client_livraison"),

    #Gestionnaire
    url(r'^gestionnaire/', auth_gest_view.LoginPageView, name="login_gest"),
    url(r'^logout_gest/', auth_gest_view.LogoutPageView, name="logout_gest"),
    url(r'^dashboard/', gestionnaire_view.gestionnaire_dashboard_page, name="gestionnaire_dashboard"),
    url(r'^add_cust_page/', gestionnaire_view.gestionnaire_ajoutclient_page, name="add_cust_page"),
    url(r'^manage_cust_page/', gestionnaire_view.gestionnaire_gererclient_page, name="manage_cust_page"),
    url(r'^manage_commande_page/', gestionnaire_view.gestionnaire_commandes_page, name="manage_commande_page"),
    url(r'^route_page/', gestionnaire_view.gestionnaire_itineraire_page, name="route_page"),
    url(r'^messages_page/', gestionnaire_view.gestionnaire_messages_page, name="messages_page"), 
    url(r'^validate_inscription_client/', insc_view.validate_inscription_client, name="validate_inscription_client"),
    url(r'^deleteclient/(?P<id>.*)$', gestionnaire_view.deleteclient, name="deleteclient"),
    url(r'^validate_commande_client/(?P<id>.*)$', gestionnaire_view.valider_commande, name="validate_commande_client"),
    url(r'^get_maps_data/', livraison_view.get_data_for_maps, name="get_maps_data"),
    url(r'^iti/', gestionnaire_view.itineraire_page, name="iti"),
]
