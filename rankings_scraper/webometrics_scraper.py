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

def get_html(url, headers={'User-Agent' : 'requests'}, post_data={}, exceptions_log_file=None):
    req = None
    html = None
    #cert = '/etc/ssl/certs/Certum_Trusted_Network_CA.pem'
    try: 
        if post_data == {}:
            #req = requests.get(url, headers=headers, verify=cert)
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

def download(download_dir, ranking_name, ranking_retrieve_params, user_agent_header):
    html_file_num = 0
    for url in ranking_retrieve_params['url_list']:
        html_file_name = ranking_name + str(html_file_num) + '.html'
        html_file_path = os.path.join(download_dir, html_file_name)
        if os.path.exists(html_file_path):
            print 'File %s already exists' % html_file_path
        else:
            print 'File %s will be downloaded' % html_file_path
            headers = dict()
            headers.update(user_agent_header)
            html = get_html(url=url, headers=headers, post_data=ranking_retrieve_params['post_data'])
            if html != None:
                save_html(html, html_file_path)
            else:
                print 'html stream is None!!!'
        html_file_num = html_file_num + 1

if __name__ == "__main__":
    
    user_agent_header = {'Mozilla/5.0 (X11; Linux x86_64; rv:31.0) Gecko/20100101 Firefox/31.0 Iceweasel/31.1.0'}

    #url = 'https://www.timeshighereducation.com/world-university-rankings/2015/world-ranking#!/page/0/length/-1'
    #url = 'http://www.webometrics.info/en/world'
    url = 'http://www.webometrics.info/en/world?page=1'

    #headers = {'User-Agent' : user_agent_header}
    #html = get_html(url, headers)
    #save_html(html, 'Webometrics_by_Requests_page_1.html')
    url_list = ['http://www.webometrics.info/en/world']
    url_list_continue = ['http://www.webometrics.info/en/world?page=' + str(i) for i in range(1, 121)]
    #print url_list_continue
    ranking_retrieve_params = {'url_list' : url_list, 'post_data' : {}}
    download('WebometricsDownloadDir', 'Webometrics', ranking_retrieve_params, user_agent_header)
