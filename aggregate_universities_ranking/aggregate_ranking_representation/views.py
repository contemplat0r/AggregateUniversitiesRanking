# -*- coding: utf8 -*- 

import datetime
import os
import codecs
import csv
#import xlwt
from functools import reduce
from zipfile import ZipFile, ZIP_DEFLATED
from gzip import GzipFile
from StringIO import StringIO
from cStringIO import StringIO as BytesIO
from django.shortcuts import render
from django.core.context_processors import csrf
from django.core.servers.basehttp import FileWrapper
from django.conf import settings
from django.http import HttpResponse
from django.core.cache import caches
from rest_framework import serializers
from rest_framework.renderers import JSONRenderer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from pandas import DataFrame, ExcelWriter
import pandas as pd
from .models import RankingDescription, RankingValue, University, Result
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

def prepare_ranktable_for_table_file(aggregate_ranking_dataframe):
    aggregate_ranking_dataframe_for_table_file = aggregate_ranking_dataframe.rename(columns={'aggregate_rank' : 'Aggregate Rank', 'rank' : 'Rank', 'university_name' : 'University'})
    columns_names = aggregate_ranking_dataframe_for_table_file.columns.tolist()
    right_ordered_columns = ['University', 'Rank', 'Aggregate Rank']
    tail = [column_name for column_name in columns_names if column_name not in right_ordered_columns]
    right_ordered_columns.extend(tail)
    aggregate_ranking_dataframe_for_table_file = aggregate_ranking_dataframe_for_table_file[right_ordered_columns]
    
    return aggregate_ranking_dataframe_for_table_file

def calculate_correlation_matrix(aggregate_ranking_dataframe):
    dataframe_prepared_for_calculate_correlation = aggregate_ranking_dataframe.drop('university_name', axis=1)
    dataframe_prepared_for_calculate_correlation.rename(columns={'aggregate_rank' : 'Aggregate Rank', 'rank' : 'Rank'}, inplace=True)
    columns_names = dataframe_prepared_for_calculate_correlation.columns.tolist()
    right_ordered_columns = ['Rank', 'Aggregate Rank']
    tail = [column_name for column_name in columns_names if column_name not in right_ordered_columns]
    right_ordered_columns.extend(tail)
    dataframe_prepared_for_calculate_correlation = dataframe_prepared_for_calculate_correlation[right_ordered_columns]

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


def assemble_filename(selected_rankings_names, year, data_type, file_type=None):
    print 'Entry in assemble_filename'
    selected_rankings_names = sorted(selected_rankings_names)
    filename = data_type + '_' +  reduce(lambda filename, rankname: filename + rankname + '_', selected_rankings_names, str()) + str(year)
    if file_type != None:
        filename = filename + '.' + file_type
    print 'assemble_filename, filename: ', filename.lower()
    return filename.lower()


def to_mem_excel(dataframe, sheet_name='WorkSheet'):
    iobuffer = BytesIO()
    writer = ExcelWriter(iobuffer, engine='xlwt')
    dataframe.to_excel(writer, sheet_name=sheet_name)
    writer.save()
    iobuffer.flush()
    iobuffer.seek(0)
    return iobuffer.getvalue()

def to_mem_csv(dataframe):
    iobuffer = BytesIO()
    dataframe.to_csv(iobuffer, sep=';', encoding='utf-8')
    iobuffer.flush()
    iobuffer.seek(0)
    return iobuffer.getvalue()

def to_gzip(data):
    iobuffer = StringIO()
    gzip_mem_object = GzipFile(mode='wb', compresslevel=6, fileobj=iobuffer)
    gzip_mem_object.write(data)
    gzip_mem_object.flush()
    gzip_mem_object.close()
    return iobuffer.getvalue()


'''
class Storage(object):

    def __init__(self):
        self.cache = caches['default']

    def save(self, key, value):
        self.cache.set(key, value, None)
        return

    def get(self, key):
        return self.cache.get(key)

    def delete(self, key):
        self.cache.delete(key)
        return

    def clear(self):
        self.cache.clear()
        '''


