from django.db import models


class User(models.Model):
    name = models.CharField(max_length=200)
    user_id = models.IntegerField(default=0, primary_key=True)

    def __str__(self):
            return self.name

    def __eq__(self, other):
        return self.name == other.name and self.user_id == other.user_id


class Movie(models.Model):
    title = models.CharField(max_length=200)

    def __str__(self):
        return self.title

    def __eq__(self, other):
        return self.title == other.title


class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    rating = models.FloatField(default=0)

    def __str__(self):
        return self.rating

    def __eq__(self, other):
        return self.user == other.user and self.movie == other.movie and self.rating == other.rating
