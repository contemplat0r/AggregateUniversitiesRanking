import requests
from lxml import etree
from StringIO import StringIO
from copy import deepcopy
import os
import glob
#import pickle
import codecs
#import difflib
import sys

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

#def get_html(url_lst=[], headers={'User-Agent' : 'requests'}, post_data={}):
#    html_lst = []
#    for url in url_lst:
#        if post_data == {}:
#            req = requests.get(url, headers=headers)
#            html_lst.append(req.text)
#        else:
#            req = requests.post(url, headers=headers, data=post_data)
#            html_lst.append(req.text)
#    return html_lst

#def get_html(url_lst=[], headers={'User-Agent' : 'requests'}, post_data={}):
#    html_lst = []
#    for url in url_lst:
#        req = None
#        try: 
#            if post_data == {}:
#                req = requests.get(url, headers=headers)
#            else:
#                req = requests.post(url, headers=headers, data=post_data)
#        except requests.exceptions.RequestException as e:
#            print e
#        if req != None:
#            html_lst.append(req.text)
#        else:
#            html_lst.append(None)
#    return html_lst

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

def get_html(url, headers={'User-Agent' : 'requests'}, post_data={}, exceptions_log_file=None):
    req = None
    html = None
    try: 
        if post_data == {}:
            req = requests.get(url, headers=headers)
        else:
            req = requests.post(url, headers=headers, data=post_data)
    except (requests.exceptions.ConnectionError, requests.exceptions.Timeout, requests.exceptions.HTTPError, httplib.IncompleteRead, requests.exceptions.MissingSchema) as e:
        print 'get_html: ' + url + '  Exception: ' + str(e) + '\n'
        if exceptions_log_file != None:
            exceptions_log_file.write('get_html: ' + url + ' Exception: ' + str(e) + '\n')
            exceptions_log_file.flush()
    if req != None:
        html = req.text

    return html

def save_html(html, filename):
    success = True
    f = codecs.open(filename, 'w', encoding='utf-8')
    f.write(html)
    f.close()
    return success

def get_saved_html(filename):
    f = codecs.open(filename, 'r', encoding='utf-8')
    #f = open(filename, 'r')
    html = f.read()
    f.close()
    ## print html
    return html

base_sources_description = {
        'the' : {
            'name' : 'Times Higher Education World University Rankings',
            'retrieve_params' : {},
            'parse_params' : {},
            'allowed_years' : [2010, 2011, 2012]
            },
        'qs' : {
            'name' : 'QS World University Rankings',
            'retrieve_params' : {},
            'parse_params' : {},
            'allowed_years' : [2008, 2009, 2011, 2012]
            },
        'leiden' : {
            'name' : 'CWTS Leiden Ranking',
            'retrieve_params' : {},
            'parse_params' : {},
            'allowed_years' : []
            },
        'arwu' : {
            'name' : 'Academic Ranking of World Universities',
            'retrieve_params' : {},
            'parse_params' : {},
            'allowed_years' : [2008, 2009, 2010, 2011, 2012]
            },
        'webometrics' : {
            'name' : 'Ranking Web of Universities',
            'retrieve_params' : {},
            'parse_params' : {},
            'allowed_years' : []
            },
        'urap' : {
            'name' : 'University Ranking by Academic Performance',
            'retrieve_params' : {},
            'parse_params' : {},
            'allowed_years' : [2010, 2011, 2012]
            }
        }

def qs_url_list_generator(retrieve_params, year):
    return [retrieve_params['base_url'] + retrieve_params['year_part_generator'](year)]

base_sources_description['qs']['retrieve_params'] = {
        'url_list' : [],
        'url_list_generator' : qs_url_list_generator,
        'year_part_generator' : lambda(year): str(year),
        'base_url' : 'http://www.topuniversities.com/university-rankings/world-university-rankings/',
        'constant_part' : None,
        'query_part' : None,
        'pages_list' : [],
        'extra_headers' : {},
        'post_data' : {}
        }
base_sources_description['qs']['parse_params'] = {
        'rank_table_xpath' : '//table[@class="views-table cols-18"]/tbody/tr',
        'rank_value_xpath' : 'td',
        'university_name_xpath' : 'td/div/a[@class="bttitle"]',
        'university_name_tag_attrib' : None,
        }

def retrieve_raitings_raw_data(raitings_source_description, user_agent_header):
    year = 2015
    for raiting_name in raitings_source_description.keys():
        raiting_source_description = raitings_source_description[raiting_name]
        print '_' * 20, ' ', raiting_name, ' ', '_' * 20
        raiting_retrieve_params = raiting_source_description['retrieve_params']
        raiting_data_download_dir = os.path.join(download_dir, str(year), raiting_name)
        raiting_url_list = raiting_retrieve_params['url_list_generator'](raiting_retrieve_params, year)
        raiting_retrieve_params['url_list'] = raiting_url_list
        for url in raiting_url_list:
            print url

        create_dirs(raiting_data_download_dir)
        download(raiting_data_download_dir, raiting_name, raiting_retrieve_params, user_agent_header)

if __name__ == "__main__":
    
    user_agent_header = {'Mozilla/5.0 (X11; Linux x86_64; rv:31.0) Gecko/20100101 Firefox/31.0 Iceweasel/31.1.0'}

    url = 'http://nturanking.lis.ntu.edu.tw/DataPage/OverallRanking.aspx?y=2015'

    headers = {'User-Agent' : user_agent_header}
    html = get_html(url, headers)
    save_html(html, 'NTU_by_Requests.html')
