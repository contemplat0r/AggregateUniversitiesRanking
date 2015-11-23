# coding: utf-8

import pandas_and_name_matching_exp_2_clean
from pandas_and_name_matching_exp_2_clean import *
reload(pandas_and_name_matching_exp_2_clean)
from pandas_and_name_matching_exp_2_clean import *

qs_name_variants_0 = get_name_variants(qs_university_names_list[0])
print 'qs_name_variants_0', qs_name_variants_0

the_university_names = the_df['university_name']
the_university_names[the_df['university_name'].map(lambda x: x.find('-')) != -1]
the_university_names_with_dash_list = list(the_university_names[the_df['university_name'].map(lambda x: x.find('-')) != -1])
print 'len(the_university_names_with_dash_list): ', len(the_university_names_with_dash_list)
print 'the_university_names_with_dash_list: ', the_university_names_with_dash_list

leiden_university_names = leiden_df['university_name']
leiden_university_names_with_dash_list = list(leiden_university_names[leiden_df['university_name'].map(lambda x: x.find('-')) != -1])
print 'len(leiden_university_names_with_dash_list): ', len(leiden_university_names_with_dash_list)
print 'leiden_university_names_with_dash_list: ', leiden_university_names_with_dash_list


qs_university_names = qs_df['university_name']
qs_university_names_with_dash_list = list(qs_university_names[qs_df['university_name'].map(lambda x: x.find('-')) != -1])
print 'len(qs_university_names_with_dash_list): ', len(qs_university_names_with_dash_list)

print 'qs_university_names_with_dash_list: ', qs_university_names_with_dash_list
