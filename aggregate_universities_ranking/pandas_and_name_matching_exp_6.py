# coding: utf-8

d = {'a' : 1}
get_ipython().magic(u'pinfo d.pop')
import pandas_and_name_matching_exp_3_clean
from pandas_and_name_matching_exp_3_clean import *
qs_df[:4]
the_df[:4]
df = DataFrame({'state' : ['A', 'B', 'C'], 'year' : [2000, 2001, 2002], 'pop' : [1.5, 1.7, 1.9]}, columns=['year', 'state', 'pop'])
qs_df[['number_in_ranking_table', 'university_name']][:4]
qs_df_short = DataFrame(qs_df[['number_in_ranking_table', 'university_name']], columns = ['rank', 'university_name'])
qs_df_short[:4]
qs_df_short = qs_df[['number_in_ranking_table', 'university_name']]
qs_df_short.index
qs_df_short._ix
qs_df.ix
qs_df.ix.name
qs_df.ix.obj
qs_df.ix.axis
qs_df_short['rank'] = 'QS'
qs_df_short = DataFrame(qs_df[['number_in_ranking_table', 'university_name']], columns = ['rank', 'university_name'])
qs_df_short = qs_df[['number_in_ranking_table', 'university_name']]
qs_df_short.index
qs_df_short.values
qs_df_short.to_dict()
qs_df_short.to_dict().keys()
qs_df_short.swapaxes().to_dict().keys()
qs_df_short.columns
qs_df_short.columns.name
qs_df_short.columns.
qs_df_short.columns.union()
qs_df_short.T
(qs_df_short.T).to_dict()
qs_short_df.rename(columns={'number_in_ranking_table' : 'rank'})
qs_short_df.head()
qs_short_df.rename(columns={'number_in_ranking_table' : 'rank'}, inplace=True)
qs_short_df.head()
qs_short_df = qs_short_df[['rank', 'university_name']]
qs_short_df.head()
qs_rank_table = {'qs' : (qs_short_df.T).to_dict().values()}
qs_rank_table
qs_rank_table.keys()
the_shor_df = the_df[['number_in_ranking_table', 'university_name']]
the_short_df.head()
the_short_df.drop('country')
the_shor_df = the_short_df[['number_in_ranking_table', 'university_name']]
the_short_df = the_short_df[['number_in_ranking_table', 'university_name']]
del the_shor_df
the_short_df.head()
the_short_df = the_short_df.rename(columns={'number_in_ranking_table : 'rank'})
the_short_df = the_short_df.rename(columns={'number_in_ranking_table' : 'rank'})
the_short_df.head()
the_rank_table = {'the' : (the_short_df.T).to_dict().values()}
the_rank_table.keys()
the_rank_table.values()
leiden_short_df = leiden_df[['number_in_ranking_table', 'university_name']]
leiden_short_df.head()
leiden_short_df = leiden_short_df.rename(columns={'number_in_ranking_table' : 'rank'})
leiden_short_df.head()
leiden_rank_table = {'leiden' : (leiden_short_df.T).to_dict().values()}
leiden_rank_table.head()
leiden_rank_table.values()
qs_exp_rank_table = {'qs' : (qs_short_df[:6].T).to_dict().values()}
qs_exp_rank_table
the_exp_rank_table = {'the' : (the_short_df[:6].T).to_dict().values()}
the_exp_rank_table
leiden_exp_rank_table = {'leiden' : (leiden_short_df[:6].T).to_dict().values()}
import name_matching
from name_matching import *
reload(name_matching)
from name_matching import *
for university in qs_exp_rank_table['qs']:
    university['university_name_variants'] = get_name_variants(university['university_name'])
    
qs_exp_rank_table
def add_name_variants(rank_table):
    for university in rank_table[rank_table.keys()[0]]:
        university['university_name_variants'] = get_name_variants(university['university_name'])
        
add_name_variants(the_exp_rank_table)
the_exp_rank_table
add_name_variants(leiden_exp_rank_table)
leiden_exp_rank_table
d1 = {'a' : 1}
d2 = {'b' : 2}
d1.update(d2)
d1
qs_exp_rank_table.update(the_exp_rank_table)
qs_exp_rank_table.update(leiden_exp_rank_table)
rank_table = qs_exp_rank_table
rank_table
union_university_ranks = union_ranks(rank_table)
reload(name_matching)
from name_matching import *
union_university_ranks = union_ranks(rank_table)
rank_table
union_university_ranks = union_ranks(rank_table)
reload(name_matching)
from name_matching import *
union_university_ranks = union_ranks(rank_table)
union_university_ranks
reload(name_matching)
from name_matching import *
union_university_ranks = union_ranks(rank_table)
reload(name_matching)
from name_matching import *
union_university_ranks = union_ranks(rank_table)
qs_exp_rank_table = {'qs' : (qs_short_df[:6].T).to_dict().values()}
reload(name_matching)
the_exp_rank_table = {'the' : (the_short_df[:6].T).to_dict().values()}
leiden_exp_rank_table = {'leiden' : (leiden_short_df[:6].T).to_dict().values()}
add_name_variants(leiden_exp_rank_table)
add_name_variants(qs_exp_rank_table)
add_name_variants(the_exp_rank_table)
leiden_exp_rank_table
from copy import deepcopy
rank_table = deepcopy(qs_exp_rank_table)
rank_table.update(deepcopy(the_exp_rank_table))
rank_table.update(deepcopy(leiden_exp_rank_table))
union_university_ranks = union_ranks(rank_table)
union_university_ranks
