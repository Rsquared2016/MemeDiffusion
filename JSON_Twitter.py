import json
import sys
from csv import writer

#with open(sys.argv[1], encoding='utf-8') as in_file, \
#     open(sys.argv[2], 'w', encoding='utf-8') as out_file:
 
import csv
...

in_fnam = 'Data\\JSON_OUT2.csv'
out_fnam = 'Data\\JSON_OUT.csv'
 
with open('Data\\twitter_data.txt', encoding='utf-8') as in_file, \
     open('Data\\JSON_OUT2.csv', 'w', encoding='utf-8') as out_file:
    
    csv = writer(out_file)
    
    row = ['tweet_id', 'tweet_time', 'tweet_author', 'tweet_author_id', 'tweet_language', 'tweet_geo', 'tweet_entities', 'tweet_text']
    #values = [(value.encode('utf8') if hasattr(value, 'encode') else value) for value in row]
    #values = [(value) for value in row]
    #csv.writerow(values)
    tweet_count = 0

    for line in in_file:
        tweet_count += 1
        try: 
            tweet = json.loads(line) 
        except: 
            pass

        values = []
        # Pull out various data from the tweets
        if 'id' in line:
            row = (
                tweet['id'],                    # tweet_id
                tweet['created_at'],            # tweet_time
                tweet['user']['screen_name'],   # tweet_author
                tweet['user']['id_str'],        # tweet_authod_id
                tweet['lang'],                  # tweet_language
                tweet['geo'],                   # tweet_geo
                tweet['entities'],              # tweet_entities
                tweet['text']                   # tweet_text
            
            )
            values = [(value) for value in row]
            print(values[2])
            csv.writerow(values)

import csv
...

input = open(in_fnam, encoding='utf-8')
output = open(out_fnam, 'w', encoding='utf-8')
writer = csv.writer(output)
for line in input.readlines():
    if ''.join(line.split(',')).strip() == '':
       continue
    output.write(line)
        
input.close()
output.close()

# print the name of the file and number of tweets imported
print("File Imported")
print("# Tweets Imported:", tweet_count)
print("File Exported")