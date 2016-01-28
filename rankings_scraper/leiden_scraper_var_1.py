# coding: utf-8

import requests
from copy import deepcopy
import os
from os.path import abspath, join, dirname
import glob
import codecs
import sys
from htmlutils import *

print join(abspath(join(dirname(__file__), '..')), 'aggregate_universities_ranking')

DJANGO_PROJECT_DIR = join(abspath(join(dirname(__file__), '..')), 'aggregate_universities_ranking')
sys.path.append(DJANGO_PROJECT_DIR)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aggregate_universities_ranking.settings')
import django
django.setup()
from aggregate_ranking_representation.models import RankingDescription, RawRankingRecord

NONE_STR_VALUE = '~~~~~~~~~'


get_attrib = generate_attrib_getter('data-tooltip')


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
        if ranking_as_list != []:
             ranking = ranking_as_list[0].text
             print 'Ranking: ', ranking
        else:
             print 'ranking_as_list is empty'
        if name_as_list != []:
            #university_name = name_as_list[0].text
            university_name = get_attrib(name_as_list[0])
            print 'University Name: ', university_name.encode('utf-8')
        if country_as_list != []:
            country = country_as_list[0].attrib.get('alt')
            print 'Country: ', country

        print '\n', '-' * 10, '\n'

        ranktable.append({'absolute_ranking' : rownum, 'ranking' : ranking, 'university_name' : university_name, 'country' : country})

        rownum = rownum + 1

    return ranktable


def get_content(url, headers={'User-Agent' : 'requests'}, post_data={}, exceptions_log_file=None):
    req = None
    content = None
    try: 
        if post_data == {}:
            req = requests.get(url, headers=headers)
        else:
            req = requests.post(url, headers=headers, data=post_data)
    except (requests.exceptions.ConnectionError, requests.exceptions.Timeout, requests.exceptions.HTTPError, httplib.IncompleteRead, requests.exceptions.MissingSchema) as e:
        print 'get_content: ' + url + '  Exception: ' + str(e) + '\n'
        if exceptions_log_file != None:
            exceptions_log_file.write('get_content: ' + url + ' Exception: ' + str(e) + '\n')
            exceptions_log_file.flush()
    if req != None:
        content = req.text

    return content


def save_content(content, filename):
    success = True
    f = codecs.open(filename, 'w', encoding='utf-8')
    f.write(content)
    f.close()
    return success


if __name__ == '__main__':


    table_row_xpath = '//table[@class="pagedtable ranking"]/tbody/tr'
    ranking_value_xpath = 'td[@class="rank"]'
    university_name_xpath = 'td[@class="university"]'
    country_xpath = 'td[@class="country"]/img'
    description = {'table_row_xpath' : table_row_xpath, 'ranking_value_xpath' : ranking_value_xpath, 'university_name_xpath' : university_name_xpath, 'country_xpath' : country_xpath}

    base_url = 'http://www.leidenranking.com'
    url = 'http://www.leidenranking.com/Ranking/Ranking2015Result'

    headers = {
            'User-Agent' : 'Mozilla/5.0 (X11; Linux x86_64; rv:42.0) Gecko/20100101 Firefox/42.0 Iceweasel/42.0',
            'Accept' : '*/*',
            'Accept-Language' : 'ru-RU,ru;q=0.7,uk;q=0.3',
            'Content-Type' : 'application/x-www-form-urlencoded; charset=UTF-8',
            'X-Requested-With' : 'XMLHttpRequest',
            'Referer' : 'http://www.leidenranking.com/ranking/2015',
            'Connection' : 'keep-alive',
            'Pragma' : 'no-cache'
            }

    headers_layer_1 = {
            'User-Agent' : 'Mozilla/5.0 (X11; Linux x86_64; rv:42.0) Gecko/20100101 Firefox/42.0 Iceweasel/42.0',
            'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language' : 'ru-RU,ru;q=0.7,uk;q=0.3',
            'Referer' : 'http://www.leidenranking.com/ranking/2015',
            'Connection' : 'keep-alive'
            }

    post_data = {'field_id' : '1', 'continent_code' : '', 'country_code' : '', 'performance_dimension' : 'false', 'ranking_indicator' : 'pp_top10', 'stability_interval' : 'true', 'size_independent' : 'true', 'fractional_counting' : 'true', 'core_pub_only' : 'false', 'number_of_publications' : '100', 'period_id' : '5', 'period_text' :' 2010%E2%80%932013'
            }

    #content = get_content(url, headers, post_data)
    #save_content(content, 'leiden_content_0_requests.txt')

    content = get_saved_content('leiden_content_0_requests.txt')


    #all_same_type_nodes = get_all_same_type_nodes(content, '//td[@class="university"]')
    #get_attrib = generate_attrib_getter('data-tooltip')
    #result_list = node_list_processor(all_same_type_nodes, get_attrib)
    #for item in result_list:
    #    print '\n'*2, '-' * 10
    #    print item
   


    #get_attrib = generate_attrib_getter('href')
    #for node in all_same_type_nodes:
    #     university_url_part = get_attrib(get_all_same_type_subnodes(node, 'a')[0])
    #     url = base_url + university_url_part

    #     content = get_content(url, headers_layer_1)

    #     all_same_type_nodes = get_all_same_type_nodes(content, '//h1[@class="head1"]')
    #     print all_same_type_nodes[0].text


    ranktable = extract_data(content, description)
    print 'Ranktable extracted'
    print 'len(ranktable): ', len(ranktable)


    ranking_descriptions_list = RankingDescription.objects.filter(short_name='Leiden')
    ranking_description = ranking_descriptions_list[0]
    print ranking_description
    
    ranking_description.rawrankingrecord_set.all().delete()

    for ranking_record in ranktable:
        print ranking_record
        ## raw_ranking_record = RawRankingRecord(university_name=ranking_record['university_name'], country=ranking_record['country'], original_value=ranking_record['ranking'], number_in_ranking_table=ranking_record['absolute_ranking'], ranking_name=ranking_name)
        ### ranking_name.rawrankingrecord_set.add(raw_ranking_record)
        ## raw_ranking_record.save(force_insert=True)

        ranking_description.rawrankingrecord_set.create(university_name=ranking_record['university_name'], country=ranking_record['country'], original_value=ranking_record['ranking'], number_in_ranking_table=ranking_record['absolute_ranking'])
    
    #print '\n' * 6, 'RawRankingRecord.objects.all(): ', '\n' * 2,  RawRankingRecord.objects.all()

