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
    def __init__(self, webdriver, selectors):
        BaseServerScraper.__init__(self, webdriver, selectors)
        self.regex_pattern_objects = get_stream_url_regex(StreamServers.OPENUPLOAD)
    
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

        # Choose openupload as streaming server
        # GoGoAnime has 2 open upload buttons. First one's broken.
        openupload_buttons = driver.find_elements_by_css_selector(selectors.OPENUPLOAD)
        openupload_buttons = openupload_buttons[1] if len(openupload_buttons) > 1 else openupload_buttons[0]
        openupload_buttons.click()

        player = driver.find_element_by_css_selector(selectors.PLAYER)
        
        '''
        while True:
            try:
                status_raw = driver.find_element_by_css_selector(LOAD_STATUS_SELECTOR).text
                status = json.loads(status_raw)
                print("in loop")
                if status["iframe_loaded"]:
                    print("iframe loaded")
                    break
            except NoSuchElementException as err:
                print("not there yet " + err.msg)
        '''

        res, calls, success = call_till_true(is_iframe_loaded, self.episode_fetch_timeout, driver)

        printd("outside wait loop ;", "success:", success, "calls:", calls)

        frame = player.find_element_by_tag_name("iframe")

        # TODO: Find alternative to use time.sleep()

        # First click opens a pop up
        frame.click()
        # [BAD] Waiting to make sure media player is accessible in the iframe 
        # (because I have a wooden PC from the stone age -_-)
        time.sleep(2) 

        # Second click triggers stream
        frame.click()
        # time.sleep(3) # [BAD] Waiting to make sure HTTP request to the stream file is made

        return self.search_url_in_perflogs(self.regex_pattern_objects)
