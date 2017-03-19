# Animeland.tv scraper

# TODO: Find a way to save files with their episode names when fetching Google cloud download URLs

import re
import json

import cfscrape
import demjson

from bs4 import BeautifulSoup as bs

QUALITY = ["360p", "720p"][0]   # Select quality
START_EPISODE = 1  # Episode number to start fetching from
END_EPISODE = 24  # Episode number to end fetching at

website_base_url = "http://www.animeland.tv/"
page_url = "http://www3.animeland.tv/dub/honey-and-clover"  # Replace with the URL to the page of the anime

print("Attempting to fetch episode download URLs from " + page_url, end="\n\n")

scraper = cfscrape.create_scraper()
source = scraper.get(page_url).content
soup = bs(source, "html.parser")

episodes_dict = {}
repisodes_dict = {}
webpages = []

# Fetch the list of episodes
for script in soup.find_all("script"):
    match = re.search(r'\$\("#load"\)\.load\(\'(.+)\'\)', str(script))
    if match:
        soup = bs(scraper.get(website_base_url + match.group(1)[1:]).content, "html.parser")
        for a in soup.find_all("a", {"class": "play"}):
            episodes_dict[a.getText()] = website_base_url + a["href"][1:]

for i in range(START_EPISODE, END_EPISODE + 1):
    try:
        webpages.append(episodes_dict["Episode " + str(i)])
    except:
        print("No Episode " + str(i))

# Reverse episodes_dict
for key in episodes_dict.keys():
    repisodes_dict[episodes_dict[key]] = key

downloads = []
failed_episodes = []
hash_map = {}

for url in webpages:
    episode = repisodes_dict[url]
    try:
        source = scraper.get(url).content
        soup = bs(source, "html.parser")
        iframe = soup.find("iframe", {"id": "video"})
        vid_url = website_base_url + iframe["src"][1:]
        iframe_response = scraper.get(vid_url)
        iframe_source = iframe_response.content
        iframe_soup = bs(iframe_source, "html.parser")
        failed = False
        # The website has 2 kinds of DOM structures for their videos
        try:
            # Method 1
            video = iframe_soup.find("video", {"id": "my-video"})
            sources = video.find_all("source")
            method = 1
        except:
            try:
                # Method 2
                parent_div = iframe_soup.find("div", {"id": "videop"})
                script = str(parent_div.script).replace("\n", "")
                json_string = "{" + re.search(r"\bsources:.*\]", script).group(0) + "}"
                sources = demjson.decode(json_string)
                sources = sources["sources"]
                method = 2
            except:
                print("Failed to get " + episode)
                failed = True
        if not failed:
            for src in sources:
                if src["label"] == QUALITY:
                    if method == 1:
                        download_url = src["src"]
                    else:
                        download_url = src["file"]
                    downloads.append(download_url)
                    print(episode + ":", download_url, end="\n\n")
                    hash_map[download_url] = episode
    except:
        failed = True

    if failed:
        failed_episodes.append(episode)

with open("hash_map.json", "w") as f:
    f.write(json.dumps(hash_map, indent=4, separators=(',', ': ')))

print("Writing download URLs to file")

with open("download_list.txt", "w") as f:
    for url in downloads:
        f.write(url + "\n")

with open("failed.txt", "w") as f:
    for ep in failed_episodes:
        f.write(ep + "\n")
