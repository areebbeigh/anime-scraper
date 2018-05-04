import sys
import os
from collections import OrderedDict

from argparse import ArgumentParser

from src.websites.kickassanime import Scraper
from src.utils.formatting import extract_episode_number
from src.utils.webdriver import get_chrome_webdriver
from src.scrape_utils.servers import StreamServers

# Parse user input
# Read config
# Check URL and get matching scraper instance - not needed for now
# Fetch episodes from prefered server
# Prepare JSON and simple text files

parser = ArgumentParser()
parser.add_argument("url", help="URL to the page of the list of episodes of the anime")

parser.add_argument("--start", "-s", type=int, help="The episode number to start fetching from")
parser.add_argument("--end", "-e", type=int, help="The episode number to stop fetching at")
parser.add_argument("--missing", "-m", help="Fetch downloads URLs only for episodes not present in this directory",
                        action="store", default=False)

parser.add_argument("--auto", "-a", help="Automatically add the downloads to IDM using the current directory as the download location",
                        action="store_true")

args = parser.parse_args()
url = args.url
is_auto = args.auto
missing = args.missing.lower() if args.missing else args.missing

print("MISSING",missing)

driver = get_chrome_webdriver()
scraper = Scraper(driver, url, StreamServers.MP4UPLOAD)

episode_dict = scraper.fetch_episode_list()
episode_numbers = [extract_episode_number(ep) for ep in episode_dict]

# Parsing start and end points
start = args.start
end = args.end
start_given = False if type(start).__name__ == "NoneType" else True
end_given = False if type(end).__name__ == "NoneType" else True

if (start_given and start < 0) or (end_given and end < 0) or ((start_given and end_given) and (end < start)):
    print("Error: Invalid start and end points")
    sys.exit()

episode_numbers_to_fetch = []

if start_given and end_given:
    episode_numbers_to_fetch = list(range(start, end+1))
elif start_given and not end_given:
    # get episode numbers
    # make list from given start point to end point
    pass
elif not start_given and end_given:
    episode_numbers_to_fetch = list(range(1,end+1))

# To find missing

if missing == "files":
    # Scan files in CWD and find missing episodes
    # XYZ/.../Episode 2.mp4 -> Episode 2
    files = [os.path.basename(os.path.splitext(f)[0]) for f in os.listdir()]
    print(files)
    downloaded_episodes_unclean = [ extract_episode_number(f) for f in files ]
    print(downloaded_episodes_unclean)
    # Filter out all falsey values
    downloaded_episode_numbers = list(filter(lambda x: x, downloaded_episodes_unclean))
    print(downloaded_episode_numbers)

    for episode_num in episode_numbers:
        if episode_num not in downloaded_episode_numbers:
            print("missing episode", episode_num)
            episode_numbers_to_fetch += [episode_num]

elif missing == "meta":
    # Scan files in metadata and find missing
    pass

fetched_episodes = OrderedDict()

print(episode_numbers_to_fetch)
if episode_numbers_to_fetch:
    for ep_number in episode_numbers_to_fetch:
        fetched_episodes["Episode " + str(ep_number)] = scraper.fetch_episode_number(ep_number)
else:
    scraper.fetch_all_episodes(fetched_episodes)

driver.close()

print(fetched_episodes)

# Output operable data
