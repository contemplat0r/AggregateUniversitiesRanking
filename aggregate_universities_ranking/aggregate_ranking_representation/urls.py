from django.conf.urls import url
from . import views

urlpatterns = [
        #url(r'^$', views.index, name='index'),
        url(r'^table$', views.RankingTableAPIView.as_view(), name='ranking_table_exp'),
]
