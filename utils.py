#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#Author: Michael Staehli

"""
Program to implement commands for a Twitter movie-bot.
"""

import pandas as pd
import re
import typing
from thefuzz import process
import tmdbsimple as tmdb
import config
import random

#3. Recommend a movie given a genre (on command).

#4. Recommend a similar movie, given a title (on command).

#5. Post a robot movie trivia (automatically/on command).

#7. Movie quotes: English or Spanish? (on command).

#8. Post quotes from podcasts (automatically).

#9. Train text generation on quemese account.

#10. Automatically post a tweet, when a new podcast is uploaded.

class BotActions(object):
    """
    Class that defines actions for a twitter bot.
    """
    def __init__(self, command: str = ""):

        self._commands = ["!help", "!search", "!pod", "!movie"]
        self._command = command.split(" ")[0]
        self._input = ""
        try:
            self._input = re.split(r"![a-z]+ ", command)[1]
        # No input passed.
        except IndexError:
            pass

    def _print_help(self) -> str:
        """
        Method to print bot commands.
        :return:
        """
        message = f"""
        Commands:\n!help: Display this message.\n
        !search: Search episode by number or title.\n
        !pod: Recommend a podcast episode.\n
        !movie: Recommend a movie.   
        """
        return message

    def _search_episode(self) -> str:
        """
        Method that searches a podcast by number or title in the episodes
        database.
        :return:
        """
        search = self._input
        df = pd.read_csv('episodios.csv')
        if search.isdigit():
            title = \
            df.loc[df['episode_number'] == search, 'title'].iloc[0]
            url = df.loc[df['episode_number'] == search, 'urls'].iloc[0]
            return f"{title}: {url}"
        else:

            # Use thefuzz library to find title with partial string.
            title = process.extractOne(search, df["title"])[0]
            url = df.loc[df['title'] == title, 'urls'].iloc[0]

            return f"{title}: {url}"

    def _get_random(self) -> str:
        """
        Retrieve a random episode from the podcast dataframe.
        :return:
        """
        df = pd.read_csv('episodios.csv')
        random_ep = df.sample(n=1)
        title = random_ep.iloc[0]["title"]
        url = random_ep.iloc[0]["urls"]

        return f"{title}: {url}"

    def _get_movie(self) -> str:
        """
        Method to recommend a random robot movie using tmdb API.
        :return:
        """

        tmdb.API_KEY = config.tmdb_key
        discover = tmdb.Discover()
        # 14544 is id for keyword 'robot'.
        rand_page = random.randrange(1, 21)
        # print(rand_page)
        results = discover.movie(with_keywords=[14544], page=rand_page)
        # print(results)
        result = random.choice(results["results"])

        return f"{result['original_title']}"

    def get_reply(self):
        """
        Method that parses command and chooses appropiate response type.
        :return:
        """
        if self._command in self._commands:
            if self._command == "!help":
                return self._print_help()
            if self._command == "!search":
                return self._search_episode()
            if self._command == "!pod":
                return self._get_random()
            if self._command == "!movie":
                return self._get_movie()
        else:
            pass

def main():
    pass
    # bot = BotActions(command="!movie")
    # reply = bot.get_reply()

if __name__ == "__main__":
    main()