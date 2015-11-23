# coding: utf-8

get_ipython().magic(u'pwd ')
import pandas_and_name_matching_exp_3_clean
s = '(PUC-Rio)'
s.isupper()
s.islower()
s.istitle()
list(s).isupper()
sum([char for char in list(s) if char.isupper()])
sum([1 for char in list(s) if char.isupper()])
import pandas_and_name_matching_exp_3_clean
reload(pandas_and_name_matching_exp_3_clean)
qs_name_variants_0 = get_name_variants(qs_university_names_list[0])
from pandas_and_name_matching_exp_3_clean import *
qs_name_variants_0 = get_name_variants(qs_university_names_list[0])
qs_name_variants_0
qs_df['university_name'][0]
leiden_df['university_name'][:20]
qs_df['university_name'][:10]
leiden_df['university_name'][:10]
qs_name_variants_0 = get_name_variants(qs_university_names_list[0])
qs_name_variants_0
qs_df['university_name'][0]
qs_df
qs_df[:6]
get_ipython().magic(u'pinfo qs_df.corr')
get_ipython().magic(u'pinfo qs_df.corrwith')
s
s1 = 'ab'
s2 = 'PU'
s1 in s
s2 in s
