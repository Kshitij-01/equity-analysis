from django.shortcuts import render

from equity.views import comps2


def home(request):

    return render(request, 'Equity home.html', {'comps': comps2})
