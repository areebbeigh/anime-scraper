# anime-joy.tv scraper
import re
import json
import os

import cfscrape
import demjson

from bs4 import BeautifulSoup as bs

QUALITY = ["360p", "720p"][0]   # Select quality
START_EPISODE = 1  # Replace with the episode number to start fetching from
END_EPISODE = 24  # Replace with the episode number to stop fetching at

website_base_url = "http://anime-joy.tv/watch/"
page_url = "http://anime-joy.tv/watch/clannad"  # Replace with the URL to the anime page
webpages = []

scraper = cfscrape.create_scraper()
sp = bs(scraper.get(page_url).content, "html.parser")

episodes_dict = {}
repisodes_dict = {}

eps_div = sp.find("div", {"class": "episodes"})

for a in eps_div.find_all("a"):
    episodes_dict[re.search(r"Episode \d+", a.getText()).group()] = a["href"].strip()

for i in range(START_EPISODE, END_EPISODE + 1):
    webpages.append(episodes_dict["Episode " + str(i)])

# Reverse episodes_dict
for key in episodes_dict.keys():
    repisodes_dict[episodes_dict[key]] = key

downloads = []
failed_downloads = []
hash_map = {}

for url in webpages:
    episode = repisodes_dict[url]
    source = scraper.get(url).content
    soup = bs(source, "html.parser")
    scripts = soup.find("div", {"id": "video_container_div"}).find_all("script")
    for script in scripts:
        download_url = ""
        try:
            download_url = re.search(
            r"https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{2,256}\.[a-z]{2,6}\b([-a-zA-Z0-9@:%_\+.~#?&//=]*.mp4)",
            str(script)).group()
        except AttributeError:
            continue

        if download_url:
            print(episode + ": " + download_url)
            downloads.append(download_url)
            hash_map[download_url] = episode

with open("hash_map.json", "w") as f:
    f.write(json.dumps(hash_map, indent=4, separators=(',', ': ')))

with open("failed.txt", "w") as f:
    for ep in failed_downloads:
        f.write(ep + "\n")

print("Writing download URLs to file")

with open("download_list.txt", "w") as f:
    for url in downloads:
        f.write(url + "\n")
