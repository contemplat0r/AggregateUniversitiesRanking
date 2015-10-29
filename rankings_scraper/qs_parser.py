# -*- coding: utf8 -*- 
from lxml import etree
from StringIO import StringIO
from copy import deepcopy
import os
import glob
import codecs
import sys

#def extract_data(html_lst, description):
#    trxpath = description['rank_table_xpath']
#    rankxpath = description['rank_value_xpath']
#    namexpath = description['university_name_xpath']
#    name_contain_attrib = description['university_name_tag_attrib']
#    parser = etree.HTMLParser()
#    rownum = 1
#    ranktable = []
#    for html in html_lst:
#        tree = etree.parse(StringIO(html), parser)
#        for row in tree.xpath(trxpath):
#            university_info = {}
#            ranklist = row.xpath(rankxpath)
#            namelist = row.xpath(namexpath)
#            if ranklist != [] and namelist != []:
#                university_info['rank'] = rownum
#                rownum = rownum + 1
                #university_info['uname'] = namelist[0].text
#                if name_contain_attrib != None:
#                    university_info['uname'] = namelist[0].attrib[name_contain_attrib]
#                else:
#                    university_info['uname'] = namelist[0].text
#                university_info['uname_variants'] = get_name_variants(university_info['uname'])
#                ranktable.append(university_info)
#    return ranktable

#def extract_rank_table(html, row_xpath, value_xpath = '', name_xpath = '', country_xpath = ''):
#    pass

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
        ranking_as_list = row.xpath(ranking_value_xpath)
        name_as_list = row.xpath(university_name_xpath)
        country_as_list = row.xpath(country_xpath)
        print '\n', '-' * 10
        print 'Absolute ranking: ', rownum
        if ranking_as_list != []:
            ranking = ranking_as_list[0].text
            print 'Ranking: ', ranking
        if name_as_list != []:
            university_name = name_as_list[0].text
            print 'University Name: ', university_name.encode('utf-8')
        if country_as_list != []:
            country = country_as_list[0].attrib.get('alt')
            print 'Country: ', country

        print '\n', '-' * 10, '\n'

        ranktable.append({'absolute_ranking' : rownum, 'ranking' : ranking, 'university_name' : university_name, 'country' : country})

        rownum = rownum + 1

    return ranktable

if __name__ == '__main__':

    html = get_saved_html('QS-World-University-Rankings-2015_16-All.html')
    #print html
    table_row_xpath = '//tr[@style="display: table-row;"]'
    #ranking_value_xpath = 'td[@class="rank"]/div/div/span[@class="ranking"]'
    ranking_value_xpath = 'td[@class="rank"]/div/div/span[starts-with(@class, "ranking")]'
    university_name_xpath = 'td[@class="uni"]/div/div/span/a'
    country_xpath = 'td[@class="country"]/div/img'
    #table_row_xpath = 'tr'
    #table_row_xpath = '//tr'
    description = {'table_row_xpath' : table_row_xpath, 'ranking_value_xpath' : ranking_value_xpath, 'university_name_xpath' : university_name_xpath, 'country_xpath' : country_xpath}
    ranktable = extract_data(html, description)
    print 'Ranktable extracted'
    print 'len(ranktable): ', len(ranktable)

    for rank_record in ranktable:
        print rank_record
