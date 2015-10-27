# -*- coding: utf8 -*- 
from lxml import etree
from StringIO import StringIO
from copy import deepcopy
import os
import glob
import requests
import pickle
import codecs
import difflib
import sys


#sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

download_dir = 'download'
#years_list = ['2008', '2009', '2010', '2011', '2012', '2013']
#years_list = ['2011']
years_list = ['2013']
#years_list = ['2012']
#years_list = ['2010']

class CSV:
    def __init__(self, delimiter=' ', header=list(), fileobj=None):
        self.delimiter = delimiter
        self.header = header
        self.fileobj = fileobj
        self.rowlen = len(header)
        if self.header != []:
            self.writerow(header)

    def __writerow__(self, row):
        for column_idx in range(self.rowlen - 1):
            self.fileobj.write(row[column_idx])
            self.fileobj.write(self.delimiter)
        self.fileobj.write(row[self.rowlen - 1])
        self.fileobj.write('\n')

    def writerow(self, row=list()):
        if row != []:
            if self.rowlen == 0:
                self.rowlen = len(row)
            if len(row) == self.rowlen:
                self.__writerow__(row)
            else:
                print 'Length of the current row not equal standart len of row of this table'

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

def extract_data_arwu(html_lst, description):
    trxpath = description['rank_table_xpath']
    rankxpath = description['rank_value_xpath']
    namexpath = description['university_name_xpath']
    print namexpath, '\n'*4
    name_contain_attrib = description['university_name_tag_attrib']
    
    parser = etree.HTMLParser()
    rownum = 1
    ranktable = []
    for html in html_lst:
        tree = etree.parse(StringIO(html), parser)
        for row in tree.xpath(trxpath):
            university_info = {}
            namelist = row.xpath(namexpath)
            if namelist != []:
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

def get_html(url_lst=[], headers={'User-Agent' : 'requests'}, post_data={}):
    html_lst = []
    for url in url_lst:
        req = None
        try: 
            if post_data == {}:
                req = requests.get(url, headers=headers)
            else:
                req = requests.post(url, headers=headers, data=post_data)
        except requests.exceptions.RequestException as e:
            print e
        if req != None:
            html_lst.append(req.text)
        else:
            html_lst.append(None)
    return html_lst

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

def save_ranktables(ranktables, filename):
    out = open(filename, 'w')
    pickle.dump(ranktables, out)
    out.close()

def get_saved_ranktables(filename):
    ranktables = None
    if os.stat(filename)[6] > 0:
        finput = open(filename, 'r')
        ranktables = pickle.load(finput)
        finput.close()
    return ranktables

def save_aggregate(aggregate, filename):
    out = open(filename, 'w')
    pickle.dump(aggregate, out)
    out.close()

def get_saved_aggregate(filename):
    aggregate = None
    if os.stat(filename)[6] > 0:
        finput = open(filename, 'r')
        aggregate = pickle.load(finput)
        finput.close()
    return aggregate 

def year_raiting_request_build_rules():
    pass

def year_span_download(raiting_site_procesing_info, year_span):
    pass


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


def the_url_list_generator(retrieve_params, year):
    url_list = list()
    year_url_part = retrieve_params['year_part_generator'](year)
    for page in retrieve_params['pages_list']:
        url_list.append(retrieve_params['base_url'] + year_url_part + retrieve_params['constant_part'] + page)
    return url_list

base_sources_description['the']['retrieve_params'] = {
        'url_list' : [],
        'url_list_generator' : the_url_list_generator,
        'year_part_generator' : lambda year: str(year) + '-' + str(year - 2000 + 1),
        'base_url' : 'http://www.timeshighereducation.co.uk/world-university-rankings/',
        'constant_part' : '/world-ranking/range/',
        'query_part' : None,
        'pages_list' : ['001-200', '201-225', '226-250', '251-275', '276-300', '301-350', '351-400'],
        'extra_headers' : {},
        'post_data' : {}
        }
