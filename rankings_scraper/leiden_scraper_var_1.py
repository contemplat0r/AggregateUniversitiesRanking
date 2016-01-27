# coding: utf-8

import requests
from copy import deepcopy
import os
import glob
import codecs
import sys
from htmlutils import *


def extract_data(html_lst, description):
    trxpath = description['rank_table_xpath']
    rankxpath = description['rank_value_xpath']
    namexpath = description['university_name_xpath']
    name_contain_attrib = description['university_name_tag_attrib']
    parser = etree.HTMLParser()
    rownum = 1
    ranktable = []
    for html in html_lst:
        tree = etree.parse(StringIO(html), parser)
        for row in tree.xpath(trxpath):
            university_info = {}
            ranklist = row.xpath(rankxpath)
            namelist = row.xpath(namexpath)
            if ranklist != [] and namelist != []:
                university_info['rank'] = rownum
                rownum = rownum + 1
                #university_info['uname'] = namelist[0].text
                if name_contain_attrib != None:
                    university_info['uname'] = namelist[0].attrib[name_contain_attrib]
                else:
                    university_info['uname'] = namelist[0].text
                university_info['uname_variants'] = get_name_variants(university_info['uname'])
                ranktable.append(university_info)
    return ranktable


#def get_html(url, headers={'User-Agent' : 'requests'}, post_data={}):
#    req = None
#    html = None
#    try: 
#        if post_data == {}:
#            req = requests.get(url, headers=headers)
#        else:
#            req = requests.post(url, headers=headers, data=post_data)
#    except requests.exceptions.RequestException as e:
#        print e
#    if req != None:
#        html = req.text
#    return html


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

    #user_agent_header = {'Mozilla/5.0 (X11; Linux x86_64; rv:31.0) Gecko/20100101 Firefox/31.0 Iceweasel/31.1.0'}
    #headers = {'User-Agent' : user_agent_header}

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
    all_same_type_nodes = get_all_same_type_nodes(content, '//td[@class="university"]')
    get_attrib = generate_attrib_getter('data-tooltip')
    result_list = node_list_processor(all_same_type_nodes, get_attrib)
    #for item in result_list:
    #    print '\n'*2, '-' * 10
    #    print item
   

    get_attrib = generate_attrib_getter('href')

    for node in all_same_type_nodes:
         university_url_part = get_attrib(get_all_same_type_subnodes(node, 'a')[0])
         url = base_url + university_url_part

         content = get_content(url, headers_layer_1)

         all_same_type_nodes = get_all_same_type_nodes(content, '//h1[@class="head1"]')
         print all_same_type_nodes[0].text


