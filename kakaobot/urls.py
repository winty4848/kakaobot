from django.conf.urls import url
from kakaobot import views
from . import crawl
urlpatterns = [
    url(r'^keyboard/', views.keyboard),
    url(r'^message', views.answer),
    url(r'^crawl/', crawl.crawl),
]