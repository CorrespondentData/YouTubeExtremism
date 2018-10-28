# -*- coding: utf-8 -*-

"""

Created on Sun Oct 28 12:58:56 2018

 

@author: daan

"""


import pandas as pd

 

##Nog joinen met channelid, channelid meenemen als nodes

comments = pd.read_csv(r'comments_right.csv', header=None)

 

del comments[2]

del comments[4]

del comments[5]

del comments[7]

del comments[8]

 

comments.columns = ['video_id','comment_id', 'username','channel_id','timestamp']

 

comments_counter = comments.groupby('username')['comment_id'].count()

 

comments_counter = pd.DataFrame(comments_counter)

 

comments_counter = comments_counter[comments_counter['comment_id'] > 15]

 

comments_counter['username']  = comments_counter.index

 

del comments_counter['comment_id']

 

comments_filtered = pd.merge(comments_counter, comments, how='left', on=['username'])

 

 

##sample vanwege memory errors

comments_filtered = comments_filtered.sample(n=200000)

 

comment_edges = pd.merge(comments_filtered,comments_filtered, how='left', on=['video_id'])

 

 

 

 

test = comment_edges.sample(n=5)

 

import networkx as nx

import community

import matplotlib as plt

G = nx.from_pandas_edgelist(comment_edges, 'username_x', 'username_y', edge_attr=None, create_using=None)

 

print nx.info(G)

 

##Delete nodes with one or less degrees

##This is done to have a lower amount of nodes (reducing visual clutter), and keep 'well networked'

##actors in the foreground

to_del = [n for n in G if G.degree(n) <= 69]

 

G.remove_nodes_from(to_del)

G.remove_nodes_from(list(nx.isolates(G)))

 

print nx.info(G)

to_del = [n for n in G if G.degree(n) <= 49]

 

G.remove_nodes_from(to_del)

print nx.info(G)

 

spring_pos = nx.spring_layout(G)

 

nx.draw_networkx(G, pos = spring_pos, with_labels = False, node_size=3)

 

communities = community.best_partition(G)

 

nx.set_node_attributes(G, communities, 'community')

 

network = nx.to_pandas_edgelist(G)

 

network_nodes = pd.DataFrame(spring_pos).transpose()

 

network_nodes['node_name'] = network_nodes.index

 

node_communities = pd.DataFrame(nx.get_node_attributes(G,'community').items())

 

node_communities.columns = ['node_name','community']

 

merged = pd.merge(network_nodes,node_communities, on=['node_name'])

 

merged.to_json('network_results.json',orient = 'records', lines = True)