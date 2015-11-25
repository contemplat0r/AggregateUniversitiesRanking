
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


def get_name_part_in_brackets(name_as_str_list):
    #print 'Entry in get_name_part_in_brackets'
    name_part_in_brackets = ''
    for name_part in name_as_str_list:
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


def get_abbreviations_from_outside_brackets(name_as_str_list):
    abbreviations = list()
    for name_part in name_as_str_list:
        #if len(name_part) > 1 and name_part.isupper():
        if len(name_part) > 1 and categorize_as_abbreviation(name_part):
            abbreviations.append(name_part)
    return abbreviations


def pick_abbreviation_from_fullname(fullname_as_str_list):
    #print 'Entry to pick_abbreviation_from_fullname'
    #print 'pick_abbreviation_from_fullname, fullname_as_str_list: ', fullname_as_str_list
    #print 'pick_abbreviation_from_fullname, len(fullname_as_str_list): ', len(fullname_as_str_list)
    abbr_from_fullname = None
    if len(fullname_as_str_list) > 1:
        abbr_from_fullname = ''
        for part in fullname_as_str_list:
            abbr_from_fullname = abbr_from_fullname + part[0]
    #print 'pick_abbreviation_from_fullname, abbr_from_fullname: ', len(abbr_from_fullname)
    return abbr_from_fullname


def exclude_anciliary_words_from_name_as_list(name_as_str_list):
    return [name_part for name_part in name_as_str_list if name_part not in anciliary_words_list]


def convert_name_as_list_to_string(name_as_str_list):
    name_as_string = name_as_str_list[0]
    for name_part in name_as_str_list[1:]:
        name_as_string = name_as_string + ' ' + name_part
    return name_as_string


