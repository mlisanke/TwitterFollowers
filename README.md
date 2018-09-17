# TwitterFollowers

A text utility using python-twitter library and twitter api to routinely check for unfollows and new followers.

This is an initial version with few embellishments.

You will need to install python-twitter api in your python environment

You must create environment variables for your Twitter Application API

To run it use: python TwitterFollowers.py \<checkpt\> 
where checkpt is the keyword "checkpt" which creates a pickle backup of followers to check next time

Twitter api is transaction limited so using the app multiple time may appear to delay (upto 15 minutes) waiting
for transaction limit timeout.
 
