from os import path, walk

from django.db import transaction
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from assignment3.models import Page, Word, WordCount, Link
from .logic.search_engine import find


def index(request):
    query = request.GET.get('query', '')
    if query:
        results = find(query=query, number_of_results=5)
    else:
        results = []
    return render(request, 'assignment3/index.html', {'original_query': query, 'results': results})


def load_data(request):
    Page.objects.all().delete()
    Word.objects.all().delete()
    WordCount.objects.all().delete()

    data_dir = path.join(path.dirname(__file__), 'data')
    word_dir = path.join(data_dir, 'data', 'Words')
    link_dir = path.join(data_dir, 'data', 'Links')

    page_rank_iterations = request.GET.get('iterations', 20)

    with transaction.atomic():
        for _, _, word_files in walk(word_dir):
            for word_file in word_files:
                page = Page.objects.create(url=path.basename(word_file))
                word_counts = {}
                with open(word_file, 'r') as words:
                    for counter, word in enumerate(words):
                        word_count = word_counts.get(word, (0, 0))
                        word_count[0] += 1
                        word_count[1] = counter if word_count[1] == 0 else word_count[1]

                for word_count_word, word_count in word_counts.items():
                    word = Word.objects.get_or_create(word_count_word)
                    WordCount.objects.create(page=page, word=word, count=word_count[0], location_score=word_count[1])

    with transaction.atomic():
        pages = Page.objects.all()
        for _, _, link_files in walk(link_dir):
            for link_file in link_files:
                source_page = pages.get(lambda x: x.url == path.basename(link_file), Page.objects.create(url=path.basename(link_file)))
                with open(link_file, 'r') as links:
                    for link in links:
                        for target_page in (page for page in pages if page.url == link):
                            Link.objects.create(sourse=source_page, target=target_page)

    with transaction.atomic():
        links = Link.objects.all()
        pages = Page.objects.all()
        page_ranks = []

        for page in pages:
            page_rank = PageRank(page, sum(link.source == page.url for link in links))
            page_ranks.add(page_rank)

        for _ in range(page_rank_iterations):
            for page_rank in page_ranks:
                for link in (link for link in links if link.target_id == page_rank.page.id):
                    source_page_rank =  page_ranks.get(lambda x: x.page.id == link.source_id, None)
                    if source_page_rank is not None:
                        page_rank.page_rank_score += source_page_rank.page.page_rank_score / source_page_rank.outward_links

            for page_rank in page_ranks:
                page_rank.page.page_rank_score = page_rank.page_rank_score * 0.85 + 15

    return HttpResponseRedirect(reverse('assignment3:index'))


class PageRank:
    def __init__(self, page, outward_links):
        self.page = page
        self.outward_links = outward_links
        self.page_rank_score = 0
