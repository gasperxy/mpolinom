from django.shortcuts import render
from search.documents import MpolynomDocument

# Create your views here.
from django.http import HttpResponse


def index(request):
    q = request.GET.get('q')
    if q:
        results = MpolynomDocument.search().query("match", structure_name = q)
    else:
        results= "Ni ujemanja"
    return render(request, 'search/index.html', {'results': results})
def results(request):
    return HttpResponse("Search results or error.")
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