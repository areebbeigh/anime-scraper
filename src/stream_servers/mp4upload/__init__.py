import os
import json

from selenium.common.exceptions import NoSuchElementException

from src.utils import printd
from src.utils.timeout import call_till_true
from src.scrape_utils.selectors import LOAD_STATUS_SELECTOR
from src.scrape_utils.regex import get_stream_url_regex
from src.scrape_utils.servers import StreamServers
from src.stream_servers.server_base_class import BaseServerScraper
from src.scrape_utils.selectors import KickassAnimeSelectors
from src.scrape_utils.is_loaded import is_document_loaded, is_iframe_loaded

class Mp4UploadScraper(BaseServerScraper):
    def __init__(self, driver, proxy, selectors):
        BaseServerScraper.__init__(self, driver, proxy, selectors)
        self.regex_pattern_objects = get_stream_url_regex(StreamServers.MP4UPLOAD)

    def fetch_stream_url(self, stream_page):
        selectors = self.selectors
        driver = self.driver
        
        driver.get(stream_page)
        self._execute_js_scripts()

        # Choose mp4upload as streaming server
        # if self.selectors != KickassAnimeSelectors:
        #     # Kickassanime uses MP4Upload by default
        #     # print("clicking")

        mp4upload_button = driver.find_element_by_css_selector(selectors.MP4UPLOAD)
        mp4upload_button.click()
        mp4upload_button.click()
        
        player = driver.find_element_by_css_selector(selectors.PLAYER)

        res, calls, success = call_till_true(is_iframe_loaded, self.episode_fetch_timeout, driver)
        printd("outside wait loop ;", "success:", success, "calls:", calls)

        iframe = player.find_element_by_css_selector("iframe")
        iframe.click()
        
        return self.search_url_in_perflogs(self.regex_pattern_objects)
