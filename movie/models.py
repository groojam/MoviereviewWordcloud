from django.db import models
from django.conf import settings
from django.utils import timezone


class Movie(models.Model):

    #영화id, 영화이름, 크롤링데이터 위치
    mvId = models.IntegerField(primary_key=True, null=False)
    mvName = models.CharField(max_length=200)
    mvData = models.TextField()
    mv_createdate = models.DateField(default=timezone.now)

    def __str__(self):
        return self.mvName

