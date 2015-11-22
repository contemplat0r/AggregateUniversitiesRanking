# coding: utf-8

import pandas_and_name_matching_exp_1_clean
from pandas_and_name_matching_exp_1_clean import *

the_df[the_df['university_name'].map(lambda x: x.find('&') != -1)]
qs_df[qs_df['university_name'].map(lambda x: x.find('&') != -1)]
leiden_df[leiden_df['university_name'].map(lambda x: x.find('&') != -1)]
