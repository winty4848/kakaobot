from django.conf.urls import url
from dguyummy import views
urlpatterns = [
    url(r'^keyboard/', views.keyboard),
    url(r'^message', views.answer),
    url(r'^crawl/', views.crawl),
]