import os
import json
import time

from selenium.common.exceptions import NoSuchElementException

from src.utils import printd
from src.utils.timeout import call_till_true
from src.scrape_utils.selectors import LOAD_STATUS_SELECTOR, GoGoAnimeSelectors
from src.scrape_utils.regex import get_stream_url_regex
from src.scrape_utils.servers import StreamServers
from src.stream_servers.server_base_class import BaseServerScraper
from src.scrape_utils.is_loaded import is_document_loaded, is_iframe_loaded


class OpenUploadScraper(BaseServerScraper):
    def __init__(self, driver, proxy, selectors):
        BaseServerScraper.__init__(self, driver, proxy, selectors)
        self.regex_pattern_objects = get_stream_url_regex(StreamServers.OPENUPLOAD)

    def fetch_stream_url(self, stream_page):
        selectors = self.selectors
        driver = self.driver

        driver.get(stream_page)
        self._execute_js_scripts()

        # Choose openupload as streaming server
        # GoGoAnime has 2 open upload buttons. First one's broken.
        openupload_buttons = driver.find_elements_by_css_selector(selectors.OPENUPLOAD)
        openupload_button = openupload_buttons[-1]
        
        if selectors == GoGoAnimeSelectors:
            openupload_button.click()
        else:
            real_btn = openupload_button.find_element_by_tag_name("a")
            time.sleep(3)
            real_btn.click()

        player = driver.find_element_by_css_selector(selectors.PLAYER)
        
        res, calls, success = call_till_true(is_iframe_loaded, self.episode_fetch_timeout, driver)
        printd("outside wait loop ;", "success:", success, "calls:", calls)

        frame = player.find_element_by_tag_name("iframe")

        if selectors == GoGoAnimeSelectors:
            frame.click() # First click opens a pop up
            time.sleep(2)
            frame.click() # Second click triggers stream
        else:
            # Kickassanime is weird. They have a fake player on top of the real one.
            time.sleep(2)
            frame.click()
            time.sleep(7)
            frame.click()
            time.sleep(3)

        stream_url = self.search_url_in_perflogs(self.regex_pattern_objects)

        if not stream_url:
            player.click()
            time.sleep(2)
            stream_url = self.search_url_in_perflogs(self.regex_pattern_objects)

        return stream_url
