from django.conf.urls import url
from . import views

urlpatterns = [
        url(r'^$', views.index, name='index'),
        #url(r'^aggregate_universities_ranking_as_table$', views.aggregate_universities_ranking_as_table, name='aggregate_universities_ranking_as_table'),
        url(r'^table$', views.aggregate_universities_ranking_as_table, name='aggregate_universities_ranking_as_table'),
]
