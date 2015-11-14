
# coding: utf-8

def entity_name_match(first_name, second_name):
    name_match = False
    
    if (first_name.find(second_name) != -1) or (second_name.find(first_name) != -1):
        name_match = True
    else:
        print 'Name %s and name %s are different' % (first_name, second_name)
    return name_match
