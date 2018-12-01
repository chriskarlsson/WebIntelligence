from django.contrib import admin

from .models import Blog, Word, WordCount

admin.site.register(Blog)
admin.site.register(Word)
admin.site.register(WordCount)
