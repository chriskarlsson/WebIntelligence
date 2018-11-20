from math import sqrt

from .models import Movie, User, Rating


class Algorithm:
    def __init__(self, name, algorithm):
        self.name = name
        self.algorithm = algorithm


def get_available_algorithms():
    return [Algorithm('Euclidean', _euclidean), Algorithm('Pearson', _pearson)]


def get_available_bases():
    return ['Item-based', 'User-based']


def find_similar_users(reference_user, algorithm):
    users = []
    for user in User.objects.exclude(name=reference_user.name):
        users.append((user, algorithm(_get_user_ratings(reference_user, user))))

    return sorted(users, key=lambda score: score[1], reverse=True)


def find_similar_movies(reference_movie, algorithm):
    movies = []
    for movie in Movie.objects.exclude(title=reference_movie.title):
        movies.append((movie, algorithm(_get_movie_ratings(reference_movie, movie))))

    return sorted(movies, key=lambda score: score[1], reverse=True)


def find_recommended_movies_user_based(reference_user, weights):
    movies = []
    for movie in Movie.objects.all():
        if movie not in [rating.movie for rating in Rating.objects.filter(user=reference_user)]:
            movie_weight = _get_user_based_weights(movie, weights)
            scores = _calculate_score(movie_weight)
            movies.append((movie, scores))

    return sorted(movies, key=lambda score: score[1], reverse=True)


def find_recommended_movies_item_based(reference_user, algorithm):
    movies = []
    for movie in Movie.objects.all():
        if movie not in [rating.movie for rating in Rating.objects.filter(user=reference_user)]:
            weights = find_similar_movies(movie, algorithm)
            movie_weight = _get_item_based_weights(reference_user, weights)
            scores = _calculate_score(movie_weight)
            movies.append((movie, scores))

    return sorted(movies, key=lambda score: score[1], reverse=True)


def _get_user_ratings(user_a, user_b):
    ratings = []
    for rating_a in Rating.objects.filter(user=user_a):
        for rating_b in Rating.objects.filter(user=user_b):
            if rating_a.movie == rating_b.movie:
                ratings.append((rating_a.rating, rating_b.rating))

    return ratings


def _get_movie_ratings(movie_a, movie_b):
    ratings = []
    for rating_a in Rating.objects.filter(movie=movie_a):
        for rating_b in Rating.objects.filter(movie=movie_b):
            if rating_a.user == rating_b.user:
                ratings.append((rating_a.rating, rating_b.rating))

    return ratings


def _get_user_based_weights(movie, weights):
    result = []
    for rating in Rating.objects.filter(movie=movie):
        for weight in weights:
            if weight[0] == rating.user:
                result.append((rating.rating, weight[1]))

    return result


def _get_item_based_weights(user, weights):
    result = []
    for rating in Rating.objects.filter(user=user):
        for weight in weights:
            if weight[0] == rating.movie:
                result.append((rating.rating, weight[1]))

    return result


def _calculate_score(weights):
    total_sum = 0
    weight_sum = 0
    for weight in weights:
        total_sum += weight[0] * weight[1]
        weight_sum += weight[1]

    return 0 if weight_sum == 0 else total_sum / weight_sum


def _euclidean(ratings):
    total_sum = 0
    n = 0

    for rating in ratings:
        total_sum += (rating[0] - rating[1])**2
        n += 1

    return 0 if n == 0 else 1/(1 + total_sum)


def _pearson(ratings):
    sum_1 = 0
    sum_2 = 0
    sum_1_sq = 0
    sum_2_sq = 0
    p_sum = 0
    n = 0

    for rating in ratings:
        sum_1 += rating[0]
        sum_2 += rating[1]
        sum_1_sq += rating[0]**2
        sum_2_sq += rating[1]**2
        p_sum += rating[0] * rating[1]
        n += 1

    if n == 0:
        return 0

    num = p_sum - (sum_1 * sum_2 / n)
    den = sqrt((sum_1_sq - sum_1**2 / n) * (sum_2_sq - sum_2**2 / n))

    return num / den
