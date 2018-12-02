from os import path
from csv import DictReader

from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic

from assignment1.recommendation import find_similar_users, find_recommended_movies_user_based,\
    get_available_algorithms, find_recommended_movies_item_based, get_available_bases
from .models import Movie, User, Rating


def index(request):
        return render(request, 'assignment1/index.html',
                      {'users': User.objects.all(),
                       'algorithms': [algorithm.name for algorithm in get_available_algorithms()],
                       'bases': get_available_bases()})


class DetailView(generic.DetailView):
    model = User
    template_name = 'assignment1/detail.html'

    def get_queryset(self):
        return User.objects.all()


def recommendation(request):
    user = get_object_or_404(User, user_id=request.GET['user'])
    selected_algorithm = next(algorithm.algorithm for algorithm in
                              get_available_algorithms() if algorithm.name == request.GET['algorithm'])
    users = find_similar_users(user, selected_algorithm)
    movies = find_recommended_movies_user_based(user, users) if 'User-based' == request.GET['base'] \
        else find_recommended_movies_item_based(user, selected_algorithm)
    return render(request, 'assignment1/recommendation.html',
                  {'reference_user': user, 'users': users[:3], 'movies': movies})


def load_data(_):
    dir_name = path.dirname(__file__)

    with open(path.join(dir_name, 'users.csv'), 'r') as users_csv:
        users = DictReader(users_csv, delimiter=';')

        for user in users:
            User.objects.get_or_create(name=user['UserName'], user_id=user['UserID'])

    with open(path.join(dir_name, 'ratings.csv'), 'r') as ratings_csv:
        ratings = DictReader(ratings_csv, delimiter=';')

        for rating in ratings:
            movie, _ = Movie.objects.get_or_create(title=rating['Movie'])
            user = User.objects.get(user_id=rating['UserID'])
            Rating.objects.get_or_create(user=user, movie=movie, rating=rating['Rating'])

    return HttpResponseRedirect(reverse('assignment1:index'))
