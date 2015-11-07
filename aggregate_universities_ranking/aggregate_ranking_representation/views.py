# -*- coding: utf8 -*- 

from django.shortcuts import render
from django.core.context_processors import csrf
from django.http import HttpResponse
from .models import RankingName, RankingValue, UniversityName 
from forms import SelectRankingsNamesAndYear

# Create your views here.


def index(request):
    return HttpResponse('Hello, world. This is first page of aggrgated rank')

def aggregate_universities_ranking_as_table(request):
    #short_rankings_names_choice_set = [(raiting_name.short_name, raiting_name.short_name) for raiting_name in RaitingName.objects.all()]
    short_rankings_names = [raiting_name.short_name for raiting_name in RankingName.objects.all()]
    short_rankings_names_choice_set = [(short_name, short_name) for short_name in short_rankings_names]
    print short_rankings_names_choice_set

    select_rankings_names_form = SelectRankingsNamesAndYear()
    select_rankings_names_form.fields['select_rankings_names_field'].choices = tuple(short_rankings_names_choice_set)
    select_rankings_names_form.fields['select_year_field'].choices = (('2014', '2014'), ('2015', '2015',))
    
    selected_rankings_names = short_rankings_names
    if request.method == 'POST':
        select_rankings_names_form = SelectRankingsNamesAndYear(request.POST)
        select_rankings_names_form.fields['select_rankings_names_field'].choices = tuple(short_rankings_names_choice_set)
        select_rankings_names_form.fields['select_year_field'].choices = (('2014', '2014'), ('2015', '2015',))
        if select_rankings_names_form.is_valid():
            selected_rankings_names = select_rankings_names_form.cleaned_data.get('select_rankings_names_field')
            selected_year = select_rankings_names_form.cleaned_data.get('select_year_field')
            print 'selected_year: ', selected_year

    #context = {'select_rankings_names_form' : select_rankings_names_form, 'short_rankings_names' : short_rankings_names}
    context = {'select_rankings_names_form' : select_rankings_names_form, 'selected_rankings_names' : selected_rankings_names}
    context.update(csrf(request))
    return render(request, 'aggregate_ranking_representation/table.html', context)
