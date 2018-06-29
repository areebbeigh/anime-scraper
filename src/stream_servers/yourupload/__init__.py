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


class YourUploadScraper(BaseServerScraper):
    def __init__(self, webdriver, selectors):
        BaseServerScraper.__init__(self, webdriver, selectors)
        self.regex_pattern_objects = get_stream_url_regex(StreamServers.YOURUPLOAD)

    # def _execute_js_scripts(self):
    #     js_libs = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "js")
    #     jquery_onMutate_js = os.path.join(js_libs, "jquery.onmutate.min.js")
    #     track_iframe_js = os.path.join(js_libs, "trackIframe.js")

    #     with open(jquery_onMutate_js, "r") as f:
    #         jquery_onMutate = f.read()

    #     with open(track_iframe_js, "r") as f:
    #         track_iframe = f.read()

    #     self.driver.execute_script(jquery_onMutate)        
    #     self.driver.execute_script(track_iframe)
    
    def fetch_stream_url(self, stream_page):
        selectors = self.selectors
        driver = self.driver
        
        driver.get(stream_page)
        self._execute_js_scripts()

        # Choose yourupload as streaming server
        yourupload_button = driver.find_element_by_css_selector(selectors.YOURUPLOAD)
        yourupload_button.click()
        yourupload_button.click()

        player = driver.find_element_by_css_selector(selectors.PLAYER)

        res, calls, success = call_till_true(is_iframe_loaded, self.episode_fetch_timeout, driver)

        printd("outside wait loop ;", "success:", success, "calls:", calls)
        
        # No need to click. YourUpload initiates the request during page load.
        # video = player.find_element_by_css_selector("video")
        # video.click()

        return self.search_url_in_perflogs(self.regex_pattern_objects)
