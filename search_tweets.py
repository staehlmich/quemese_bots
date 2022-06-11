#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#Author: Michael Staehli

import tweepy
import requests
import config

def main():
    auth = tweepy.OAuthHandler(config.api_key, config.api_secret)
    auth.set_access_token(config.access_token,
                          config.access_token_secret)
    api = tweepy.API(auth)
    # status = "Bot that tweets movie quotes!"
    api.update_status(status="Testing!")

if __name__ == "__main__":
    main()