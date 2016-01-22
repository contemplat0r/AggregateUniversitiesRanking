# -*- coding: utf8 -*- 

import datetime
import os
import codecs
import md5
import csv
import xlwt
from functools import reduce
from zipfile import ZipFile, ZIP_DEFLATED
from gzip import GzipFile
from StringIO import StringIO
from django.shortcuts import render
from django.core.context_processors import csrf
from django.core.servers.basehttp import FileWrapper
from django.conf import settings
from django.http import HttpResponse
from rest_framework import serializers
from rest_framework.renderers import JSONRenderer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from pandas import DataFrame
from .models import RankingDescription, RankingValue, University 
from .name_matching import ranking_descriptions, build_aggregate_ranking_dataframe, assemble_aggregate_ranking_dataframe
from forms import SelectRankingsNamesAndYear

# Create your views here.

START_AGGREGATE_YEAR = getattr(settings, 'START_AGGREGATE_YEAR', 2014)
FINISH_AGGREGATE_YEAR = getattr(settings, 'FINISH_AGGREGATE_YEAR', datetime.date.today().year)

BASE_DIR = getattr(settings, 'BASE_DIR')
current_dir = os.path.join(BASE_DIR, 'aggregate_ranking_representation')
csv_files_dir_relative_path = os.path.join('static', 'csv')
csv_files_dir = os.path.join(current_dir, csv_files_dir_relative_path)

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

def calculate_correlation_matrix(aggregate_ranking_dataframe):
    dataframe_prepared_for_calculate_correlation = aggregate_ranking_dataframe.drop('university_name', axis=1)
    dataframe_prepared_for_calculate_correlation.rename(columns={'aggregate_rank' : 'Aggregate Rank', 'rank' : 'Rank'}, inplace=True)
    return dataframe_prepared_for_calculate_correlation.corr(method='spearman')

def prepare_correlation_matrix_to_response(correlation_matrix):
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


def assemble_csv_filename(selected_rankings_names, year):
    selected_rankings_names = sorted(selected_rankings_names)
    csv_filename = reduce(lambda filename, rankname: filename + rankname + '_', selected_rankings_names, str()) + str(year) + '.csv'
    return csv_filename.lower()


def assemble_filename(selected_rankings_names, year, data_type, file_type):
    print 'Entry in assemble_filename'
    selected_rankings_names = sorted(selected_rankings_names)
    filename = data_type + '_' +  reduce(lambda filename, rankname: filename + rankname + '_', selected_rankings_names, str()) + str(year) + '.' + file_type
    print 'assemble_filename, filename: ', filename.lower()
    return filename.lower()


def get_file(file_dir, filename):
    print 'Entry in get_file'
     
    file_path = os.path.join(file_dir, filename)
    print 'get_file, file_path: ', file_path
    if check_file_exist(file_path):
        #file_stream = codecs.open(file_path, 'r', encoding='utf-8')
        file_stream = open(file_path, 'r')
        file_content = file_stream.read()
        file_stream.close()
        return file_content
    else:
        return None


def check_file_exist(csv_file_path):
    return os.path.exists(csv_file_path)


def to_csv(csv_file_path, dataframe):
    print 'Entry in to_csv'
    print 'to_csv, before call dataframe.to_csv'
    dataframe.to_csv(csv_file_path, sep=';', encoding='utf-8')
    return


def to_xls(xls_file_path, dataframe):
    print 'Entry in to_xls'
    print 'to_xls, before call dataframe.to_xls'
    dataframe.to_excel(xls_file_path, index=False)
    return


def index(request):
    return render(request, 'aggregate_ranking_representation/base.html')


