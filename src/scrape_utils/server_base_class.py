class BaseServerScraper:
    def __init__(self, webdriver, selectors):
        self.driver = webdriver
        self.selectors = selectors

    def search_url_in_perflogs(self, regex_objects):
        """
        Access driver performance logs and find the stream URL by matching with the
        regular expression for the server.
        """
        perf_logs = str(self.driver.get_log('performance'))
        for obj in regex_objects:
            search_result = obj.search(perf_logs)
            if search_result:
                return search_result.group(0).replace("\"", "").replace("'", "")
        
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
    
    