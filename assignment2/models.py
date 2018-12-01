from django.db import models


class Blog(models.Model):
    title = models.CharField(max_length=200)

    def __str__(self):
            return self.title

    def __lt__(self, other):
        return self.title < other.title

    def __eq__(self, other):
        return self.title == other.title


class Word(models.Model):
    word = models.CharField(max_length=200)

    def __str__(self):
        return self.word


class WordCount(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    word = models.ForeignKey(Word, on_delete=models.CASCADE)
    count = models.IntegerField(default=0)

    def __str__(self):
        return self.count
