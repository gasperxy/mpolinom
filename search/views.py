from django.shortcuts import render
from search.documents import MpolynomDocument
from elasticsearch_dsl.query import Q, MultiMatch
from .models import rewrite_mpolynomial




from operator import itemgetter

# from elasticsearch import Elasticsearch
# from elasticsearch_dsl import Search, Q

#printing for debug
import logging
logger = logging.getLogger("mylogger")
logger.info("Whatever to log")

from django.core.paginator import Paginator, Page, PageNotAnInteger, EmptyPage

class DSEPaginator(Paginator):
    """
    Override Django's built-in Paginator class to take in a count/total number of items;
    Elasticsearch provides the total as a part of the query results, so we can minimize hits.
    """
    def __init__(self, *args, **kwargs):
        super(DSEPaginator, self).__init__(*args, **kwargs)
        self._count = self.object_list.hits.total

    def page(self, number):
        # this is overridden to prevent any slicing of the object_list - Elasticsearch has
        # returned the sliced data already.
        number = self.validate_number(number)
        return Page(self.object_list, number, self)



# Create your views here.
from django.http import HttpResponse

def mpoly_query(query, lte, gte):
    q0 = Q('bool',
        must=[Q("multi_match", query = query, fields = ['mpolynomyal^4','structure_name^3','keywords^2',
        'comments','references','links','author^2'],fuzziness = 0, minimum_should_match = '-20%'# 90, '85%' 
        ),
        Q('range',  nb_tokens = {'lte': lte, 'gte': gte})
    ]) 
    results0 = MpolynomDocument.search().query(q0) 
    response0 = results0.execute()
    return response0
# "AUTO:4,7"


def index(request): #search all fields
    q = request.GET.get('q')
    if q:
        # remove whitespace and check if mpolynom
        #     sign_list.append("^"+ str(i))
        wq = q.replace(" ", "")
        sign_list = ["x^", "y^"]
        # for i in range(2,10):
        for sign in sign_list:
            # contains mpoly sign
            if wq.find(sign) != -1:
                print("rezultat prvega tipa")
                # rewrite in same form as elasticsearch storage
                b = rewrite_mpolynomial(wq)
                split = b.split()
                nb_tokens = len(split)

                # range_results = MpolynomDocument.search().filter('range', nb_tokens ={'lte': nb_tokens+2, 'gte': nb_tokens-2})
                #match_results =  MpolynomDocument.search().query("multi_match", query = b, fields = ['mpolynomyal^3',
                #'structure_name^3','keywords^2','comments','references','links','author^2'],fuzziness = "AUTO")

                # search for mpoly with the same length
                response0 = mpoly_query(b, nb_tokens, nb_tokens)
                print(response0)

                # search for mpoly with 1 part (člen) more than original mpoly
                response1 = mpoly_query(b, nb_tokens+4, nb_tokens+1)
                # search for mpoly with 1 part less than original mpoly
                response2 = mpoly_query(b, nb_tokens-1, nb_tokens-4)

                # a res želiš omejit št rezultatov

                number_results0 = response0.hits.total.value
                # if number_results0 > 10:
                #     response0 = response0[0:10]

                number_results1 = response1.hits.total.value
                # if number_results1 > 10:
                #     response1 = response1[0:10]

                number_results2 = response2.hits.total.value
                # if number_results2 > 10:
                #     response2 = response2[0:10]

                
                
                results_tuples = []
                for item in response0:
                    results_tuples.append((item, float(item.meta.score)))
                for item in response2:
                    results_tuples.append((item, float(item.meta.score)))
                for item in response1.hits:
                    results_tuples.append((item, float(item.meta.score)))

                #results = match_results
                results_t = sorted(results_tuples,key=itemgetter(1))
                results_t = results_t[::-1]
                print(results_t)
                results = [result[0] for result in results_t]



                number_results = number_results0 + number_results1 + number_results2
                print("number results :" , number_results)
                paginator = Paginator(results, 2)
                #results = str("search")
                # if no results, search as usual
                if number_results == 0:
                    print("ni rezultatov prvega tipa")
                    results =  MpolynomDocument.search().query("multi_match", query = q, fields = ['mpolynomyal^3',
                    'structure_name^3','keywords^2','comments','references','links','author^2'],fuzziness = "AUTO") 
                    results = results.execute()
                    paginator = Paginator(results, 2)
                break
        else:
            print("besedni rezultat")
            results =  MpolynomDocument.search().query("multi_match", query = q, fields = ['mpolynomyal^3',
            'structure_name^3','keywords^2','comments','references','links','author^2'],fuzziness = "AUTO") 
            results = results[0:100].execute()
            number_resul = results.hits.total.value
            print("number_results:", number_resul)
            paginator = Paginator(results, 2)
    else:
        print("no q given")
        results= "No q given."
    print(results)
    if results == "No q given.":
        return render(request, 'search/index.html', {'results': results})
    else:    
        page = request.GET.get('page')

        try:
            results = paginator.page(page)
        except PageNotAnInteger:
            results = paginator.page(1)
        except EmptyPage:
            results = paginator.page(paginator.num_pages)
        return render(request,'search/index.html',
                              {'results': results})
        # return render(request, 'search/index.html', {'results': results})

def detail(request, polynomial):
    return HttpResponse("You're looking at detail site of M-polynom %s." % polynomial)
# def instructions(request):
#     return HttpResponse("Here are usage instructions and hints." )
# def contribute(request):
#     return HttpResponse("Contribute new M-polynomials or comment.")
# def register(request):
#     return HttpResponse("Registring allows you to contribute new M-polynomials and comment.")
# def advanced_search(request):
#     return HttpResponse("Advanced search.")