# anime-scraper
Scrape and add anime episode stream URLs to uGet (Linux) or IDM (Windows).

## Motivation for v3
Let me take a moment to explain the upgrade to v3. If you were a regular user of anime-scraper before (upto any version v2)
you probably noticed that it broke very often. The reason was because of the frequent DOM updation of the supported websites or of the video hosting websites. In an attempt to avoid this breakage to some extent I've implemented a new scraping method in this version of anime-scraper. 

How it works:

anime-scraper now uses Selenium (with Google Chrome, for now) to scrape episode download URLs. While it still depends on the streaming website's DOM structure to some extent, the code structure aims to be a lot more maintainable and expandable than before. Also, instead of extracting the stream URLs from the minimised JavaScript files from the hosting services, anime-scraper extracts the download URLs from the network file exchange logs, which makes the overall scrapping process less nested.

The disadvantage:

Since anime-scraper is using a browser instance for scraping, it has to wait for webpages to load all the elements unlike previous scraping methods where it only needed to fetch the DOM of webpages. This means v3 will take longer to scrape episodes.

## REAL Motivation for v3
If you're still reading, you deserve to know my real motivation behind the rewrite: The previous code was absolutely horrible and I wanted to work on something simple and fun after I'd finished high school. :P

## Shiny new stuff
- Linux support with [uGet Download Manager](http://http://ugetdm.com/) (only cuz I moved to Ubuntu)

## Get it working

`git clone https://github.com/areebbeigh/anime-scraper.git`

`pip install -r requirements.txt`

### Ubuntu

1. Installing some packages:

```
sudo apt-get update
sudo apt-get install -y unzip xvfb libxi6 libgconf-2-4
```

2. Installing Google Chrome:

```
sudo curl -sS -o - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add
sudo echo "deb [arch=amd64]  http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list
sudo apt-get -y update
sudo apt-get -y install google-chrome-stable
```

3. Installing and setting up chrome webdriver:

```
wget https://chromedriver.storage.googleapis.com/2.35/chromedriver_linux64.zip
unzip chromedriver_linux64.zip

sudo mv chromedriver /usr/bin/chromedriver
sudo chown root:root /usr/bin/chromedriver
sudo chmod +x /usr/bin/chromedriver
```

4. Finally, add anime-scraper repository directory to PATH. This allows you to run the command `scrape.py` in any directory.


### Windows

1. Download the [Chrome Webdriver](https://sites.google.com/a/chromium.org/chromedriver/downloads)
2. Place it in `C:/webdrivers` (or where ever you want)
3. Add `C:/webdrivers` to system environment variable PATH  (# TODO: Make this step optional through config.py)
4. Make sure your Internet Download Manager installation directory (the one in which idman.exe sits) is added to PATH or anime-scraper can't add downloads automatically to IDM.
5. Add anime-scraper repository directory to PATH. This allows you to run the command `scrape` in any directory.

## Usage
The usage is pretty much the same as the previous version:

```
usage: scrape.py [-h] [--start START] [--end END] [--missing MISSING] [--auto]
                 url

positional arguments:
  url                   URL to the page of the list of episodes of the anime

optional arguments:
  -h, --help            show this help message and exit
  --start START, -s START
                        The episode number to start fetching from
  --end END, -e END     The episode number to stop fetching at
  --missing MISSING, -m MISSING
                        Fetch downloads URLs only for episodes not present in
                        this directory (if =files) or metadata (if =metadata)
  --auto, -a            Automatically add the downloads to IDM using the
                        current directory as the download location
```
### Example
For fetching Clannad:

`mkdir Clannad ; cd Clannad`  (optional, this is just to keep everything organzed)

For all episodes:

`scrape.py https://www.kickassanime.ru/anime/clannad`

If I want to fetch episodes 2, 6 and everything that lies in between for myself I'd:

`scrape.py https://www.kickassanime.ru/anime/clannad -s 2 -e 6`

To fetch episodes that are missing from the current directory:

`scrape.py https://www.kickassanime.ru/anime/clannad -m files`

To fetch episodes that are missing from the scraping metadata (metadata.json):

`scrape.py https://www.kickassanime.ru/anime/clannad -m metadata`

To automatically add the downloads to IDM/uGet:

`scrape.py https://www.kickassanime.ru/anime/clannad -s 2 -e 6 -a`

Additionally, you can change a very tiny bit (for now) of the configuration in `src/config.py`.

## A few things
- If you're not able to scrape episodes of a particular series try changing the stream server
in the configuration. You can choose an ideal stream server by opening the episodes of the anime in the browser and seeing which stream servers are actually available.
- Right now [May 11 2018], anime-scraper doesn't work on the more recent ongoing kickassanime.ru anime. Works for all of the completed anime though.

## Supported websites
- kickassanime.ru
- gogoanime.se

## Not mine
anime-scraper uses the following additional "resources":

- [jQuery](http://jquery.com)
- [jQuery onMutate](https://github.com/eclecto/jQuery-onMutate)
- [Pop Up Blocker](http://www.poperblocker.com/) Chrome extension
- [Browsermob Proxy](https://github.com/lightbody/browsermob-proxy)

Thanks a bunch to the developers.

## TODO 
- Expand config.py
- Add support for ~2~ 1 more sites
- Reduce scrapping time
- Contributing.md
- **This implementation is still kinda hacky and breaks from time to time. Come up with a more robust scraping method.**

(no promises)

## Bye Bye
That's pretty much it. Feel free to contribute by fixing/reporting bugs and/or expanding anime-scraper. Cheers.
