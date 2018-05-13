import os

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.keys import Keys

from src.config import TimeoutConfig
from . import printd
from .timeout import call_till_true

# 'Thank you' tabs expected to open from chrome extensions
EXPECTED_EXTRA_TABS = 1

def _get_addons():
    addons_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "chrome_addons")
    return [os.path.join(addons_dir, f) for f in os.listdir(addons_dir) if f.endswith(".crx")]

def switch_to_main_tab(self):
    """ 
        Switches the webdriver's focus to the main tab (the one that opens on launch)
    """
    self.switch_to.window(self.window_handles[0])

def close_extra_tabs(self):
    """ 
        Closes any extra tabs and returns focus to the first tab
    """
    tabs = self.window_handles

    if len(tabs) > 1:
        for tab in tabs[1:]:
            self.switch_to.window(tab)
            self.close()
            #self.find_element_by_css_selector('body').send_keys(Keys.COMMAND + 'W')
    
    self.switch_to.window(self.window_handles[0])

def get_chrome_webdriver():
    """
        Returns a chrome webdriver instance with all the addons in /chrome_addons
    """
    options = Options()

    for addon in _get_addons():
        options.add_extension(addon)

    caps = DesiredCapabilities.CHROME
    caps['loggingPrefs'] = {'performance': 'ALL'}

    driver = webdriver.Chrome(desired_capabilities=caps, chrome_options=options)
    driver.set_window_size(450, 500)

    # Binding methods to driver object. These metods are needed because the extensions
    # open new tabs on first launch which change the focus from the main tab in the browser
    driver.switch_to_main_tab = switch_to_main_tab.__get__(driver)
    driver.close_extra_tabs = close_extra_tabs.__get__(driver)

    # Killing extra tabs from extensions
    def tab_count_reached(webdriver):
        return len(webdriver.window_handles) >= EXPECTED_EXTRA_TABS + 1

    res, calls, success = call_till_true(tab_count_reached, TimeoutConfig.KILLING_EXTRA_TABS, driver)
    
    if success:
        printd("calls", calls)
        driver.close_extra_tabs()
    else:
        printd("Couldn't kill extra tabs")

    return driver

