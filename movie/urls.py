from django.contrib import admin
from django.urls import include, path
from django.conf.urls import url
from django.views.generic.base import RedirectView

from . import views

app_name = "movie"

urlpatterns = [

    path('index.do', views.index.as_view(), name='main'),
]