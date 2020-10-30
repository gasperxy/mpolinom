from django.shortcuts import get_object_or_404, render
from search.documents import MpolynomDocument
from elasticsearch_dsl.query import Q, MultiMatch
from .models import rewrite_mpolynomial, Mpolynom
from django.http import HttpResponse
from django.core.paginator import Paginator, Page, PageNotAnInteger, EmptyPage
from operator import itemgetter

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


def mpoly_query(query, lte, gte):
    """Executes Elasticsearch query
        args:
        str query - query we want to search
        int lte - upper bound for nb_tokens
        int gte - lower bound for nb_tokens
        returns:
        MpolynomDocument objects list response0 - execued query results
    """
    q0 = Q('bool',
        must=[Q("multi_match", query = query, fields = ['mpolynomial^4','structure_name^3','keywords^2',
        'comments','references','links','author^2', 'Mid^2'],fuzziness = "AUTO", minimum_should_match = '85%'# 90, '85%' 
        ),
        Q('range',  nb_tokens = {'lte': lte, 'gte': gte})
    ]) 
    results0 = MpolynomDocument.search().query(q0).filter("terms", status=["approved", "new_comments"])
    response0 = results0.execute()
    return response0


def index(request):
    q = request.GET.get('q')
    if q:
        if q.find("x") != -1 and q.find("y") != -1 and q.find("^"):
            # user query is probably mpolynomial

            # rewrite in the same manner as saved Elasticsearch mpolynomials
            b = rewrite_mpolynomial(q)
            split = b.split()
            nb_tokens = len(split)
            # search for mpoly with the same length
            response0 = mpoly_query(b, nb_tokens+8, nb_tokens-8)
            number_results0 = response0.hits.total.value 
            results_tuples = []
            for item in response0:
                results_tuples.append((item, float(item.meta.score)))
            results_t = sorted(results_tuples,key=itemgetter(1))
            results_t = results_t[::-1]
            results = [result[0] for result in results_t]
            number_results = number_results0 
            paginator = Paginator(results, 10)
            # if no results, search as usual (unchaged user query)
            if number_results == 0:
                results =  MpolynomDocument.search().query("multi_match", query = q, fields = ['mpolynomial^3',
                'structure_name^3','keywords^2','comments','references','links','author^2','Mid^2'],fuzziness = "AUTO").filter("terms", status=["approved", "new_comments"])
                results = results.execute()
                paginator = Paginator(results, 10)
        else:
            # user query is word
            results =  MpolynomDocument.search().query("multi_match", query = q, fields = ['mpolynomial^3',
            'structure_name^3','keywords^2','comments','references','links','author^2','Mid^2'],fuzziness = "AUTO").filter("terms", status=["approved", "new_comments"])
            results = results[0:100].execute()
            number_resul = results.hits.total.value
            paginator = Paginator(results, 10)
    else:
        results= "No q given."
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
        return render(request,'search/index.html', {'results': results})

def detail(request, Mid):
    mpolynomial_object = get_object_or_404(Mpolynom, Mid=Mid)
    return render(request, 'search/detail.html', {'Mobject': mpolynomial_object})

def contribute(request):
    return render(request, 'search/contribute.html')

def access(request):
    return render(request, 'search/access.html')

def instructions(request):
    return render(request, 'search/instructions.html')


# def about(request):
#     return render(request, 'search/about.html')
