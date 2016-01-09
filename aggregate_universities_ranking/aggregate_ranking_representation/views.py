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


def prepare_ranktable_to_response(selected_rankings_names, aggregate_ranking_dataframe):
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

def prepare_correlation_matrix_to_response(aggregate_ranking_dataframe):
    dataframe_prepared_for_calculate_correlation = aggregate_ranking_dataframe.drop('university_name', axis=1)
    dataframe_prepared_for_calculate_correlation.rename(columns={'aggregate_rank' : 'Aggregate Rank', 'rank' : 'Rank'}, inplace=True)
    correlation_matrix = dataframe_prepared_for_calculate_correlation.corr(method='spearman')
    correlation_matrix_dict = correlation_matrix.to_dict()
    correlation_matrix_dict_keys = correlation_matrix_dict.keys()
    correlation_matrix_table = []
    correlation_matrix_table_first_row = [' ']
    correlation_matrix_table_first_row.extend(correlation_matrix_dict_keys)
    correlation_matrix_table.append(correlation_matrix_table_first_row)
    for key in correlation_matrix_dict_keys:
        row = [key]
        record = correlation_matrix_dict[key]
        for key_1 in correlation_matrix_dict_keys:
            row.append(float('{0:.2f}'.format(record[key_1])))
        correlation_matrix_table.append(row)

    return correlation_matrix_table

def index(request):

    return render(request, 'aggregate_ranking_representation/base.html')

def aggregate_universities_ranking_as_table(request):

    return render(request, 'aggregate_ranking_representation/table.html')

def ranktable(request):
    return HttpResponse('Hello, world. This is rankings table')


class RankingTableAPIView(APIView):

    def get(self, request, *args, **kw):
        response = Response('', status=status.HTTP_200_OK) #Must inform about error

        return response
    
    def post(self, request, format=None):
        request_data = request.data
        print 'recordsPerPage: ', request_data.get('recordsPerPage')
        print 'needsToBeUpdated: ', request_data.get('needsToBeUpdated')
        response_data = {'rankTable' : None, 'rankingsNamesList' : None, 'yearsList' : None, 'selectedYear' : None, 'paginationParameters' : {'recordsPerPageSelectionList' : [5, 10, 20, 50, 100, 200], 'currentPageNum' : 1, 'totalTableRecords' : 1000, 'totalPages' : 0, 'correlationMatrix' : None}}
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
            response_data['rankingsNamesList'] = short_rankings_names
            response_data['yearsList'] = years
            if request_data['selectedYear'] != None:
                selected_year = request_data['selectedYear']
        response_data['paginationParameters']['recordsPerPage']  = records_per_page
        response_data['paginationParameters']['currentPageNum'] = current_page_num
        print 'response_data[\'paginationParameters\'][\'currentPageNum\']: ', response_data['paginationParameters']['currentPageNum']
        print 'selected_year: ', selected_year

        ## This is temp!!!
        if selected_year > 2015:
            selected_year = 2015
        response_data['selectedYear'] = selected_year
        aggregate_ranking_dataframe = assemble_aggregate_ranking_dataframe(selected_rankings_names, int(selected_year))
        if request_data['needsToBeUpdated']:
            correlation_matrix = prepare_correlation_matrix_to_response(aggregate_ranking_dataframe)
        else:
            correlation_matrix = None
        response_data['correlationMatrix'] = correlation_matrix
        print 'response_data[\'correlationMatrix\']: ', response_data['correlationMatrix']
        aggregate_ranking_dataframe_len = aggregate_ranking_dataframe.count()[0]
        if records_per_page >= aggregate_ranking_dataframe_len:
            current_page_num = 1
        print 'aggregate_ranking_dataframe_len: ', aggregate_ranking_dataframe_len
        last_page_record_num = current_page_num * records_per_page
        first_page_record_num = last_page_record_num - records_per_page
        if last_page_record_num > aggregate_ranking_dataframe_len:
            last_page_record_num = aggregate_ranking_dataframe_len
        print 'first_page_record_num: ', first_page_record_num, ' last_page_record_num: ', last_page_record_num
        ranktable = prepare_ranktable_to_response(selected_rankings_names, aggregate_ranking_dataframe[first_page_record_num:last_page_record_num])
        total_records = aggregate_ranking_dataframe_len
        total_pages = total_records / records_per_page 
        if total_records % records_per_page > 0:
            total_pages = total_pages + 1
        response_data['paginationParameters']['totalPages'] = total_pages
        response_data['rankTable'] = ranktable
        response = Response(response_data, status=status.HTTP_200_OK)

        return response

