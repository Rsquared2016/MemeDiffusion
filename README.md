# MemeDiffusion
Analyzing Meme Diffusion on Twitter

Idea is to build a system such as this: 
http://www.nature.com/srep/2013/130828/srep02522/full/srep02522.html

In short: 

Sample all public tweets
Get the users tweeting in English
Construct an undirected, unweighted network based on reciprocal following relationships between 
randomly selected users (as bi-directional links reflect more stable and reliable social connections). 

Apply Infomap, an established algorithm to identify the community structure. 

And see how the memes are spreading for different hashtags.



