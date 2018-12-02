from os import path
from csv import DictReader
from django.db import transaction
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import Blog, Word, WordCount
from .logic.hierarchical_clustering import get_clusters
from .logic.k_means_clustering import get_centroids


def index(request):
    return render(request, 'assignment2/index.html',
                  {'algorithms': {('k_means', 'K Means Clustering'), ('hierarchical', 'Hierarchical Clustering')}})


def k_means(request):
    (centroids, iterations) = get_centroids(2, 100)
    return render(request, 'assignment2/k_means.html', {'centroids': centroids, 'iterations': iterations})


def hierarchical(request):
    root_cluster = get_clusters()

    # Strip unused data
    def _strip_unused_data(cluster):
        if hasattr(cluster, 'children'):
            for child in cluster.children:
                _strip_unused_data(child)
        cluster.word_counts = None

    _strip_unused_data(root_cluster)

    return render(request, 'assignment2/hierarchical.html', {'root_cluster': root_cluster})


def load_data(_):
    Blog.objects.all().delete()
    Word.objects.all().delete()
    WordCount.objects.all().delete()

    dir_name = path.dirname(__file__)

    with open(path.join(dir_name, 'blogdata.txt'), 'r') as blog_data:
        words = DictReader(blog_data, delimiter='\t')

        with transaction.atomic():
            for word in filter(lambda x: x != 'Blog', words.fieldnames):
                Word.objects.create(word=word)

            for word_row in words:
                blog = Blog.objects.create(title=word_row['Blog'])
                for word_item in filter(lambda x: x[0] != 'Blog' and x[1] != '0', word_row.items()):
                    word = Word.objects.get(word=word_item[0])
                    WordCount.objects.create(blog=blog, word=word, count=word_item[1])

    return HttpResponseRedirect(reverse('assignment2:index'))
