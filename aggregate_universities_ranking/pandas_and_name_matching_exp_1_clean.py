# coding: utf-8

import pandas_and_name_matching_exp_0
from pandas_and_name_matching_exp_0 import *
reload(pandas_and_name_matching_exp_0)
from pandas_and_name_matching_exp_0 import *

qs_university_names_list = list(qs_df['university_name'])
qs_university_names_as_string_list = [name.split() for name in qs_university_names_list]

qs_maybe_names_with_anciliary_words_list = [name_as_str_list for name_as_str_list in qs_university_names_as_string_list if anciliary_words_filter(name_as_str_list)]
print 'len(qs_maybe_names_with_anciliary_words_list): ', len(qs_maybe_names_with_anciliary_words_list)
print 'qs_maybe_names_with_anciliary_words_list[:20]: ', qs_maybe_names_with_anciliary_words_list[:20]
all_qs_anciliary_words = select_anciliary_words(qs_maybe_names_with_anciliary_words_list)
print 'len(all_qs_anciliary_words): ', len(all_qs_anciliary_words)
print 'all_qs_anciliary_words: ', all_qs_anciliary_words
qs_name_containing_las = [name for name in qs_maybe_names_with_anciliary_words_list if 'las' in name]
print 'qs_name_containing_las: ', qs_name_containing_las


the_university_names_list = list(the_df['university_name'])
the_university_names_as_string_list = [name.split() for name in the_university_names_list]

the_maybe_names_with_anciliary_words_list = [name_as_str_list for name_as_str_list in the_university_names_as_string_list if anciliary_words_filter(name_as_str_list)]
print 'len(the_maybe_names_with_anciliary_words_list): ', len(the_maybe_names_with_anciliary_words_list)
print 'the_maybe_names_with_anciliary_words_list[:20]: ', the_maybe_names_with_anciliary_words_list[:20]
all_the_anciliary_words = select_anciliary_words(the_maybe_names_with_anciliary_words_list)
print 'len(all_the_anciliary_words): ', len(all_the_anciliary_words)
print 'all_the_anciliary_words: ', all_the_anciliary_words
the_name_containing_las = [name for name in the_maybe_names_with_anciliary_words_list if 'las' in name]
print 'the_name_containing_las: ', the_name_containing_las


leiden_university_names_list = list(leiden_df['university_name'])
leiden_university_names_as_string_list = [name.split() for name in leiden_university_names_list]

leiden_maybe_names_with_anciliary_words_list = [name_as_str_list for name_as_str_list in leiden_university_names_as_string_list if anciliary_words_filter(name_as_str_list)]
print 'len(leiden_maybe_names_with_anciliary_words_list): ', len(leiden_maybe_names_with_anciliary_words_list)
print 'leiden_maybe_names_with_anciliary_words_list[:20]: ', leiden_maybe_names_with_anciliary_words_list[:20]
all_leiden_anciliary_words = select_anciliary_words(leiden_maybe_names_with_anciliary_words_list)
print 'len(all_leiden_anciliary_words): ', len(all_leiden_anciliary_words)
print 'all_leiden_anciliary_words: ', all_leiden_anciliary_words
leiden_name_containing_las = [name for name in leiden_maybe_names_with_anciliary_words_list if 'las' in name]
print 'leiden_name_containing_las: ', leiden_name_containing_las
