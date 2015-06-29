import csv
import sys
import itertools
import glob
import os
from Extract_followers import extract

enc = lambda x: x.encode('utf-8', errors='ignore')

filelist = glob.glob("following\\*.*")
for f in filelist:
    os.remove(f)
    
filelist = glob.glob("twitter-users\\*.*")
for f in filelist:
    os.remove(f)

handle = 'A' 

with open('Data\\JSON_OUT.csv', encoding='utf8') as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',')
    for row in readCSV:
        try:
            print('Extracting friend list for: ',row[2])
            handle = row[2]
            # Call extract function to extract the 
            extract(handle, 1)
            sleep(60)
        except: 
            pass


