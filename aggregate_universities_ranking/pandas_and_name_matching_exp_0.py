# coding: utf-8

import prepare_for_pandas_exps
from prepare_for_pandas_exps import *
import name_matching
from name_matching import *
reload(name_matching)
from name_matching import *

qs_university_names_list = list(qs_df['university_name'])
qs_university_name_variants_list = [get_name_variants(university_name) for university_name in qs_university_names_list]
print 'qs_university_name_variants_list[0]: ', qs_university_name_variants_list[0]
