import glob
import os
import json
import sys
from collections import defaultdict
 
users = defaultdict(lambda: { 'followers': 0 })
 

def process_follower_list(screen_name, edges=[], depth=0, max_depth=2):
    f = os.path.join('following', screen_name + '.csv')
 
    if not os.path.exists(f):
        print([f])
        return edges
 
    file_handle = open(f, encoding='utf8')
    followers = [line.strip().split(',') for line in file_handle]
    file_handle.close()
     
    for follower_data in followers:
        if len(follower_data) < 2:
            continue
 
        screen_name_2 = follower_data[1]
 
        # use the number of followers for screen_name as the weight
        weight = users[screen_name]['followers']
 
        edges.append([screen_name, screen_name_2, weight])
        print([screen_name, screen_name_2, weight])
 
        if depth+1 < max_depth:
            process_follower_list(screen_name_2, edges, depth+1, max_depth)
            print([screen_name_2])
        
    return edges
    
# Initialize the above variable users with data from the json file 
for f in glob.glob('twitter-users/*.json'):
    file_handle = open(f)
    data = json.load(file_handle)
    file_handle.close()
    screen_name = data['screen_name']
    print(screen_name)
    users[screen_name] = { 'followers': data['followers_count'] }
    print(users[screen_name]['followers'])
    edges = process_follower_list(screen_name, max_depth=3)
 
SEED = sys.argv[1]
 
with open('Data/twitter_network.csv', 'w', encoding='utf8') as outf:
    edge_exists = {}
    for edge in edges:
        key = ','.join([str(x) for x in edge])
        if not(key in edge_exists):
            outf.write('%s,%s,%d\n' % (edge[0], edge[1], edge[2]))
            edge_exists[key] = True