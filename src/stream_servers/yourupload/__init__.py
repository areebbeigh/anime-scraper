import os
import json

from selenium.common.exceptions import NoSuchElementException

from src.scrape_utils.selectors import LOAD_STATUS_SELECTOR
from src.scrape_utils.regex import get_stream_url_regex
from src.scrape_utils.servers import StreamServers
from src.scrape_utils.server_base_class import BaseServerScraper
from src.scrape_utils.selectors import KickassAnimeSelectors

class YourUploadScraper(BaseServerScraper):
    def __init__(self, webdriver, selectors):
        BaseServerScraper.__init__(self, webdriver, selectors)
        self.regex_pattern_objects = get_stream_url_regex(StreamServers.YOURUPLOAD)

    def _execute_js_scripts(self):
        js_libs = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "js")
        jquery_onMutate_js = os.path.join(js_libs, "jquery.onmutate.min.js")
        track_iframe_js = os.path.join(js_libs, "trackIframe.js")

        with open(jquery_onMutate_js, "r") as f:
            jquery_onMutate = f.read()

        with open(track_iframe_js, "r") as f:
            track_iframe = f.read()

        self.driver.execute_script(jquery_onMutate)        
        self.driver.execute_script(track_iframe)
    
    def fetch_stream_url(self, stream_page):
        selectors = self.selectors
        driver = self.driver
        
        driver.get(stream_page)
        self._execute_js_scripts()

        # Choose yourupload as streaming server
        driver.find_element_by_css_selector(selectors.YOURUPLOAD).click()

        player = driver.find_element_by_css_selector(selectors.PLAYER)

        while True:
            try:
                status_raw = driver.find_element_by_css_selector(LOAD_STATUS_SELECTOR).text
                status = json.loads(status_raw)
                print("in loop")
                if status["iframe_loaded"]:
                    print("loaded")
                    break
            except NoSuchElementException as err:
                print("not there yet", err.msg)
        
        print("outside loop")
        # No need to click. YourUpload initiates the request during page load.
        # video = player.find_element_by_css_selector("video")
        # video.click()
        
        return self.search_url_in_perflogs(self.regex_pattern_objects)
