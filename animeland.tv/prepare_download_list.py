# Animeland.tv scraper
import re
import json

import cfscrape
import demjson

from bs4 import BeautifulSoup as bs

QUALITY = ["360p", "720p"][0]   # Select quality
NUMBER_OF_EPISODES = 24  # Replace with anime's number of episodes

website_base_url = "http://www.animeland.tv/"
base_path = "clannad-episode-{}-english-dubbed"  # Replace with the anime's base path and the episode number with {}
websites = []

scraper = cfscrape.create_scraper()

for i in range(1,NUMBER_OF_EPISODES + 1):
    websites.append(website_base_url + base_path.format(str(i)))

downloads = []
ep_number = 1
hash_map = {}

for url in websites:
    try:
        source = scraper.get(url).content
        soup = bs(source, "html.parser")
        iframe = soup.find("iframe", {"id": "video"})
        vid_url = website_base_url + iframe["src"][1:]
        iframe_response = scraper.get(vid_url)
        iframe_source = iframe_response.content
        iframe_soup = bs(iframe_source, "html.parser")
        parent_div = iframe_soup.find("div", {"id": "videop"})
        script = str(parent_div.script).replace("\n", "")
        json_string = "{" + re.search(r"\bsources:.*\]", script).group(0) + "}"
        sources = demjson.decode(json_string)
        sources = sources["sources"]

        for src in sources:
            if src["label"] == QUALITY:
                downloads.append(src["file"])
                episode = "Episode " + str(ep_number)
                download_url = src["file"]
                print(episode + ":", download_url)
                hash_map[download_url] = episode
    except:
        print("Failed to get Episode", ep_number)

    ep_number += 1

with open("hash_map.json", "w") as f:
    f.write(json.dumps(hash_map, indent=4, separators=(',', ': ')))

print("Writing download URLs to file")

with open("download_list.txt", "w") as f:
    for url in downloads:
        f.write(url + "\n")
