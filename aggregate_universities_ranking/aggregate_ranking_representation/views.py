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


class RecordSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=128)


def record_rest(request):
    print 'Entry in record_rest'
    record = Record('MIT')
    print 'record_rest, record: ', record
    serializer = RecordSerializer(record)
    print 'record_rest, serializer.data: ', serializer.data
    json = JSONRenderer().render(serializer.data)
    print 'record_rest, json: ', json
    return HttpResponse(json)

class ListAPIView(APIView):

    def get(self, request, *args, **kw):
        response = Response(['a', 'b', 'c'], status=status.HTTP_200_OK)
        return response

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

def index(request):
    return HttpResponse('Hello, world. This is first page of aggrgated rank')

def assign_choices_values(select_form, short_rankings_names_choice_set, year_choice_set):
    select_form.fields['select_rankings_names_field'].choices = short_rankings_names_choice_set
    select_form.fields['select_year_field'].choices = year_choice_set
    return 

def aggregate_universities_ranking_as_table(request):
    #print 'Entry in aggregate_universities_ranking_as_table'
    short_rankings_names = [ranking_name.short_name for ranking_name in RankingDescription.objects.all()]
    short_rankings_names_choice_set = tuple([(short_name, short_name) for short_name in short_rankings_names])
    year_choice_set = tuple([(year, year) for year in range(FINISH_AGGREGATE_YEAR, START_AGGREGATE_YEAR - 1, -1)])

    select_rankings_names_form = SelectRankingsNamesAndYear()
    assign_choices_values(select_rankings_names_form, short_rankings_names_choice_set, year_choice_set)

    selected_rankings_names = short_rankings_names
    selected_year = FINISH_AGGREGATE_YEAR
    
    if request.method == 'POST':
        select_rankings_names_form = SelectRankingsNamesAndYear(request.POST)
        assign_choices_values(select_rankings_names_form, short_rankings_names_choice_set, year_choice_set)
        if select_rankings_names_form.is_valid():
            selected_rankings_names = select_rankings_names_form.cleaned_data.get('select_rankings_names_field')
            selected_year = select_rankings_names_form.cleaned_data.get('select_year_field')

    ranking_names_list = short_rankings_names
    if selected_rankings_names != []:
        ranking_names_list = selected_rankings_names
    aggregate_ranking_dataframe = assemble_aggregate_ranking_dataframe(ranking_names_list, int(selected_year))
    
    selected_ranking_names = [ranking_name for ranking_name in ranking_names_list if ranking_name in ranking_descriptions.keys()]
    ranktable = make_show_ranktable(selected_ranking_names, aggregate_ranking_dataframe)

    context = {'select_rankings_names_form' : select_rankings_names_form, 'selected_rankings_names' : selected_rankings_names, 'ranktable' : ranktable}
    context.update(csrf(request))

    return render(request, 'aggregate_ranking_representation/table.html', context)


class RankingTableAPIView(APIView):

    def get(self, request, *args, **kw):
        #response = Response(['a', 'b', 'c'], status=status.HTTP_200_OK)
        short_rankings_names = [ranking_name.short_name for ranking_name in RankingDescription.objects.all()]
        short_rankings_names_choice_set = tuple([(short_name, short_name) for short_name in short_rankings_names])
        year_choice_set = tuple([(year, year) for year in range(FINISH_AGGREGATE_YEAR, START_AGGREGATE_YEAR - 1, -1)])

        #select_rankings_names_form = SelectRankingsNamesAndYear()
        #assign_choices_values(select_rankings_names_form, short_rankings_names_choice_set, year_choice_set)

        selected_rankings_names = short_rankings_names
        selected_year = 2015
       
        '''
        if request.method == 'POST':
            select_rankings_names_form = SelectRankingsNamesAndYear(request.POST)
            assign_choices_values(select_rankings_names_form, short_rankings_names_choice_set, year_choice_set)
            if select_rankings_names_form.is_valid():
                selected_rankings_names = select_rankings_names_form.cleaned_data.get('select_rankings_names_field')
                selected_year = select_rankings_names_form.cleaned_data.get('select_year_field')
        '''
        ranking_names_list = short_rankings_names
        #if selected_rankings_names != []:
        #    ranking_names_list = selected_rankings_names
        aggregate_ranking_dataframe = assemble_aggregate_ranking_dataframe(ranking_names_list, int(selected_year))
        
        selected_ranking_names = [ranking_name for ranking_name in ranking_names_list if ranking_name in ranking_descriptions.keys()]
        ranktable = make_show_ranktable(selected_ranking_names, aggregate_ranking_dataframe)

        #context = {'select_rankings_names_form' : select_rankings_names_form, 'selected_rankings_names' : selected_rankings_names, 'ranktable' : ranktable}
        #context.update(csrf(request))
        response = Response(ranktable, status=status.HTTP_200_OK)

        return response
    
    def post(self, request, format=None):
        print dir(request)
        print request.data
        #data = request.DATA
        #print 'POST data: ', data
        #return Response({'a' :, 'b' : 2}, status=status.HTTP_200_OK)
        return Response('', status=status.HTTP_200_OK)

