from django.shortcuts import render
from vectorise.utils import retrieve_documents
from crawler.models import TextData
from django.views.decorators.csrf import csrf_exempt
from search.utils import relevant_doc_weigts, pseudo_relevance_feedback
from vectorise.utils import tokenize


# Create your views here.
def index(request):
    """View function for home page of site."""

    return render(request, 'search/index.html', context={})


@csrf_exempt
def search(request):
    if request.method == 'GET':
        query = request.GET.get('query')
        max_no_of_results = int(request.GET.get('no_of_results', 10))
        doc_ids = retrieve_documents(query)
        pseudo_expansion = pseudo_relevance_feedback(doc_ids)
        query_words = tokenize(query)
        for word in pseudo_expansion:
            if word not in query_words:
                query_words.append(word)
        new_query = ' '.join(query_words)
        doc_ids = retrieve_documents(new_query)
        td_dict = {}
        result = []
        tds = TextData.objects.filter(id__in=doc_ids)
        if len(doc_ids) > max_no_of_results:
            doc_ids = doc_ids[:max_no_of_results]
        for td in tds:
            td_dict[td.id] = td.url
        for i, val in enumerate(doc_ids):
            if val in td_dict:
                result.append({'rank': (i + 1), 'url': td_dict[val], 'id': val})
        return render(request, 'search/search_results.html',
                      context={'result': result, 'query': query, 'no_of_results': max_no_of_results})
    elif request.method == 'POST':
        query = request.POST.get('query')
        max_no_of_results = int(request.POST.get('no_of_results', 10))
        query_words = tokenize(query)
        relevant_docs = []
        non_relevant_docs = []
        post_dict = request.POST
        for key, value in post_dict.items():
            if 'relevance' in key:
                if int(value) == 1:
                    relevant_docs.append(int(key.split('-')[1]))
                else:
                    non_relevant_docs.append(int(key.split('-')[1]))
        rw = relevant_doc_weigts(relevant_docs)
        nrw = relevant_doc_weigts(non_relevant_docs)
        new_query = []
        for word in query_words:
            if word not in nrw:
                new_query.append(word)
        for word in rw:
            if word not in query_words:
                new_query.append(word)
        new_query = ' '.join(new_query)
        doc_ids = retrieve_documents(new_query)
        if len(doc_ids) > max_no_of_results:
            doc_ids = doc_ids[:max_no_of_results]
        td_dict = {}
        result = []
        tds = TextData.objects.filter(id__in=doc_ids)
        for td in tds:
            td_dict[td.id] = td.url
        for i, val in enumerate(doc_ids):
            result.append({'rank': (i + 1), 'url': td_dict[val], 'id': val})
        return render(request, 'search/search_results.html',
                      context={'result': result, 'query': new_query, 'no_of_results': max_no_of_results})
