from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
#about us views
def about (request):
    return render(request, 'about/about.html')