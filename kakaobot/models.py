from django.db import models

class Menu(models.Model):
    id = models.AutoField(primary_key=True)
    ## 식당이름 저장
    cafe_name = models.CharField(max_length=30, default="")
    ## 메뉴와 가격 저장
    menu = models.CharField(max_length=100, default="")
    ## 날짜 저장
    date=models.CharField(max_length=30, default="")

class Game(models.Model):
    user_key = models.CharField(max_length=255, primary_key=True)
    ## 이긴 횟수
    win = models.IntegerField()
    ## 비긴횟수
    draw = models.IntegerField()
    ## 진 횟수
    lose = models.IntegerField()