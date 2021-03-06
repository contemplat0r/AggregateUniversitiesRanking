
# coding: utf-8

import os
from os.path import abspath, join, dirname
import sys

import datetime
from functools import reduce
from copy import deepcopy
from pandas import Series, DataFrame
import pandas as pd
import numpy as np
#import django
from timeit import default_timer as timer
import cProfile

#DJANGO_PROJECT_DIR = join(abspath(join(dirname(__file__), '..')), 'aggregate_universities_ranking')
#sys.path.append(DJANGO_PROJECT_DIR)
#os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aggregate_universities_ranking.settings')

#django.setup()
from aggregate_ranking_representation.models import RankingDescription, RawRankingRecord, University, RankingValue

NaN = np.nan


NONE_STR_VALUE = '~~~~~~~~~'



# Добавить "очищенный от вспомогательных слов (артиклей) вариант". Аббревиатуры тогда
# тоже вычислять два варианта: "очищенную от вспомогательных слов" и "со вспомогательными словами".

anciliary_words_list = ['of', 'the', 'The', 'a', 'A', 'an', 'An', '&', '-']
special_symbols_list = ['-', '.']


def profile(func):
    def wrapper(*args, **kwargs):
        profile_filename = func.__name__ + '.prof'
        profiler = cProfile.Profile()
        result = profiler.runcall(func, *args, **kwargs)
        profiler.dump_stats(profile_filename)
        return result
    return wrapper


def the_dataframe_postprocessor(the_dataframe):
    #the_dataframe = the_dataframe.drop(0, axis=0)
    the_dataframe = the_dataframe[the_dataframe['university_name'] != NONE_STR_VALUE]
    the_dataframe['number_in_ranking_table'] = the_dataframe['number_in_ranking_table'].map(lambda x: x -1 ) 
    return the_dataframe


#ranking_table_as_list_preprocessor = lambda df: df[:6].T
#ranking_table_as_list_preprocessor = lambda df: df[:4].T
ranking_table_as_list_preprocessor = lambda df: df.T


ranking_descriptions = {
        'QS' : {
            'dataframe_postprocessor' : None,
            'ranking_table_as_list_preprocessor' : ranking_table_as_list_preprocessor
            },
        'THE' : {
            #'dataframe_postprocessor' : the_dataframe_postprocessor,
            'dataframe_postprocessor' : None,
            'ranking_table_as_list_preprocessor' : ranking_table_as_list_preprocessor
            },
        #'Leiden' : {
        #    'dataframe_postprocessor' : None,
        #    'ranking_table_as_list_preprocessor' : ranking_table_as_list_preprocessor
        #    },
        'ARWU' : {
            'dataframe_postprocessor' : None,
            'ranking_table_as_list_preprocessor' : ranking_table_as_list_preprocessor
            },
        'NTU' : {
            'dataframe_postprocessor' : None,
            'ranking_table_as_list_preprocessor' : ranking_table_as_list_preprocessor
            },
        'URAP' : {
            'dataframe_postprocessor' : None,
            'ranking_table_as_list_preprocessor' : ranking_table_as_list_preprocessor
            },
        }


def rawranking_records_to_dataframes(ranking_descriptions):
    
    dataframes_dict = deepcopy(ranking_descriptions)
    for ranking_short_name, additional_processors in ranking_descriptions.items():
        ranking_name_description = RankingDescription.objects.filter(short_name=ranking_short_name)[0]
        raw_ranking_records = list(ranking_name_description.rawrankingrecord_set.all().values())
        ranking_dataframe = DataFrame(raw_ranking_records)
        ranking_dataframe.sort_values(by='number_in_ranking_table', inplace=True)
        dataframe_postprocessor = additional_processors['dataframe_postprocessor']
        if dataframe_postprocessor:
            ranking_dataframe = dataframe_postprocessor(ranking_dataframe)
        dataframes_dict[ranking_short_name]['dataframe'] = ranking_dataframe
    return dataframes_dict


def dataframes_to_ranking_tables(dataframes_dict):
    #print 'Entry to dataframes_to_ranking_tables'
    rank_tables_dict = dict()
    for dataframe_short_name, dataframe_and_additional_processors in dataframes_dict.items():
        #print 'dataframes_to_ranking_tables, dataframe_short_name: ', dataframe_short_name
        dataframe = dataframe_and_additional_processors['dataframe']
        short_dataframe = dataframe[['number_in_ranking_table', 'university_name', 'country']]
        short_dataframe = short_dataframe.rename(columns={'number_in_ranking_table' : 'rank'})
        ranking_table_as_list_preprocessor = dataframe_and_additional_processors['ranking_table_as_list_preprocessor']
        if ranking_table_as_list_preprocessor != None:
            #print 'dataframes_to_ranking_tables, ranking_table_as_list_preprocessor != None'
            short_dataframe = ranking_table_as_list_preprocessor(short_dataframe)
        else:
            #print 'dataframes_to_ranking_tables, ranking_table_as_list_preprocessor == None'
            pass
        ranking_table_as_list = short_dataframe.to_dict().values()
        for university in ranking_table_as_list:
            #print 'dataframes_to_ranking_tables, university: ', university
            #university['university_name_variants'] = get_name_variants(university['university_name'])
            university['university_name_variants'] = prepare_name_to_match(university['university_name'])
        rank_tables_dict[dataframe_short_name] = deepcopy(ranking_table_as_list)
    return rank_tables_dict


def anciliary_words_filter(name_as_string_list):
    maybe_is_anciliary_words = False
    if [word for word in name_as_string_list if len(word) < 4] != []:
        maybe_is_anciliary_words = True
    return maybe_is_anciliary_words


def select_anciliary_words(list_of_string_list):
    def list_containinig_anciliary_words_processor(anciliary_words_list, word):
        #if len(word) < 4 and word not in anciliary_words_list and word.isupper() == False:
        if len(word) < 4 and word not in anciliary_words_list and categorize_as_abbreviation(word) == False:
            anciliary_words_list.append(word)
        return anciliary_words_list

    all_anciliary_words_list = list()
    for string_list in list_of_string_list:
        current_anciliary_words_list = reduce(list_containinig_anciliary_words_processor, string_list, list())
        for anciliary_word in current_anciliary_words_list:
            if anciliary_word not in all_anciliary_words_list:
                all_anciliary_words_list.append(anciliary_word)
    return all_anciliary_words_list


def get_name_part_in_brackets(name_as_string_list):
    ##print 'Entry in get_name_part_in_brackets'
    name_part_in_brackets = ''
    for name_part in name_as_string_list:
        if name_part.startswith('(') and name_part.endswith(')'):
            ##print 'get_name_part_in_brackets: name_part start with \'(\' and end with \')\''
            name_part_in_brackets = name_part
            break
    return name_part_in_brackets


