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


class BaseScraper:
    def __init__(self, **kwargs):
        self.driver = kwargs.get('webdriver')
        self.proxy = kwargs.get('proxy')
        self.anime_url = kwargs.get('url')
        self.server = kwargs.get('server')

