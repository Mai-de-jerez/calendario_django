from django.shortcuts import render
from django.views.generic.base import TemplateView

class HomeView(TemplateView):
    template_name="core/home.html"
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {'title': 'Calend-Art'})


    