def detect_special_symbol_in_string(string):
    special_symbol_detected = False
    for special_symbol in special_symbols_list:
        if special_symbol in string:
            special_symbol_detected = True
            break
    return special_symbol_detected


#
# Begin code part that describe new dissasemble full name algorithm, that applicable
# to names from Webometrics ranking.
# Function categorize_as_abbreviation also used old algorithm version. New alogrithm
# also used pick_abbreviation_from_fullname function wrote for old algorithm (must be
# renamed).
# To do. Detect identical words that meet more than in one name, and not belong to {'Unversity', 'Institute'} set. That words may be city (where university located) names.
# Remove all abbreviations that meet more then one time in one ranking.
#


def divide_name_by_slash(name_as_string):
    name_parts_list = [name_part for name_part in name_as_string.split('/') if name_part != '']
    name_parts_dict = {
            'name_part_before_slash' : name_parts_list[0],
            'name_part_after_slash' : name_part_list[1]
            }
    #return name_parts_dict
    return name_parts_list


def divide_by_brackets(name_part_as_string):
    name_variants = {'not_in_bracket_name_variant' : None, 'in_bracket_name_variants' : None}
    not_in_bracket_name_variant = []
    current_in_bracket_name_variant = []
    concatenate_string = ''
    in_bracket_state = False
    in_bracket_in_bracket_state = False
    for symbol in name_part_as_string:
        if symbol == '(' and not in_bracket_state and not in_bracket_in_bracket_state:
            in_bracket_state = True
            name_variants['in_bracket_name_variants'] = []
        elif symbol == '(' and in_bracket_state and not in_bracket_in_bracket_state:
            in_bracket_in_bracket_state = True
        elif symbol == ')' and in_bracket_in_bracket_state:
            in_bracket_in_bracket_state = False
        elif symbol == ')' and not in_bracket_in_bracket_state and in_bracket_state:
            name_variants['in_bracket_name_variants'].append(concatenate_string.join(current_in_bracket_name_variant))
            current_in_bracket_name_variant = []
            in_bracket_state = False
        elif in_bracket_state:
            current_in_bracket_name_variant.append(symbol)
        else:
            not_in_bracket_name_variant.append(symbol)
    name_variants['not_in_bracket_name_variant'] = concatenate_string.join(not_in_bracket_name_variant)
    return name_variants


def convert_to_list(name_variant_as_string):
    return [name_item.strip() for name_item in name_variant_as_string.split() if len(name_item) > 1]


def categorize_as_abbreviation(word):
    word_is_abbreviation = False
    word_len = len(word)
    upper_symbols_number = sum([1 for char in list(word) if char.isupper()])
    if word_len > 1 and (upper_symbols_number > word_len - upper_symbols_number) and not detect_special_symbol_in_string(word):
        word_is_abbreviation = True
    return word_is_abbreviation


def detect_one_word_list(word_list):
    if len(word_list) == 1:
        return True
    else:
        return False

def categorize_one_word_list(one_word_list):
    word = one_word_list[0]
    if categorize_as_abbreviation(word):
        return 'abbreviation'
    else:
        return 'shortname'


def categorize_word_list(word_list):
    if detect_one_word_list(word_list):
        return categorize_one_word_list(word_list)
    else:
        return 'longname'

def extract_abbreviations_from_longname(longname):
    return [word for word in longname if categorize_as_abbreviation(word)]


def delete_abbreviations_from_longname(abbreviations, longname):
    for abbreviation in abbreviations:
        if abbreviation in longname:
            longname.remove(abbreviation)
    return longname


def process_word_list(word_list):
    result = {'abbreviations' : None, 'shortnames' : None, 'longname_as_list' : None, 'abbreviations_picked_from_longname' : None, 'abbreviations_picked_from_longname_upper' : None}
    word_list_category = categorize_word_list(word_list)
    if word_list_category == 'abbreviation':
        result['abbreviations'] = word_list
    elif word_list_category == 'shortname':
        result['shortnames'] = word_list
    elif word_list_category == 'longname':
        abbreviations = extract_abbreviations_from_longname(word_list)
        if abbreviations != []:
            result['abbreviations'] = abbreviations
        result['longname_as_list'] = delete_abbreviations_from_longname(abbreviations, word_list)
        abbreviation_picked_from_longname = pick_abbreviation_from_fullname(result['longname_as_list'])
        result['abbreviations_picked_from_longname'] = [abbreviation_picked_from_longname]
        result['abbreviations_picked_from_longname_upper'] = [abbreviation_picked_from_longname.upper()]
    else:
        print 'Unknown category'
    return result


def get_name_variants_as_lists(name_part):
    not_in_bracket_name_variant = name_part['not_in_bracket_name_variant']
    in_bracket_name_variants = name_part['in_bracket_name_variants']
    not_in_bracket_name_variant_as_list = exclude_anciliary_words_from_name_as_list(convert_to_list(not_in_bracket_name_variant))
    #print not_in_bracket_name_variant_as_list

    name_part['not_in_bracket_name_variant_as_list'] = not_in_bracket_name_variant_as_list

    in_bracket_name_variants_as_lists = [exclude_anciliary_words_from_name_as_list(convert_to_list(name_variant)) for name_variant in in_bracket_name_variants]
    #print in_bracket_name_variants_as_lists

    name_part['in_bracket_name_variants_as_lists'] = in_bracket_name_variants_as_lists
    return name_part


def process_name(name):
    processed_name = {'raw_name_as_string' : name, 'name_parts_divided_by_slash' : []}
    name_parts_divided_by_slash = divide_name_by_slash(name)
    for name_part in name_parts_divided_by_slash:
        processed_name_part = {'name_part' : name_part}
        name_variants_divided_by_brackets = divide_by_brackets(name_part)
        processed_name_part['name_variants_divided_by_brackets'] = name_variants_divided_by_brackets
        #print name_variants_divided_by_brackets
        name_variants = get_name_variants_as_lists(name_variants_divided_by_brackets)
        #print name_variants
        not_in_bracket_name_variant_as_list = name_variants['not_in_bracket_name_variant_as_list']
        processed_name_part['not_in_bracket_name_variant_as_list'] = not_in_bracket_name_variant_as_list
        in_bracket_name_variants_as_lists = name_variants['in_bracket_name_variants_as_lists']
        processed_name_part['in_bracket_name_variants_as_lists'] = in_bracket_name_variants_as_lists
        processed_not_in_bracket_name_variant_as_list = process_word_list(not_in_bracket_name_variant_as_list)
        processed_name_part['processed_not_in_bracket_name_variant_as_list'] = processed_not_in_bracket_name_variant_as_list
        #print processed_not_in_bracket_name_variant_as_list
        processed_name_part['processed_in_bracket_name_variants_as_lists'] = []
        for in_bracket_name_variant in in_bracket_name_variants_as_lists:
            processed_in_bracket_name_variant_as_list = process_word_list(in_bracket_name_variant)
            #print processed_in_bracket_name_variant_as_list
            processed_name_part['processed_in_bracket_name_variants_as_lists'].append(processed_in_bracket_name_variant_as_list)
        processed_name['name_parts_divided_by_slash'].append(processed_name_part)
    return processed_name
            

