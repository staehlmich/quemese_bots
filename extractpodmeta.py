#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#Author: Michael Staehli

import requests
import pandas as pd
# from pydub import AudioSegment


class PodMetaData:
    """
    Class to retrieve metadata from a podcast using an API.
    """

    def __init__(self, url: str):
        self.url = url
        self.meta = None
        self.__fetch_meta__()
        self.all_pods = None

    def __fetch_meta__(self):
        """
        Fetch podcast metadata.
        :return:
        """
        self.meta = requests.get(self.url).json()["body"]["channels"]

    def __set_all_pods__(self):
        """
        Method to retrieve the metadata of all podcasts.
        :return:
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
                #TODO: Move this to format_pods
                # Keep only plays of counts.
                item["counts"] = item["counts"]["plays"]
                # Keep only first url.
                item["urls"] = item["urls"]["detail"]
                episodes.append(item)
            page += 1

        self.all_pods = pd.DataFrame(episodes)

    def get_all_pods(self, format=True):
        """
        Method to retrieve the metadata of all podcasts.
        :param format: If true, format dataframe.
        :return: pd.dataframe
        """
        self.__set_all_pods__()
        if format == True:
            self.__format_pods__()
        return self.all_pods

    def __format_pods__(self):
        """
        Method to format the metadata of all podcasts
        :param dataframe: Dataframe to format
        :return: Formatted dataframe
        """
        #Split title at episode number
        self.all_pods[["episode_number", "title"]] = self.all_pods["title"].str.split(r"\.", 1,expand=True)
        #Set duration by minutes.
        self.all_pods["duration"] = self.all_pods["duration"].div(60).astype(int)
        # Keep relevant columns and rearrange
        self.all_pods = self.all_pods[
            ["episode_number", "title", "description", "updated_at", "duration",
             "uploaded_at", "counts", "urls"]]

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
    df.to_csv('episodios.csv', sep=",", encoding="utf8")
    # maverick = AudioSegment.from_file("510-top-gun-maverick.mp3")
    # mav_outro = maverick[:30000]

if __name__ == "__main__":
    main()