from django.shortcuts import render
from search.documents import MpolynomDocument
from elasticsearch_dsl.query import Q

# from elasticsearch import Elasticsearch
# from elasticsearch_dsl import Search, Q



# Create your views here.
from django.http import HttpResponse


def index(request): #search all fields
    q = request.GET.get('q')
    if q:
        # remove whitespace and check if mpolynom
        wq = q.replace(" ", "")
        sign_list = []
        for i in range(2,10):
            sign_list.append("^"+ str(i))
        for sign in sign_list:
            # contains mpoly sign
            if wq.find(sign) != -1:
            # rewrite in same form as elasticsearch storage
                b = ""
                for elt in wq:
                    if elt == "-" or elt == "+":
                        b = b + " " + elt + " "
                    elif elt == "x" or elt == "y":
                        b = b + " " + elt
                    #elif elt == " ": naceloma to ni mozno ker smo nardil replace (wq)
                    #    b = b
                    else:
                        b = b + elt
                if b[0] == " ":
                    b = b[1:len(b)]
                if b[len(b)-1] == " ":
                    b == b[0:len(b) - 1]
                split = b.split(" ")
                nb_tokens = len(split)
                range_results = MpolynomDocument.search().filter('range', nb_tokens ={'lte': nb_tokens+2, 'gte': nb_tokens-2})
                match_results =  MpolynomDocument.search().query("multi_match", query = b, fields = ['mpolynomyal^3',
                'structure_name^3','keywords^2','comments','references','links','author^2'],fuzziness = "AUTO")
                results = search.query().query(
                    Q('match', author = 'Mate Fik in P. Olde') & 
                    Q( "match", structure_name = 'Mpolirolii')
                )
                response = results.execute()
                number_results = response.hits.total.value
                if number_results == 0:
                    #results = str("ni ni")
                    results =  MpolynomDocument.search().query("multi_match", query = q, fields = ['mpolynomyal^3',
                    'structure_name^3','keywords^2','comments','references','links','author^2'],fuzziness = 0) 
                break
        else:
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