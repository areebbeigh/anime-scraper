import json

from src.scrape_utils.selectors import LOAD_STATUS_SELECTOR
from src.utils import printd

def is_document_loaded(webdriver):
    status_raw = webdriver.find_element_by_css_selector(LOAD_STATUS_SELECTOR).text
    status = json.loads(status_raw)
    printd("waiting")
    if status["document_loaded"]:
        printd("loaded")
        return True
    return False

def is_iframe_loaded(webdriver):
    status_raw = webdriver.find_element_by_css_selector(LOAD_STATUS_SELECTOR).text
    status = json.loads(status_raw)
    printd("waiting")
    if status["iframe_loaded"]:
        printd("iframe loaded")
        return True
    return False