def get_name_variants(name_str):
    #print '\n'*4, 'Entry in get_name_variants'
    #print 'get_name_variants, name_str: ', name_str
    name_variants = {
            'raw_fullname_as_string' : name_str,
            'fullname_as_list' : None,
            'fullname_as_list_anciliary_words_excluded' : None,
            'shortname' : None,
            'abbreviation_from_brackets' : None,
            'abbreviation' : None,
            'abbreviations' : list(),
            'abbreviations_build_from_first_letters' : list(),
            'abbreviation_picked_from_fullname' : None,
            'abbreviation_picked_from_fullname_exclude_anciliary_words' : None,
            'abbreviation_with_ampersand' : None,
            'all_abbreviations_list' : None,
            'fullname_as_string' : None,
            'fullname_as_string_anciliary_words_excluded' : None,
            }

    name_as_str_list = name_str.split()
    #print '\nget_name_variants, name_str: ', name_str
    name_as_str_list = [name_part.strip(',') for name_part in name_as_str_list]
    name_part_in_brackets = get_name_part_in_brackets(name_as_str_list)
    #print '\nget_name_variants, name_part_in_brackets: ', name_part_in_brackets
    abbreviation_from_brackets = None
    abbreviation = None
    abbreviations = list()
    #abbreviations_build_from_first_letters = list()
    if name_part_in_brackets != None and len(name_part_in_brackets) > 1:
        name_as_str_list.remove(name_part_in_brackets)
        name_as_str_list = [part.strip('()') for part in name_as_str_list]
        name_part_in_brackets = name_part_in_brackets.strip('()')
        #if name_part_in_brackets.isupper():
        if categorize_as_abbreviation(name_part_in_brackets):
            abbreviation_from_brackets = name_part_in_brackets
            name_variants['abbreviation_from_brackets'] = name_part_in_brackets
            abbreviations.append(name_part_in_brackets)
        else:
            name_variants['shortname'] = name_part_in_brackets
    #else if name_part_in_bracket != None:
    #    print 'Nonstandart situation! Type name part in bracket not recognized'

    #print '\nget_name_variants, name_part_in_brackets: ', name_part_in_brackets
    if name_variants['abbreviation_from_brackets'] == None:
        abbreviation = get_abbreviations_from_outside_brackets(name_as_str_list)
        abbreviations = get_abbreviations_from_outside_brackets(name_as_str_list)
        #print '\nget_name_variants, abbreviation_from_brackets: ', name_variants['abbreviation_from_brackets']
        #print '\nget_name_variants, shortname: ', name_variants['shortname']
        #print '\nget_name_variants, abbreviation: ', abbreviation

        #if abbreviation != None:
        #    name_variants['abbreviation'] = abbreviation
        #    for abbreviation_variant in abbreviation:
        #        name_as_str_list.remove(abbreviation_variant)

        if abbreviations != None:
            name_variants['abbreviations'] = abbreviations
            for abbreviation_variant in abbreviations:
                name_as_str_list.remove(abbreviation_variant)

    abbreviations_build_from_first_letters = list()
    if name_as_str_list != []:
        name_variants['fullname_as_list'] = name_as_str_list
        name_as_str_list_cleaned_from_anciliary_word = exclude_anciliary_words_from_name_as_list(name_as_str_list)

        #print '\nget_name_variants, name_as_str_list_cleaned_from_anciliary_word: ', name_as_str_list_cleaned_from_anciliary_word
        name_variants['fullname_as_list_anciliary_words_excluded'] = name_as_str_list_cleaned_from_anciliary_word

        #if (abbreviation_from_brackets == None) and (abbreviation == []) and (len(name_as_str_list)) > 1:
        if (abbreviations == []) and (len(name_as_str_list)) > 1:
            name_variants['abbreviation_picked_from_fullname'] = pick_abbreviation_from_fullname(name_as_str_list).upper()
            name_variants['abbreviation_picked_from_fullname_exclude_anciliary_words'] = pick_abbreviation_from_fullname(name_as_str_list_cleaned_from_anciliary_word).upper()
            abbreviation_picked_from_fullname = pick_abbreviation_from_fullname(name_as_str_list)
            abbreviation_picked_from_fullname_exclude_anciliary_words = pick_abbreviation_from_fullname(name_as_str_list_cleaned_from_anciliary_word)
            abbreviations = [abbreviation_picked_from_fullname, abbreviation_picked_from_fullname.upper(), abbreviation_picked_from_fullname_exclude_anciliary_words, abbreviation_picked_from_fullname_exclude_anciliary_words.upper()]
            # Здесь добавить строки без .upper() для получения аббревиатур в "изначальном" виде

        name_variants['fullname_as_string'] = convert_name_as_list_to_string(name_as_str_list)
        name_variants['fullname_as_string_anciliary_words_excluded'] = convert_name_as_list_to_string(name_as_str_list_cleaned_from_anciliary_word)
    return name_variants 


#def determine_names_as_string_match(first_name_as_string, second_name_as_string):
#    names_match = False
    
#    if (first_name_as_string.find(second_name_as_string) != -1) or (second_name_as_string.find(first_name_as_string) != -1):
#        names_match = True
#    else:
#        print 'Name %s and name %s are different' % (first_name_as_string, second_name_as_string)
#    return names_match


def determine_names_as_string_match(first_name_as_string, second_name_as_string):
    return (first_name_as_string == second_name_as_string) or (second_name_as_string in first_name_as_string) or (first_name_as_string in second_name_as_string)


def compare_abbreviations(first_name_description, second_name_description):
    result = False
    abbr_keys = ['abbreviation', 'br_abbreviation', 'abbr_from_fullname']
    first_descr_abbrs = [first_name_description[key] for key in abbr_keys]
    second_descr_abbrs = [second_name_description[key] for key in abbr_keys]
    return compare_string_lists(first_descr_abbrs, second_descr_abbrs, lambda str1, str2: str1 == str2)


def abbreviations_not_in_brackets_match_abbreviation(abbrevation, abbreviation_from_outside_brackets):
    match = False
    for abbreviation_not_in_bracket in abbreviations_not_in_brackets:
        if abbreviation == abbreviation_not_in_bracket:
            match = True
            break
    return match


