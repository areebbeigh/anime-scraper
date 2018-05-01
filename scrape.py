from src.websites.kickassanime import Scraper
from src.utils.webdriver import get_chrome_webdriver
from src.scrape_utils.servers import StreamServers

url = "https://www.kickassanime.ru/anime/clannad"
episodes = []
driver = get_chrome_webdriver()
scraper = Scraper(driver, url, StreamServers.YOURUPLOAD)

fetched_episodes = {}

meta_data = scraper.fetch_metadata() # -> { title: _____, synopsis: _____, poster: ____ }


# Parse user input
# Options: Anime URL, Start episode, End episode, Missing -> [Use metadata, Use file list], Auto-add, Metadata only
# Read config
# Check URL and get matching scraper instance
# Fetch episodes from prefered server
# Prepare JSON and simple text files


'''
if episodes:
    for ep in episodes: # TODO: fix this
        fetched_episodes += [scraper.fetch_episode(ep)] # -> { stream_page: ____, stream_url: ___ }
else:
    scraper.fetch_all_episodes(fetched_episodes)

driver.close()

print(fetched_episodes)

# New Anime object
# Serialize object
# Output operable data

'''