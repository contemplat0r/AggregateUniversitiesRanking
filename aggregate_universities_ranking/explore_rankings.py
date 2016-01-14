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

DJANGO_PROJECT_DIR = join(abspath(join(dirname(__file__), '..')), 'aggregate_universities_ranking')
sys.path.append(DJANGO_PROJECT_DIR)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aggregate_universities_ranking.settings')

django.setup()
from aggregate_ranking_representation.models import RankingDescription, RawRankingRecord, University, RankingValue


anciliary_words_list = ['of', 'the', 'The', 'a', 'A', 'an', 'An', '&', '-', '\/']
special_symbols_list = ['-', '.']


ranking_names = ['QS', 'THE', 'Leiden', 'ARWU', 'NTU', 'URAP']

def explore():
    for ranking_name in ranking_names:
        print '\n\n', '-' * 20, '\n', ranking_name
        ranking_df = DataFrame(list(RankingDescription.objects.filter(short_name=ranking_name)[0].rawrankingrecord_set.all().values()))
        university_names = ranking_df['university_name']

        names_without_whitespace = university_names[university_names.map(lambda x: x.find(' ') == -1)]
        print 'names_without_whitespace.count(): ', names_without_whitespace.count()
        #print 'names_without_whitespace: ', list(names_without_whitespace)

        names_upper = university_names[university_names.map(lambda x: x.isupper())]
        print 'names_upper.count(): ', names_upper.count()
        #print 'names_upper: ', list(names_upper)



        names_containing_slash = university_names[university_names.map(lambda x: x.find('/') != -1)]
        print 'names_containing_slash.count(): ', names_containing_slash.count()
        print 'names_containing_slash: ', list(names_containing_slash)
=
        #names_containing_one_slash = university_names[university_names.map(lambda x: x.count('/') == 1)]
        #print 'names_containing_one_slash.count(): ', names_containing_one_slash.count()
        names_containing_many_slash = university_names[university_names.map(lambda x: x.count('/') > 1)]
        print 'names_containing_many_slash.count(): ', names_containing_many_slash.count()
        print 'names_containing_many_slash: ', list(names_containing_many_slash)


        names_containing_dash = university_names[university_names.map(lambda x: x.find('-') != -1)]
        print 'names_containing_dash.count(): ', names_containing_dash.count()
        print 'names_containing_dash: ', list(names_containing_dash)

        names_containing_many_dashes = university_names[university_names.map(lambda x: x.count('-') > 1)]

        print 'names_containing_many_dashes.count(): ', names_containing_many_dashes.count()
        print 'names_containing_many_dashes: ', list(names_containing_many_dashes)


        names_containing_bracket = university_names[university_names.map(lambda x: x.find('(') != -1)]
        print 'names_containing_bracket.count(): ', names_containing_bracket.count()
        print 'names_containing_bracket: ', list(names_containing_bracket)

        names_containing_many_brackets = university_names[university_names.map(lambda x: x.count('(') > 1)]
        print 'names_containing_many_brackets.count(): ', names_containing_many_brackets.count()
        print 'names_containing_many_brackets: ', list(names_containing_many_brackets)


if __name__ == '__main__':
    explore()
