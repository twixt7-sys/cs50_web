from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):
    return render(request, "hello/index.html")

def trisha(request):
    return HttpResponse("Trisha")

def luke(request):
    return HttpResponse("Luke")

def greet(request, name):
    return render(request, "greet/greet.html", {
        #json??
        "name": name.capitalize()
    })