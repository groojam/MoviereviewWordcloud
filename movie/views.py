from config.settings import STATICFILES_DIR
import movie
from django.shortcuts import render
from django.views import generic
from django.conf import settings
from django.conf.urls.static import settings

from django.core.files.storage import default_storage

from .models import Movie
import os
import json
import urllib.request
import requests
from selenium import webdriver
import time

import csv
from bs4 import BeautifulSoup
import datetime

import pytagcloud
import random
import webbrowser
from konlpy.tag import Okt
from collections import Counter

from wordcloud import WordCloud

from io import BytesIO
import cv2
import numpy as np

from tqdm import tqdm
from tqdm import trange




class index(generic.ListView):
    def __init__(self):
        self.title_nm = "영화리뷰 워드클라우드 분석"
        self.ogImgUrl = ""
        self.descript = "영화리뷰 워드클라우드 분석페이지 입니다."
        self.template_name = "movie/index.html"

    def get(self, request, *args, **kwargs):


        self.content = {"descript":self.descript,
                        "title_nm":self.title_nm,
                        "ogImgUrl":self.ogImgUrl,
                        "dataList":Movie.objects.all()}
        
        return render(request, self.template_name, self.content)

def home(request):
    pass


def search(request):

    if request.method == 'GET':


        q = request.GET.get('q')
        encText = urllib.parse.quote("{}".format(q))
        url = "https://openapi.naver.com/v1/search/movie?query=" + encText  # json 결과
        movie_api_request = urllib.request.Request(url)
        movie_api_request.add_header("X-Naver-Client-Id", "tEzvl3Zbb_YdGSpp7hYv")
        movie_api_request.add_header("X-Naver-Client-Secret", "r3fyE410yt")
        response = urllib.request.urlopen(movie_api_request)
        rescode = response.getcode()
        if (rescode == 200):
            response_body = response.read()
            result = json.loads(response_body.decode('utf-8'))
            items = result.get('items')
            print(result)

            # mvID = items.link
            # print(mvID)

            # movie = Movie()
            # movie.Id = items.id
            # movie.Poster = items.image
            # movie.Name = items.title
            # movie.Year = items.pubDate
            # movie.save()

            
            context = {
                'items': items
            }
                
            return render(request, 'movie/search.html', context=context)


def selector(request):

    if request.method == 'GET':
        
        mvinfo = request.GET.getlist('mvinfo[]')
        print("list")
        print(mvinfo)
        temp = mvinfo[6]
        slicngid = temp[51:]
        slicngid.replace("'", "")
        print("id")
        print(slicngid)
        del mvinfo[6]
        mvinfo.append(slicngid)
        print(mvinfo)
        

        keylist = ['image', 'title', 'pubDate', 'director', 'actor', 'userRating', 'mvId']
        items = dict(zip(keylist, mvinfo))
        #mvid = request.GET.get('code','')
        #print(mvinfo)
        print(items)
        context = {
            'items' : items
        }


        return render(request, 'movie/select.html', context = context)


def crawler(request):
    
    if request.method == 'GET':
        
        mvinfo = request.GET.getlist('mvinfo[]')

        #print(mvinfo)
        #포스터 이미지 저장.
        movieid = mvinfo[0]
        mvImgUrl = mvinfo[1]



        # tempImg = BytesIO()
        # tempImg.write(mvImgUrl)
        # tempImg.seek(0)
        #imgSavePath = "./media/poster/" + movieid + ".jpg"
        #print(imgSavePath)
        #poster = urllib.request.urlretrieve(mvImgUrl, imgSavePath)

        resp = urllib.request.urlopen(mvImgUrl)
        image = np.asarray(bytearray(resp.read()), dtype='uint8')
        image = cv2.imdecode(image, cv2.IMREAD_COLOR)

        #포스터 이미지 불러오기.
        #res = request.urlopen(mvImgUrl).read()

        now = datetime.datetime.today()
        nowDateTime = now.strftime('%Y-%m-%d %H:%M:%S')

        SaveDir = os.getcwd()
        #크롤링 데이터 저장 위치.
        saveLocation = "/movie/media/crawldata/" + movieid + ".csv"

        print(SaveDir)

        csvPath = SaveDir + saveLocation

        print(csvPath)

        # 이미지 url저장, 불러오기 or 이미지를 db에 저장, 불러오기.
        Movie(mvId = movieid, mvPoster = image, mvName = mvinfo[1], mvYear = mvinfo[2]).save

        test_url = "https://movie.naver.com/movie/bi/mi/pointWriteFormList.nhn?code=" + movieid + "&type=after"
        resp = requests.get(test_url)
        html = BeautifulSoup(resp.content, 'html.parser')
        result = html.find('div', {'class':'score_total'}).find('strong').findChildren('em')[0].getText()
        total_count = int(result.replace(',', ''))

        review =[]

        def get_data(url):
            resp = requests.get(url)
            html = BeautifulSoup(resp.content, 'html.parser')
            score_result = html.find('div', {'class': 'score_result'})
            lis = score_result.findAll('li')
            for li in lis:
                #nickname = li.find('dt').find('span').getText()
                #created_at = datetime.strptime(li.find('dt').findAll('em')[-1].getText(), "%Y.%m.%d %H:%M")

                review_text = li.find('p').find('span', {'class' : '_unfold_ment'})
                if review_text == None:
                    review_text = li.find('p').getText(' ',strip=True)
                    review_text = review_text.replace("관람객","")
                else:
                    review_text = review_text.select('a')[0]['data-src']
                    review_text = review_text.strip()
                    review_text = review_text.replace("관람객","")

                #score = li.find('em').getText()
                # btn_likes = li.find('div', {'class': 'btn_area'}).findAll('span')
                # like = btn_likes[1].getText()
                # dislike = btn_likes[3].getText()

                # watch_movie = li.find('span', {'class':'ico_viewer'})
                
                # output='' 
                # for item in content.contents: 
                #     stripped=str(item).strip() # strip()으로 공백제거
                #     if stripped=='': 
                #         continue 
                #     if stripped[0] not in['<','/']: #태그나 주석제거 
                #         output+=str(item).strip() 
                # output=output.replace('function _flash_removeCallback() {}','') 
                # output=output.strip() 
                review.append(review_text)

                with open(csvPath, mode='a', newline='', encoding='utf-8') as review_csv:
                    writer = csv.writer(review_csv)
                    writer.writerow([review_text])



                #print(nickname, review_text, score, like, dislike, created_at, watch_movie and True or False)
            time.sleep(0.5)

        #get_data(test_url)
        for i in range(1, int(total_count / 10) + 1):
            url = test_url + '&page=' + str(i)
            print('url: "' + url + '" is parsing....')
            get_data(url)

        context = {'movieid' : movieid}
    return render(request, 'movie/crawler.html', context=context)


