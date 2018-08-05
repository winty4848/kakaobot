from django.conf.urls import url
from kakaobot import views
urlpatterns = [
    url(r'^keyboard/', views.keyboard),
    url(r'^message', views.answer),
    url(r'^crawl/', views.crawl),
]