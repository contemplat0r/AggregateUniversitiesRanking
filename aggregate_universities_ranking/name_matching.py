
# coding: utf-8

from functools import reduce
import numpy as np
NaN = np.nan

# Добавить "очищенный от вспомогательных слов (артиклей) вариант". Аббревиатуры тогда
# тоже вычислять два варианта: "очищенную от вспомогательных слов" и "со вспомогательными словами".

anciliary_words_list = ['of', 'the', 'The', 'a', 'A', 'an', 'An', '&', '-']
special_symbols_list = ['-', '.']



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


def compare_name_descriptions(first_name_description, second_name_description):
    result = False
    #return difflib.SequenceMatcher(None, first_name_description['fullname'], second_name_description['fullname']).ratio()
    if first_name_description['fullname_as_list'] != None and second_name_description['fullname_as_list'] != None:
        result = compare_full_names_as_list(first_name_description, second_name_description)
    else:
        result = compare_abbreviations(first_name_description, second_name_description)
    return result

    
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
            print 'university: ', university
            university['ranks'] = default_ranks.copy()
            #university['ranks'][rankname] = university.pop('rank')
            university['ranks'][rankname] = university['rank']
            for another_rankname in rest_ranknames:
                another_ranktable = ranktables[another_rankname]
                to_remove_universities = list()
                for another_university in another_ranktable:
                    math = names_match(university['university_name_variants'], another_university['university_name_variants'])
                    if math:
                        university['ranks'][another_rankname] = another_university['rank']
                        to_remove_universities.append(another_university)
                        break
                for another_university in to_remove_universities:
                    another_ranktable.remove(another_university)
            union_universities_list.append(university)
    return union_universities_list

def aggregate_rank(union_university_ranks_list):
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