def cloud(request):
        ####################################################
    # get_tags 새함수 만듦:
    # 기능 1. 댓글별로 명사만 추출
    # 기능 2. 명사 빈도수 집계
    # 기능 3. 단어구름에 표시할 명사에 3가지 시각화 속성
    #        (색상'color', 단어'tag', 크기'size')부여

    if request.method == 'GET':
        movieid = request.GET.get('movieid')

        SaveDir = os.getcwd()
        #크롤링 데이터 저장 위치.
        saveLocation = "/movie/media/crawldata/" + movieid + ".csv"


        csvPath = SaveDir + saveLocation

        imgSaveLocation = "/moive/media/cloudimg/" + movieid + ".png"

        imgPath = SaveDir + imgSaveLocation

        #fontPath = ""

        print(csvPath)
        print(imgPath)
    # 입력변수- text : 댓글, ntags : 표시할 단어수, multiplier : 크기가중치
        def get_tags(text, ntags=100):
            t = Okt()
            nouns = []

        # 모든 댓글에서 명사만 추출하고 nouns변수에 누적해 저장함
            for sentence in text:
                for noun in t.nouns(sentence):
                    if len(noun) >=2 :
                        nouns.append(noun)
                    # 각 명사별로 빈도계산
                    count = Counter(nouns)
            # n : 명사, c : 빈도
            tags = count.most_common(ntags)
            return tags
            #[{'color': color(),'tag':n,'size':c} for n,c in count.most_common(ntags)]

        # draw_cloud 새함수 만듦:
        # 기능 1. pytagclud 모듈을 사용해 단어구름 이미지를 만듦
        # 기능 2. 단어구름 이미지를 파일로 저장함
        # 기능 3. 화면에 단어구름을 표시함

        # 입력변수 tags : get_tags()에서 리턴되는 color, tag, size(이미지크기) 값이 전달됨.
        # fontname : Noto Sans CJK - 한글폰트

        def draw_cldimg(tags, filename):
            wordcld = WordCloud(font_path='/usr/share/fonts/truetype/SeoulHangangM.ttf', background_color='white', width='1000', height='1000', max_words='100', max_font_size='300')
            wordcld.generate_from_frequencies(dict(tags))
            wordcld.to_file(filename)

            return wordcld


        # def draw_cloud(tags, filename, fontname = 'Nanum Gothic',size1 = (1300,800)):
        #     cloud = pytagcloud.create_tag_image(tags,filename,fontname=fontname,size=size1, rectangular=False)
        #     # 저장된 단어구름 이미지파일(wc1.png)을 내 컴퓨터에 띄움
        #     #webbrowser.open(filename)
        #     return cloud
        ####################################################
        # 명사에 적용할 색상 랜덤지정
        r = lambda: random.randint(0, 255)
        color = lambda: (r(), r(), r())

        # 옥자 댓글(okja1.txt) 읽기 전용으로 읽어들임.
        reviews = []
        
        file = open(csvPath, 'r', encoding ='utf-8')
        lines = file.readlines()

        for line in lines:
            reviews.append(line)
        file.close()

    ####################################################
    # 댓글 명사추출 및 빈도분석(get_tags) 실시
        tags = get_tags(reviews)
        #print(tags)
        # 관심명사 단어구름 이미지 파일 저장 및 출력하기
        cloudimg = draw_cldimg(tags, imgPath)
        
        #생성된 클라우드 이미지 db에 저장.
        #mvData = Movie.objects.get(mvId=movieid)
        #mvData.mvCloud = cloudimg
        #mvData.save()
        
        context = { 'cloudimg' : cloudimg, 'movieid' : movieid}
        return render(request, 'movie/cloud.html', context=context)

def showImage(request):
    #저장된 클라우드 이미지 표시.


    mvid = request.GET.get('movieid')
    # 포스터 이미지
    SaveDir = os.getcwd()

    posterPath = "moive/media/poster/" + mvid + ".jpg"
    # 클라우드 이미지
    cldPath = "moive/media/cloudimg/" + mvid + ".png"

    posterimgPath = SaveDir + posterPath
    cldimgPath = SaveDir + cldPath

    mvData = Movie.objects.get(mvId=mvid)
    
    mvinfoList = []

    for i in mvData:
        mvinfoList[i] = mvData[i]

    context = { 'mvinfoList' : mvinfoList, 'poster': posterimgPath, 'cloud': cldimgPath}

    return render(request, 'movie/showimage.html', context = context)


    




