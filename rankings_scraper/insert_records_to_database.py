# -*- coding: utf8 -*- 

def raw_records_to_database(ranking_name_as_list, ranktable):
    print ranking_name_as_list
    ranking_name = ranking_name_as_list[0]


    for ranking_record in ranktable:
        print ranking_record
        ranking_name.rawrankingrecord_set.create(university_name=ranking_record['university_name'], country=ranking_record['country'], original_value=ranking_record['ranking'], number_in_ranking_table=ranking_record['absolute_ranking'])

