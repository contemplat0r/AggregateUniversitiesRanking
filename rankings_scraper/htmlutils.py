# -*- coding: utf8 -*- 

from lxml import etree
from StringIO import StringIO
import codecs
from copy import deepcopy

parser = etree.HTMLParser()

def get_saved_content(filename):
    f = codecs.open(filename, 'r', encoding='utf-8')
    #f = open(filename, 'r')
    content = f.read()
    f.close()
    ## print html
    return content

def get_xpath_to_root(node):
    if node != None:
        xpath_to_root = get_xpath_to_root(node.getparent())
        xpath_to_root = xpath_to_root + '/' + node.tag
        if node.items() != []:
            attribs_string = '['
            for attrib, value in node.items():
                attribs_string = attribs_string + '@%s=\"%s\" ' % (attrib, value)
            xpath_to_root = xpath_to_root + attribs_string[0:len(attribs_string) - 1] + ']'
        return xpath_to_root
    else:
        return ''

def get_xpath_to_root_as_nodes_list(node):
    if node != None:
        xpath_to_root = get_xpath_to_root_as_nodes_list(node.getparent())
        xpath_to_root.append(node)
        return xpath_to_root
    else:
        return []

def get_node_attribs(node):
    return node.items()

def node_attribs_to_string(node_attribs):
    if node_attribs != []:
        attribs_string = '['
        for attrib, value in node_attribs:
            attribs_string = attribs_string + '@%s=\"%s\" ' % (attrib, value)
        return attribs_string[0:len(attribs_string) - 1] + ']'
    else:
        return ''

def convert_xpath_as_list_to_string(xpath_as_list):
    xpath_as_string = str()
    for node in xpath_as_list:
        xpath_as_string = xpath_as_string + '/' + node.tag + node_attribs_to_string(get_node_attribs(node))
    return xpath_as_string

def get_xpath_to_root_procedural(node):
    xpath_to_root_as_list = get_xpath_to_root_as_nodes_list(node)
    #print 'xpath_to_root_as_list: ', xpath_to_root_as_list
    xpath_to_root_as_string = convert_xpath_as_list_to_string(xpath_to_root_as_list)
    return xpath_to_root_as_string

def check_equality_two_nodes_tags(first_node, second_node):
    return first_node.tag == second_node.tag

def check_equality_two_nodes_attribs(first_node, second_node):
    first_node_attribs_names_list = first_node.keys()
    second_node_attribs_names_list = second_node.keys()
    if len(first_node_attribs_names_list) != len(second_node_attribs_names_list):
        return False
    else:
        if first_node_attribs_names_list == second_node_attribs_names_list:
            attrib_values_comparation_result = True
            for attrib_name in first_node_attribs_names_list:
                if first_node.get(attrib_name) != second_node.get(attrib_name):
                    attrib_values_comparation_result = False
                    break
            return attrib_values_comparation_result
        else:
            return False

def check_two_nodes_equality(first_node, second_node):
    return check_equality_two_nodes_tags(first_node, second_node) and check_equality_two_nodes_attribs(first_node, second_node)

def check_two_nodes_coincide(first_node, second_node):
    return first_node == second_node

def check_two_xpath_overlap(first_xpath_as_nodes_list, second_xpath_as_nodes_list):
    check_result = False
    last_coincide_node = None
    compare_two_current_nodes_result = True
    for first_xpath_node, second_xpath_node in zip(first_xpath_as_nodes_list, second_xpath_as_nodes_list):
        if check_two_nodes_coincide(first_xpath_node, second_xpath_node) == False:
            compare_two_current_nodes_result = False
            break
        else:
            last_coincide_node = first_xpath_node
    check_result = compare_two_current_nodes_result
    return check_result, last_equal_node

def detect_overlap_part_of_two_xpath(first_xpath_as_nodes_list, second_xpath_as_nodes_list):
    last_coincide_node = None
    overlap_part_of_two_xpath = list()
    for first_xpath_node, second_xpath_node in zip(first_xpath_as_nodes_list, second_xpath_as_nodes_list):
        if check_two_nodes_coincide(first_xpath_node, second_xpath_node) == False:
            break
        else:
            last_coincide_node = first_xpath_node
            overlap_part_of_two_xpath.append(first_xpath_node)
    return last_coincide_node, overlap_part_of_two_xpath

def check_two_xpath_coincide(first_xpath_as_nodes_list, second_xpath_as_nodes_list):
    #last_coincide_node, overlap_part_of_two_xpath = detect_overlap_part_of_two_xpath(first_xpath_as_nodes_list, second_xpath_as_nodes_list)
    if (first_xpath_as_nodes_list != []) and (second_xpath_as_nodes_list != []):
        if (first_xpath_as_nodes_list[0] == second_xpath_as_nodes_list[0]) and (first_xpath_as_nodes_list[-1] == second_xpath_as_nodes_list[-1]):
            return True
        else:
            return False
    elif (first_xpath_as_nodes_list == []) and (second_xpath_as_nodes_list == []):
        return True
    else:
        return False

