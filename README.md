# anime-scraper
Scrape and add anime episode stream URLs to uGet (Linux) or IDM (Windows)

## Motivation for v3
Let me take a moment to explain the upgrade to v3. If you were a regular user of anime-scraper before (upto any version v2)
you probably noticed that it broke very often. The reason was because of the frequent DOM manipulation of the supported websites or of the video hosting websites. In an attempt to avoid this breakage to some extent I've implemented a new scraping method in this version of anime-scraper. 

How it works:

anime-scraper now uses Selenium (with Google Chrome, for now) to scrape episode download URLs. While it still depends on the streaming website's DOM structure to some extent, the code structure aims to be a lot more maintainable and expandable than before. Also, instead of extracting the stream URLs from the minimised JavaScript files from the hosting services, anime-scraper extracts the download URLs from the network file exchanges, which makes the overall scrapping process less nested.

The disadvantage:

Since anime-scraper is using a browser instance for scraping, it has to wait for webpages to load all the elements unlike previous scraping methods where it only needed to fetch the DOM of webpages. This means v3 will take longer to scrape episodes.

## REAL Motivation for v3
If you're still reading, you deserve to know my real motivation behind the rewrite: The previous code was absolutely horrible and I wanted to work on something simple and fun after I'd finished high school. :P

## Shiny new stuff
- Linux support with [uGet Download Manager](http://http://ugetdm.com/) (only cuz I moved to Ubuntu)

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

So to fetch episodes 2, 6 and everything that lies in between:

`python scrape.py https://www.kickassanime.ru/anime/clannad -s 2 -e 6`

To automatically add the downloads to IDM/uGet:

`python scrape.py https://www.kickassanime.ru/anime/clannad -s 2 -e 6 -a`

