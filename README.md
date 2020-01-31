# votecount-bot
discord bot to count upvotes &amp; downvote reactions

a discord bot that replicates a system similar to reddit's karma system, only with discord reactions (upvotes, downvotes, retweets).  
upvote, downvote & rt emoji ID's are defined at the start of runBot.py, as integers.


dependencies:  
discord.py #pip install discord  
Pillow #pip install Pillow  
apikeys.txt #in master directory  
adminlist.txt #in master directory (blank file)  
blacklist.txt #in master directory (blank file)  


apikeys.txt is formatted as such:  
```
lastfm=KEY_HERE
maindiscord=KEY_HERE
testdiscord=KEY_HERE
genius=KEY_HERE
```
