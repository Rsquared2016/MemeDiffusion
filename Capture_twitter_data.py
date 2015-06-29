from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import tweepy
import time
from functools import partial
import struct


ckey="QIqgjITOfksfMW4lRLDacQ"
csecret="R8x0xN9iSKXGNxUtGKA2hgnlIhh5INZIOdgEfxzk"
atoken="1401204486-BeLUAuruh294KeJX8NXvdqjCeZOQcLl6HWmMlgA"
asecret="pwjiLF42TbORaXtkCS5Oc24qywOU0eFN0esVcibA"


#This is a basic listener that just prints received tweets to stdout.
class StdOutListener(StreamListener):
    def on_data(self, data):
        f = open('Data\\twitter_data.txt','a', encoding='utf-8')
        f.write(data)
        f.close()
        print('Captured ', len(data), ' bytes')
        return True

    def on_error(self, status):
        print(status)


if __name__ == "__main__":

    auth = OAuthHandler(ckey, csecret)
    
    #This handles Twitter authetification and the connection to Twitter Streaming API
    l = StdOutListener()
    auth = OAuthHandler(ckey, csecret)
    auth.set_access_token(atoken, asecret)
    stream = Stream(auth, l)
    
    # This line filters Twitter Stream to capture data
    
    stream.filter(locations=[-180,-90,180,90], languages=["en"]) # All tweets
    
    # This or previous line 
    # stream.filter(track=['#Creativity']) # Tweets based on a specific hashtag
    api = tweepy.API(auth)
    
