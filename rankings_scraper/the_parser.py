# -*- coding: utf8 -*- 
from lxml import etree
from StringIO import StringIO
from copy import deepcopy
import os
from os.path import abspath, join, dirname
import glob
import codecs
import sys

DJANGO_PROJECT_DIR = join(abspath(join(dirname(__file__), '..')), 'aggregate_universities_ranking')
sys.path.append(DJANGO_PROJECT_DIR)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aggregate_universities_ranking.settings')
import django
django.setup()
from aggregate_ranking_representation.models import RawRankingRecord, RankingDescription

NONE_STR_VALUE = '~~~~~~~~~'

def get_saved_html(filename):
    f = codecs.open(filename, 'r', encoding='utf-8')
    #f = open(filename, 'r')
    html = f.read()
    f.close()
    ## print html
    return html

def extract_data(html, description):
    table_row_xpath = description['table_row_xpath']
    ranking_value_xpath = description['ranking_value_xpath']
    university_name_xpath = description['university_name_xpath']
    country_xpath = description['country_xpath']
    print 'table_row_xpath = %s' % table_row_xpath
    parser = etree.HTMLParser()
    rownum = 1
    ranktable = []
    tree = etree.parse(StringIO(html), parser)
    row_is_empty = False
    for row in tree.xpath(table_row_xpath):
        ranking = NONE_STR_VALUE
        university_name = NONE_STR_VALUE
        country = NONE_STR_VALUE
        ranking_as_list = row.xpath(ranking_value_xpath)
        name_as_list = row.xpath(university_name_xpath)
        country_as_list = row.xpath(country_xpath)
        print '\n', '-' * 10
        print 'Absolute ranking: ', rownum
        if ranking_as_list != []:
            ranking = ranking_as_list[0].text
            print 'Ranking: ', ranking
            row_is_empty = False
        else:
            print 'ranking_as_list is empty'
            row_is_empty = True
        if name_as_list != []:
            university_name = name_as_list[0].text
            print 'University Name: ', university_name.encode('utf-8')
        if country_as_list != []:
            country = country_as_list[0].text
            print 'Country: ', country

        print '\n', '-' * 10, '\n'

        if not row_is_empty:
            ranktable.append({'absolute_ranking' : rownum, 'ranking' : ranking, 'university_name' : university_name, 'country' : country})
            rownum = rownum + 1

    return ranktable

if __name__ == '__main__':

    html = get_saved_html('Times-Higher-Education-2015-2016-All.html')
    #print html
    table_row_xpath = '//tr[@role="row"]'
    ranking_value_xpath = 'td[@class="all details-control sorting_1 sorting_2"]'
    university_name_xpath = 'td[@class=" all "]/a'
    country_xpath = 'td[@class=" all "]/div[@class="country"]'
    description = {'table_row_xpath' : table_row_xpath, 'ranking_value_xpath' : ranking_value_xpath, 'university_name_xpath' : university_name_xpath, 'country_xpath' : country_xpath}
    ranktable = extract_data(html, description)
    print 'Ranktable extracted'
    print 'len(ranktable): ', len(ranktable)

    ranking_description_list = RankingDescription.objects.filter(short_name='THE')
    print ranking_description_list
    ranking_description = ranking_description_list[0]
    ranking_description.rawrankingrecord_set.all().delete()


    for ranking_record in ranktable:
        print ranking_record
        raw_ranking_record = RawRankingRecord(university_name=ranking_record['university_name'], country=ranking_record['country'], original_value=ranking_record['ranking'], number_in_ranking_table=ranking_record['absolute_ranking'], ranking_description=ranking_description)
        ### ranking_description.rawrankingrecord_set.add(raw_ranking_record)
        raw_ranking_record.save(force_insert=True)
        ranking_description.rawrankingrecord_set.create(university_name=ranking_record['university_name'], country=ranking_record['country'], original_value=ranking_record['ranking'], number_in_ranking_table=ranking_record['absolute_ranking'])
    
    ## print '\n' * 6, 'RawRankingRecord.objects.all(): ', '\n' * 2,  RawRankingRecord.objects.all()