class Storage(object):

    def __init__(self):
        #self.cache = caches['default']
        self.storage_model = Result

    def save(self, key, value):
        print 'Entry in Storage.save method'
        #self.cache.set(key, value, None)
        item_list = self.storage_model.objects.filter(key=key)
        #if item_list == []:
        if len(item_list) == 0:
            print 'len(item_list) == 0'
            new_stored_item = self.storage_model(key=key, value=value)
            print 'After create new_stored item'
            try:
                new_stored_item.save()
            except Error as e:
                print e
            print 'After save new_stored item'
        else:
            print 'len(item_list) == ', len(item_list)
        return

    def get(self, key):
        print 'Entry in storage.get'
        #return self.cache.get(key)
        item_list = self.storage_model.objects.filter(key=key)
        print 'storage.get, item_list: ', item_list
        #if item_list != []:
        if len(item_list) > 0:
            print 'storage.get, item_list != []'
            return item_list[0].value
        else:
            print 'storage.get, item_list == []'
            return None


    def delete(self, key):
        #self.cache.delete(key)
        item_list = self.storage_model.objects.filter(key=key)
        #if item_list != []:
        if len(item_list) > 0:
            item = item_list[0]
            item.delete()
        return
    
    def clear(self):
        self.storage_model.objects.all().delete()



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
        #storage = Storage()
        #storage.clear()
        request_data = request.data
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

        selected_year = FINISH_AGGREGATE_YEAR # This is right!

        if (request_data['selectedRankingNames'] != None) and (request_data['selectedRankingNames'] != []):
            selected_rankings_names = request_data['selectedRankingNames']
            selected_rankings_names = [ranking_name for ranking_name in selected_rankings_names if ranking_name in ranking_descriptions.keys()] # This is temp!
            if request_data['selectedYear'] != None:
                selected_year = request_data['selectedYear']
        else:
            response_data['rankingsNamesList'] = short_rankings_names
            response_data['yearsList'] = years
            if request_data['selectedYear'] != None:
                selected_year = request_data['selectedYear']
        response_data['paginationParameters']['recordsPerPage']  = records_per_page
        response_data['paginationParameters']['currentPageNum'] = current_page_num

        response_data['selectedYear'] = selected_year

        aggregate_ranking_dataframe = DataFrame()

        print 'Before generating various storgae keys'
        aggregate_ranking_dataframe_storage_key = assemble_filename(selected_rankings_names, selected_year, 'ranktable')
        aggregate_ranking_storage_key_csv = aggregate_ranking_dataframe_storage_key + '.csv'
        aggregate_ranking_storage_key_xls = aggregate_ranking_dataframe_storage_key + '.xls'
        print 'Before save/retrieve aggregate_ranking_dataframe to/from storage'

        print 'aggregate_ranking_dataframe_storage_key: ', aggregate_ranking_dataframe_storage_key
        saved_aggregate_ranking_dataframe_list = Result.objects.filter(key=aggregate_ranking_dataframe_storage_key)
        print 'saved_aggregate_ranking_dataframe_list: ', saved_aggregate_ranking_dataframe_list
        if list(saved_aggregate_ranking_dataframe_list) == []:
            print 'before call assemble_aggregate_ranking_dataframe'
            aggregate_ranking_dataframe = assemble_aggregate_ranking_dataframe(selected_rankings_names, int(selected_year))

            print 'before create assemble_aggregate_ranking_dataframe storage_record'
            storage_record = Result(key=aggregate_ranking_dataframe_storage_key, value=to_mem_csv(aggregate_ranking_dataframe))
            print 'before save storage records'
            storage_record.save()
        else:
            print 'saved_aggregate_ranking_dataframe_list != []'
            print 'retrieve aggregate_ranking_dataframe from storage'
            aggregate_ranking_dataframe = pd.read_csv(StringIO(saved_aggregate_ranking_dataframe_list[0].value), sep=';', encoding='utf-8')


        '''
        if storage.get(aggregate_ranking_dataframe_storage_key) is None:
        #if storage.get(aggregate_ranking_dataframe_storage_key) == None:
            print 'storage.get(aggregate_ranking_dataframe_storage_key) is None'
            aggregate_ranking_dataframe = assemble_aggregate_ranking_dataframe(selected_rankings_names, int(selected_year))
            #storage.save(aggregate_ranking_dataframe_storage_key, aggregate_ranking_dataframe)
            storage.save(aggregate_ranking_dataframe_storage_key, to_mem_csv(aggregate_ranking_dataframe))
            #storage.save(aggregate_ranking_dataframe_storage_key, to_mem_csv(aggregate_ranking_dataframe_for_table_file))
        else:
            print 'storage.get(aggregate_ranking_dataframe_storage_key) not None'
            aggregate_ranking_dataframe = pd.read_csv(StringIO(storage.get(aggregate_ranking_dataframe_storage_key)), sep=';', encoding='utf-8')
            print type(storage.get(aggregate_ranking_dataframe_storage_key))
            print 'after load aggregate_ranking_dataframe: '
        
        ''' 
        print 'Before call assemble_aggregate_ranking_dataframe'
        #aggregate_ranking_dataframe = assemble_aggregate_ranking_dataframe(selected_rankings_names, int(selected_year))
        print 'After call assemble_aggregate_ranking_dataframe'
        #print 'aggregate_ranking_dataframe.head(): ', aggregate_ranking_dataframe.head()
        print 'aggregate_ranking_dataframe[:3]: ', aggregate_ranking_dataframe[:3]

        print 'Before call prepare_ranktable_for_table_file'
        aggregate_ranking_dataframe_for_table_file = prepare_ranktable_for_table_file(aggregate_ranking_dataframe)
        print 'After call prepare_ranktable_for_table_file'

        '''
        if storage.get(aggregate_ranking_storage_key_csv) is None:
        #if storage.get(aggregate_ranking_storage_key_csv) == None:
            storage.save(aggregate_ranking_storage_key_csv, to_gzip(to_mem_csv(aggregate_ranking_dataframe_for_table_file)))
        
        if storage.get(aggregate_ranking_storage_key_xls) is None:
        #if storage.get(aggregate_ranking_storage_key_xls) == None:
            storage.save(aggregate_ranking_storage_key_xls, to_gzip(to_mem_excel(aggregate_ranking_dataframe_for_table_file)))
        '''


        correlation_matrix = DataFrame()
        
        print 'Before generation various correlation matrix keys'
        correlation_matrix_storage_key = assemble_filename(selected_rankings_names, selected_year, 'correlation')
        correlation_matrix_storage_key_csv = correlation_matrix_storage_key + '.csv'
        correlation_matrix_storage_key_xls = correlation_matrix_storage_key + '.xls'
        print 'After generation various correlation matrix keys'
        
        '''
        if storage.get(correlation_matrix_storage_key) is None:
        #if storage.get(correlation_matrix_storage_key) == None:
            correlation_matrix = calculate_correlation_matrix(aggregate_ranking_dataframe)
            storage.save(correlation_matrix_storage_key, to_mem_csv(correlation_matrix))
        else:
            correlation_matrix = pd.read_csv(StringIO(storage.get(correlation_matrix_storage_key)), sep=';', encoding='utf-8')
        print correlation_matrix
        '''
        
        print 'Before call calculate_correlation_matrix'
        correlation_matrix = calculate_correlation_matrix(aggregate_ranking_dataframe)
        print 'After call calculate_correlation_matrix'
        print 'correlation_matrix: '
        print correlation_matrix

        '''
        if storage.get(correlation_matrix_storage_key_csv) is None:
        #if storage.get(correlation_matrix_storage_key_csv) == None:
            storage.save(correlation_matrix_storage_key_csv, to_gzip(to_mem_csv(correlation_matrix)))
        
        if storage.get(correlation_matrix_storage_key_xls) is None:
        #if storage.get(correlation_matrix_storage_key_xls) == None:
            storage.save(correlation_matrix_storage_key_xls, to_gzip(to_mem_excel(correlation_matrix)))
        '''

        #prepared_for_response_correlation_matrix = None
        #if request_data['needsToBeUpdated']:
        #    prepared_for_response_correlation_matrix = prepare_correlation_matrix_to_response(correlation_matrix)
        #else:
        #    prepared_for_response_correlation_matrix = None

        print 'Before call prepare_correlation_matrix_to_response'
        prepared_for_response_correlation_matrix = prepare_correlation_matrix_to_response(correlation_matrix)
        print 'After call prepare_correlation_matrix_to_response'
        response_data['correlationMatrix'] = prepared_for_response_correlation_matrix

        aggregate_ranking_dataframe_len = aggregate_ranking_dataframe.count()[0]
        if records_per_page >= aggregate_ranking_dataframe_len:
            current_page_num = 1

        last_page_record_num = current_page_num * records_per_page
        first_page_record_num = last_page_record_num - records_per_page
        
        if last_page_record_num > aggregate_ranking_dataframe_len:
            last_page_record_num = aggregate_ranking_dataframe_len

        ranktable = prepare_ranktable_to_response(selected_rankings_names, aggregate_ranking_dataframe[first_page_record_num:last_page_record_num])
        total_records = aggregate_ranking_dataframe_len
        total_pages = total_records / records_per_page 

        if total_records % records_per_page > 0:
            total_pages = total_pages + 1

        response_data['paginationParameters']['totalPages'] = total_pages
        response_data['rankTable'] = ranktable
        
        print 'Before creating response'
        response = Response(response_data, status=status.HTTP_200_OK)
        print 'After creating response and before return'

        return response


