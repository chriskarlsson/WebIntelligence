from random import randint
from django.db.models import Max

from assignment2.models import WordCount, Word, Blog
from shared_logic.distance_calculations import pearson


class Centroid:
    def __init__(self):
        self.blogs_in_previous = []
        self.blogs = []
        self.word_counts = dict()

    def clear_assignments(self):
        self.blogs_in_previous = self.blogs
        self.blogs = []

    def blog_collection_unchanged(self):
        return self.blogs_in_previous == self.blogs


def get_centroids(number_of_centroids, number_of_iterations):
    centroids = _get_random_centroids(number_of_centroids)
    blog_word_counts = dict()
    for blog in Blog.objects.all():
        word_counts = dict()
        for word_count in WordCount.objects.filter(blog=blog):
            word_counts[word_count.word_id] = word_count.count
        blog_word_counts[blog] = word_counts

    for iteration in range(number_of_iterations):
        if iteration > 0 and sum(centroid.blog_collection_unchanged() for centroid in centroids) == len(centroids):
            break

        for centroid in centroids:
            centroid.clear_assignments()

        for (blog, blog_word_count) in blog_word_counts.items():
            min_distance = -1

            for centroid in centroids:
                word_counts = []
                for (word_id, word_count) in centroid.word_counts.items():
                    word_counts.append((word_count, blog_word_count.get(word_id, 0)))

                distance = pearson(word_counts)

                if distance > min_distance:
                    min_distance = distance
                    best_centroid = centroid

            best_centroid.blogs.append(blog)

        _recalculate_center(centroids, blog_word_counts)

    return ([sorted(centroid.blogs) for centroid in centroids], iteration)


def _get_random_centroids(number_of_centroids):
    word_maxes = [(word['word'], word['max']) for word in WordCount.objects.values('word').annotate(max=Max('count'))]

    centroids = []
    for _ in range(number_of_centroids):
        centroid = Centroid()
        for word_max in word_maxes:
            centroid.word_counts[word_max[0]] = randint(0, word_max[1])

        centroids.append(centroid)

    return centroids


def _recalculate_center(centroids, blog_word_counts):
    for centroid in centroids:
        if len(centroid.blogs) > 0:
            for word_id in centroid.word_counts:
                average = 0
                for blog in centroid.blogs:
                    average += blog_word_counts[blog].get(word_id, 0)

                centroid.word_counts[word_id] = average / len(centroid.blogs)


