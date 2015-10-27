# -*- coding: utf8 -*- 

from django.shortcuts import render
from django.core.context_processors import csrf
from django.http import HttpResponse
from .models import RaitingName, RaitingValue, UniversityName 
from forms import SelectRaitingsNames

# Create your views here.


def index(request):
    return HttpResponse('Hello, world. This is first page of aggrgated rank')

def aggregate_universities_ranking_as_table(request):
    #short_raitings_names_choice_set = [(raiting_name.short_name, raiting_name.short_name) for raiting_name in RaitingName.objects.all()]
    short_raitings_names = [raiting_name.short_name for raiting_name in RaitingName.objects.all()]
    short_raitings_names_choice_set = [(short_name, short_name) for short_name in short_raitings_names]
    print short_raitings_names_choice_set

    select_raitings_names_form = SelectRaitingsNames()
    select_raitings_names_form.fields['select_raitings_names_field'].choices = tuple(short_raitings_names_choice_set)
    
    selected_raitings_names = short_raitings_names
    if request.method == 'POST':
        select_raitings_names_form = SelectRaitingsNames(request.POST)
        select_raitings_names_form.fields['select_raitings_names_field'].choices = tuple(short_raitings_names_choice_set)
        if select_raitings_names_form.is_valid():
            selected_raitings_names = select_raitings_names_form.cleaned_data.get('select_raitings_names_field')

    #context = {'select_raitings_names_form' : select_raitings_names_form, 'short_raitings_names' : short_raitings_names}
    context = {'select_raitings_names_form' : select_raitings_names_form, 'selected_raitings_names' : selected_raitings_names}
    context.update(csrf(request))
    return render(request, 'aggregate_ranking_representation/table.html', context)
