def detect_university_in_ranktable(current_university_info, rankname, ranktable):
    aggregate_current_university_info = None
    for university in ranktable:
        math = compare_name_descriptions(current_university_info['uname_variants'], university['uname_variants'])
        if math:
            aggregate_current_university_info = current_university_info
            aggregate_current_university_info['uname_variants']['another_name'] = university['uname_variants']['fullname']
            aggregate_current_university_info['ranks'][rankname] = university['rank']
            break
    return aggregate_current_university_info

def union_ranks(ranktables):
    union_universities_list = list()
    ranknames = ranktables.keys()
    rest_ranknames = ranknames[:]
    rank_lenghts = dict()
    for rankname in ranknames:
        rank_lenghts[rankname] = len(ranktables[rankname])
    default_ranks = {rankname : (len(ranktable) + 1) for rankname, ranktable in ranktables.items()}
    math_counter = 0
    no_math_counter = 0
    for rankname in ranknames:
        ranktable = ranktables[rankname]
        rest_ranknames.remove(rankname)
        for university in ranktable:
            university['ranks'] = default_ranks.copy()
            university['ranks'][rankname] = university.pop('rank')
            for another_rankname in rest_ranknames:
                another_ranktable = ranktables[another_rankname]
                to_remove_universities = list()
                for another_university in another_ranktable:
                    math = compare_name_descriptions(university['uname_variants'], another_university['uname_variants'])
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

