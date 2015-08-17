from django.shortcuts import render
from django.views.generic import TemplateView

from registrar.models import *


class IndexView(TemplateView):
    template_name = 'registrar/index.html'

    def get_context_data(self, **kwargs):
        context = super(TemplateView, self).get_context_data(**kwargs)
        context['sessions'] = Session.objects.all()
        return context
