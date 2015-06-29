import networkx as net
import matplotlib.pyplot as plt
import sys
import glob
import json
 
from collections import defaultdict
import math
 
file_handle = open('Data/twitter_network.csv', encoding='utf8')
twitter_network = [line.strip().split(',') for line in file_handle]
 
'''for (twitter_user, followed_by, followers) in twitter_network:
    print(twitter_user, followed_by, followers)'''

print('Edges in the network: ', len(twitter_network))
o = net.DiGraph()
hfollowers = defaultdict(lambda: 0)
for (twitter_user, followed_by, followers) in twitter_network:
    o.add_edge(twitter_user, followed_by, followers=int(followers))
    hfollowers[twitter_user] = int(followers)
 
SEED = twitter_user
SEED2 = 'KatieSpoor' 

def trim_degrees_ted(g, degree=1, ted_degree=1):
    g2 = g.copy()
    d = net.degree(g2)
    for n in g2.nodes():
        if n == SEED: continue # don't prune the SEED node
        if d[n] <= degree and not n.lower().startswith(SEED):
            g2.remove_node(n)
        elif n.lower().startswith(SEED) and d[n] <= ted_degree:
            g2.remove_node(n)
    return g2
 
def trim_edges_ted(g, weight=1, ted_weight=10):
    g2 = net.DiGraph()
    for f, to, edata in g.edges_iter(data=True):
        if f == SEED or to == SEED: # keep edges that link to the SEED node
            g2.add_edge(f, to, edata)
        elif f.lower().startswith(SEED) or to.lower().startswith(SEED):
            if edata['followers'] >= ted_weight:
                g2.add_edge(f, to, edata)
        elif edata['followers'] >= weight:
            g2.add_edge(f, to, edata)
    return g2

''' # centre around the SEED node and set radius of graph
g = net.DiGraph(net.ego_graph(o, SEED, radius=4)) 
print('g: ', len(g))
core = g; '''

plt.figure(figsize=(18,18))
plt.axis('off')

# centre around the SEED node and set radius of graph




''' core = trim_degrees_ted(g, degree=25, ted_degree=1)
print('core after node pruning: ', len(core))
core = trim_edges_ted(core, weight=25, ted_weight=35)
print('core after edge pruning: ', len(core)) '''
         
for ff in glob.glob('twitter-users/*.json'):
    
    file_handle = open(ff)
    data = json.load(file_handle)
    file_handle.close()
    
    if SEED == data['screen_name']:
        print('Draw Graph')
        g = net.DiGraph(net.ego_graph(o, SEED, radius=4)) 
        print('g: ', len(g))
        core = g;
        pos = net.spring_layout(core) # compute layout
        # DRAW THE NODES:
        net.draw_networkx_nodes(core, pos, node_color='red')
    elif SEED2 == data['screen_name']:
        g2 = net.DiGraph(net.ego_graph(o, SEED2, radius=4)) 
        print('g: ', len(g2))
        core = g2;
        pos = net.spring_layout(core) # compute layout
        # DRAW THE NODES:
        net.draw_networkx_nodes(core, pos, node_color='green')
    else:
        continue   
    
    ''' nodeset_types = { SEED: lambda s: s.lower().startswith(SEED), 'Not ' + SEED: lambda s: not s.lower().startswith(SEED) }
 
    nodesets = defaultdict(list)
 
    for nodeset_typename, nodeset_test in iter(nodeset_types.items()):
        nodesets[nodeset_typename] = [ n for n in core.nodes_iter() if nodeset_test(n) ]
    
 
    colours = ['red','green']
    colourmap = {}
 
    # draw nodes
    i = 0
    alphas = {SEED: 0.6, 'Not ' + SEED: 0.4}
    for k in nodesets.keys():
        ns = [ math.log10(hfollowers[n]+1) * 80 for n in nodesets[k] ]
        print('NODE SIZE:', k, len(ns))
        net.draw_networkx_nodes(core, pos, nodelist=nodesets[k], node_size=ns, node_color=colours[i], alpha=alphas[k])
        colourmap[k] = colours[i]
        i += 1
    print('colourmap: ', colourmap, '\n')'''
 

    
    # draw edges
    net.draw_networkx_edges(core, pos) #, width=0.5, alpha=0.5)
 
    '''# draw labels
    alphas = { SEED: 1.0, 'Not ' + SEED: 0.5}
    for k in nodesets.keys():
        for n in nodesets[k]:
            x, y = pos[n]
            plt.text(x, y+0.02, s=n, alpha=alphas[k], horizontalalignment='center', fontsize=9)'''
        
print('Saving Image ... ')
plt.savefig('Images/twitter_net.png')
file_handle.close()

