# Animeland.tv scraper
import re
import json

import cfscrape
import demjson

from bs4 import BeautifulSoup as bs

QUALITY = ["360p", "720p"][0]   # Select quality
NUMBER_OF_EPISODES = 24  # Replace with anime's number of episodes

website_base_url = "http://anime-joy.tv/watch/"
base_path = "clannad/{}"  # Replace with the anime's base path and the episode number with {}
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
                ep = "Episode " + str(ep_number)
                print(ep + ": " + download_url)
                downloads.append(download_url)
                hash_map[download_url] = ep
    except:
        print("Failed to get Episode " + str(ep_number))

    ep_number += 1

with open("hash_map.json", "w") as f:
    f.write(json.dumps(hash_map, indent=4, separators=(',', ': ')))

print("Writing download URLs to file")

with open("download_list.txt", "w") as f:
    for url in downloads:
        f.write(url + "\n")
