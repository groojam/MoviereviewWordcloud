from django.core.files.storage import FileSystemStorage
from django.db import models
from django.conf import settings
from django.utils import timezone


class Movie(models.Model):

    #영화id, 영화이름, 크롤링데이터 위치
    mvId = models.CharField(max_length=20, primary_key=True, null=False)
    mvName = models.CharField(max_length=200, null=True)
    mvData = models.TextField(null=True)
    mvYear = models.CharField(max_length=20, null=True)
    mvPoster = models.TextField(null=True)
    mvcloud = models.TextField(null=True)
    mv_createdate = models.DateField(default=timezone.now)
    mvLocation = models.TextField(null=True)
    cldImgPath = models.TextField(null=True)
    pstImgPath = models.TextField(null=True)
    def __str__(self):
        return self.mvId