from django.shortcuts import render
from search.documents import MpolynomDocument
from elasticsearch_dsl.query import Q, MultiMatch
from .models import rewrite_mpolynomial

# from elasticsearch import Elasticsearch
# from elasticsearch_dsl import Search, Q



# Create your views here.
from django.http import HttpResponse


def index(request): #search all fields
    q = request.GET.get('q')
    if q:
        # remove whitespace and check if mpolynom
        wq = q.replace(" ", "")
        sign_list = ["x^", "y^"]
        # for i in range(2,10):
        #     sign_list.append("^"+ str(i))
        for sign in sign_list:
            # contains mpoly sign
            if wq.find(sign) != -1:
                # rewrite in same form as elasticsearch storage
                b = rewrite_mpolynomial(wq)
                split = b.split()
                nb_tokens = len(split)
                # range_results = MpolynomDocument.search().filter('range', nb_tokens ={'lte': nb_tokens+2, 'gte': nb_tokens-2})
                match_results =  MpolynomDocument.search().query("multi_match", query = b, fields = ['mpolynomyal^3',
                'structure_name^3','keywords^2','comments','references','links','author^2'],fuzziness = "AUTO")

                # search for mpoly with the same length
                q0 = Q('bool',
                must=[Q("multi_match", query = b, fields = ['mpolynomyal^3','structure_name^3','keywords^2',
                'comments','references','links','author^2'],fuzziness = "AUTO:4,7", minimum_should_match = '85%'  #, collapse = {"field" : "nb_tokens"} , sort = [{"nb_tokens" : {"order" : "asc", "mode" : "median"}}]
                ),
                Q('range',  nb_tokens = {'lte': nb_tokens, 'gte': nb_tokens})
                ]) 
                q1 = Q('bool',
                must=[Q("multi_match", query = b, fields = ['mpolynomyal^3','structure_name^3','keywords^2',
                'comments','references','links','author^2'],fuzziness = "AUTO:4,7", minimum_should_match = '85%'  #, collapse = {"field" : "nb_tokens"} , sort = [{"nb_tokens" : {"order" : "asc", "mode" : "median"}}]
                ),
                Q('range',  nb_tokens = {'lte': nb_tokens+2, 'gte': nb_tokens+1})
                ])
                q2 = Q('bool',
                must=[Q("multi_match", query = b, fields = ['mpolynomyal^3','structure_name^3','keywords^2',
                'comments','references','links','author^2'],fuzziness = "AUTO:4,7", minimum_should_match = '85%'  #, collapse = {"field" : "nb_tokens"} , sort = [{"nb_tokens" : {"order" : "asc", "mode" : "median"}}]
                ),
                Q('range',  nb_tokens = {'lte': nb_tokens-1, 'gte': nb_tokens-2})
                ])

                #def query(lte, gte): # lahko spreminjaš +2 -2 glede na dolžino besede - delež
                # spremeni v funkcijo, da se ne ponavljaš
                # q0 = Q('bool',
                # must=[Q("multi_match", query = b, fields = ['mpolynomyal^3','structure_name^3','keywords^2',
                # 'comments','references','links','author^2'],fuzziness = "AUTO"  #, collapse = {"field" : "nb_tokens"} , sort = [{"nb_tokens" : {"order" : "asc", "mode" : "median"}}]
                # ),
                # Q('range',  nb_tokens = {'lte': lte, 'gte': gte})
                # ]) 

                results0 = MpolynomDocument.search().query(q0) 
                response0 = results0.execute()
                number_results0 = response0.hits.total.value
                if number_results0 > 10:
                    response0 = response0[0:10]

                results1 = MpolynomDocument.search().query(q1) 
                response1 = results1.execute()
                number_results1 = response1.hits.total.value
                if number_results1 > 10:
                    response1 = response1[0:10]

                results2 = MpolynomDocument.search().query(q2) 
                response2 = results2.execute()
                number_results2 = response2.hits.total.value
                if number_results2 > 10:
                    response2 = response2[0:10]
                
                results = []
                for item in response0:
                    results.append(item)
                for item in response2:
                    results.append(item)
                for item in response1:
                    results.append(item)
                #results = match_results
                number_results = number_results0 + number_results1 + number_results2
                #results = str("search")
                # if no results, search as usual
                if number_results == 0:
                    #results = str("ni ni")
                    results =  MpolynomDocument.search().query("multi_match", query = q, fields = ['mpolynomyal^3',
                    'structure_name^3','keywords^2','comments','references','links','author^2'],fuzziness = "AUTO") 
                break
        else:
            results =  MpolynomDocument.search().query("multi_match", query = q, fields = ['mpolynomyal^3',
            'structure_name^3','keywords^2','comments','references','links','author^2'],fuzziness = "AUTO") 
    else:
        results= "Ni podanega q"
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