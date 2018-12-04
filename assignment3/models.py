from django.db import models


class Page(models.Model):
    url = models.CharField(max_length=200)

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
    page_rank_score = models.IntegerField(default=1)

    def __str__(self):
        return self.count


class Link(models.Model):
    source = models.ForeignKey(Page, related_name='source_page', on_delete=models.CASCADE)
    target = models.ForeignKey(Page, related_name='target_page', on_delete=models.CASCADE)
