# -*- coding: utf8 -*- 

import datetime
from django.shortcuts import render
from django.core.context_processors import csrf
from django.conf import settings
from django.http import HttpResponse
from rest_framework import serializers
from rest_framework.renderers import JSONRenderer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import RankingDescription, RankingValue, University 
from .name_matching import ranking_descriptions, build_aggregate_ranking_dataframe, assemble_aggregate_ranking_dataframe
from forms import SelectRankingsNamesAndYear

# Create your views here.

START_AGGREGATE_YEAR = getattr(settings, 'START_AGGREGATE_YEAR', 2014)
FINISH_AGGREGATE_YEAR = getattr(settings, 'FINISH_AGGREGATE_YEAR', datetime.date.today().year)


class Record(object):
    def __init__(self, name):
        self.name = name


#class RecordSerializer(serializers.Serializer):
#    name = serializers.CharField(max_length=128)

def make_show_ranktable(selected_rankings_names, aggregate_ranking_dataframe):
    ranktable = list()
    ranktable.append(['Rank', 'Aggregate Rank', 'University Name'] + selected_rankings_names)
    if aggregate_ranking_dataframe is not None:
        aggregate_ranking_as_list_of_dict = aggregate_ranking_dataframe.to_dict('record')
        for row in aggregate_ranking_as_list_of_dict:
            record = [row['rank'], row['aggregate_rank'], row['university_name']]
            for ranking_name in selected_rankings_names:
                record.append(row[ranking_name])
            ranktable.append(record)
    return ranktable

prepare_ranktable_to_response = make_show_ranktable


def index(request):
    return HttpResponse('Hello, world. This is first page of aggrgated rank')


def aggregate_universities_ranking_as_table(request):

    return render(request, 'aggregate_ranking_representation/table.html')


class RankingTableAPIView(APIView):

    def get(self, request, *args, **kw):
        response = Response('', status=status.HTTP_200_OK) #Must inform about error

        return response
    
    def post(self, request, format=None):
        request_data = request.data
        print 'recordsPerPage: ', request_data.get('recordsPerPage')
        response_data = {'ranktable' : None, 'rankings_names_list' : None, 'years_list' : None, 'paginationParameters' : {'recordsPerPageSelectionList' : [5, 10, 20, 50, 100, 200], 'currentPageNum' : 1, 'totalTableRecords' : 1000, 'totalPages' : 0}}
        current_page_num = request_data.get('currentPageNum')
        if current_page_num is None:
            current_page_num = 1
        records_per_page = request_data.get('recordsPerPage')
        if records_per_page is None:
            records_per_page = response_data['paginationParameters']['recordsPerPageSelectionList'][0]
        short_rankings_names = [ranking_name.short_name for ranking_name in RankingDescription.objects.all()] #This is right!
        short_rankings_names = [ranking_name for ranking_name in short_rankings_names if ranking_name in ranking_descriptions.keys()] # This is temp?
        years = range(FINISH_AGGREGATE_YEAR, START_AGGREGATE_YEAR - 1, -1)

        selected_rankings_names = short_rankings_names

        # selected_year = FINISH_AGGREGATE_YEAR # This is right!
        selected_year = 2015 # This is temp!

        if (request_data['selectedRankingNames'] != None) and (request_data['selectedRankingNames'] != []):
            print 'selectedRankingNames not None and not []'
            selected_rankings_names = request_data['selectedRankingNames']
            print 'selected_rankings_names: ', selected_rankings_names
            selected_rankings_names = [ranking_name for ranking_name in selected_rankings_names if ranking_name in ranking_descriptions.keys()] # This is temp!
            if request_data['selectedYear'] != None:
                selected_year = request_data['selectedYear']
        else:
            print 'selectedRankingNames is None'
            response_data['rankings_names_list'] = short_rankings_names
            response_data['years_list'] = years
            if request_data['selectedYear'] != None:
                selected_year = request_data['selectedYear']
        response_data['paginationParameters']['recordsPerPage']  = records_per_page
        response_data['paginationParameters']['currentPageNum'] = current_page_num
        print 'response_data[\'paginationParameters\'][\'currentPageNum\']: ', response_data['paginationParameters']['currentPageNum']
        print 'selected_year: ', selected_year

        ## This is temp!!!
        if selected_year > 2015:
            selected_year = 2015
        aggregate_ranking_dataframe = assemble_aggregate_ranking_dataframe(selected_rankings_names, int(selected_year))
        aggregate_ranking_dataframe_len = aggregate_ranking_dataframe.count()[0]
        print 'aggregate_ranking_dataframe_len: ', aggregate_ranking_dataframe_len
        last_page_record_num = current_page_num * records_per_page
        first_page_record_num = last_page_record_num - records_per_page
        if last_page_record_num > aggregate_ranking_dataframe_len:
            last_page_record_num = aggregate_ranking_dataframe_len
        print 'first_page_record_num: ', first_page_record_num, ' last_page_record_num: ', last_page_record_num
        ranktable = prepare_ranktable_to_response(selected_rankings_names, aggregate_ranking_dataframe[first_page_record_num:last_page_record_num])
        #ranktable = prepare_ranktable_to_response(selected_rankings_names, aggregate_ranking_dataframe)
        #total_records = len(ranktable) - 1
        total_records = aggregate_ranking_dataframe_len
        total_pages = total_records / records_per_page 
        if total_records % records_per_page > 0:
            total_pages = total_pages + 1
        response_data['paginationParameters']['totalPages'] = total_pages
        response_data['ranktable'] = ranktable
        #response = Response(ranktable, status=status.HTTP_200_OK)
        response = Response(response_data, status=status.HTTP_200_OK)

        return response

