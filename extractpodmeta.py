#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#Author: Michael Staehli

import requests
import pandas as pd

class PodMetaData:
    """
    Class to retrieve metadata from a podcast using an API.
    """

    def __init__(self, url: str):
        self.url = url
        self.meta = None
        self.__fetch_meta__()

    def __fetch_meta__(self):
        """
        Fetch podcast metadata.
        :return:
        """
        self.meta = requests.get(self.url).json()["body"]["channels"]

    def get_all_pods(self):
        """
        Method to return the metadata of all podcasts
        :return: Return pd.dataframe
        """
        eps_url = "https://api.audioboom.com/channels/4254821/audio_clips"
        episodes = []
        new_results = True
        page = 1
        while new_results:
            eps_api = requests.get(
                eps_url + f"?page[number]={page}&page[items]=150").json()
            new_results = eps_api.get("body")["audio_clips"]
            for item in new_results:
                episodes.append(item)
            page += 1

        return pd.DataFrame(episodes)

    def get_latest_pod(self):
        """
        Method to extract the metadata from the latest episode.
        :return:
        """
        pass

def main():
    pod_url = "https://api.audioboom.com/channels?find[title]=quemese-despues-de-escuchar"

    quemese = PodMetaData(pod_url)
    # print(quemese.meta)

    df = quemese.get_all_pods()

    # saving as tsv file
    # df.to_csv('episodios.csv', sep="\t")

if __name__ == "__main__":
    main()