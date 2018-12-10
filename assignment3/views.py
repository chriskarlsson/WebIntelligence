from django.shortcuts import render

from .logic.search_engine import search


def index(request):
    query = request.GET.get('query', '')
    if query:
        results = search(query=query, number_of_results=5)
    else:
        results = []
    return render(request, 'assignment3/index.html', {'original_query': query, 'results': results})