#
# End code part that describe new dissasemble name (and name matching) algorithm. 
#


def detect_trust_abbreviation(abbreviation):
    return len(abbreviation) >= MIN_TRUST_ABBR_LEN


def detect_trust_word_list(word_list):
    return len(word_list) >= MIN_TRUST_LIST_LEN


def strip_words_in_list(word_list):
    return [word.strip().strip(',') for word in word_list]


def glue_by_dash(word_list):
    dash_ended_word_index = None
    word_list_len = len(word_list)
    
    for i in xrange(0, word_list_len):
        word = word_list[i]
        if word.endswith('-') and i < word_list_len - 1:
            dash_ended_word_index = i
            break
    if dash_ended_word_index != None:
        j = dash_ended_word_index
        k = dash_ended_word_index + 1
        word_list = word_list[:j] + [word_list[j] + word_list[k]] + word_list[k + 1:]
    return word_list


def word_list_to_string(word_list):
    concatenate_string = ' '
    return concatenate_string.join(word_list)


def prepare_name_to_match(original_name_as_string):
    prepared_name = {
            'original_name_as_string' : original_name_as_string,
            'abbreviation' : None,
            'cleaned_name_as_string' : None,
            'cleaned_alternative_name_as_string' : None,
            'one_word_in_bracket' : None,
            'cleaned_name_as_list' : None,
            'cleaned_alternative_name_as_list' : None,
            'cleaned_from_special_words_name_as_list' : None,
            'cleaned_from_special_words_alternative_name_as_list' : None,
            ## For compatibility with get_name_variants function output
            'raw_fullname_as_string' : original_name_as_string,
            'fullname_variants_as_lists' : list(),
            'fullname__variants_as_lists_anciliary_words_excluded' : list(),
            'shortnames' : list(),
            'abbreviations' : list(),
            'abbreviations_build_from_first_letters' : list(),
            'fullnames_variants_as_strings' : list(),
            'fullname_variants_as_strings_anciliary_words_excluded' : list(),

            }

    name_variants = divide_by_brackets(original_name_as_string)
    #print name_variants

    not_in_bracket_name_variant = name_variants['not_in_bracket_name_variant']
    in_bracket_name_variants_list = name_variants['in_bracket_name_variants']
    
    in_bracket_name_variant = None
    in_bracket_name_variant_as_list = []
    if in_bracket_name_variants_list != None:
        in_bracket_name_variant = in_bracket_name_variants_list[0]
        not_in_bracket_name_variant = not_in_bracket_name_variant.replace('(' + in_bracket_name_variant + ')', '')
        in_bracket_name_variant_as_list = strip_words_in_list(in_bracket_name_variant.split())
        in_bracket_name_variant_as_list = glue_by_dash(in_bracket_name_variant_as_list)

    not_in_bracket_name_variant_as_list = strip_words_in_list(not_in_bracket_name_variant.split())
    not_in_bracket_name_variant_as_list = glue_by_dash(not_in_bracket_name_variant_as_list)
    print not_in_bracket_name_variant_as_list, in_bracket_name_variant_as_list
    if in_bracket_name_variant != None:
        if detect_one_word_list(in_bracket_name_variant_as_list):
            if categorize_as_abbreviation(in_bracket_name_variant) and detect_trust_abbreviation(in_bracket_name_variant):
                prepared_name['abbreviation'] = in_bracket_name_variant
            else:
                prepared_name['one_word_in_bracket'] = in_bracket_name_variant
            prepared_name['cleaned_name_as_list'] = not_in_bracket_name_variant_as_list
            prepared_name['cleaned_name_as_string'] = word_list_to_string(not_in_bracket_name_variant_as_list)
        else:
            if detect_one_word_list(not_in_bracket_name_variant_as_list):
                if categorize_as_abbreviation(not_in_bracket_name_variant) and detect_trust_abbreviation(not_in_bracket_name_variant):
                    prepared_name['abbreviation'] = not_in_bracket_name_variant
                prepared_name['cleaned_name_as_list'] = in_bracket_name_variant_as_list
                prepared_name['cleaned_name_as_string'] = word_list_to_string(in_bracket_name_variant_as_list)
            else:
                prepared_name['cleaned_name_as_list'] = not_in_bracket_name_variant_as_list
                prepared_name['cleaned_name_as_string'] = word_list_to_string(not_in_bracket_name_variant_as_list)
                if detect_trust_word_list(in_bracket_name_variant_as_list):
                    prepared_name['cleaned_alternative_name_as_list'] = in_bracket_name_variant_as_list
                    prepared_name['cleaned_alternative_name_as_string'] = word_list_to_string(in_bracket_name_variant_as_list)
    else:
        prepared_name['cleaned_name_as_list'] = not_in_bracket_name_variant_as_list
        prepared_name['cleaned_name_as_string'] = word_list_to_string(not_in_bracket_name_variant_as_list)


    prepared_name['fullname_variants_as_lists'].append(prepared_name['cleaned_name_as_list'])
    if prepared_name['cleaned_alternative_name_as_list'] != None:
        prepared_name['fullname_variants_as_lists'].append(prepared_name['cleaned_alternative_name_as_list'])
    if prepared_name['one_word_in_bracket'] != None:
        prepared_name['shortnames'].append(prepared_name['one_word_in_bracket'])
    if prepared_name['abbreviation'] != None:
        prepared_name['abbreviations'].append(prepared_name['abbreviation']),
    prepared_name['fullnames_variants_as_strings'].append(prepared_name['cleaned_name_as_string'])
    if prepared_name['cleaned_alternative_name_as_string'] != None:
        prepared_name['fullnames_variants_as_strings'].append(prepared_name['cleaned_alternative_name_as_string'])

    return prepared_name


