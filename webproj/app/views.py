from django.shortcuts import render
from django.http import Http404, HttpResponse
from datetime import datetime

def home(request):
    tparams = {
        'title': 'Platoon Merging',
        'year': datetime.now().year,
    }
    return render(request, 'index.html', tparams)