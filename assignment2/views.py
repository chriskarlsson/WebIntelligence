from csv import DictReader
from django.db import transaction
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import Blog, Word, WordCount
from .logic.hierarchical_clustering import iterate
from .logic.k_means_clustering import get_centroids


def index(request):
    #(centroids, iterations) = get_centroids(2, 100)
    clusters = iterate()
    return render(request, 'assignment2/index.html',
                  {'algorithms': {''}})


def load_data(_):
    Blog.objects.all().delete()
    Word.objects.all().delete()
    WordCount.objects.all().delete()

    with open('../assignment2/blogdata.txt', 'r') as blog_data:
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
