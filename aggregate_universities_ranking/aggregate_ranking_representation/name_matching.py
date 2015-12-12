
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

#DJANGO_PROJECT_DIR = join(abspath(join(dirname(__file__), '..')), 'aggregate_universities_ranking')
#sys.path.append(DJANGO_PROJECT_DIR)
#os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aggregate_universities_ranking.settings')

#django.setup()
from .models import RankingDescription, RawRankingRecord, University, RankingValue

NaN = np.nan


# Добавить "очищенный от вспомогательных слов (артиклей) вариант". Аббревиатуры тогда
# тоже вычислять два варианта: "очищенную от вспомогательных слов" и "со вспомогательными словами".

anciliary_words_list = ['of', 'the', 'The', 'a', 'A', 'an', 'An', '&', '-']
special_symbols_list = ['-', '.']


def the_dataframe_postprocessor(the_dataframe):
    the_dataframe = the_dataframe.drop(0, axis=0)
    the_dataframe['number_in_ranking_table'] = the_dataframe['number_in_ranking_table'].map(lambda x: x -1 ) 
    return the_dataframe

ranking_table_as_list_preprocessor = lambda df: df[:6].T
#ranking_table_as_list_preprocessor = lambda df: df[:4].T


ranking_descriptions = {
        'QS' : {
            'dataframe_postprocessor' : None,
            'ranking_table_as_list_preprocessor' : ranking_table_as_list_preprocessor
            },
        'THE' : {
            'dataframe_postprocessor' : the_dataframe_postprocessor,
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
        dataframe_postprocessor = additional_processors['dataframe_postprocessor']
        if dataframe_postprocessor:
            ranking_dataframe = dataframe_postprocessor(ranking_dataframe)
        dataframes_dict[ranking_short_name]['dataframe'] = ranking_dataframe
    return dataframes_dict

def dataframes_to_ranking_tables(dataframes_dict):
    rank_tables_dict = dict()
    for dataframe_short_name, dataframe_and_additional_processors in dataframes_dict.items():
        dataframe = dataframe_and_additional_processors['dataframe']
        short_dataframe = dataframe[['number_in_ranking_table', 'university_name', 'country']]
        short_dataframe = short_dataframe.rename(columns={'number_in_ranking_table' : 'rank'})
        ranking_table_as_list_preprocessor = dataframe_and_additional_processors['ranking_table_as_list_preprocessor']
        if ranking_table_as_list_preprocessor != None:
            short_dataframe = ranking_table_as_list_preprocessor(short_dataframe)
        ranking_table_as_list = short_dataframe.to_dict().values()
        for university in ranking_table_as_list:
            university['university_name_variants'] = get_name_variants(university['university_name'])
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
    #print 'Entry in get_name_part_in_brackets'
    name_part_in_brackets = ''
    for name_part in name_as_string_list:
        if name_part.startswith('(') and name_part.endswith(')'):
            #print 'get_name_part_in_brackets: name_part start with \'(\' and end with \')\''
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


def categorize_as_abbreviation(string):
    string_is_abbreviation = False
    string_len = len(string)
    upper_symbols_number = sum([1 for char in list(string) if char.isupper()])
    if string_len > 1 and (upper_symbols_number > string_len - upper_symbols_number) and not detect_special_symbol_in_string(string):
        string_is_abbreviation = True
    return string_is_abbreviation


def get_abbreviations_from_outside_brackets(name_as_string_list):
    abbreviations = list()
    for name_part in name_as_string_list:
        #if len(name_part) > 1 and name_part.isupper():
        if len(name_part) > 1 and categorize_as_abbreviation(name_part):
            abbreviations.append(name_part)
    return abbreviations


def pick_abbreviation_from_fullname(fullname_as_string_list):
    #print 'Entry to pick_abbreviation_from_fullname'
    #print 'pick_abbreviation_from_fullname, fullname_as_string_list: ', fullname_as_string_list
    #print 'pick_abbreviation_from_fullname, len(fullname_as_string_list): ', len(fullname_as_string_list)
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

    
def names_match(first_name_description, second_name_description):
    names_match = False

    raw_first_name_as_string = first_name_description['raw_fullname_as_string']
    raw_second_name_as_string = second_name_description['raw_fullname_as_string']
    
    if names_as_string_match(raw_first_name_as_string, raw_second_name_as_string) == True:
        names_match = True
    elif names_as_string_match(first_name_description['fullname_as_string'], second_name_description['fullname_as_string']) == True:
        names_match = True
    elif names_as_string_match(first_name_description['fullname_as_string_anciliary_words_excluded'], second_name_description['fullname_as_string_anciliary_words_excluded']) == True:
        names_match = True
    elif full_names_as_list_match(first_name_description['fullname_as_list'], second_name_description['fullname_as_list']) == True:
        names_match = True
    elif full_names_as_list_match(first_name_description['fullname_as_list_anciliary_words_excluded'], second_name_description['fullname_as_list_anciliary_words_excluded']) == True:
        names_match = True
    elif first_name_description['abbreviations'] != []:
        if (second_name_description['abbreviations'] != []) and (abbreviations_match(first_name_description['abbreviations'], second_name_description['abbreviations']) != False):
            names_match = True
        elif (second_name_description['abbreviations_build_from_first_letters'] != []) and (abbreviations_match(first_name_description['abbreviations'], second_name_description['abbreviations_build_from_first_letters']) != False):
            names_match = True
    elif first_name_description['abbreviations_build_from_first_letters'] != []:
        if (second_name_description['abbreviations'] != []) and (abbreviations_match(first_name_description['abbreviations_build_from_first_letters'], second_name_description['abbreviations']) != False):
            names_match = True

    return names_match


def assign_longest_name_variant(university_description):
    print 'Entry in assign_longest_name_variant'
    longest_name_variant = str()
    #print 'assign_longest_name_variant, university ranks: ', university_description['collected_from_all_ranktables_description'].keys()
    #for description_variants in university_description['collected_from_all_ranktables_description'].values():
    for rankname, description_variants in university_description['collected_from_all_ranktables_description'].items():
        #print 'assign_longest_name_variant, rankname: ', rankname
        #print 'assign_longest_name_variant, name_variants: ', description_variants['university_name_variants']
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
                    math = names_match(university['university_name_variants'], another_university['university_name_variants'])
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
    ranking_name_descriptions = list(RankingDescription.objects.all())

    for university_record in union_rank_tables:
        print '\n' *4, '-' * 40, '\n'
        #print 'university_name\t-\t', university_record['university_name']
        print 'canonical_name\t-\t', university_record['canonical_name']
        print 'ranks\t-\t', university_record['ranks']
        print 'country\t-\t', university_record['country']
        
        for ranking_name_description in ranking_name_descriptions:
            for ranking_name, ranking_value in university_record['ranks'].items():
                if ranking_name_description.short_name == ranking_name:
                    print 'Ranking %s detected' % ranking_name
                    university_name = university_record['canonical_name']
                    country = university_record['country']
                    year = datetime.date(datetime.date.today().year, 1, 1)
                    already_saved_university_descriptions = list(University.objects.all())
                    university_already_in_database = False
                    for already_saved_university_description in already_saved_university_descriptions:
                        print 'already_saved_university_description.university_name: ', already_saved_university_description.university_name, ', university_name: ', university_name
                        if already_saved_university_description.university_name == university_name:
                            print "already_saved_university_description.university_name == university_name"
                            #ranking_value_db_record = RankingValue(year=datetime.date.today(), original_value = '~~~', number_in_ranking_table = ranking_value, ranking_name = ranking_name_description, university_name = already_saved_university_description)
                            ranking_value_db_record = RankingValue(year=year, original_value = '~~~', number_in_ranking_table = ranking_value, ranking_name = ranking_name_description, university_name = already_saved_university_description)
                            ranking_value_db_record.save()
                            print 'Ranking value ', ranking_value, ' saved for university ', university_name, ' and for ranking ', ranking_name
                            university_already_in_database = True
                            print 'Inner break'
                            break
                    if university_already_in_database == False:
                        print 'University %s, not in database' % university_name
                        new_db_university_description_record = University(university_name = university_name, country = country)
                        new_db_university_description_record.save()
                        print 'University %s, saved to database' % university_name
                        #ranking_value_db_record = RankingValue(year=datetime.date.today(), original_value = str(), number_in_ranking_table = ranking_value, ranking_name = ranking_name_description, university_name = new_db_university_description_record)
                        ranking_value_db_record = RankingValue(year=year, original_value = str(), number_in_ranking_table = ranking_value, ranking_name = ranking_name_description, university_name = new_db_university_description_record)
                        ranking_value_db_record.save()
                    print 'Outer break'
                    break

    return 


def prepare_year_to_compare(year):
    return datetime.date(year, 1, 1)


def from_database(rankings_names_list, year):

    year = prepare_year_to_compare(year)
    rank_tables = list()

    for university_description in University.objects.all():
        print 'university_description.university_name: ', university_description.university_name
        university_name = university_description.university_name
        record = {'canonical_name' : university_name}
        ranks = dict()
        for ranking_value_description in university_description.rankingvalue_set.filter(year=year):
            print '\tranking_value_descriptions: ', ranking_value_description
            rank_name = ranking_value_description.ranking_name.short_name
            if rank_name in rankings_names_list:
                ranks.update({rank_name : ranking_value_description.number_in_ranking_table})
        if ranks != {}:
            record['ranks'] = ranks
            rank_tables.append(record)
    return rank_tables


def convert_aggregate_ranking_dict_to_dataframe(grouped_aggregate_ranking_dict):
    sorted_aggregate_ranks = sorted(grouped_aggregate_ranking_dict.keys())
    dataframe_data_dict = dict()

    dataframe_data_dict['rank'] = list()
    dataframe_data_dict['aggregate_rank'] = list()
    dataframe_data_dict['university_name'] = list()

    rank_in_aggregate_rank_table = 1
    for ranking_name in grouped_aggregate_ranking_dict[sorted_aggregate_ranks[0]]['university_list'][0]['ranks'].keys():
        print 'convert_aggregate_ranking_dict_to_dataframe, ranking_name: ', ranking_name
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


def build_aggregate_ranking_dataframe(ranking_descriptions):
    dataframes_dict = rawranking_records_to_dataframes(ranking_descriptions)
    ranking_tables_dict = dataframes_to_ranking_tables(dataframes_dict)

    union_rank_tables = union_ranks(ranking_tables_dict)
    print 'build_aggregate_ranking_dataframe, type(aggregate_rank): ', type(append_aggregate_rank)
    union_rank_tables_with_aggregated_rank = append_aggregate_rank(union_rank_tables)
    
    universities_grouped_by_aggregate_rank = group_by_aggregate_rank(union_rank_tables_with_aggregated_rank)

    aggregate_ranking_dataframe = convert_aggregate_ranking_dict_to_dataframe(universities_grouped_by_aggregate_rank)

    return aggregate_ranking_dataframe


def assemble_aggregate_ranking_dataframe(ranking_names_list, year):
    rank_tables = from_database(ranking_names_list, year)
    if rank_tables != []:
        rank_tables_with_aggregated_rank = append_aggregate_rank(rank_tables)
        
        universities_grouped_by_aggregate_rank = group_by_aggregate_rank(rank_tables_with_aggregated_rank)

        aggregate_ranking_dataframe = convert_aggregate_ranking_dict_to_dataframe(universities_grouped_by_aggregate_rank)

        #print aggregate_ranking_dataframe
        print 'assemble_aggregate_ranking_dataframe: rank_tables != []'
        return aggregate_ranking_dataframe
    else:
        print 'assemble_aggregate_ranking_dataframe: rank_tables == []'
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
        #print ranking_name
        for university_record in ranking_table:
            pass
            #print university_record

    print '\n' * 6
    union_rank_tables = union_ranks(ranking_tables_dict)

    union_rank_tables_with_aggregated_rank = append_aggregate_rank(union_rank_tables)
    
    for record in union_rank_tables_with_aggregated_rank:
        print '\n' *4, '-' * 40, '\n'
        print 'university_name\t-\t', record['university_name']
        print 'canonical_name\t-\t', record['canonical_name']
        print 'ranks\t-\t', record['ranks']
        print 'aggregate_rank\t-\t', record['aggregate_rank']
        print 'university_name_variants: '
        for key, value in record['university_name_variants'].items():
            print ' ' * 2, key, '\t-\t', value
        print '\ncollected_from_all_ranktables_description: '
        collected_from_all_ranktables_description = record['collected_from_all_ranktables_description']
        for rank_name, description in  collected_from_all_ranktables_description.items():
            print '\t', rank_name, ' :'
            print '\t\t', 'rankvalue\t-\t', description['rankvalue']
            print '\t\t', 'name_variants:'
            university_name_variants = description['university_name_variants']
            for name_of_name_variant, name_variant in university_name_variants.items():
                print '\t' * 3, name_of_name_variant, '\t-\t', name_variant
    
    universities_grouped_by_aggregate_rank = group_by_aggregate_rank(union_rank_tables_with_aggregated_rank)

    #print universities_grouped_by_aggregate_rank
    
    print '\n' * 6

    #for aggregate_rank, rank_record in universities_grouped_by_aggregate_rank.items():
    #    print '-' * 40, '\n'
    #    print 'aggregate_rank\t-\t', aggregate_rank
    #    print '\tfinal_rank\t-\t', rank_record['final_rank']
    #    print '\tuniversities:'
    #    for university in rank_record['university_list']:
    #        print '\t' * 2, university['canonical_name']
    
    reranked_by_aggregate_rank_universities_records = reranked(universities_grouped_by_aggregate_rank)

    for aggregate_rank, rank_record in reranked_by_aggregate_rank_universities_records.items():
        print '-' * 40, '\n'
        print 'aggregate_rank\t-\t', aggregate_rank
        print '\tfinal_rank\t-\t', rank_record['final_rank']
        print '\tuniversities:'
        for university in rank_record['university_list']:
            print '\t' * 2, university['canonical_name']
            print '\t' * 2, university['ranks']
    
    aggregate_ranking_df = convert_aggregate_ranking_dict_to_dataframe(universities_grouped_by_aggregate_rank)

    print aggregate_ranking_df