def determine_abbreviations_not_in_brackets_match(first_abbreviations_list, second_abbreviations_list):
    match = False
    for abbreviation in first_abbreviations_list:
        if abbreviations_not_in_brackets_match_abbreviation(abbreviation, second_abbreviations_list) == True:
            match = True
            break
    return match


def determine_name_parts_match(first_name_part, second_name_part):
    result = False
    if (len(first_name_part) > 1 and len(second_name_part) > 1) and (first_name_part == second_name_part or first_name_part in second_name_part or second_name_part in first_name_part):
        result = True
    return result



def determine_full_names_as_list_match(first_name_as_list, second_name_as_list):
    result_of_determine = False
    determine_result_as_bool_list = [list(set([determine_name_parts_match(second_name_part, first_name_part) for second_name_part in second_name_as_list])) for first_name_part in first_name_as_list]
    if len(determine_result_as_bool_list) == len([result for result in determine_result_as_bool_list if result != [False]]):
        result_of_determine = True
    return result_of_determine


def determine_string_lists_match(first_string_list, second_string_list, comparator):
    result_of_determine = False
    result_of_determine_as_bool_list = list(set((comparator(second_string, first_string) for second_string in second_string_list if second_string != None for first_string in first_string_list if first_string != None)))
    if result_of_determine_as_bool_list == [True]:
        result_of_determine = True
    return result_of_determine


def caluclate_distantion(first_name_as_string, second_name_as_string):
    return 0


def compare_name_descriptions(first_name_description, second_name_description):
    result = False
    #return difflib.SequenceMatcher(None, first_name_description['fullname'], second_name_description['fullname']).ratio()
    if first_name_description['fullname_as_list'] != None and second_name_description['fullname_as_list'] != None:
        result = compare_full_names_as_list(first_name_description, second_name_description)
    else:
        result = compare_abbreviations(first_name_description, second_name_description)
    return result

    
def determine_names_match(first_name_description, second_name_description):
    names_match = False

    raw_first_name_as_string = first_name_description['raw_fullname_as_string']
    raw_second_name_as_string = second_name_description['raw_fullname_as_string']
    
    if determine_names_as_string_match(raw_first_name_as_string, raw_second_name_as_string) == True:
        names_match = True
    elif determine_names_as_string_match(first_name_description['full_name_as_string'], second_name_description['full_name_as_string']) == True:
        names_match = True
    elif determine_names_as_string_match(first_name_description['fullname_as_string_anciliary_words_excluded'], second_name_description['fullname_as_string_anciliary_words_excluded']) == True:
        names_match = True
    elif determine_full_names_as_list_match(first_name_description['fullname_as_list'], second_name_description['fullname_as_list']) == True:
        names_match = True
    elif determine_full_names_as_list_match(first_name_description['fullname_as_list_anciliary_words_excluded'], second_name_description['fullname_as_list_anciliary_words_excluded']) == True:
        names_match = True
    elif determine_abbreviations_not_in_brackets_match(first_name_description['abbreviation'], second_name_description['abbreviation']) == True:
        names_match = True
    elif abbreviations_not_in_brackets_match_abbreviation(first_name_description['abbreviation_from_brackets'], second_name_description['abbreviation']) == True:
        names_match = True
    elif abbreviations_not_in_brackets_match_abbreviation(second_name_description['abbreviation_from_brackets'], first_name_description['abbreviation']) == True:
        names_match = True
    elif abbreviations_not_in_brackets_match_abbreviation(first_name_description['abbreviation_from_brackets'], second_name_description['abbreviation']) == True:
        names_match = True
    elif abbreviations_not_in_brackets_match_abbreviation(second_name_description['abbreviation_from_brackets'], first_name_description['abbreviation']) == True:
        names_match = True

    elif determine_names_as_string_match(first_name_description['abbreviation_from_brackets'], second_name_description['abbreviation_from_brackets']) == True:
        names_match = True
