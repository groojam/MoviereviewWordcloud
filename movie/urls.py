from django.contrib import admin
from django.urls import include, path
from django.conf.urls import url
from django.views.generic.base import RedirectView
from django.conf.urls.static import static
from django.conf import settings

from . import views

app_name = "movie"

urlpatterns = [

    path('index.do', views.index.as_view(), name='main'),
    url(r'^/', views.home, name='home'),
    url(r'^search/', views.search, name='api_search'),
    url(r'^cloud/', views.cloud, name='wordcloud'),
    url(r'^crawler/', views.crawler, name='moviecrawler'),
    url(r'^select/', views.selector, name='movieselect'),
    url(r'^showimage.html', views.showImage, name='showimage')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)