
# coding: utf-8

import os
from os.path import abspath, join, dirname
import sys

import datetime
from functools import reduce
from copy import deepcopy
import pickle
import codecs
from pandas import Series, DataFrame
import pandas as pd
import numpy as np
import django
from timeit import default_timer as timer
from django.db import connection
from django.db.models import Sum, Count

DJANGO_PROJECT_DIR = join(abspath(join(dirname(__file__), '..')), 'aggregate_universities_ranking')
sys.path.append(DJANGO_PROJECT_DIR)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aggregate_universities_ranking.settings')

django.setup()
from aggregate_ranking_representation.models import RankingDescription, RawRankingRecord, University, RankingValue


ranking_table_as_list_preprocessor = lambda df: df.T
ranking_descriptions = {
        'QS' : {
            'dataframe_postprocessor' : None,
            'ranking_table_as_list_preprocessor' : ranking_table_as_list_preprocessor
            },
        'THE' : {
            #'dataframe_postprocessor' : the_dataframe_postprocessor,
            'dataframe_postprocessor' : None,
            'ranking_table_as_list_preprocessor' : ranking_table_as_list_preprocessor
            },
        #'Leiden' : {
        #    'dataframe_postprocessor' : None,
        #    'ranking_table_as_list_preprocessor' : ranking_table_as_list_preprocessor
        #    },
        'ARWU' : {
            'dataframe_postprocessor' : None,
            'ranking_table_as_list_preprocessor' : ranking_table_as_list_preprocessor
            },
        'NTU' : {
            'dataframe_postprocessor' : None,
            'ranking_table_as_list_preprocessor' : ranking_table_as_list_preprocessor
            },
        'URAP' : {
            'dataframe_postprocessor' : None,
            'ranking_table_as_list_preprocessor' : ranking_table_as_list_preprocessor
            },

        }


def prepare_year_to_compare(year):
    #return datetime.date(year, 1, 1)
    return year


def from_database(rankings_names_list, year):
    this_function_start_time = timer()

    rank_tables = list()

    year = prepare_year_to_compare(year)

    universities = University.objects.all()
    rankings_descriptions = RankingDescription.objects.filter(short_name__in=rankings_names_list, year=year)
    rankings_descriptions_related_dict = {description.short_name : description.rankingvalue_set.all().prefetch_related() for description in rankings_descriptions}
    
    multi_value_university_names = list()
    for university in universities:
        record = {'canonical_name' : university.university_name}
        ranks = dict()
        for ranking_name, ranking_values_related in rankings_descriptions_related_dict.items():
            #value_record = ranking_values_related.get(university_id=university.id)

            value_record = ranking_values_related.filter(university_id=university.id)[0]

            #value_record = ranking_values_related.filter(university_id=university.id)
            #if len(value_record) > 1:
            #    print ranking_name, university.id, university.university_name
            #    for value in value_record:
            #        print '\t', value.ranking_description.short_name, value.number_in_ranking_table
            #    multi_value_university_names.append(university.university_name)

            ranks.update({ranking_name : value_record.number_in_ranking_table})

        print 'len(connection.queries): ', len(connection.queries)
        if ranks != {}:
            record['ranks'] = ranks
            rank_tables.append(record)
    #print list(set(multi_value_university_names))
    #print len(list(set(multi_value_university_names)))
    print 'Total len(connection.queries): ', len(connection.queries)

    this_function_finish_time = timer()
    print 'from_database: total runtime = ', this_function_finish_time - this_function_start_time

    return rank_tables


def from_database_exp(rankings_names_list, year):
    # {'ranks': {u'QS': 156, u'NTU': 530, u'THE': 1603, u'URAP': 2001, u'ARWU': 501}, 'canonical_name': u'Ecole Centrale de Paris'}
    this_function_start_time = timer()

    rank_tables = list()

    year = prepare_year_to_compare(year)
    
    '''
    rankings_values_all = RankingValue.objects.all()
    universities = University.objects.all()
    for university in universities:
        print university.university_name
    print 'rankings_values_all.count(): ', rankings_values_all.count()
    #rankings_values_related = RankingValue.objects.all().prefetch_related()
    rankings_values_related = RankingValue.objects.all().select_related()
    print 'After RankingValue prefetch_related:  len(connection.queries): ', len(connection.queries)
    rankings_values_related_2014 = rankings_values_related.filter(ranking_description__year=2014)
    print 'rankings_values_related_2014.count(): ', rankings_values_related_2014.count()
    rankings_values_related_2015 = rankings_values_related.filter(ranking_description__year=2015)
    print 'rankings_values_related_2015.count(): ', rankings_values_related_2015.count()

    rankings_values_related_2015_qs = rankings_values_related_2015.filter(ranking_description__short_name='QS')
    for ranking_value in rankings_values_related_2015_qs:
    #for ranking_value in rankings_values_related:
        print ranking_value.university.university_name
        #pass
    print 'rankings_values_related_2015_qs.count(): ', rankings_values_related_2015_qs.count()

    print 'After RankingValue prefetch_related filter by year:  len(connection.queries): ', len(connection.queries)
    rankings_values_related = RankingValue.objects.all().select_related()
    print 'After RankingValue select_related:  len(connection.queries): ', len(connection.queries)
    '''

    universities = University.objects.all()
    rankings_values_related = RankingValue.objects.filter(ranking_description__short_name__in=rankings_names_list).filter(ranking_description__year=year).select_related()
    #rankings_values_related = RankingValue.objects.filter(ranking_description__year=year).select_related()
    for university in universities:
        #print university.university_name
        record = {'canonical_name' : university.university_name, 'ranks' : {}}
        ranks = {}
        '''
        for ranking_name in rankings_names_list:
            for ranking_value_record in rankings_values_related.filter(ranking_description__short_name=ranking_name):
                #print ranking_value_record.number_in_ranking_table
                if university.university_name == ranking_value_record.university.university_name:
                    print ranking_name, university.university_name, ranking_value_record.number_in_ranking_table
                    ranks.update({ranking_name : ranking_value_record.number_in_ranking_table})
                    break
        '''
        for ranking_value_record in rankings_values_related:
            if university.university_name == ranking_value_record.university.university_name:
                ranks.update({ranking_value_record.ranking_description.short_name : ranking_value_record.number_in_ranking_table})

        print 'len(connection.queries): ', len(connection.queries)
        record['ranks'] = ranks
        rank_tables.append(record)


    print 'len(connection.queries): ', len(connection.queries)

    this_function_finish_time = timer()
    print 'from_database: total runtime = ', this_function_finish_time - this_function_start_time

    return rank_tables