# Must be removed
def divide_raw_name_by_brackets(raw_fullname_as_list):
    out_bracket_name_part = list()
    in_bracket_name_part = list()
    in_bracket_state = False

    for item in raw_fullname_as_list:
        if item.startswith('(') and not in_bracket_state:
            in_bracket_state = True
            #in_bracket_name_part.append(item[1:])
            in_bracket_name_part.append(item.lstrip('('))
        elif item.endswith(')') and in_bracket_state:
            in_bracket_state = False
            in_bracket_name_part.append(item.rstrip(')'))
        elif in_bracket_state:
            in_bracket_name_part.append(item)
        else:
            out_bracket_name_part.append(item)
    in_bracket_name_part = [name_item for name_item in in_bracket_name_part if name_item != '']
    return {'out_bracket_name_part' : out_bracket_name_part, 'in_bracket_name_part' : in_bracket_name_part}


#Must be removed
def get_already_existing_abbreviation(name_part_as_string_list):
    abbreviations = list()
    for name_item in name_part_as_string_list:
        if len(name_item) > 1 and categorize_as_abbreviation(name_item):
            abbreviations.append(name_item)
    return abbreviations


def pick_abbreviation_from_fullname(fullname_as_string_list):
    abbr_from_fullname = None
    if len(fullname_as_string_list) > 1:
        abbr_from_fullname = ''
        for part in fullname_as_string_list:
            abbr_from_fullname = abbr_from_fullname + part[0]
    #print 'pick_abbreviation_from_fullname, abbr_from_fullname: ', len(abbr_from_fullname)
    return abbr_from_fullname


def exclude_anciliary_words_from_name_as_list(name_as_string_list):
    if (name_as_string_list != None) and (name_as_string_list != []):
        return [name_part for name_part in name_as_string_list if name_part not in anciliary_words_list]
    else:
        return []


def convert_name_as_list_to_string(name_as_string_list):
    if (name_as_string_list != None) and (name_as_string_list != []):
        name_as_string = name_as_string_list[0]
        for name_part in name_as_string_list[1:]:
            name_as_string = name_as_string + ' ' + name_part
        return name_as_string
    else:
        return str()


def get_name_variants(name_str):
    name_variants = {
            'raw_fullname_as_string' : name_str,
            'fullname_as_list' : None,
            'fullname_as_list_anciliary_words_excluded' : None,
            'shortname' : None,
            'abbreviations' : list(),
            'abbreviations_build_from_first_letters' : list(),
            'fullname_as_string' : None,
            'fullname_as_string_anciliary_words_excluded' : None,
            }

    name_as_string_list = name_str.split()
    name_as_string_list = [name_part.strip(',') for name_part in name_as_string_list]
    name_part_in_brackets = get_name_part_in_brackets(name_as_string_list)
    abbreviations = list()
    if name_part_in_brackets != None and len(name_part_in_brackets) > 1:
        name_as_string_list.remove(name_part_in_brackets)
        name_part_in_brackets = name_part_in_brackets.strip('()')
        if categorize_as_abbreviation(name_part_in_brackets):
            abbreviations.append(name_part_in_brackets)
            name_variants['abbreviations'] = abbreviations
        else:
            name_variants['shortname'] = name_part_in_brackets

    if abbreviations == []:
        abbreviations = get_abbreviations_from_outside_brackets(name_as_string_list)
        if abbreviations != []:
            name_variants['abbreviations'] = abbreviations
            for abbreviation_variant in abbreviations:
                name_as_string_list.remove(abbreviation_variant)

    abbreviations_build_from_first_letters = list()
    if name_as_string_list != []:
        name_variants['fullname_as_list'] = name_as_string_list
        name_as_string_list_cleaned_from_anciliary_word = exclude_anciliary_words_from_name_as_list(name_as_string_list)
        name_variants['fullname_as_list_anciliary_words_excluded'] = name_as_string_list_cleaned_from_anciliary_word

        if (abbreviations == []) and (len(name_as_string_list) > 1):
            abbreviation_picked_from_fullname = pick_abbreviation_from_fullname(name_as_string_list)
            abbreviation_picked_from_fullname_exclude_anciliary_words = pick_abbreviation_from_fullname(name_as_string_list_cleaned_from_anciliary_word)
            abbreviations_build_from_first_letters = [abbreviation_picked_from_fullname, abbreviation_picked_from_fullname.upper(), abbreviation_picked_from_fullname_exclude_anciliary_words, abbreviation_picked_from_fullname_exclude_anciliary_words.upper()]
            name_variants['abbreviations_build_from_first_letters'] = abbreviations_build_from_first_letters

        name_variants['fullname_as_string'] = convert_name_as_list_to_string(name_as_string_list)
        name_variants['fullname_as_string_anciliary_words_excluded'] = convert_name_as_list_to_string(name_as_string_list_cleaned_from_anciliary_word)
    return name_variants 


def names_as_string_match(first_name_as_string, second_name_as_string):
    if (first_name_as_string != None) and (second_name_as_string != None):
        return (first_name_as_string == second_name_as_string) or (second_name_as_string in first_name_as_string) or (first_name_as_string in second_name_as_string)
    else:
        return False


def abbreviations_from_list_match_abbreviation(abbreviation, abbreviations_list):
    match = False
    for abbreviation_from_list in abbreviations_list:
        if abbreviation == abbreviation_from_list:
            match = True
            break
    return match


def abbreviations_match(first_abbreviations_list, second_abbreviations_list):
    match = False
    if (first_abbreviations_list != []) and (second_abbreviations_list != []):
        for abbreviation in first_abbreviations_list:
            if abbreviations_from_list_match_abbreviation(abbreviation, second_abbreviations_list) == True:
                match = True
                break
    #else:
    #    match = False
    return match


def name_parts_match(first_name_part, second_name_part):
    result = False
    if (len(first_name_part) > 1 and len(second_name_part) > 1) and (first_name_part == second_name_part or first_name_part in second_name_part or second_name_part in first_name_part):
        result = True
    return result


def full_names_as_list_match(first_name_as_list, second_name_as_list):
    match = False
    if (first_name_as_list != None) and (second_name_as_list != None):
        matching_result_as_bool_list = [list(set([name_parts_match(second_name_part, first_name_part) for second_name_part in second_name_as_list])) for first_name_part in first_name_as_list]
        if len(matching_result_as_bool_list) == len([result for result in matching_result_as_bool_list if result != [False]]):
            match = True
    return match


def string_lists_match(first_string_list, second_string_list, comparator):
    result_of_determine = False
    result_of_as_bool_list = list(set((comparator(second_string, first_string) for second_string in second_string_list if second_string != None for first_string in first_string_list if first_string != None)))
    if result_of_as_bool_list == [True]:
        result_of_determine = True
    return result_of_determine


def caluclate_distance(first_name_as_string, second_name_as_string):
    return 0


