from django.shortcuts import render
from search.documents import MpolynomDocument
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search, Q

client = Elasticsearch()
s = Search(using=client)

# Create your views here.
from django.http import HttpResponse


def index(request): #search all fields
    q = request.GET.get('q')
    if q: #popravi da bo iskalnik prilagodil polinom - kako določiti kakšen input je
        # pazi splosne polinome
        results =  MpolynomDocument.search().query("multi_match", query = q, fields = ['mpolynomyal^3',
        'structure_name^3','keywords^2','comments','references','links','author^2'],fuzziness = 0) 
    else:
        results= "Ni ujemanja"
    return render(request, 'search/index.html', {'results': results})
# def about(request):
#     return HttpResponse("This site is about M-polynomials page.")
# def instructions(request):
#     return HttpResponse("Here are usage instructions and hints." )
# def contribute(request):
#     return HttpResponse("Contribute new M-polynomials or comment.")
# def register(request):
#     return HttpResponse("Registring allows you to contribute new M-polynomials and comment.")
# def advanced_search(request):
#     return HttpResponse("Advanced search.")