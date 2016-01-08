from django.conf.urls import url
from . import views

urlpatterns = [
        url(r'^$', views.index, name='index'),
        #url(r'^table$', views.aggregate_universities_ranking_as_table, name='aggregate_universities_ranking_as_table'),
        url(r'^api/table$', views.RankingTableAPIView.as_view(), name='ranking_table'),
        url(r'^#/table$', views.RankingTableAPIView.as_view(), name='ranking_table'),
        url(r'^ranktable$', views.ranktable, name='ranktable'),
]