#Must be removed    
def detect_multi_match(first_name_description, second_name_description, university_name):
    #return ('Massachusetts Institute' in first_name_description['raw_fullname_as_string']) or ('Massachusetts Institute' in second_name_description['raw_fullname_as_string'])
    return (university_name in first_name_description['raw_fullname_as_string']) or (university_name in second_name_description['raw_fullname_as_string'])


#Must be removed    
def detect_multi_match_intersection(first_name_description, second_name_description, university_name):
    #return ('Massachusetts Institute' in first_name_description['raw_fullname_as_string']) and ('Massachusetts Institute' in second_name_description['raw_fullname_as_string'])
    return (university_name in first_name_description['raw_fullname_as_string']) and (university_name in second_name_description['raw_fullname_as_string'])


#Must be removed    
def names_match(first_name_description, second_name_description, rankname=None, another_rankname=None):
    matching_result = False
    #multi_match_name = detect_multi_match(first_name_description, second_name_description, '')
    #multi_match_intersection = detect_multi_match_intersection(first_name_description, second_name_description, '')

    #multi_match_name = detect_multi_match(first_name_description, second_name_description, 'City University of Hong Kong')
    #multi_match_intersection = detect_multi_match_intersection(first_name_description, second_name_description, 'City University of Hong Kong')

    #multi_match_name = detect_multi_match(first_name_description, second_name_description, 'Federal University of Rio de Janeiro')
    #multi_match_intersection = detect_multi_match_intersection(first_name_description, second_name_description, 'Federal University of Rio de Janeiro')

    multi_match_name = detect_multi_match(first_name_description, second_name_description, 'University of Milano-Bicocca')
    multi_match_intersection = detect_multi_match_intersection(first_name_description, second_name_description, 'University of Milano-Bicocca')


    raw_first_name_as_string = first_name_description['raw_fullname_as_string']
    raw_second_name_as_string = second_name_description['raw_fullname_as_string']
    if multi_match_intersection:
        print '\n' * 4, '-' * 10, '\nEntry in names_match\n\n'
        print 'raw_first_name_as_string: ', raw_first_name_as_string, ' raw_second_name_as_string: ', raw_second_name_as_string
   
    if names_as_string_match(raw_first_name_as_string, raw_second_name_as_string) == True:
        matching_result = True
        if multi_match_name:
            print 'names_as_string_match(raw_first_name_as_string, raw_second_name_as_string): ', raw_first_name_as_string, raw_second_name_as_string
            print 'rankname: ', rankname, ' another_rankname: ', another_rankname
    elif names_as_string_match(first_name_description['fullname_as_string'], second_name_description['fullname_as_string']) == True:
        matching_result = True
        if multi_match_name:
            print 'names_as_string_match(first_name_description[\'fullname_as_string\'], second_name_description[\'fullname_as_string\']): ', first_name_description['fullname_as_string'], second_name_description['fullname_as_string']
            print 'rankname: ', rankname, ' another_rankname: ', another_rankname

    elif names_as_string_match(first_name_description['fullname_as_string_anciliary_words_excluded'], second_name_description['fullname_as_string_anciliary_words_excluded']) == True:
        matching_result = True
        if multi_match_name:
            print 'names_as_string_match(first_name_description[\'fullname_as_string_anciliary_words_excluded\'], second_name_description[\'fullname_as_string_anciliary_words_excluded\']): ', first_name_description['fullname_as_string_anciliary_words_excluded'], second_name_description['fullname_as_string_anciliary_words_excluded']
            print 'rankname: ', rankname, ' another_rankname: ', another_rankname

    elif full_names_as_list_match(first_name_description['fullname_as_list'], second_name_description['fullname_as_list']) == True:
        matching_result = True
        if multi_match_name:
            print 'full_names_as_list_match(first_name_description[\'fullname_as_list\'], second_name_description[\'fullname_as_list\']): ',  first_name_description['fullname_as_list'], second_name_description['fullname_as_list']
            print 'rankname: ', rankname, ' another_rankname: ', another_rankname

    elif full_names_as_list_match(first_name_description['fullname_as_list_anciliary_words_excluded'], second_name_description['fullname_as_list_anciliary_words_excluded']) == True:
        matching_result = True
        if multi_match_name:
            print 'full_names_as_list_match(first_name_description[\'fullname_as_list_anciliary_words_excluded\'], second_name_description[\'fullname_as_list_anciliary_words_excluded\']): ',  first_name_description['fullname_as_list_anciliary_words_excluded'], second_name_description['fullname_as_list_anciliary_words_excluded']
            print 'rankname: ', rankname, ' another_rankname: ', another_rankname


    elif first_name_description['abbreviations'] != []:
        if (second_name_description['abbreviations'] != []) and (abbreviations_match(first_name_description['abbreviations'], second_name_description['abbreviations']) != False):
            matching_result = True
            if multi_match_name:
                print '(second_name_description[\'abbreviations\'] != []) and (abbreviations_match(first_name_description[\'abbreviations\'], second_name_description[\'abbreviations\']) != False): ', first_name_description['abbreviations'], second_name_description['abbreviations']
                print 'raw_first_name_as_string: ', raw_first_name_as_string, ' raw_second_name_as_string: ', raw_second_name_as_string
                print 'rankname: ', rankname, ' another_rankname: ', another_rankname

        elif (second_name_description['abbreviations_build_from_first_letters'] != []) and (abbreviations_match(first_name_description['abbreviations'], second_name_description['abbreviations_build_from_first_letters']) != False):
            matching_result = True
            if multi_match_name:
                print '(second_name_description[\'abbreviations_build_from_first_letters\'] != []) and (abbreviations_match(first_name_description[\'abbreviations\'], second_name_description[\'abbreviations_build_from_first_letters\']) != False): ', first_name_description['abbreviations'], second_name_description['abbreviations_build_from_first_letters']
                print 'raw_first_name_as_string: ', raw_first_name_as_string, ' raw_second_name_as_string: ', raw_second_name_as_string
                print 'rankname: ', rankname, ' another_rankname: ', another_rankname
    elif first_name_description['abbreviations_build_from_first_letters'] != []:
        if (second_name_description['abbreviations'] != []) and (abbreviations_match(first_name_description['abbreviations_build_from_first_letters'], second_name_description['abbreviations']) != False):
            matching_result = True
            if multi_match_name:
                print '(second_name_description[\'abbreviations\'] != []) and (abbreviations_match(first_name_description[\'abbreviations_build_from_first_letters\'], second_name_description[\'abbreviations\']) != False): ', first_name_description['abbreviations_build_from_first_letters'], second_name_description['abbreviations']
                print 'raw_first_name_as_string: ', raw_first_name_as_string, ' raw_second_name_as_string: ', raw_second_name_as_string
                print 'rankname: ', rankname, ' another_rankname: ', another_rankname
    if multi_match_intersection:
        print '\n' * 2, 'Return from names_match\n', '-' * 10 
    return matching_result


