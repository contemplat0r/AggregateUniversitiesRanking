# coding: utf-8

from pandas_and_name_matching_exp_0 import *
918 + 525
def anciliary_words_filter(name_as_string_list):
    maybe_is_anciliary_words = False
    if [word for word in in name_as_string_list if len(word) < 2] != []:
        maybe_is_anciliary_words = True
        
reload(name_matching)
from name_matching import *
qs_university_names_list = list(qs_df['university_name']
)
qs_university_names_list[:3]
qs_university_names_as_string_list = [name.split() for name in qs_university_names_list]
qs_university_names_as_string_list[:3]
qs_maybe_names_with_anciliary_words_list = [anciliary_words_filter(name_as_str_list) for name_as_str_list in qs_university_names_as_string_list]
len(qs_maybe_names_with_anciliary_words_list)
qs_maybe_names_with_anciliary_words_list = [name_as_str_list for name_as_str_list in qs_university_names_as_string_list if anciliary_words_filter(name_as_str_list)]
len(qs_maybe_names_with_anciliary_words_list)
qs_maybe_names_with_anciliary_words_list[:20]
reload(name_matching)
from name_matching import *
all_qs_anciliary_words = select_anciliary_words(qs_maybe_names_with_anciliary_words_list)
len(all_qs_anciliary_words)
all_qs_anciliary_words
name_containing_las = [name for name in qs_maybe_names_with_anciliary_words_list if 'las' in name]
name_containing_las
