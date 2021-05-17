from django.contrib import admin
from .models import Movie


class Lay_movie(admin.ModelAdmin):
    list_display = ('mvId', 'mvName', 'mvData', 'mv_createdate')

admin.site.register(Movie, Lay_movie)
