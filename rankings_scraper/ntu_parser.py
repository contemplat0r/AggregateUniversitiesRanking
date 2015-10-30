# -*- coding: utf8 -*- 
from lxml import etree
from StringIO import StringIO
from copy import deepcopy
import os
import glob
import codecs
import sys

NONE_STR_VALUE = '~~~~~~~~~'

def get_saved_html(filename):
    f = codecs.open(filename, 'r', encoding='utf-8')
    #f = open(filename, 'r')
    html = f.read()
    f.close()
    ## print html
    return html

def extract_data(html, description, absolute_ranking):
    table_row_xpath = description['table_row_xpath']
    ranking_value_xpath = description['ranking_value_xpath']
    university_name_xpath = description['university_name_xpath']
    country_xpath = description['country_xpath']
    print 'table_row_xpath = %s' % table_row_xpath
    parser = etree.HTMLParser()
    # rownum = 1
    rownum = absolute_ranking
    
    ranktable = []
    tree = etree.parse(StringIO(html), parser)
    for row in tree.xpath(table_row_xpath):
        ranking = NONE_STR_VALUE
        university_name = NONE_STR_VALUE
        country = NONE_STR_VALUE

        ranking_as_list = row.xpath(ranking_value_xpath)
        name_as_list = row.xpath(university_name_xpath)
        ## country_as_list = row.xpath(country_xpath)
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
        ## if country_as_list != []:
        ##     country = country_as_list[0].attrib.get('title').split()[-1].rstrip('.')
        ##     print 'Country: ', country

        #print '\n', '-' * 10, '\n'

        ranktable.append({'absolute_ranking' : rownum, 'ranking' : ranking, 'university_name' : university_name, 'country' : country})

        rownum = rownum + 1
    absolute_ranking = rownum - 1
    return ranktable[0:-1], absolute_ranking

if __name__ == '__main__':

    #print html
    table_row_xpath = '//table[@id="MainContain_GridView1"]/tbody/tr[not(@valign)]'
    #ranking_value_xpath = 'td[@align="center"]'
    ranking_value_xpath = 'td'
    university_name_xpath = 'td[@class="University"]'
    country_xpath = 'td/a[@title]'
    description = {'table_row_xpath' : table_row_xpath, 'ranking_value_xpath' : ranking_value_xpath, 'university_name_xpath' : university_name_xpath, 'country_xpath' : country_xpath}
    ranktable = list()
    absolute_ranking = 1
    for i in range(1, 7):
        path_string = 'NTU/NTURanking-2015-' + str(i) + '.html'
        # print path_string
        html = get_saved_html(path_string)
        ranktable_next_part, absolute_ranking = extract_data(html, description, absolute_ranking)
        #ranktable = ranktable + extract_data(html, description)
        ranktable = ranktable + ranktable_next_part
    print 'Ranktable extracted'
    print 'len(ranktable): ', len(ranktable)

    for rank_record in ranktable:
        print rank_record