def strings_match(first_string, second_string):
    return first_string == second_string


def lists_match(first_strings_list, second_strings_list):
    match = True

    if ((first_strings_list != None) and (second_strings_list != None) and (first_strings_list != []) and (second_strings_list != [])) and (len(first_strings_list) == len(second_strings_list)):
        for string in first_strings_list:
            if string not in second_strings_list:
                match = False
                break
        for string in second_strings_list:
            if string not in first_strings_list:
                match = False
                break
    else:
        match = False
    return match


def names_match_improved(first_prepared_name, second_prepared_name, first_ranking=None, second_ranking=None):
    match = False
    print 'names_match_improved: first_prepared_name[\'original_name_as_string\']: ', first_prepared_name['original_name_as_string'].encode('utf-8'), ' second_prepared_name[\'original_name_as_string\']: ', second_prepared_name['original_name_as_string'].encode('utf-8')
    if strings_match(first_prepared_name['original_name_as_string'], second_prepared_name['original_name_as_string']):
        match = True
    elif strings_match(first_prepared_name['cleaned_name_as_string'], second_prepared_name['cleaned_name_as_string']):
        match = True
    elif lists_match(first_prepared_name['cleaned_name_as_list'], second_prepared_name['cleaned_name_as_list']):
        print 'names_match_improved, lists match is True'
        print 'first_prepared_name[\'cleaned_name_as_list\']: ', first_prepared_name['cleaned_name_as_list']
        print 'second_prepared_name[\'cleaned_name_as_list\']: ', second_prepared_name['cleaned_name_as_list']
        match = True
    elif len(first_prepared_name['cleaned_name_as_list']) == 1 and categorize_as_abbreviation(first_prepared_name['cleaned_name_as_string']) and detect_trust_abbreviation(first_prepared_name['cleaned_name_as_string']) and (first_prepared_name['cleaned_name_as_string'] in second_prepared_name['original_name_as_string']):
        match = True
    elif len(second_prepared_name['cleaned_name_as_list']) == 1 and categorize_as_abbreviation(second_prepared_name['cleaned_name_as_string']) and detect_trust_abbreviation(second_prepared_name['cleaned_name_as_string']) and (second_prepared_name['cleaned_name_as_string'] in first_prepared_name['original_name_as_string']):
        match = True
    
    return match


def assign_longest_name_variant(university_description):
    #print 'Entry in assign_longest_name_variant'
    longest_name_variant = str()
    ##print 'assign_longest_name_variant, university ranks: ', university_description['collected_from_all_ranktables_description'].keys()
    #for description_variants in university_description['collected_from_all_ranktables_description'].values():
    for rankname, description_variants in university_description['collected_from_all_ranktables_description'].items():
        ##print 'assign_longest_name_variant, rankname: ', rankname
        ##print 'assign_longest_name_variant, name_variants: ', description_variants['university_name_variants']
        full_university_name = description_variants['university_name_variants']['raw_fullname_as_string']
        if len(full_university_name) > len(longest_name_variant):
            longest_name_variant = full_university_name
    return longest_name_variant


def union_ranks(ranktables):
    union_universities_list = list()
    ranknames = ranktables.keys()
    rest_ranknames = ranknames[:]
    rank_lenghts = dict()
    for rankname in ranknames:
        rank_lenghts[rankname] = len(ranktables[rankname])
    default_ranks = {rankname : (len(ranktable) + 1) for rankname, ranktable in ranktables.items()}
    for rankname in ranknames:
        ranktable = ranktables[rankname]
        rest_ranknames.remove(rankname)
        for university in ranktable:
            #print 'university: ', university
            university['ranks'] = default_ranks.copy()
            #university['ranks'][rankname] = university['rank']
            university['collected_from_all_ranktables_description'] = {rankname : {'rankvalue' : university['rank'], 'university_name_variants' : university['university_name_variants']}}
            university['ranks'][rankname] = university.pop('rank')
            #university['ranks'][rankname] = university['rank']
            for another_rankname in rest_ranknames:
                another_ranktable = ranktables[another_rankname]
                to_remove_universities = list()
                for another_university in another_ranktable:
                    #math = names_match(university['university_name_variants'], another_university['university_name_variants'], rankname, another_rankname)
                    math = names_match_improved(university['university_name_variants'], another_university['university_name_variants'])
                    if math:
                        #print 'another_university: ', another_university
                        university['ranks'][another_rankname] = another_university['rank']
                        university['collected_from_all_ranktables_description'].update({another_rankname : {'rankvalue' : another_university['rank'], 'university_name_variants' : another_university['university_name_variants']}})
                        to_remove_universities.append(another_university)
                        break
                for another_university in to_remove_universities:
                    another_ranktable.remove(another_university)
            university['canonical_name'] = assign_longest_name_variant(university)
            union_universities_list.append(university)
    #print 'union_ranks, union_universities_list[0]', union_universities_list[0]
    
    '''
    for university in union_universities_list:
        if 'Massachusetts Institute' in university['university_name']:
            print '\n' * 4, '*' * 10, '\n', university
        if 'University of Amsterdam' in university['university_name']:
            print '\n' * 4, '*' * 10, '\n', university
        if ' Amsterdam' in university['university_name']:
            print '\n' * 4, '*' * 10, '\n', university
        if 'North Carolina' in university['university_name']:
            print '\n' * 4, '*' * 10, '\n', university
            '''

    return union_universities_list


def append_aggregate_rank(union_university_ranks_list):
    for university in union_university_ranks_list:
        university['aggregate_rank'] = sum(university['ranks'].values())
    return union_university_ranks_list


def group_by_aggregate_rank(union_university_ranks_list):
    grouped_by_rank_dict = dict()
    for university in union_university_ranks_list:
        aggregate_rank = university.pop('aggregate_rank')
        if aggregate_rank not in grouped_by_rank_dict.keys():
            rank_record = dict()
            rank_record['university_list'] = list()
            rank_record['final_rank'] = 0
            grouped_by_rank_dict[aggregate_rank] = rank_record
        grouped_by_rank_dict[aggregate_rank]['university_list'].append(university)
    return grouped_by_rank_dict


def reranked(grouped_by_rank_dict):
    sorted_aggregate_ranks = sorted(grouped_by_rank_dict.keys())
    i = 1
    for rank_value in sorted_aggregate_ranks:
        grouped_by_rank_dict[rank_value]['final_rank'] = i
        i = i + 1

    return grouped_by_rank_dict


