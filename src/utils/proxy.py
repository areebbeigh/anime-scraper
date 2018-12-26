import json
import requests

from browsermobproxy import Server, Client

from src.config import BrowserMobProxyConfig

# TODO: Add more extras. Makes scraping faster.
extras = [
    'disqus',
    'advertising',
    'bidswitch',
    'mgid',
    'adtech',
    'bebi',
    'mybestmv',
    'clksite',
    'adgrx',
    'dotomi',
    'pubmatic',
    'adnxs',
    'ad-m',
    'playground',
    'g',
    'adsrvr'
]

def get_generic_url_regex(site_name):
    return "https?:\\/\\/([a-z0-9]*\\.)?{}\\.[a-z]*\\b([-a-zA-Z0-9@:%_\\+.~#?&//=]*)".format(site_name)

class BrowserMobProxy:
    def __init__(self, **kwargs):
        self.server = Server(BrowserMobProxyConfig.binary)
        self.server.start()
        self.host = 'localhost'
        self.trust_all_servers = kwargs.get('trust_all_servers')
        self.create_proxy()
        if kwargs.get('capture_content'):
            self.capture_content()
        self.blacklist_extras()

    @property
    def api_base_url(self):
        return "http://{}:{}".format(self.host, self.server.port)

    @property
    def proxy_server(self):
        return "{}:{}".format(self.host, self.port)

    def _at(self, path):
        return "{}/{}".format(self.api_base_url, path)

    def create_proxy(self):
        options = { 'trustAllServers': 'true' } if self.trust_all_servers else {}
        r = requests.post(self._at('proxy'), data = options)
        self.port = json.loads(r.text)['port']
        self.proxy = Client(self.api_base_url.replace('http://', ''), 
            options={ 'existing_proxy_port_to_use': self.port })

    def capture_content(self):
        requests.put(self._at('proxy/{}/har'.format(self.port)), data = {'captureContent':'true'})

    def blacklist_extras(self):
        for site_name in extras:
            self.proxy.blacklist(get_generic_url_regex(site_name), 401)

    def close(self):
        self.proxy.close()
        self.server.stop()
