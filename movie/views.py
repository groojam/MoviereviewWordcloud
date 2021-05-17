from django.shortcuts import render
from django.views import generic

from .models import Movie

class index(generic.ListView):
    def __init__(self):
        self.title_nm = "영화리뷰 워드클라우드 분석"
        self.ogImgUrl = ""
        self.descript = "영화리뷰 워드클라우드 분석페이지 입니다."
        self.template_name = "index.html"

    def get(self, request, *args, **kwargs):


        self.content = {"descript":self.descript,
                        "title_nm":self.title_nm,
                        "ogImgUrl":self.ogImgUrl,
                        "dataList":Movie.objects.all()}

        return render(request, self.template_name, self.content)