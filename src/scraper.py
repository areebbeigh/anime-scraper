import re
import os
import json
import sys

import cfscrape
import demjson
import jsbeautifier

from bs4 import BeautifulSoup as bs

WATCHANIME = "watchanime.me"
ANIMELAND = "animeland.tv"


def identify_website(url):
    watchanime = re.compile(r"^(http:\/\/|https:\/\/)*([a-z0-9][a-z0-9\-]*\.)*(watchanime)\.me(\/.*)?$")
    animeland = re.compile(r"^(http:\/\/|https:\/\/)*([a-z0-9][a-z0-9\-]*\.)*(animeland)\.tv(\/.*)?$")

    if watchanime.match(url):
        return WATCHANIME

    if animeland.match(url):
        return ANIMELAND

    return False


def _get_webpages(episodes_dict, start, end):
    webpages = []

    if start > 0 and end > 0:
        for i in range(start, end + 1):
            try:
                # Matching episodes
                for episode in episodes_dict.keys():
                    ep_index = re.search(r"Episode (\d+)", episode).group(1)
                    if i == int(ep_index):
                        webpages.append(episodes_dict["Episode " + ep_index])
            except:
                print("No Episode " + str(i))
    else:
        keys = list(episodes_dict.keys())

        if re.match(r"^Episode \d+$", keys[0]):
            keys.sort(key = lambda episode: episode.split()[1])

        for episode in keys:
            webpages.append(episodes_dict[episode])

    return webpages


def _is_episode_missing(ep):
    if ep not in [os.path.splitext(f)[0] for f in os.listdir()]:
        return True
    return False