def from_database_accelerated():
    cursor = connection.cursor()
    #cursor.execute('SELECT * FROM aggregate_ranking_representation_rankingdescription')
    year = 2015
    #cursor.execute('SELECT aggregate_ranking_representation_rankingdescription.short_name AS ranking_name, aggregate_ranking_representation_rankingvalue.number_in_ranking_table AS ranking_value, aggregate_ranking_representation_university.university_name AS university_name, COUNT(aggregate_ranking_representation_rankingdescription.short_name) AS rankings_num, SUM(aggregate_ranking_representation_rankingvalue.number_in_ranking_table) AS aggregate_ranking FROM aggregate_ranking_representation_rankingdescription, aggregate_ranking_representation_rankingvalue, aggregate_ranking_representation_university WHERE aggregate_ranking_representation_rankingvalue.ranking_description_id = aggregate_ranking_representation_rankingdescription.id AND aggregate_ranking_representation_rankingvalue.university_id = aggregate_ranking_representation_university.id AND aggregate_ranking_representation_rankingdescription.year = %s GROUP BY university_name' % year)
    #cursor.execute('SELECT aggregate_ranking_representation_rankingdescription.short_name, aggregate_ranking_representation_rankingvalue.number_in_ranking_table, aggregate_ranking_representation_university.university_name AS university_name, COUNT(aggregate_ranking_representation_rankingdescription.short_name) AS rankings_num, SUM(aggregate_ranking_representation_rankingvalue.number_in_ranking_table) AS aggregate_ranking FROM aggregate_ranking_representation_rankingdescription, aggregate_ranking_representation_rankingvalue, aggregate_ranking_representation_university WHERE aggregate_ranking_representation_rankingvalue.ranking_description_id = aggregate_ranking_representation_rankingdescription.id AND aggregate_ranking_representation_rankingvalue.university_id = aggregate_ranking_representation_university.id AND aggregate_ranking_representation_rankingdescription.year = %s GROUP BY university_name' % year)
    cursor.execute('SELECT aggregate_ranking_representation_university.university_name AS university_name, COUNT(aggregate_ranking_representation_rankingdescription.short_name) AS rankings_num, SUM(aggregate_ranking_representation_rankingvalue.number_in_ranking_table) AS aggregate_ranking FROM aggregate_ranking_representation_rankingdescription, aggregate_ranking_representation_rankingvalue, aggregate_ranking_representation_university WHERE aggregate_ranking_representation_rankingvalue.ranking_description_id = aggregate_ranking_representation_rankingdescription.id AND aggregate_ranking_representation_rankingvalue.university_id = aggregate_ranking_representation_university.id AND aggregate_ranking_representation_rankingdescription.year = %s GROUP BY university_name' % year)

    rows = cursor.fetchall()

    for row in rows:
        print row


def from_database_accelerate(rankings_names_list, year):
    # {'ranks': {u'QS': 156, u'NTU': 530, u'THE': 1603, u'URAP': 2001, u'ARWU': 501}, 'canonical_name': u'Ecole Centrale de Paris'}
    this_function_start_time = timer()

    rank_tables = list()

    year = prepare_year_to_compare(year)

    universities = University.objects.all()
    rankings_values_related = RankingValue.objects.filter(ranking_description__short_name__in=rankings_names_list).filter(ranking_description__year=year).select_related()

    #temp = rankings_values_related.values('university__university_name').annotate(aggregate_ranking_value=Sum('number_in_ranking_table'))
    #for row in temp[:10]:
    #    print row

    df = DataFrame(list(rankings_values_related.values('ranking_description__short_name', 'number_in_ranking_table', 'university__university_name')))
    print df.head()

    grouped_df = df.groupby(df.university__university_name)

    for name, group in grouped_df:
        print name
        print group



if __name__ == '__main__':
    

    #ranking_table = from_database(ranking_descriptions.keys(), 2015)
    #print ranking_table[0]
    #from_database_exp(ranking_descriptions.keys(), 2015)
    from_database_accelerate(ranking_descriptions.keys(), 2015)
    #from_database_accelerated()
