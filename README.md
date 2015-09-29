# MemeDiffusion
Analyzing Meme Diffusion on Twitter

Idea is to build a system such as this: 
http://www.nature.com/srep/2013/130828/srep02522/full/srep02522.html

In short: 

Sample all public tweets for a period of time.
Get the users tweeting in English.
Construct an undirected, unweighted network based on reciprocal following relationships between 
randomly selected users (as bi-directional links reflect more stable and reliable social connections). 

Apply Infomap, an established algorithm to identify the community structure. 

And see how the memes are spreading for different types of hashtags such as viral memes and non-viral ones.

Execution:
------------

Once the files are downloaded into a folder, issue the following commands:
1. py Capture_twitter_data.py --> Capture Twitter stream
2. py JSON_twitter.py
3. py Read_CSV.py --> Reads data into a CSV
4. py Extract_followers.py
5. py Network_edgelist.py
6. py Visualize_net.py 