def _scrape_episodes(url, start, end, find_missing):
    if not (url[:7] == "http://" or url[:8] == "https://"):
        url = "http://" + url

    page_url = url
    START_EPISODE = start
    END_EPISODE = end
    episodes_dict = {}
    repisodes_dict = {}
    webpages = []
    failed_episodes = []
    hash_map = {}

    scraper = cfscrape.create_scraper()

    if identify_website(url) == ANIMELAND:
        # Animeland
        QUALITY = ["360p", "480p", "720p"][0]   # Select quality
        website_base_url = "http://www.animeland.tv/"
        source = scraper.get(page_url).content
        soup = bs(source, "html.parser")

        # Fetch the list of episodes
        for script in soup.find_all("script"):
            match = re.search(r'\$\("#load"\)\.load\(\'(.+)\'\)', str(script))
            if match:
                soup = bs(scraper.get(website_base_url + match.group(1)[1:]).content, "html.parser")
                for a in soup.find_all("a", {"class": "play"}):
                    ep = a.getText()
                    if find_missing:
                        if _is_episode_missing(ep):
                            episodes_dict[ep] = website_base_url + a["href"][1:]
                        continue
                    episodes_dict[ep] = website_base_url + a["href"][1:]

        webpages = _get_webpages(episodes_dict, START_EPISODE, END_EPISODE)

        # Reverse episodes_dict
        for key in episodes_dict.keys():
            repisodes_dict[episodes_dict[key]] = key

        downloads = []

        for url in webpages:
            episode = repisodes_dict[url]
            failed = False

            try:
                source = scraper.get(url).content
                soup = bs(source, "html.parser")
                iframe = soup.find("iframe", {"id": "video"})

                vidurl = iframe["src"]
                vidurl_source = scraper.get(vidurl).content
                vidurl_soup = bs(vidurl_source, "html.parser")

                new_player = False
                for meta in vidurl_soup.find_all("meta"):
                    if meta.has_attr("http-equiv"):
                        if meta["http-equiv"].lower() == "refresh":
                            new_player = True
                            vidurl = re.search(r'url=(.+)', meta["content"].split(";")[1]).group(1)
                            vidurl_source = scraper.get(vidurl).content
                            vidurl_soup = bs(vidurl_source, "html.parser")

                if new_player:
                    vidjs = vidurl_soup.find_all("script", {"type": "text/javascript"})[1].text.replace("\n", "")
                else:
                    vidjs = jsbeautifier.beautify(vidurl_soup.body.find("script", {"type": "text/javascript"}).text.replace("\n", "")).replace("\n", "")
                sources = demjson.decode("{" + re.search(r'playerInstance\.setup\(.+(sources:.+?\[.+?\])', vidjs).group(1).replace(" ", "") + "}")
            except:
                print(sys.exc_info())
                print("Failed to get " + episode)
                failed = True

            if not failed:
                for source in sources["sources"]:
                    download_url = ""
                    if source["label"] == QUALITY:
                        download_url = source["file"]

                if not download_url:
                    download_url = sources["sources"][0]["file"]  # Sorry ;p
                downloads.append(download_url)
                print(episode + ":", download_url, end="\n\n")
                hash_map[download_url] = episode

            else:
                failed_episodes.append(episode)

            '''
            # The website has 3 kinds of DOM structures for their videos
                try:
                    # Method 1
                    video = iframe_soup.find("video", {"id": "video"})
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
                        try:
                            # Method 3
                            sources = [{"file": iframe_soup.find("div", {"id": "vid"}).source["src"], "label": QUALITY}]  # Sorry for lying :(
                            method = 3
                        except:
                            #print(sys.exc_info())
                            print("Failed to get " + episode)
                            failed = True'''
    else:
        # Watchanime
        QUALITY = ["360", "480", "720"][1]
        website_base_url = "http://watchanime.me/"
        sp = bs(scraper.get(page_url).content, "html.parser")
        eps_div = sp.find("div", {"id": "episodes_1-0"})

        for a in eps_div.find_all("a"):
            #print(a.getText())
            ep = "Episode " + re.search(r"Ep\. (\d+(\.\d+)?) \[.+\]", a.getText()).group(1)
            if find_missing:
                if _is_episode_missing(ep):
                    episodes_dict[ep] = a["href"].strip()
                continue
            episodes_dict[ep] = a["href"].strip()

        webpages = _get_webpages(episodes_dict, START_EPISODE, END_EPISODE)

        # Reverse episodes_dict
        for key in episodes_dict.keys():
            repisodes_dict[episodes_dict[key]] = key

        downloads = []
        for url in webpages:
            episode = repisodes_dict[url]
            source = scraper.get(url).content
            soup = bs(source, "html.parser")
            download_url = ""
            mp4upload = re.compile(r"^(http:\/\/|https:\/\/)*([a-z0-9][a-z0-9\-]*\.)*(mp4upload)\.com(\/.*)?$")
            yourupload = re.compile(r"^(http:\/\/|https:\/\/)*([a-z0-9][a-z0-9\-]*\.)*(yourupload)\.com(\/.*)?$")
            video_frames = soup.find("div", {"class": "autosize-container"}).find_all("iframe")
            try:
                #print("method 1")
                # Method 1 (YourUpload)
                #raise ValueError("")  # For when I need only Mp4Upload
                for frame in video_frames:
                    if yourupload.match(frame["src"]):
                        yourup_iframe_source = scraper.get(frame["src"]).content
                        yourup_soup = bs(yourup_iframe_source, "html.parser")
                        path = yourup_soup.find("video", {"id": "player"}).source["src"]
                        download_url = "https://yourupload.com" + path
                        #print(download_url)
                        if path.lower() == "undefined":
                            raise ValueError("")  # Failing method 1.
                if not download_url:
                    raise ValueError("")
            except:
                #print(sys.exc_info())
                # Method 2 (MP4Upload)
                try:
                    #print("method 2")
                    for frame in video_frames:
                        if mp4upload.match(frame["src"]):
                            mp4up_iframe_source = scraper.get(frame["src"]).content
                            mp4up_soup = bs(mp4up_iframe_source, "html.parser")
                            mp4up_js = jsbeautifier.beautify(mp4up_soup.body.find("script", {"type": "text/javascript"}).text)
                            download_url = re.search(r'src:"(.+\.mp4")', mp4up_js).group(1).replace('"', "")
                            #print(download_url, url)
                    if not download_url:
                        raise ValueError("")
                except:
                    print(sys.exc_info())
                    failed_episodes.append(episode)
                    print("Failed to get", episode)

            if download_url:
                print(episode + ": " + download_url, end="\n\n")
                downloads.append(download_url)
                hash_map[download_url] = episode

    return hash_map, failed_episodes

def get_episodes_dictionary(url, start=0, end=0, find_missing=False):
    """
    Returns a dictionary with episode download URLs mapped to their named and a list of episodes that couldn't be fetched.
        start: Episode to start fetching from
        end: Episode to stop fetching at
    """
    if start < 0 or end < 0:
        raise Exception("Invalid argument(s) for start and/or end")
    if identify_website(url):
        return _scrape_episodes(url, start, end, find_missing)
    else:
        raise Exception("Given URL not supported")