def get_xpath_segment_as_nodes_list(maybe_superparent_node, node):
    if node != maybe_superparent_node or None:
        xpath_segment = get_xpath_to_root_as_nodes_list(maybe_superparent_node, node.getparent())
        if xpath_segment != None:
            xpath_segment.append(node)
        return xpath_segment
    elif node == maybe_superparent_node:
        return []
    elif node == None:
        return None
    else:
        return None

def get_all_same_type_nodes(html, node_tag_xpath):
    parser = etree.HTMLParser()
    tree = etree.parse(StringIO(html), parser)
    node_container = tree.xpath(node_tag_xpath)
    #print node_container
    #for node in node_container:
    #    print node 
    return node_container


def get_all_same_type_subnodes(node, subnode_xpath):
    return node.xpath(subnode_xpath)


def get_all_same_type_nodes_1(node_tag_xpath, html):
    parser = etree.HTMLParser()
    tree = etree.parse(StringIO(html), parser)
    node_container = tree.xpath(node_tag_xpath)
    #print node_container
    #for node in node_container:
    #    print node 
    return node_container


def a_tag_processor(a_tag):
    #return a_tag.text
    return a_tag.attrib.get('href')


def generate_attrib_getter(attrib_name):
    def attrib_getter(node):
        return node.attrib.get(attrib_name)
    return attrib_getter


def generate_nodes_getter(xpath):
    def nodes_getter(html):
        return get_all_same_type_nodes_1(xpath, html)
    return nodes_getter
        

def node_list_processor(node_list, node_processor, extraction_result_processor=None):
    result_list = list()
    for node in node_list:
        from_node_extracted = node_processor(node)
        #print from_node_extracted
        if extraction_result_processor != None:
            result_list.append(extraction_result_processor(from_node_extracted))
        else:
            result_list.append(from_node_extracted)
    return result_list

def get_root_xpathes_for_all_same_type_nodes(all_same_type_nodes_list):
    return node_list_processor(all_same_type_nodes_list, get_xpath_to_root_as_nodes_list)

def extract_different_root_xpathes_for_same_type_nodes(same_type_nodes_list):
    different_root_xpathes_for_same_type_nodes = list()
    xpathes_group_num = 0
    same_type_nodes_list_len = len(same_type_nodes_list)
    root_xpathes_for_all_same_type_nodes_list = get_root_xpathes_for_all_same_type_nodes(same_type_nodes_list)
    #for i in range(0, same_type_nodes_list_len - 1):
    #    current_xpath = root_xpathes_for_all_same_type_nodes_list[i]
    #    for j in range(i, same_type_nodes_list_len - 1):
    for xpath in root_xpathes_for_all_same_type_nodes_list:
        add_xpath_to_different_xpathes_list = True 
        for xpath_group_representative in different_root_xpathes_for_same_type_nodes:
            if check_two_xpath_coincide(xpath[0:-1], xpath_group_representative[0:-1]):
                add_xpath_to_different_xpathes_list = False
                break
        if add_xpath_to_different_xpathes_list == True:
            different_root_xpathes_for_same_type_nodes.append(xpath)
    return different_root_xpathes_for_same_type_nodes


if __name__ == '__main__':
    
    '''
    html = get_saved_content('Fundays-Second-Layer-Example.html')
    #all_same_type_nodes = get_all_same_type_tags(html, '//a')
    all_same_type_nodes = get_all_same_type_nodes(html, '//a')
    #result_list = node_list_processor(all_same_type_tags, a_tag_processor, lambda x: x)

    result_list = node_list_processor(all_same_type_nodes, get_xpath_to_root)
    for item in result_list:
        print '\n'*2, '-' * 10, '\n'
        print item

    #print '\n' * 3, '-' * 10, 'get_xpath_to_root_procedural:', '-'*10, '\n'
    #result_list = node_list_processor(all_same_type_nodes, get_xpath_to_root_procedural)
    #for item in result_list:
    #    print item
    '''

    #html = get_saved_content('leiden_curl_result_0.txt')
    #all_same_type_nodes = get_all_same_type_nodes(html, '//td[@class="university"]')
    #result_list = node_list_processor(all_same_type_nodes, get_xpath_to_root)

    html = get_saved_content('leiden_curl_result_0.txt')
    all_same_type_nodes = get_all_same_type_nodes(html, '//td[@class="university"]')
    get_attrib = generate_attrib_getter('data-tooltip')
    result_list = node_list_processor(all_same_type_nodes, get_attrib)
    for item in result_list:
        print '\n'*2, '-' * 10
        print item

