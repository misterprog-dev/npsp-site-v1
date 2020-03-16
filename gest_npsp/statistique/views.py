from django.shortcuts import render
from django.views.generic import TemplateView

# Create your views here.

class StatistiquePageView(TemplateView):
    def get(self, request, **kwargs):
        return render(request, 'statistique.html', context=None)