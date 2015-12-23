from django.conf.urls import url
from . import views

urlpatterns = [
        url(r'^$', views.index, name='index'),
        #url(r'^aggregate_universities_ranking_as_table$', views.aggregate_universities_ranking_as_table, name='aggregate_universities_ranking_as_table'),
        url(r'^table$', views.aggregate_universities_ranking_as_table, name='aggregate_universities_ranking_as_table'),
        url(r'^api/record$', views.record_rest, name='record_rest'),
        #url(r'^api/list$', views.records_list, name='records_list'),
        url(r'^api/list$', views.ListAPIView.as_view(), name='records_list'),
        url(r'^api/table$', views.RankingTableAPIView.as_view(), name='ranking_table'),
]
