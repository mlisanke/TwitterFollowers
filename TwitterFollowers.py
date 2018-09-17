import os
import time
import sys
import pickle
import twitter
from shutil import copyfile

def CheckFollowerUpdates(checkpt):	

	mcnt = 0
	tstrt = time.time()
	
	if checkpt:
		print("Starting CheckFollowerUpdates with checkpoint.")
	else:
		print("Starting CheckFollowerUpdates.")

	env = { "TWITTER_CONSUMER_KEY":0,  "TWITTER_CONSUMER_SECRET":0,  "TWITTER_ACCESS_KEY":0,  "TWITTER_ACCESS_SECRET":0 }
	for key, value in env.items():
		env[key]=os.getenv(key)

	api = twitter.Api(consumer_key=env['TWITTER_CONSUMER_KEY'], consumer_secret=env['TWITTER_CONSUMER_SECRET'],
					access_token_key=env['TWITTER_ACCESS_KEY'], access_token_secret=env['TWITTER_ACCESS_SECRET'],
					sleep_on_rate_limit=True)

	users = api.GetFriends()
	tintr = time.time()
	print("Loaded {} friends after {} seconds".format( len(users), (tintr - tstrt) ))
	mcudict = {u.id:u for u in users}

	my_followers = api.GetFollowers()
	tintr = time.time()
	print("Loaded {} current followers after {} seconds".format( len(my_followers), (tintr - tstrt) ))
	mcfdict = {u.id:u for u in my_followers}

	try:
		myp_followers = pickle.load(open("mypfollowers.p","rb"))
	except FileNotFoundError:
		myp_followers = {}
		print("No pickle file found - using a null dictionary")
	tintr = time.time()
	print("Loaded {} previous followers after {} seconds".format( len(myp_followers), (tintr - tstrt) ))
	mpfdict = {u.id:u for u in myp_followers}

	ucnt = 0    # unfollow count
	fcnt = 0    # unfollowed friend count
	ncnt = 0    # new follow count

	for pf in myp_followers:

		if pf.id not in mcfdict:
			ucnt += 1
			print(pf.id, "@{} has unfollowed me; has {} friends and {} followers.".format(pf.screen_name,pf.friends_count,pf.followers_count))

			if pf.id in mcudict:
				fcnt += 1
				print(pf.id, "... @{} was followed by me.".format(pf.screen_name))

	for cf in my_followers:

		if cf.id not in mpfdict:
			ncnt += 1
			print(cf.id, "@{} has followed me, with {} friends and {} followers.".format(cf.screen_name,cf.friends_count,cf.followers_count))
			print("... @{} was created on {} with description: {}.".format(cf.screen_name,cf.created_at,cf.description))

	if checkpt:
		dst = time.strftime("mypfollowers-%Y%m%d-%H%M%S.p")
		copyfile( 'mypfollowers.p', dst)
		pickle.dump( my_followers, open( "mypfollowers.p", "wb" ) )

	tstop = time.time()
	print("Unfollows: {} Following: {} New Follows: {} in {} seconds".format( ucnt, fcnt, ncnt, (tstop - tstrt) ))

				
if __name__ == "__main__":

	checkpt = False
	if len(sys.argv) > 1:
		if "checkpt" == sys.argv[1]:
			checkpt = True
	
	CheckFollowerUpdates(checkpt)
	