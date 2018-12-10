from django.db import models


class Page(models.Model):
    title = models.CharField(max_length=200)
    page_rank_score = models.FloatField(default=1)
    outward_links = models.IntegerField(default=0)

    def __str__(self):
            return self.url

    def __lt__(self, other):
        return self.url < other.title

    def __eq__(self, other):
        return self.url == other.title


class Word(models.Model):
    word = models.CharField(max_length=200)

    def __str__(self):
        return self.word


class WordCount(models.Model):
    page = models.ForeignKey(Page, on_delete=models.CASCADE)
    word = models.ForeignKey(Word, on_delete=models.CASCADE)
    count = models.IntegerField(default=0)
    location_score = models.IntegerField(default=0)

    def __str__(self):
        return self.count