class RankingTableAPIView(APIView):

    def get(self, request, *args, **kw):
        response = Response('', status=status.HTTP_200_OK) #Must inform about error

        return response
    
    def post(self, request, format=None):
        request_data = request.data
        print 'recordsPerPage: ', request_data.get('recordsPerPage')
        print 'needsToBeUpdated: ', request_data.get('needsToBeUpdated')
        response_data = {'rankTable' : None, 'rankingsNamesList' : None, 'yearsList' : None, 'selectedYear' : None, 'paginationParameters' : {'recordsPerPageSelectionList' : [100, 200], 'currentPageNum' : 1, 'totalTableRecords' : 1000, 'totalPages' : 0, 'correlationMatrix' : None}}
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

        aggregate_ranking_dataframe = DataFrame()
        csv_filename = assemble_filename(selected_rankings_names, selected_year, 'ranktable', 'csv')
        xls_filename = assemble_filename(selected_rankings_names, selected_year, 'ranktable', 'xls')
        print 'csv_filename: ', csv_filename
        print 'csv_files_dir', csv_files_dir
        csv_file_path = os.path.join(csv_files_dir, csv_filename)
        xls_file_path = os.path.join(csv_files_dir, xls_filename)

        if not check_file_exist(csv_file_path):
            print 'csv file, %s' % csv_file_path, ' not exists'
            aggregate_ranking_dataframe = assemble_aggregate_ranking_dataframe(selected_rankings_names, int(selected_year))
            print 'aggregate_ranking_dataframe.count():\n', aggregate_ranking_dataframe.count()
            to_csv(csv_file_path, aggregate_ranking_dataframe)
            print 'After aggregate_ranking_to_csv'
        else:
            print 'csv file, %s' % csv_file_path, ' exists'
            aggregate_ranking_dataframe = DataFrame.from_csv(csv_file_path, sep=';', encoding='utf-8')

        if not check_file_exist(xls_file_path):
            to_xls(xls_file_path, aggregate_ranking_dataframe)

        correlation_matrix = DataFrame()
        csv_filename = assemble_filename(selected_rankings_names, selected_year, 'correlation', 'csv')
        print 'csv_filename: ', csv_filename
        print 'csv_files_dir', csv_files_dir
        csv_file_path = os.path.join(csv_files_dir, csv_filename)

        if not check_file_exist(csv_file_path):
            print 'csv file, %s' % csv_file_path, ' not exists'
            correlation_matrix = calculate_correlation_matrix(aggregate_ranking_dataframe)
            to_csv(csv_file_path, correlation_matrix)
            print 'After aggregate_ranking_to_csv'
        else:
            print 'csv file, %s' % csv_file_path, ' exists'
            correlation_matrix = DataFrame.from_csv(csv_file_path, sep=';', encoding='utf-8')


        #print 'Before correlation_matrix calculation'
        #correlation_matrix = calculate_correlation_matrix(aggregate_ranking_dataframe)
        prepared_for_response_correlation_matrix = None
        if request_data['needsToBeUpdated']:
            prepared_for_response_correlation_matrix = prepare_correlation_matrix_to_response(correlation_matrix)
        else:
            prepared_for_response_correlation_matrix = None
        response_data['correlationMatrix'] = prepared_for_response_correlation_matrix
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


class FileDownloadAPIView(APIView):

    def get(self, request, *args, **kw):
        response = Response('', status=status.HTTP_200_OK) #Must inform about error

        return response
    
    def post(self, request, format=None):
        request_data = request.data
        print dir(request)
        #print request.get('accepted_media_type')
        print request.accepted_media_type
        #print request.get('content_type')
        print request.content_type
        #print request.get('query_params')
        print request.query_params
        
        selected_rankings_names = request_data.get('selectedRankingNames') 
        selected_year = request_data.get('selectedYear')
        data_type = request_data.get('dataType')
        file_type = request_data.get('fileType')


        selected_year = 2015 # This is temp!
        
        if selected_year == None or (selected_year != None and (selected_year > FINISH_AGGREGATE_YEAR or selected_year < START_AGGREGATE_YEAR)):
            pass
            #selected_year = FINISH_AGGREGATE_YEAR

        short_rankings_names = [ranking_name.short_name for ranking_name in RankingDescription.objects.all()] #This is right!
        short_rankings_names = [ranking_name for ranking_name in short_rankings_names if ranking_name in ranking_descriptions.keys()] # This is temp?
        selected_rankings_names = short_rankings_names

        if selected_rankings_names == []:
            selected_rankings_names = short_rankings_names

        if data_type != None:
            data_type = data_type.lower()
        else:
            data_type = 'ranktable'

        if file_type != None:
            file_type = file_type.lower()
        else:
            file_type = 'csv'

        filename = assemble_filename(selected_rankings_names, selected_year, data_type, file_type)
        file_content = get_file(csv_files_dir , filename)
        print md5.new(file_content).hexdigest()
        file_buffer = StringIO()
        gzip_file = GzipFile(mode='wb', compresslevel=6, fileobj=file_buffer)
        gzip_file.write(file_content)
        gzip_file.flush()
        gzip_file.close()
        gzipped_content = file_buffer.getvalue()

        response = HttpResponse(gzipped_content)
        ##response = HttpResponse(file_content)
        response['Content-Encoding'] = 'gzip'
        ##response['Content-Encoding'] = 'application/vnd.ms-excel;charset=utf-8'
        response['Content-Length'] = str(len(gzipped_content))
        ##response['Content-Type'] = 'application/vnd.ms-excel'
        #response['Content-Length'] = str(len(file_content))
        ##print response['Content-Encoding']
        #print response['Content-Length']
        ##response = HttpResponse(content_type='application/vnd.ms-excel')
        ##response['Content-Disposition'] = 'attachment; filename=%s' % filename
        ##print response['Content-Disposition']
        ##response.write(file_content)
        return response