base_sources_description['the']['parse_params'] = {
        'rank_table_xpath' : '//table[@class="ranking main ind-OS overall"]/tbody/tr',
        'rank_value_xpath' : 'td[@class="rank"]/strong',
        'university_name_xpath' : 'td[@class="uni"]/a',
        'university_name_tag_attrib' : None,
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

def leiden_url_list_generator(retrieve_params, year):
    return [retrieve_params['base_url']]
base_sources_description['leiden']['retrieve_params'] = {
        'url_list' : [],
        'url_list_generator' : leiden_url_list_generator,
        'year_part_generator' : None,
        #'base_url' : 'http://www.leidenranking.com/ranking',
        'base_url' : 'http://www.leidenranking.com/Ranking/Ranking',
        'constant_part' : None,
        'query_part' : None,
        'pages_list' : [],
        'extra_headers' : {
            'Accept-Language' : 'ru-ru,ru;q=0.7,uk;q=0.3',
            'Accept-Encoding' : 'gzip, deflate',
            'Proxy-Connection' : 'keep-alive',
            'Content-Type' : 'application/x-www-form-urlencoded; charset=UTF-8',
            'X-Requested-With' : 'XMLHttpRequest',
            'Referer' : 'http://www.leidenranking.com/ranking',
            },
        'post_data' : {
            'field_id' :  '1',
            'continent_code' : '',
            'country_code' : '',
            'performance_dimension' :  'false',
            'ranking_indicator' : 'pp_top',
            'stability_interval' : 'true',
            'size_independent' : 'true',
            'fractional_counting' : 'true',
            'core_pub_only' : 'true',
            'number_of_publications' : '1'
            }
        }
base_sources_description['leiden']['parse_params'] = {
        'rank_table_xpath' : '//table[@class="pagedtable ranking"]/tbody/tr',
        'rank_value_xpath' : 'td[@class="rank"]',
        'university_name_xpath' : 'td[@class="university"]',
        'university_name_tag_attrib' : 'data-tooltip',
        }

def arwu_url_list_generator(retrieve_params, year):
    return [retrieve_params['base_url'] + retrieve_params['year_part_generator'](year) + retrieve_params['constant_part']]
base_sources_description['arwu']['retrieve_params'] = {
        'url_list' : [],
        'url_list_generator' : arwu_url_list_generator,
        'year_part_generator' : lambda(year): 'ARWU' + str(year),
        'base_url' : 'http://www.shanghairanking.com/',
        'constant_part' : '.html',
        'query_part' : None,
        'pages_list' : [],
        'extra_headers' : {},
        'post_data' : {}
        }
base_sources_description['arwu']['parse_params'] = {
        'rank_table_xpath' : '//table[@id="UniversityRanking"]/tr',
        'rank_value_xpath' : 'td[@class="ranking"]',
        'university_name_xpath' : 'td[@class="rankingname"]/a[@target="_blank"]/div',
        'university_name_tag_attrib' : None,
        }

def webometrics_url_list_generator(retrieve_params, year):
    base_url = retrieve_params['base_url']
    url_list = [base_url]
    query_part = '?' + retrieve_params['query_part']
    for page in retrieve_params['pages_list']:
        url_list.append(base_url + query_part + page)
    return url_list

base_sources_description['webometrics']['retrieve_params'] = {
        'url_list' : [],
        'url_list_generator' : webometrics_url_list_generator,
        'year_part_generator' : None,
        'base_url' : 'http://www.webometrics.info/en/world',
        'constant_part' : None,
        'query_part' : 'page=',
        'pages_list' : ['1', '2', '3', '4'],
        'extra_headers' : {},
        'post_data' : {}
        }
base_sources_description['webometrics']['parse_params'] = {
        'rank_table_xpath' : '//div[@class="content"]/table[@class="sticky-enabled"]/tbody/tr',
        'rank_value_xpath' : 'td/center',
        'university_name_xpath' : 'td/a[@target="_blank"]',
        'university_name_tag_attrib' : None,
        }

def urap_url_list_generator(retrieve_params, year):
    url_list = list()
    base_url = retrieve_params['base_url']
    year_part = retrieve_params['year_part_generator'](year)
    constant_part = retrieve_params['constant_part']
    query_part = '?' + retrieve_params['query_part']
    for page in retrieve_params['pages_list']:
        url_list.append(base_url + year_part + constant_part + query_part + page)
    return url_list
base_sources_description['urap']['retrieve_params'] = {
        'url_list' : [],
        'url_list_generator' : urap_url_list_generator,
        'year_part_generator' : lambda(year): str(year),
        'base_url' : 'http://www.urapcenter.org/',
        'constant_part' : '/world.php',
        'query_part' : 'q=',
        'pages_list' : ['MS0yNTA=', 'MjUxLTUwMA==', 'NTAxLTc1MA==', 'NzUxLTEwMDA=', 'MTAwMS0xMjUw', 'MTI1MS0xNTAw', 'MTUwMS0xNzUw', 'MTc1MS0yMDAw'],
        'extra_headers' : {},
        'post_data' : {}
        }
base_sources_description['urap']['parse_params'] = {
        'rank_table_xpath' : '//table[@id="rankinglist"]/tr',
        'rank_value_xpath' : 'td[@style="text-align:center"]',
        'university_name_xpath' : 'td/a',
        'university_name_tag_attrib' : None,
        }

def create_dirs(path):
    if not os.path.exists(path):
        try:
            os.makedirs(path)
        except OSError as e:
            print 'Error: ', e

def download(download_dir, raiting_name, raiting_retrieve_params, user_agent_header):
    html_file_num = 0
    for url in raiting_retrieve_params['url_list']:
        html_file_name = raiting_name + str(html_file_num) + '.html'
        html_file_path = os.path.join(download_dir, html_file_name)
        if os.path.exists(html_file_path):
            print 'File %s already exists' % html_file_path
        else:
            print 'File %s will be downloaded' % html_file_path
            headers = dict()
            headers.update(user_agent_header)
            headers.update(raiting_retrieve_params['extra_headers'])
            html = get_html(url=url, headers=headers, post_data=raiting_retrieve_params['post_data'])
            if html != None:
                save_html(html, html_file_path)
            else:
                print 'html stream is None!!!'
        html_file_num = html_file_num + 1



def retrieve_raitings_raw_data(raitings_source_description, year_list, user_agent_header):
    last_year = year_list[-1::][0]
    for year in year_list:
        print '_' * 20, ' ', year, ' ', '_' * 20
        print
        for raiting_name in raitings_source_description.keys():
            raiting_source_description = raitings_source_description[raiting_name]
            print '_' * 20, ' ', raiting_name, ' ', '_' * 20
            raiting_retrieve_params = raiting_source_description['retrieve_params']
            allowed_years = raiting_source_description['allowed_years']
            raiting_data_download_dir = os.path.join(download_dir, str(year), raiting_name)
            raiting_url_list = raiting_retrieve_params['url_list_generator'](raiting_retrieve_params, year)
            raiting_retrieve_params['url_list'] = raiting_url_list
            for url in raiting_url_list:
                print url
            if (allowed_years != [] and year in allowed_years) or year == last_year:
                create_dirs(raiting_data_download_dir)
                download(raiting_data_download_dir, raiting_name, raiting_retrieve_params, user_agent_header)
            else:
                print 'Nothing download for this year'
        print '\n' * 2


if __name__ == "__main__":
    
    user_agent_header = {'User-Agent': 'Mozilla/5.0 (X11; Linux i686; rv:10.0.7) Gecko/20100101 Firefox/10.0.7 Iceweasel/10.0.7'}

    rank_name_lst = ['the', 'qs', 'leiden', 'arwu', 'webometrics', 'urap']

    the_base_url = 'http://www.timeshighereducation.co.uk/world-university-rankings/2012-13/world-ranking/range/'
    the_url_list = [the_base_url + '001-200']
    the_url_list.append(the_base_url + '201-225')
    the_url_list.append(the_base_url + '226-250')
    the_url_list.append(the_base_url + '251-275')
    the_url_list.append(the_base_url + '276-300')
    the_url_list.append(the_base_url + '301-350')
    the_url_list.append(the_base_url + '351-400')


    #qs_url_list = ['http://www.topuniversities.com/university-rankings/world-university-rankings/2012']
    qs_url_list = ['http://www.topuniversities.com/university-rankings/world-university-rankings/2013']

    leiden_url_list = ['http://www.leidenranking.com/Ranking/Ranking']
    leiden_extra_headers = {
            'Accept-Language' : 'ru-ru,ru;q=0.7,uk;q=0.3',
            'Accept-Encoding' : 'gzip, deflate',
            'Proxy-Connection' : 'keep-alive',
            'Content-Type' : 'application/x-www-form-urlencoded; charset=UTF-8',
            'X-Requested-With' : 'XMLHttpRequest',
            'Referer' : 'http://www.leidenranking.com/ranking',
            }
    leiden_post_data = {
            'field_id' :  '1',
            'continent_code' : '',
            'country_code' : '',
            'performance_dimension' :  'false',
            'ranking_indicator' : 'pp_top',
            'stability_interval' : 'true',
            'size_independent' : 'true',
            'fractional_counting' : 'true',
            'core_pub_only' : 'true',
            'number_of_publications' : '1'
            }

    arwu_url_list = ['http://www.shanghairanking.com/ARWU2012.html']

    webometrics_base_url = 'http://www.webometrics.info/en/world'
    webometrics_url_list = [webometrics_base_url]
    webometrics_url_list.append(webometrics_base_url + '?page=1')
    webometrics_url_list.append(webometrics_base_url + '?page=2')
    webometrics_url_list.append(webometrics_base_url + '?page=3')
    webometrics_url_list.append(webometrics_base_url + '?page=4')

    urap_base_url = 'http://www.urapcenter.org/2012/world.php'
    urap_url_list = [urap_base_url + '?q=MS0yNTA=']
    urap_url_list.append(urap_base_url + '?q=MjUxLTUwMA==')

    rank_data_sources_description = []

    # THE html data fragment
    # <td class="rank"><strong>1</strong></td>
    # <td class="uni"><a href="/world-university-rankings/2012-13/world-ranking/institution/california-institute-of-technology" title="California Institute of Technology">California Institute of Technology</a></td>
    # <td class="region-title">United States</td>
    rank_data_sources_description.append(
            {
                'name' : 'the',
                'url_list' : the_url_list,
                'rank_table_xpath' : '//table[@class="ranking main ind-OS overall"]/tbody/tr',
                'rank_value_xpath' : 'td[@class="rank"]/strong',
                'university_name_xpath' : 'td[@class="uni"]/a',
                'university_name_tag_attrib' : None,
                'extra_headers' : {},
                'post_data' : {}
                })
    rank_data_sources_description.append(
            {
                'name' : 'qs',
                'url_list' : qs_url_list,
                'rank_table_xpath' : '//table[@class="views-table cols-18"]/tbody/tr',
                #'rank_table_xpath' : '//table[@id="ranking-table"]/tbody/tr',
                'rank_value_xpath' : 'td',
                'university_name_xpath' : 'td/div/a[@class="bttitle"]',
                #'university_name_xpath' : 'td/div/div/span/a[@target="_blank"]',
                'university_name_tag_attrib' : None,
                'extra_headers' : {},
                'post_data' : {}
                })
    # Leiden html data fragment
    # <td class="rank">1</td>
    # <td class="university" id="1188" data-tooltip="Massachusetts Institute of Technology">MIT</td>
    # <td class='country'><img src="/content/images/flags/US.png" data-tooltip="United States" alt="United States"/></td>
    rank_data_sources_description.append(
            {
                'name' : 'leiden',
                'url_list' : leiden_url_list,
                'rank_table_xpath' : '//table[@class="pagedtable ranking"]/tbody/tr',
                'rank_value_xpath' : 'td[@class="rank"]',
                'university_name_xpath' : 'td[@class="university"]',
                'university_name_tag_attrib' : 'data-tooltip',
                'extra_headers' : leiden_extra_headers,
                'post_data' : leiden_post_data
                })

    # ARWU html data fragment
    # <td class="rankingname"><a target="_blank"href="http://www.shanghairanking.com/Institution.jsp?param=Harvard University"><div align="left">Harvard University</div></a></td>
    # <td><a target="_blank" href="Country2012Main.jsp?param=United States" title="View universities in United States."><div align="center"><img src=flag/UnitedStates.png style="border: solid 1px #B7A971"></div></a></td>
    rank_data_sources_description.append(
            {
                'name' : 'arwu',
                'url_list' : arwu_url_list,
                'rank_table_xpath' : '//table[@id="UniversityRanking"]/tr',
                'rank_value_xpath' : 'td[@class="ranking"]',
                #'university_name_xpath' : 'td[@class="rankingname"]/a[@target="_blank"]/div',
                'university_name_xpath' : 'td/a[@target="_blank"]/div',
                #'university_name_xpath' : 'td/a[@target="_blank"]',
                'university_name_tag_attrib' : None,
                'extra_headers' : {},
                'post_data' : {}
                })

    rank_data_sources_description.append(
            {
                'name' : 'webometrics',
                'url_list' : webometrics_url_list,
                'rank_table_xpath' : '//div[@class="content"]/table[@class="sticky-enabled"]/tbody/tr',
                'rank_value_xpath' : 'td/center',
                'university_name_xpath' : 'td/a[@target="_blank"]',
                'university_name_tag_attrib' : None,
                'extra_headers' : {},
                'post_data' : {}
                })

    rank_data_sources_description.append(
            {
                'name' : 'urap',
                'url_list' : urap_url_list,
                'rank_table_xpath' : '//table[@id="rankinglist"]/tr',
                'rank_value_xpath' : 'td[@style="text-align:center"]',
                'university_name_xpath' : 'td/a',
                'university_name_tag_attrib' : None,
                'extra_headers' : {},
                'post_data' : {}
                })


    #retrieve_raitings_raw_data(base_sources_description, [2008, 2009, 2010, 2011, 2012], user_agent_header)
    #retrieve_raitings_raw_data(base_sources_description, [2013], user_agent_header)
    print 'current_dir: ', os.path.dirname(__file__)
    print 'current_dir: ', os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    print '__file__: ',  __file__

    extract_data = extract_data_arwu





    for year in years_list:
        print 'Year: ', year
        
        '''
        ranktables = {}
        for description in rank_data_sources_description:
            headers = {}
            headers.update(user_agent_header)
            headers.update(description['extra_headers'])
            html_lst = get_html(url_lst=description['url_list'], headers=headers, post_data=description['post_data'])
            #i = 0
            #for html in html_lst:
            #    save_html(html, description['name'] + str(i) + '.html')
            #    i = i + 1
            
            print description['name']
            
            list_saved_html_files = glob.glob(download_dir + '/' + year + '/' + description['name'] + '/' + '%s*.html' % description['name'])
            print list_saved_html_files
            saved_html_lst = [get_saved_html(html_name) for html_name in sorted(list_saved_html_files)]
            print 'Length saved_html_lst: ', len(saved_html_lst)

            #ranktables[description['name']] = extract_data(html_lst, description)
            ranktables[description['name']] = extract_data(saved_html_lst, description)

            print ranktables[description['name']]
        '''
    
        year_ranktables_file = 'ranktables' + year

        ## save_ranktables(ranktables, 'ranktables' + year)
        #save_ranktables(ranktables, year_ranktables_file)

        ## ranktables = get_saved_ranktables('ranktables')
        ranktables = get_saved_ranktables(year_ranktables_file)

        for key, table in ranktables.items():
            print key, table[:3]


       

        '''
        union_university_ranks = union_ranks(ranktables)

        union_university_ranks = aggregate_rank(union_university_ranks)
        grouped_by_rank_dict = group_by_aggregate_rank(union_university_ranks)
        grouped_by_rank_dict = reranked(grouped_by_rank_dict)
        
        ## aggregate_rank_csv_file = codecs.open('aggregaterank.csv', 'w', encoding='utf-8')
        aggregate_rank_csv_file = codecs.open('aggregaterank_' + year + '.csv', 'w', encoding='utf-8')
        ## detailed_aggregate_rank_csv_file = codecs.open('aggregaterank_detailed.csv', 'w', encoding='utf-8')
        detailed_aggregate_rank_csv_file = codecs.open('aggregaterank_detailed_' + year + '.csv', 'w', encoding='utf-8')
        aggregate_rank_csv = CSV(delimiter=';', header=['New rank', 'Universities', 'Sum of ranks'], fileobj=aggregate_rank_csv_file)
        detailed_aggregate_rank_csv = CSV(delimiter=';', header=['New rank', 'Universities', 'THE', 'QS', 'Leiden', 'ARWU', 'Webometrics', 'URAP', 'Sum of ranks'], fileobj=detailed_aggregate_rank_csv_file)
        for rank_value in sorted(grouped_by_rank_dict.keys()):
            rank_record = grouped_by_rank_dict[rank_value]
            #unversities_list = rank_record['university_list']
            final_rank = rank_record['final_rank']
            university_list = rank_record['university_list']
            unames = str()
            for university in university_list:
                ranks = university['ranks']
                uname = university['uname']
                detailed_aggregate_rank_csv.writerow([str(final_rank), uname, str(ranks['the']), str(ranks['qs']), str(ranks['leiden']), str(ranks['arwu']), str(ranks['webometrics']), str(ranks['urap']),  str(rank_value)])
                if unames == '':
                    unames = unames + uname
                else:
                    unames = unames + ', ' + uname
            aggregate_rank_csv.writerow([str(final_rank), unames, str(rank_value)])
        aggregate_rank_csv_file.close()
        detailed_aggregate_rank_csv_file.close()
        '''
