from django.conf.urls import url
from . import views

urlpatterns = [
        #url(r'^$', views.index, name='index'),
        url(r'^table$', views.RankingTableAPIView.as_view(), name='ranking_table_exp'),
        url(r'^download$', views.FileDownloadAPIView.as_view(), name='file_download'),
        url(r'^texts$', views.BigSiteTextsAPIView.as_view(), name='big_site_texts'),
]
