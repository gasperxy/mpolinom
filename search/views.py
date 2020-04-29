from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse

# popravi na novo razdeljene applikacije
def index(request):
    return HttpResponse("Hello, world. You're at the search index.")
def about(request):
    return HttpResponse("This site is about M-polynomials page.")
def instructions(request):
    return HttpResponse("Here are usage instructions and hints." )
def contribute(request):
    return HttpResponse("Contribute new M-polynomials or comment.")
def register(request):
    return HttpResponse("Registring allows you to contribute new M-polynomials and comment.")
def advanced_search(request):
    return HttpResponse("Advanced search.")