class FileDownloadAPIView(APIView):

    def get(self, request, *args, **kw):
        response = Response('', status=status.HTTP_200_OK) #Must inform about error

        return response
    
    def post(self, request, format=None):
        storage = Storage()
        request_data = request.data
        
        selected_rankings_names = request_data.get('selectedRankingNames') 
        print 'FileDownloadAPIView post, selected_rankings_names: ', selected_rankings_names
        selected_year = request_data.get('selectedYear')
        data_type = request_data.get('dataType')
        file_type = request_data.get('fileType')

        if selected_year == None or (selected_year != None and (selected_year > FINISH_AGGREGATE_YEAR or selected_year < START_AGGREGATE_YEAR)):
            selected_year = FINISH_AGGREGATE_YEAR

        short_rankings_names = [ranking_name.short_name for ranking_name in RankingDescription.objects.all()] #This is right!
        short_rankings_names = [ranking_name for ranking_name in short_rankings_names if ranking_name in ranking_descriptions.keys()] # This is temp?

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

        storage_key = assemble_filename(selected_rankings_names, selected_year, data_type, file_type)
        print 'FileDownloadAPIView post, storage_key: ', storage_key
        #download_file_data = storage.get(storage_key)
        download_file_buffer = storage.get(storage_key)
        download_file_data = StringIO(download_file_buffer).getvalue()
        #print 'FileDownloadAPIView post, download_file_data: ', download_file_data
        response = HttpResponse(download_file_data)
        response['Content-Encoding'] = 'gzip'
        response['Content-Length'] = str(len(download_file_data))
        return response

