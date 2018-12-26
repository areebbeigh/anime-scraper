import os
import re

from src.config import TimeoutConfig
from src.scrape_utils.selectors import GoGoAnimeSelectors, LOAD_STATUS_SELECTOR
from src.scrape_utils.servers import StreamServers
from src.stream_servers.openupload import OpenUploadScraper
from src.stream_servers.mp4upload import Mp4UploadScraper
from src.stream_servers.yourupload import YourUploadScraper
from src.utils import printing
from src.utils.timeout import call_till_true
from src.utils import sort_nicely, printd
from .base_scraper import BaseScraper


class Scraper(BaseScraper):
    def __init__(self, **kwargs):
        super(Scraper, self).__init__(**kwargs)
        self.driver.get(self.anime_url)
        self.episodes_dict = {}
        self.episodes_dict = self.fetch_episode_list()
        self.server_scraper = self._get_server_scraper()

    def _get_server_scraper(self):
        scrapers = {
            StreamServers.OPENUPLOAD: OpenUploadScraper(
                self.driver, self.proxy, GoGoAnimeSelectors),
            StreamServers.MP4UPLOAD: Mp4UploadScraper(
                self.driver, self.proxy, GoGoAnimeSelectors),
            StreamServers.YOURUPLOAD: YourUploadScraper(
                self.driver, self.proxy, GoGoAnimeSelectors)
        }
        
        return scrapers[self.server]

    def _execute_js_scripts(self):
        js_libs = os.path.join(os.path.dirname(os.path.abspath(__file__)), "js")

        load_episode_list_js = os.path.join(js_libs, "loadEpisodeList.js")

        with open(load_episode_list_js, "r") as f:
            load_episode_list = f.read()

        self.driver.execute_script(load_episode_list)

    def fetch_episode_list(self):
        # -> { 'Episode 1': 'https://www.kickassanime.ru/anime/gintama/episode-1', ... }
        if self.episodes_dict:
            return self.episodes_dict

        printd("fetching episode list")
        printing.fetching_list(self.anime_url)
        driver = self.driver

        # Execute JS to load the entire episode list
        self._execute_js_scripts()

        ep_list_container = driver.find_element_by_css_selector(GoGoAnimeSelectors.EPISODE_LIST)

        def fetch_ep_list(container):
            return container.find_elements_by_css_selector(GoGoAnimeSelectors.EPISODE)

        # Sometimes the episode list takes a while to load and fetch_ep_list gets 0 episodes
        # call_till_true will keep trying for n seconds till we get >0 episodes
        ep_list, calls, success = call_till_true(fetch_ep_list, TimeoutConfig.FETCHING_EPISODE_LIST, ep_list_container)

        if not success:
            # TODO: Change error raised
            raise ValueError("Failed to fetch episode list")

        printd("calls", calls)
        # print(ep_list_container.text)
        # print(len(ep_list))

        ep_dict = {}

        for ep in ep_list:
            if ep.text:
                episode_name = re.search(r"EP ([\d\-\.]+)", ep.text).group().replace("EP", "Episode")
                ep_dict[episode_name] = ep.get_attribute("href")
        # print(ep_dict)
        return ep_dict

    def fetch_episode(self, episode_name):
        # -> { stream_page: http://.../watch/episode-01, stream_url: http://.../file.mp4 }
        
        if episode_name in self.episodes_dict:
            stream_page = self.episodes_dict[episode_name]

            printd("Fetching", episode_name)
            printing.fetching_episode(episode_name, stream_page)
            # stream_url = self.server_scraper.fetch_stream_url(stream_page)
            try:
                stream_url = self.server_scraper.fetch_stream_url(stream_page)
            except Exception as err:
                printd(err)
                stream_url = ""

            result = {"stream_page": stream_page, "stream_url": stream_url}

            printd(result)
            printing.fetched_episode(episode_name, stream_url, True if stream_url else False)

            return result

        raise ValueError("%s does not exist" % episode_name)

    def fetch_episode_number(self, episode_number):
        for episode_name in self.episodes_dict:
            if episode_number == int(episode_name.replace("Episode ", "")):
                return self.fetch_episode(episode_name)
        raise ValueError("Episode %d does not exist" % episode_number)

    def fetch_all_episodes(self, episodes_dict):
        # -> { 'Episode 1': { 'stream_page': http://.../watch/episode-01, 'stream_url': http://.../file.mp4 }  }
        episode_names = list(self.episodes_dict.keys())
        sort_nicely(episode_names)

        for ep_name in episode_names:
            try:
                episodes_dict[ep_name] = self.fetch_episode(ep_name)
            except ValueError:
                episodes_dict[ep_name] = ""
