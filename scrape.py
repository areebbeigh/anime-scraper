import os
import sys
import json
import time

from collections import OrderedDict

from argparse import ArgumentParser

from src.utils.formatting import extract_episode_number
from src.utils.webdriver import get_chrome_webdriver
from src.websites.kickassanime import Scraper
from src.scrape_utils.servers import StreamServers

# TODO: Catch errors

start_time = time.time()

parser = ArgumentParser()
parser.add_argument("url", help="URL to the page of the list of episodes of the anime")

parser.add_argument("--start", "-s", type=int, help="The episode number to start fetching from")
parser.add_argument("--end", "-e", type=int, help="The episode number to stop fetching at")
parser.add_argument("--missing", "-m", help="Fetch downloads URLs only for episodes not present in this directory (if =files) or metadata (if =metadata)",
                        action="store", default=False)

parser.add_argument("--auto", "-a", help="Automatically add the downloads to IDM using the current directory as the download location",
                        action="store_true")

args = parser.parse_args()
url = args.url
is_auto = args.auto
missing = args.missing.lower() if args.missing else args.missing

# print("MISSING",missing)

driver = get_chrome_webdriver()
scraper = Scraper(driver, url, StreamServers.MP4UPLOAD)

episode_dict = scraper.fetch_episode_list()
episode_numbers = [extract_episode_number(ep) for ep in episode_dict]
episode_numbers.sort()
episode_numbers_to_fetch = []

# Parsing start and end points
start = args.start
end = args.end
start_given = False if type(start).__name__ == "NoneType" else True
end_given = False if type(end).__name__ == "NoneType" else True

if (start_given and start < 0) or (end_given and end < 0) or ((start_given and end_given) and (end < start)):
    print("Error: Invalid start and end points")
    sys.exit()

if start_given and end_given:
    episode_numbers_to_fetch = list(range(start, end+1))
elif start_given and not end_given:
    episode_numbers_to_fetch = episode_numbers[start-1:]
elif not start_given and end_given:
    episode_numbers_to_fetch = episode_numbers[0:end_given]

# Find missing episodes
downloaded_episode_numbers = []

if missing == "files":
    # Scan files in CWD and find missing episodes
    # XYZ/.../Episode 2.mp4 -> Episode 2
    files = [os.path.basename(os.path.splitext(f)[0]) for f in os.listdir()]
    downloaded_episodes_unclean = [ extract_episode_number(f) for f in files ]
    # Filter out all falsey values
    downloaded_episode_numbers += list(filter(lambda x: x, downloaded_episodes_unclean))

elif missing == "metadata":
    # Fetch only episodes that are not in metadata.json
    if not os.path.isfile("metadata.json"):
        # print("Error: metadata.json does not exist")
        sys.exit()

    with open("metadata.json", "r") as f:
        read_meta_data = json.loads(f.read())

    for episode_name in read_meta_data["Episodes"]:
        episode_number = extract_episode_number(episode_name)
        if episode_number:
            # print("downloaded: ", episode_number)
            downloaded_episode_numbers += [episode_number]

if missing:
    for episode_num in episode_numbers:
        if episode_num not in downloaded_episode_numbers:
            # print("missing episode", episode_num)
            episode_numbers_to_fetch += [episode_num]

fetched_episodes = OrderedDict()

# Fetch all episodes by default
episode_numbers_to_fetch = episode_numbers if not episode_numbers_to_fetch else episode_numbers_to_fetch
# print(episode_numbers_to_fetch)

for ep_number in episode_numbers_to_fetch:
    fetched_episodes["Episode " + str(ep_number)] = scraper.fetch_episode_number(ep_number)

driver.close()

failed = []

# This dictionary won't contain episodes that we couldn't find a stream url for
fetched_episodes_final = fetched_episodes.copy()

for episode_name, value in fetched_episodes.items():
    if not value["stream_url"]:
        failed += [episode_name]
        fetched_episodes_final.pop(episode_name)

# Prepare and write metadata
meta_data = { 
    "Episodes": fetched_episodes_final,
    "Failed": failed,
    "Time taken": str(time.time() - start_time) + " seconds"
    }

with open("metadata.json", "w") as f:
    f.write(json.dumps(meta_data, indent=4, separators=(',', ': ')))

# Prepare download scripts - Linux

# Add to IDM - Windows
