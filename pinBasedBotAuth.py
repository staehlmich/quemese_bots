#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#Author: https://gist.github.com/CombustibleToast/0e175a174d3666fff0c498097f021e01
import tweepy
import config

# Instructions:
# 1. Log in to your bot's Twitter account.
# 2. Fill in the lines below for the consumer key and secret.
# 3. Run this script.
# 4. Click on the link that the script produces, then click "Authorize App" (Make sure you are logged in to your bot's Twitter account!).
# 5. Copy the code shown on the web browser and paste it into the console running this script and press enter.
# 6. The auth key and secret for your bot's account should be shown. Use them in your other Tweepy script!

# From your app settings page
CONSUMER_KEY = config.api_key
CONSUMER_SECRET = config.api_secret

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.secure = True
auth_url = auth.get_authorization_url()

print('Please authorize: ' + auth_url)

verifier = input('PIN: ').strip()

auth.get_access_token(verifier=verifier)

print("ACCESS_KEY = '{}'".format(auth.access_token))
print("ACCESS_SECRET = '{}'".format(auth.access_token_secret))