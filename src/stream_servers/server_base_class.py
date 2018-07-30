import os
from src.config import TimeoutConfig

class BaseServerScraper:
    def __init__(self, webdriver, selectors):
        self.driver = webdriver
        self.previos_urls = []
        self.selectors = selectors
        self.episode_fetch_timeout = TimeoutConfig.FETCHING_EPISODE_STREAM

    def _execute_js_scripts(self):
        js_libs = os.path.join(os.path.dirname(os.path.abspath(__file__)), "js")

        loadStatus_js = os.path.join(js_libs, "loadStatus.js")
        jquery_js = os.path.join(js_libs, "jquery-3.3.1.min.js")
        jquery_onMutate_js = os.path.join(js_libs, "jquery.onmutate.min.js")
        trackIframe_js = os.path.join(js_libs, "trackIframe.js")

        with open(loadStatus_js, "r") as f:
            loadStatus = f.read()

        with open(jquery_js, "r") as f:
            jquery = f.read()

        with open(jquery_onMutate_js, "r") as f:
            jquery_onMutate = f.read()
        
        with open(trackIframe_js, "r") as f:
            trackIframe = f.read()
        
        self.driver.execute_script(jquery + jquery_onMutate + loadStatus + trackIframe)

    def search_url_in_perflogs(self, regex_objects):
        """
        Access driver performance logs and find the stream URL by matching with the
        regular expression for the server.
        """
        complete_perf_logs = str(self.driver.get_log('performance'))
        perf_logs = complete_perf_logs

        # Replacing previously fetched URLs from performance logs.
        # In some cases, regex search was returning previously fetched URLs.
        for previous_url in self.previos_urls:
            perf_logs = perf_logs.replace(previous_url, "")

        # with open("perf logs.txt", "w") as f:
        #     f.write(perf_logs)

        for obj in regex_objects:
            search_result = obj.search(perf_logs)
            if search_result:
                url = search_result.group(0).replace("\"", "").replace("'", "")
                self.previos_urls += [url]
                # print(self.previos_urls)
                return url
        
        return ""

    def convert_to_old_form(self):
        """
        [NOT IMPLEMENTED YET]
        Anime streaming websites don't have consistent DOM structures when it comes to new
        episode releases. This method executes a JS script in the browser that attempts to
        convert the current page to an old-form page which the scrapers are originally 
        compatible with.
        """
        pass
    
    