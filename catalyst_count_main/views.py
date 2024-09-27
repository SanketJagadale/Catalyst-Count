from django.http import HttpResponse
from django.shortcuts import render
# Create your views here.

def Layout(request):
    templatefilename="layout.html"
    return render(request,templatefilename)