def to_database(union_rank_tables):
    # Надо будет написать общую функцию, которая реализует заполнение (двух) таблиц
    # Связанных отношением многие-ко-многим через промежуточную таблицу. Главное
    # (самое трудное) что надо будет реализовать - это заполнение промежуточной
    # таблицы.
<<<<<<< HEAD
    ranking_name_descriptions = list(RankingDescription.objects.all())
=======
    ranking_descriptions = list(RankingDescription.objects.all())
>>>>>>> not_optimised_database

    for university_record in union_rank_tables:
        #print '\n' *4, '-' * 40, '\n'
        ##print 'university_name\t-\t', university_record['university_name']
        #print 'canonical_name\t-\t', university_record['canonical_name']
        #print 'ranks\t-\t', university_record['ranks']
        #print 'country\t-\t', university_record['country']
        
        for ranking_description in ranking_descriptions:
            for ranking_name, ranking_value in university_record['ranks'].items():
                if ranking_description.short_name == ranking_name:
                    #print 'Ranking %s detected' % ranking_name
                    university_name = university_record['canonical_name']
                    country = university_record['country']
                    year = datetime.date(datetime.date.today().year, 1, 1)
                    already_saved_university_descriptions = list(University.objects.all())
                    university_already_in_database = False
                    for already_saved_university_description in already_saved_university_descriptions:
                        #print 'already_saved_university_description.university_name: ', already_saved_university_description.university_name, ', university_name: ', university_name
                        if already_saved_university_description.university_name == university_name:
                            #print "already_saved_university_description.university_name == university_name"
                            ranking_value_db_record = RankingValue(original_value = '~~~', number_in_ranking_table = ranking_value, ranking_description = ranking_description, university = already_saved_university_description)
                            ranking_value_db_record.save()
                            #print 'Ranking value ', ranking_value, ' saved for university ', university_name, ' and for ranking ', ranking_name
                            university_already_in_database = True
                            #print 'Inner break'
                            break
                    if university_already_in_database == False:
<<<<<<< HEAD
                        print 'University %s, not in database' % university_name
                        new_db_university_description_record = University(university_name = university_name, country = country)
                        new_db_university_description_record.save()
                        print 'University %s, saved to database' % university_name
                        #ranking_value_db_record = RankingValue(year=datetime.date.today(), original_value = str(), number_in_ranking_table = ranking_value, ranking_name = ranking_name_description, university_name = new_db_university_description_record)
                        ranking_value_db_record = RankingValue(year=year, original_value = str(), number_in_ranking_table = ranking_value, ranking_name = ranking_name_description, university_name = new_db_university_description_record)
=======
                        #print 'University %s, not in database' % university_name
                        new_db_university_record = University(university_name = university_name, country = country)
                        new_db_university_record.save()
                        #print 'University %s, saved to database' % university_name
                        ranking_value_db_record = RankingValue(original_value = '~~~', number_in_ranking_table = ranking_value, ranking_description = ranking_description, university = new_db_university_record)
>>>>>>> not_optimised_database
                        ranking_value_db_record.save()
                    #print 'Outer break'
                    break
    return 


def prepare_year_to_compare(year):
    #return datetime.date(year, 1, 1)
    return year

#@profile

'''
def from_database(rankings_names_list, year):

    year = prepare_year_to_compare(year)
    rank_tables = list()

    for university_description in University.objects.all():
<<<<<<< HEAD
        print 'university_description.university_name: ', university_description.university_name
=======
>>>>>>> not_optimised_database
        university_name = university_description.university_name
        record = {'canonical_name' : university_name}
        ranks = dict()
        for ranking_value_description in university_description.rankingvalue_set.filter(ranking_description__year=year):
            rank_name = ranking_value_description.ranking_description.short_name
            if rank_name in rankings_names_list:
                ranks.update({rank_name : ranking_value_description.number_in_ranking_table})
        if ranks != {}:
            record['ranks'] = ranks
            rank_tables.append(record)
            #print 'from_database, before return:\n', '=' * 10, '\n', rank_tables
    return rank_tables
'''


def convert_aggregate_ranking_dict_to_dataframe(grouped_aggregate_ranking_dict):
    sorted_aggregate_ranks = sorted(grouped_aggregate_ranking_dict.keys())
    dataframe_data_dict = dict()

    dataframe_data_dict['rank'] = list()
    dataframe_data_dict['aggregate_rank'] = list()
    dataframe_data_dict['university_name'] = list()

    rank_in_aggregate_rank_table = 1
    for ranking_name in grouped_aggregate_ranking_dict[sorted_aggregate_ranks[0]]['university_list'][0]['ranks'].keys():
        #print 'convert_aggregate_ranking_dict_to_dataframe, ranking_name: ', ranking_name
        dataframe_data_dict[ranking_name] = list()

    for aggregate_rank_value in sorted_aggregate_ranks:
        aggregate_ranking_record = grouped_aggregate_ranking_dict[aggregate_rank_value]
        for university in aggregate_ranking_record['university_list']:
            dataframe_data_dict['rank'].append(rank_in_aggregate_rank_table)
            dataframe_data_dict['aggregate_rank'].append(aggregate_rank_value)
            dataframe_data_dict['university_name'].append(university['canonical_name'])
            ranks = university['ranks']
            for ranking_name, ranking_value in ranks.items():
                dataframe_data_dict[ranking_name].append(ranking_value)
        rank_in_aggregate_rank_table = rank_in_aggregate_rank_table + 1
    return DataFrame(dataframe_data_dict)



def get_rankings_values(grouped_df_part, rankings_num):
    grouped_data_list = grouped_df_part[['ranking_name', 'number_in_ranking_table']].to_dict('index').values()
    university_name = grouped_df_part['university_name'].tolist()[0]
    ranks_values_num = len(grouped_data_list)

    ranks_values = None

    if ranks_values_num == rankings_num:
        ranks_values = {record['ranking_name'] : record['number_in_ranking_table'] for record in grouped_data_list}
    #print ranks_values
    return {'canonical_name' : university_name, 'ranks' : ranks_values}


def from_database(rankings_names_list, year):
    rankings_num = len(rankings_names_list)

    this_function_start_time = timer()

    rank_tables = list()

    year = prepare_year_to_compare(year)

    universities = University.objects.all()
    rankings_values_related = RankingValue.objects.filter(ranking_description__short_name__in=rankings_names_list).filter(ranking_description__year=year).select_related()


    df = DataFrame(list(rankings_values_related.values('ranking_description__short_name', 'number_in_ranking_table', 'university__university_name')))

    df.rename(columns={'ranking_description__short_name' : 'ranking_name', 'university__university_name' : 'university_name'}, inplace=True)


    ranks_by_university_names = df.groupby(df.university_name).apply(get_rankings_values, rankings_num = rankings_num)

    return [record for record in ranks_by_university_names if record['ranks'] != None]
    

