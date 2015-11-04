# -*- coding: utf8 -*- 
from lxml import etree
from StringIO import StringIO
from copy import deepcopy
import os
from os.path import abspath, join, dirname
import glob
import codecs
import sys

print join(abspath(join(dirname(__file__), '..')), 'aggregate_universities_ranking')

DJANGO_PROJECT_DIR = join(abspath(join(dirname(__file__), '..')), 'aggregate_universities_ranking')
sys.path.append(DJANGO_PROJECT_DIR)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aggregate_universities_ranking.settings')
import django
django.setup()
from aggregate_ranking_representation.models import RankingName, RawRankingRecord

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
    for row in tree.xpath(table_row_xpath):
        ranking = NONE_STR_VALUE
        university_name = NONE_STR_VALUE
        country = NONE_STR_VALUE

        ranking_as_list = row.xpath(ranking_value_xpath)
        name_as_list = row.xpath(university_name_xpath)
        country_as_list = row.xpath(country_xpath)
        print '\n', '-' * 10
        print 'Absolute ranking: ', rownum
        ranking = NONE_STR_VALUE
        university_name = NONE_STR_VALUE
        country = NONE_STR_VALUE
        if ranking_as_list != []:
             ranking = ranking_as_list[0].text
             print 'Ranking: ', ranking
        if name_as_list != []:
            university_name = name_as_list[0].text
            print 'University Name: ', university_name.encode('utf-8')
        if country_as_list != []:
            country = country_as_list[0].attrib.get('title').split()[-1].rstrip('.')
            print 'Country: ', country

        print '\n', '-' * 10, '\n'

        ranktable.append({'absolute_ranking' : rownum, 'ranking' : ranking, 'university_name' : university_name, 'country' : country})

        rownum = rownum + 1

    return ranktable

if __name__ == '__main__':

    html = get_saved_html('ARWU_by_Requests-All.html')
    #print html
    table_row_xpath = '//table[@id="UniversityRanking"]/tr[starts-with(@class, "bgf")]'
    ranking_value_xpath = 'td/div'
    university_name_xpath = 'td[@class="left"]/a'
    country_xpath = 'td/a[@title]'
    description = {'table_row_xpath' : table_row_xpath, 'ranking_value_xpath' : ranking_value_xpath, 'university_name_xpath' : university_name_xpath, 'country_xpath' : country_xpath}
    ranktable = extract_data(html, description)
    print 'Ranktable extracted'
    print 'len(ranktable): ', len(ranktable)

    ranking_name_list = RankingName.objects.filter(short_name='ARWU')
    print ranking_name_list
    ranking_name = ranking_name_list[0]


    for ranking_record in ranktable:
        print ranking_record
        ## raw_ranking_record = RawRankingRecord(university_name=ranking_record['university_name'], country=ranking_record['country'], original_value=ranking_record['ranking'], number_in_ranking_table=ranking_record['absolute_ranking'], ranking_name=ranking_name)
        ### ranking_name.rawrankingrecord_set.add(raw_ranking_record)
        ## raw_ranking_record.save(force_insert=True)
        ranking_name.rawrankingrecord_set.create(university_name=ranking_record['university_name'], country=ranking_record['country'], original_value=ranking_record['ranking'], number_in_ranking_table=ranking_record['absolute_ranking'])
    
    print '\n' * 6, 'RawRankingRecord.objects.all(): ', '\n' * 2,  RawRankingRecord.objects.all()

