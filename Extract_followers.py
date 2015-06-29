import tweepy
import time
import os
import sys
import json
import argparse
import glob
import csv

   
FOLLOWING_DIR = 'following'
MAX_FRIENDS = 20000
FRIENDS_OF_FRIENDS_LIMIT = 5000

if not os.path.exists(FOLLOWING_DIR):
    os.makedir(FOLLOWING_DIR)

enc = lambda x: x.encode('utf-8', errors='ignore')

CONSUMER_KEY="QIqgjITOfksfMW4lRLDacQ"
CONSUMER_SECRET="R8x0xN9iSKXGNxUtGKA2hgnlIhh5INZIOdgEfxzk"
ACCESS_TOKEN="1401204486-BeLUAuruh294KeJX8NXvdqjCeZOQcLl6HWmMlgA"
ACCESS_TOKEN_SECRET="pwjiLF42TbORaXtkCS5Oc24qywOU0eFN0esVcibA"

# == OAuth Authentication ==
#
# This mode of authentication is the new preferred way
# of authenticating with Twitter.
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

api = tweepy.API(auth)

def get_follower_ids(centre, max_depth=1, current_depth=0, taboo_list=[]):

    # print 'current depth: %d, max depth: %d' % (current_depth, max_depth)
    # print 'taboo list: ', ','.join([ str(i) for i in taboo_list ])

    if current_depth == max_depth:
        print('out of depth')
        return taboo_list

    if centre in taboo_list:
        # we've been here before
        print('Already been here.')
        return taboo_list
    else:
        taboo_list.append(centre)

    try:
        userfname = os.path.join('twitter-users', str(centre) + '.json')
        print(userfname)
        if not os.path.exists(userfname):
            print(('Retrieving user details for twitter id %s' % str(centre)))
            while True:
                try:
                    user = api.get_user(centre)

                    d = {'name': user.name,
                         'screen_name': user.screen_name,
                         'id': user.id,
                         'friends_count': user.friends_count,
                         'followers_count': user.followers_count,
                         'followers_ids': user.followers_ids()}

                    with open(userfname, 'w', encoding='utf8') as outf:
                        outf.write(json.dumps(d, indent=1))

                    user = d
                    break
                except tweepy.TweepError as error:
                    print((type(error)))

                    if str(error) == 'Not authorized.':
                        print('Can''t access user data - not authorized.')
                        return taboo_list

                    if str(error) == 'User has been suspended.':
                        print('User suspended.')
                        return taboo_list

                    errorObj = error[0][0]

                    print(errorObj)

                    if errorObj['message'] == 'Rate limit exceeded':
                        print('Rate limited. Sleeping for 15 minutes.')
                        time.sleep(15 * 60 + 15)
                        continue

                    return taboo_list
        else:
            user = json.loads(file(userfname).read())

        screen_name = user['screen_name']
        print(screen_name)
        fname = os.path.join(FOLLOWING_DIR, screen_name + '.csv')
        friendids = []
        fscreen_names = []
        fnames = []
        
        # only retrieve friends of TED... screen names
        if screen_name:
            if not os.path.exists(fname):
                print(('No cached data for screen name "%s"' % screen_name))
                with open(fname, 'w', encoding='utf8') as outf:
                    params = (user['name'], screen_name)
                    print(('Retrieving friends for user "%s" (%s)' % params))

                    try:
                        
                        for page in tweepy.Cursor(api.followers_ids, screen_name).pages():
                            friendids.extend(page)
                            time.sleep(65)
                                                    
                        print(len(friendids), "followers have been gathered")
                        list_size = 100
                        
                        for i in range(0, len(friendids), list_size):
                            slists = friendids[i:i+list_size]
                            screen_names = [user.screen_name for user in api.lookup_users(user_ids=slists)]
                            names = [user.name for user in api.lookup_users(user_ids=slists)]
                            fscreen_names.extend(screen_names)
                            fnames.extend(names)
                        
                        print(len(friendids), "followers have been gathered")
                        print('Followers\' names and screen names have been gathered')
                        
                    except tweepy.TweepError as e:
                        if e.reason.find('Rate limit exceeded') != -1:
                            sys.exit('ERROR: Rate limit exceeded!!')
                        else:
                            sys.exit('ERROR retrieving followers: '+ str(e.reason))
                    
                    print('STATUS: After printing followers')
                    
                    friend_count = 0
                    
                    while friend_count < len(friendids):
                        try:
                            params = (friendids[friend_count], fscreen_names[friend_count], fnames[friend_count])
                            outf.write('%s,%s,%s\n' % params)
                            friend_count += 1
                            if friend_count >= MAX_FRIENDS:
                                print(('Reached max no. of friends for "%s".' % friend.screen_name))
                                break
                        except tweepy.TweepError:
                            # hit rate limit, sleep for 15 minutes
                            print('Rate limited. Sleeping for 15 minutes.')
                            time.sleep(15 * 60 + 15)
                            continue
                        except StopIteration:
                            break
            else:
                friendids = [int(line.strip().split('\t')[0]) for line in file(fname)]
                print("ELSE HERE")

            print(('Found %d friends for %s \n' % (len(friendids), screen_name)))

            # get friends of friends
            '''cd = current_depth
            if cd+1 < max_depth:
                for fid in friendids[:FRIENDS_OF_FRIENDS_LIMIT]:
                    taboo_list = get_follower_ids(fid, max_depth=max_depth,
                        current_depth=cd+1, taboo_list=taboo_list)

            if cd+1 < max_depth and len(friendids) > FRIENDS_OF_FRIENDS_LIMIT:
                print(('Not all friends retrieved for %s.' % screen_name)) '''

    except Exception as error:
        print(('Error retrieving followers for user id: ', centre))
        print(error)

        if os.path.exists(fname):
            os.remove(fname)
            print(('Removed file "%s".' % fname))

        sys.exit(1)

    print('Before return taboo_list')
    return taboo_list

#if __name__ == '__main__':
def extract(twitter_screenname, depth):    
   
    ''' ap = argparse.ArgumentParser()
    ap.add_argument("-s", "--screen-name", required=True, help="Screen name of twitter user")
    ap.add_argument("-d", "--depth", required=True, type=int, help="How far to follow user network")
    args = vars(ap.parse_args())

    twitter_screenname = args['screen_name']
    depth = int(args['depth'])
    print(depth) '''

    if depth < 1 or depth > MAX_FRIENDS:
        print(('Depth value %d is not valid. Valid range is 1-3.' % depth))
        sys.exit('Invalid depth argument.')

    print(('Max Depth: %d' % depth))
    matches = api.lookup_users(screen_names=[twitter_screenname])

    if len(matches) == 1:
        print((get_follower_ids(matches[0].id, max_depth=depth)))
        print('After get_follower_ids')
    else:
        print(('Sorry, could not find twitter user with screen name: %s' % twitter_screenname))
        
    return
    
if __name__ == '__main__':
    
    ap = argparse.ArgumentParser()
    ap.add_argument("-s", "--screen-name", required=True, help="Screen name of twitter user")
    ap.add_argument("-d", "--depth", required=True, type=int, help="How far to follow user network")
    args = vars(ap.parse_args())   
    twitter_screenname = args['screen_name']
    depth = int(args['depth'])
    extract(twitter_screenname, depth);