def build_aggregate_ranking_dataframe(ranking_descriptions):
    dataframes_dict = rawranking_records_to_dataframes(ranking_descriptions)
    ranking_tables_dict = dataframes_to_ranking_tables(dataframes_dict)

    union_rank_tables = union_ranks(ranking_tables_dict)
    #print 'build_aggregate_ranking_dataframe, type(aggregate_rank): ', type(append_aggregate_rank)
    union_rank_tables_with_aggregated_rank = append_aggregate_rank(union_rank_tables)
    
    universities_grouped_by_aggregate_rank = group_by_aggregate_rank(union_rank_tables_with_aggregated_rank)

    aggregate_ranking_dataframe = convert_aggregate_ranking_dict_to_dataframe(universities_grouped_by_aggregate_rank)

    return aggregate_ranking_dataframe


def assemble_aggregate_ranking_dataframe(ranking_names_list, year):
    print 'Entry in assemble_aggregate_ranking_dataframe'
    this_func_start_time = timer()
    start = timer()
    rank_tables = from_database(ranking_names_list, year)
    end = timer()
    #print 'assemble_aggregate_ranking_dataframe: from_database function runtime = ', end - start

    if rank_tables != []:
        start = timer()
        rank_tables_with_aggregated_rank = append_aggregate_rank(rank_tables)
        end = timer()
        #print 'assemble_aggregate_ranking_dataframe: append_aggregate_rank function runtime = ', end - start
        
        start = timer()
        universities_grouped_by_aggregate_rank = group_by_aggregate_rank(rank_tables_with_aggregated_rank)
        end = timer()
        #print 'assemble_aggregate_ranking_dataframe: group_by_aggregate_rank function runtime = ', end - start

        start = timer()
        aggregate_ranking_dataframe = convert_aggregate_ranking_dict_to_dataframe(universities_grouped_by_aggregate_rank)
        end = timer()
        #print 'assemble_aggregate_ranking_dataframe: convert_aggregate_ranking_dict_to_dataframe_rank function runtime = ', end - start

        #print 'assemble_aggregate_ranking_dataframe: rank_tables != []'
        this_func_end_time = timer()
        #print 'assemble_aggregate_ranking_dataframe: total runtime = ', this_func_end_time - this_func_start_time
        return aggregate_ranking_dataframe
    else:
        #print 'assemble_aggregate_ranking_dataframe: rank_tables == []'
        return None

def db_to_python_structures():
    db_as_list = list()
    for ranking_name in RankingDescription.objects.all():
        ranking = {'short_name' : ranking_name.short_name, 'full_name' : ranking_name.full_name}
        raw_ranking_records = ranking_name.rawrankingrecord_set.all()
        rank_table = list()
        for record in raw_ranking_records:
            rank_table.append({'university_name': record.university_name, 'country' : record.country, 'original_value' : record.original_value, 'number_in_ranking_table' : record.number_in_ranking_table})
        ranking['rank_table'] = rank_table
        db_as_list.append(ranking)
    return db_as_list

def db_as_list_to_db(db_as_list):
    for ranking in db_as_list:
        ranking_table = ranking['rank_table']
        ranking_description = RankingDescription(short_name=ranking['short_name'], full_name=ranking['full_name'], original_ranking_length=len(ranking_table), year=datetime.date.today().year)
        ranking_description.save()
        for record in ranking_table:
            ranking_description.rawrankingrecord_set.create(university_name=record['university_name'], country=record['country'], original_value=record['original_value'], number_in_ranking_table=record['number_in_ranking_table'])



if __name__ == '__main__':
    dataframes_dict = rawranking_records_to_dataframes(ranking_descriptions)
    ranking_tables_dict = dataframes_to_ranking_tables(dataframes_dict)

    for ranking_name, ranking_table in ranking_tables_dict.items():
        ##print ranking_name
        for university_record in ranking_table:
            pass
            ##print university_record

    #print '\n' * 6
    union_rank_tables = union_ranks(ranking_tables_dict)

    union_rank_tables_with_aggregated_rank = append_aggregate_rank(union_rank_tables)
    
    for record in union_rank_tables_with_aggregated_rank:
        #print '\n' *4, '-' * 40, '\n'
        #print 'university_name\t-\t', record['university_name']
        #print 'canonical_name\t-\t', record['canonical_name']
        #print 'ranks\t-\t', record['ranks']
        #print 'aggregate_rank\t-\t', record['aggregate_rank']
        #print 'university_name_variants: '
        for key, value in record['university_name_variants'].items():
            #print ' ' * 2, key, '\t-\t', value
            pass
        #print '\ncollected_from_all_ranktables_description: '
        collected_from_all_ranktables_description = record['collected_from_all_ranktables_description']
        for rank_name, description in  collected_from_all_ranktables_description.items():
            #print '\t', rank_name, ' :'
            #print '\t\t', 'rankvalue\t-\t', description['rankvalue']
            #print '\t\t', 'name_variants:'
            university_name_variants = description['university_name_variants']
            for name_of_name_variant, name_variant in university_name_variants.items():
                #print '\t' * 3, name_of_name_variant, '\t-\t', name_variant
                pass
    
    universities_grouped_by_aggregate_rank = group_by_aggregate_rank(union_rank_tables_with_aggregated_rank)

    ##print universities_grouped_by_aggregate_rank
    
    #print '\n' * 6

    #for aggregate_rank, rank_record in universities_grouped_by_aggregate_rank.items():
    #    #print '-' * 40, '\n'
    #    #print 'aggregate_rank\t-\t', aggregate_rank
    #    #print '\tfinal_rank\t-\t', rank_record['final_rank']
    #    #print '\tuniversities:'
    #    for university in rank_record['university_list']:
    #        #print '\t' * 2, university['canonical_name']
    
    reranked_by_aggregate_rank_universities_records = reranked(universities_grouped_by_aggregate_rank)

    for aggregate_rank, rank_record in reranked_by_aggregate_rank_universities_records.items():
        #print '-' * 40, '\n'
        #print 'aggregate_rank\t-\t', aggregate_rank
        #print '\tfinal_rank\t-\t', rank_record['final_rank']
        #print '\tuniversities:'
        pass
        for university in rank_record['university_list']:
            #print '\t' * 2, university['canonical_name']
            #print '\t' * 2, university['ranks']
            pass
    
    aggregate_ranking_df = convert_aggregate_ranking_dict_to_dataframe(universities_grouped_by_aggregate_rank)

    #print aggregate_ranking_df
