import sys

from argparse import ArgumentParser

from src.websites.kickassanime import Scraper
from src.utils.webdriver import get_chrome_webdriver
from src.scrape_utils.servers import StreamServers

parser = ArgumentParser()
parser.add_argument("url", help="URL to the page of the list of episodes of the anime")

parser.add_argument("--start", "-s", type=int, help="The episode number to start fetching from")
parser.add_argument("--end", "-e", type=int, help="The episode number to stop fetching at")
parser.add_argument("--missing", "-m", help="Fetch downloads URLs only for episodes not present in this directory",
                        action="store_true")

parser.add_argument("--auto", "-a", help="Automatically add the downloads to IDM using the current directory as the download location",
                        action="store_true")

args = parser.parse_args()
url = args.url
is_auto = args.auto

driver = get_chrome_webdriver()
scraper = Scraper(driver, url, StreamServers.YOURUPLOAD)

# Parsing start and end points
start = args.start
end = args.end
start_given = False if type(start).__name__ == "NoneType" else True
end_given = False if type(end).__name__ == "NoneType" else True

if (start_given and start < 0) or (end_given and end < 0) or ((start_given and end_given) and (end < start)):
    print("Error: Invalid start and end points")
    sys.exit()

if start_given and end_given:
    episodes = list(range(start, end+1))
elif start_given and not end_given:
    # get episode numbers
    # make list from given start point to end point
    pass
elif not start_given and end_given:
    episodes = list(range(1,end+1))

# To find missing

# Check the available episodes in directory (or in the JSON file depending on options)
# Make a list of the missing episodes and fetch

# Parse user input
# Options: Anime URL, Start episode, End episode, Missing -> [Use metadata, Use file list], Auto-add, Metadata only
# Read config
# Check URL and get matching scraper instance
# Fetch episodes from prefered server
# Prepare JSON and simple text files

fetched_episodes = {}

# meta_data = scraper.fetch_metadata() # -> { title: _____, synopsis: _____, poster: ____ }

if episodes:
    for ep_nuber in episodes:
        fetched_episodes["Episode " + str(ep_nuber)] = scraper.fetch_episode_number(ep_nuber)
else:
    scraper.fetch_all_episodes(fetched_episodes)

driver.close()

print(fetched_episodes)

# Output operable data
