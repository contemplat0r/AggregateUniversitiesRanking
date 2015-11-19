
# coding: utf-8

# Добавить "очищенный от вспомогательных слов (артиклей) вариант". Аббревиатуры тогда
# тоже вычислять два варианта: "очищенную от вспомогательных слов" и "со вспомогательными словами".

def entity_name_match(first_name, second_name):
    name_match = False
    
    if (first_name.find(second_name) != -1) or (second_name.find(first_name) != -1):
        name_match = True
    else:
        print 'Name %s and name %s are different' % (first_name, second_name)
    return name_match

def get_name_variants(name_str):
    name_description = {
            'fullname_as_list' : None,
            'fullname' : None,
            'shortname' : None,
            'br_abbreviation' : None,
            'abbreviation' : None,
            'abbr_from_fullname' : None}
    raw_name_parts = name_str.split()
    br_part = None
    for part in raw_name_parts:
        if part.startswith('(') and part.endswith(')'):
            br_part = part
            in_br_part = br_part.strip('()')
            if len(in_br_part) > 1 and in_br_part.isupper():
                name_description['br_abbreviation'] = in_br_part
            else:
                name_description['shortname'] = in_br_part
            break
    if br_part != None:
        raw_name_parts.remove(br_part)
    name_parts = [part.strip('()') for part in raw_name_parts]
    abbreviation = None
    for part in name_parts:
        if len(part) > 1 and part.isupper():
            abbreviation = part
            break
    if abbreviation != None:
        name_description['abbreviation'] = abbreviation
        name_parts.remove(abbreviation)
    if name_parts != []:
        #name_description['fullname_as_list'] = [part.strip(',') for part in name_parts if part.istitle()]
        name_description['fullname_as_list'] = [part.strip(',') for part in name_parts if part[0].isupper()]
        if len(name_parts) > 1:
            abbr_from_fullname = ''
            for part in name_parts:
                #if part[0].isupper():
                    #abbr_from_fullname = abbr_from_fullname + part[0]
                abbr_from_fullname = abbr_from_fullname + part[0]
            name_description['abbr_from_fullname'] = abbr_from_fullname
        fullname_as_string = name_parts[0]
        for part in name_parts[1:]:
            fullname_as_string = fullname_as_string + ' ' + part
        name_description['fullname'] = fullname_as_string
    name_description['fullname'] = name_str
    return name_description 

def compare_abbreviations(first_name_description, second_name_description):
    result = False
    abbr_keys = ['abbreviation', 'br_abbreviation', 'abbr_from_fullname']
    first_descr_abbrs = [first_name_description[key] for key in abbr_keys]
    second_descr_abbrs = [second_name_description[key] for key in abbr_keys]
    return compare_string_lists(first_descr_abbrs, second_descr_abbrs, lambda str1, str2: str1 == str2)

def compare_name_parts(first, second):
    result = False
    if (len(first) > 1 and len(second) > 1) and (first == second or first in second or second in first):
        result = True
    return result

def compare_full_names_as_list(first_name_description, second_name_description):
    result = False
    first_name = first_name_description['fullname_as_list']
    second_name = second_name_description['fullname_as_list']
    compare_results = [list(set([compare_name_parts(sn, fn) for sn in second_name])) for fn in first_name]
    if len(compare_results) == len([cr for cr in compare_results if cr != [False]]):
        result = True
    return result

def compare_string_lists(first_lst, second_lst, comparator):
    result = False
    compare_results_set = list(set((comparator(s_str, f_str) for s_str in second_lst if s_str != None for f_str in first_lst if f_str != None)))
    if compare_results_set == [True]:
        result = True
    return result

def compare_name_descriptions(first_name_description, second_name_description):
    result = False
    #return difflib.SequenceMatcher(None, first_name_description['fullname'], second_name_description['fullname']).ratio()
    if first_name_description['fullname_as_list'] != None and second_name_description['fullname_as_list'] != None:
        result = compare_full_names_as_list(first_name_description, second_name_description)
    else:
        result = compare_abbreviations(first_name_description, second_name_description)
    return result

