import praw
import spellcheck
from time import sleep
from collections import deque
import re

USERNAME = "username"
PASSWORD = "password"
VERSION = '1.4'
USERAGENT = "SpellCheckerBot version %s by /u/thirdegree, run by /u/PM_ME_YOUR_TITS_GIRL"%VERSION
SUBREDDITS = 'subreddits'

r = praw.Reddit(USERAGENT)
r.login(USERNAME, PASSWORD)

commonly_misspelled = file('commonly_misspelled.txt').read().split('\n')
banned_subs = file('banned_subs.txt').read().split('\n')
already_done = deque(maxlen=300)
ignored_users = file('ignored_users.txt').read().split('\n')

#checks if comment is posted in a banned subreddit
def banned(subreddit):
	if subreddit in banned_subs:
		return True
	else:
		return False

#Important codework is here and in spellcheck.py. Everything in the while loop is fluffy stuff. This is the spellchecker.
def corrector(post):
	corrected_list = []
	if not (banned(str(post.subreddit)) or (post.id in already_done) or (post.author.name in ignored_users)):
		word_list = [re.sub('[^\w\']', '', word).lower() for word in post.body.strip().split() if '/' not in word]
		print "\n\nSUBREDDIT:"
		print str(post.subreddit)+'\n'
		print "POST "+post.id+':' 
		print '"'+post.body+'"\n'
		print "CORRECTIONS:"
		for word in word_list:
			if word[:3] == ('/u/' or '/r/'):
				continue
			checked = spellcheck.correct(word)
			if not ((word in checked) or not (checked&set(commonly_misspelled))):
				print '* OR '.join(list(checked&set(commonly_misspelled)))+ '*\n'
				corrected_list.append('* OR '.join(list(checked&set(commonly_misspelled)))+'*\n\n')
	already_done.append(post.id)
	return corrected_list

#Easter eggs, manual control, and posting are in here.
running = True
while running:	
	#Checks inbox for new messages (stop checking me, easter eggs, manual control by thirdegree and pm_me_your_tits)
	inbox = r.get_unread()
	print "\n\nChecking inbox"
	for post in inbox:
		if (post.body == "Quit spellchecking me") and (post.author.name not in ignored_users):
			post.reply("I'll stop spellchecking you.")
			print "Ignoring user " + post.author.name
			already_done.append(post.id)
			ignored_users.append(post.author.name)
			with open('ignored_users.txt', 'a+') as ignored:
				ignored.write(post.author.name+'\n')
		#manual control for ignoring users
		elif ("ignore user:" in post.body.lower().strip()) and (post.author.name == 'thirdegree' or post.author.name == 'PM_ME_YOUR_TITS_GIRL'):
			users = [i.replace(',', '') for i in post.body.split()[2:] if i != 'and']
			for username in users:
				print "Ignoring user " + username
				ignored_users.append(username)
				with open('ignored_users.txt', 'a+') as ignored:
					ignored.write(username+'\n')
		#manual control for ignoring subreddits
		elif ("ignore subreddit:" in post.body.lower().strip()) and (post.author.name == 'thirdegree' or post.author.name == 'PM_ME_YOUR_TITS_GIRL'):
			subreddits = [i.replace(',', '') for i in post.body.split()[2:] if i!= 'and']
			for sub in subreddits:
				print "Ignoring subreddit "+ sub
				banned_subs.append(sub)
				with open('banned_subs.txt', 'a+') as banned:
					banned.write(sub+'\n')
		#next four are easter eggs
		elif ("are you a bot" in post.body.lower().strip()) and (post.author.name not in ignored_users):
			post.reply("Yes, I am a bot. [Here's a link to my wiki!](http://www.reddit.com/r/SpellCheckerBot/wiki/index).")
			print "I have been reminded that I am a bot."
		elif (post.body.lower().strip() == "what is the airspeed velocity of an unladen swallow?") and (post.author.name not in ignored_users):
			post.reply("African or European?")
			print "Replying to easter egg"
		elif (post.body.lower().strip() == "what is the answer to life, the universe, and everything?") and (post.author.name not in ignored_users):
			post.reply("42")
			print "Replying to easter egg"
		elif (post.body.lower().strip() == "life is like a box of chocolates. you never know what you're gonna get.") and (post.author.name not in ignored_users):
			post.reply("Me and Jenny goes togeather like peas and carrots.")
			print "Replying to easter egg"
		sleep(5)
		post.mark_as_read()
	sleep(4)
	#Gets new comments, spellchecks them, and replies if there are any corrections.
	try:
		comments = r.get_comments(SUBREDDITS)
		print "\nGetting comments"
		for post in comments:
			if '[serious]' not in post.link_title.lower():
				corrected_list = corrector(post)
				if corrected_list != []:
					post.reply(' '.join(corrected_list)+'\n_____\n\n\n[Questions?](http://www.reddit.com/r/SpellCheckerBot/wiki/index) [Suggestions? Complaints?](http://www.reddit.com/r/SpellCheckerBot)\n\nReply "Quit spellchecking me" to make me stop.')
					sleep(10)
	except praw.errors.RateLimitExceeded:
		print "Rate limit exceeded, sleeping 10 min"
		sleep(590)
	except KeyboardInterrupt:
		running = False
	except:
		print "Unknown Reddit error, sleeping 1 min"
		sleep(50)
	sleep(10)
