# Animedoor.com scraper

from urllib import request
from bs4 import BeautifulSoup as bs

import json

episode_list_url = "http://www.animedoor.com/2016/04/death-note-s01e01-37-download.html" # Replace with URL to the list of episodes

source = request.urlopen(episode_list_url)
soup = bs(source, "html.parser")
anchor_tags = soup.find_all("a", {"class": "downloadb"})

downloads = {}

for tag in anchor_tags:
    episode = tag.text
    url = tag["href"]
    print(episode + ":", url)
    downloads[url] = episode

with open("hash_map.json", "w") as f:
    f.write(json.dumps(downloads, indent=4, separators=(',', ': ')))

print("Writing download URLs")
with open("download_list.txt", "w") as f:
    for url in downloads:
        f.write(url + "\n")
