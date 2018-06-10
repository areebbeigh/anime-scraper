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
    def __init__(self, webdriver, selectors):
        BaseServerScraper.__init__(self, webdriver, selectors)
        self.regex_pattern_objects = get_stream_url_regex(StreamServers.MP4UPLOAD)

    # def _execute_js_scripts(self):
    #     js_libs = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "js")
    #     onDocLoad_js = os.path.join(js_libs, "onDocumentLoad.js")
    #     trackIframe_js = os.path.join(js_libs, "trackIframe.js")
        
    #     with open(trackIframe_js, "r") as f:
    #         trackIframe = f.read()

    #     with open(onDocLoad_js, "r") as f:
    #         onDocLoad = f.read()
        
    #     self.driver.execute_script(onDocLoad)

    #     if self.selectors != KickassAnimeSelectors:
    #         self.driver.execute_script(trackIframe)
    
    def fetch_stream_url(self, stream_page):
        selectors = self.selectors
        driver = self.driver
        
        driver.get(stream_page)

        # Choose mp4upload as streaming server
        if self.selectors != KickassAnimeSelectors:
            # Kickassanime uses MP4Upload by default
            # print("clicking")
            driver.find_element_by_css_selector(selectors.MP4UPLOAD).click()

        player = driver.find_element_by_css_selector(selectors.PLAYER)
        self._execute_js_scripts()

        if self.selectors != KickassAnimeSelectors:
            res, calls, success = call_till_true(is_iframe_loaded, self.episode_fetch_timeout, driver)
        else:
            res, calls, success = call_till_true(is_document_loaded, self.episode_fetch_timeout, driver)

        printd("outside wait loop ;", "success:", success, "calls:", calls)
        
        # No need to click. MP4Upload initiates the request during page load.
        # video = player.find_element_by_css_selector("video")
        # video.click()
        
        return self.search_url_in_perflogs(self.regex_pattern_objects)
