from django.http import HttpResponse
from django.shortcuts import render
# Create your views here.

def Home(request):
    templatefilename="home.html"
    return render(request,templatefilename)