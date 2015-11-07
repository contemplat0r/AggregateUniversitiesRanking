# -*- coding: utf8 -*- 

import datetime
from django.shortcuts import render
from django.core.context_processors import csrf
from django.conf import settings
from django.http import HttpResponse
from .models import RankingName, RankingValue, UniversityName 
from forms import SelectRankingsNamesAndYear

# Create your views here.

START_AGGREGATE_YEAR = getattr(settings, 'START_AGGREGATE_YEAR', 2014)
FINISH_AGGREGATE_YEAR = getattr(settings, 'FINISH_AGGREGATE_YEAR', datetime.date.today().year)

def index(request):
    return HttpResponse('Hello, world. This is first page of aggrgated rank')

def aggregate_universities_ranking_as_table(request):
    #short_rankings_names_choice_set = [(raiting_name.short_name, raiting_name.short_name) for raiting_name in RaitingName.objects.all()]
    print 'START_AGGREGATE_YEAR: ', START_AGGREGATE_YEAR
    short_rankings_names = [raiting_name.short_name for raiting_name in RankingName.objects.all()]
    short_rankings_names_choice_set = [(short_name, short_name) for short_name in short_rankings_names]
    print short_rankings_names_choice_set

    select_rankings_names_form = SelectRankingsNamesAndYear()
    select_rankings_names_form.fields['select_rankings_names_field'].choices = tuple(short_rankings_names_choice_set)
    #select_rankings_names_form.fields['select_year_field'].choices = (('2014', '2014'), ('2015', '2015',))
    #select_rankings_names_form.fields['select_year_field'].choices = tuple([(year, year) for year in range(START_AGGREGATE_YEAR, FINISH_AGGREGATE_YEAR + 1)])
    select_rankings_names_form.fields['select_year_field'].choices = tuple([(year, year) for year in range(FINISH_AGGREGATE_YEAR, START_AGGREGATE_YEAR - 1, -1)])
    
    selected_rankings_names = short_rankings_names
    if request.method == 'POST':
        select_rankings_names_form = SelectRankingsNamesAndYear(request.POST)
        select_rankings_names_form.fields['select_rankings_names_field'].choices = tuple(short_rankings_names_choice_set)
        #select_rankings_names_form.fields['select_year_field'].choices = (('2014', '2014'), ('2015', '2015',))
        #select_rankings_names_form.fields['select_year_field'].choices = tuple([(year, year) for year in range(START_AGGREGATE_YEAR, FINISH_AGGREGATE_YEAR + 1)])
        select_rankings_names_form.fields['select_year_field'].choices = tuple([(year, year) for year in range(FINISH_AGGREGATE_YEAR, START_AGGREGATE_YEAR - 1, -1)])
        if select_rankings_names_form.is_valid():
            selected_rankings_names = select_rankings_names_form.cleaned_data.get('select_rankings_names_field')
            selected_year = select_rankings_names_form.cleaned_data.get('select_year_field')
            year_as_datetime = datetime.date(int(selected_year), 1, 1)
            print 'year date string: ', year_as_datetime.strftime('%Y-%m-%y')
        else:
            select_rankings_names_form.fields['select_rankings_names_field'].choices = tuple(short_rankings_names_choice_set)
            select_rankings_names_form.fields['select_year_field'].choices = tuple([(year, year) for year in range(FINISH_AGGREGATE_YEAR, START_AGGREGATE_YEAR - 1, -1)])
            selected_year = FINISH_AGGREGATE_YEAR
    else:
        select_rankings_names_form.fields['select_rankings_names_field'].choices = tuple(short_rankings_names_choice_set)
        select_rankings_names_form.fields['select_year_field'].choices = tuple([(year, year) for year in range(FINISH_AGGREGATE_YEAR, START_AGGREGATE_YEAR - 1, -1)])
        selected_year = FINISH_AGGREGATE_YEAR
        print 'selected_year: ', selected_year, 'type(selected_year): ', type(selected_year)

        year_as_datetime = datetime.date(int(selected_year), 1, 1)
        print 'year date string: ', year_as_datetime.strftime('%Y-%m-%y')

    #context = {'select_rankings_names_form' : select_rankings_names_form, 'short_rankings_names' : short_rankings_names}
    context = {'select_rankings_names_form' : select_rankings_names_form, 'selected_rankings_names' : selected_rankings_names}
    context.update(csrf(request))
    return render(request, 'aggregate_ranking_representation/table.html', context)
