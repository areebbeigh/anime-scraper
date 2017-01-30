anime-scraper 
=============

This is a simple collection of simple web scrapers that extracts the MP4 download URLs from anime stream/download websites. I made it because of my love for anime and put it on GitHub to share with my IRL friends who are crazy about anime like me.

It doesn't work for all the series on animeland.tv because of the different DOM structure in some of them. It should work for most of them
though.

This doesn't download the episodes, it only creates a new text file with the download URLs. I use IDM to batch download after and run 
``rename.py`` after the downloads are complete. Works perfectly good for me so far. 

**Note:** The files created after running ``prepare_download_list.py`` should not be deleted until you have downloaded the episodes using IDM and then ran the ``rename.py`` script.

Usage
-----
The usage is straight forward. Everything is hard coded in the script. You have to change only two lines in the script to fetch download links for another anime. 

- The line in which the variable for number of episodes is set
- The line in which the name of the anime is set

For example in `animeland.tv`:

::

  QUALITY = ["360p", "720p"][0]   # Select quality
  NUMBER_OF_EPISODES = 24  # Replace with anime's number of episodes

  website_base_url = "http://www.animeland.tv/"
  base_path = "clannad-episode-{}-english-dubbed"  # Replace with the anime's base path and the episode number with {}
  websites = []

In the snippet above you can see ``NUMBER_OF_EPISODES`` and ``base_path``. These are the values you'll have to change while downloading an anime other than Clannad. The ``base_path`` is the last part of the URL when you open an episode on animeland.tv. Note that you must replace the episode number with ``{}``

Dependencies
------------

- BeautifulSoup
- cfscrape (for websites using CloadFare DDoS protection)
- demjson

Additional Info
---------------

| **Developer:** Areeb Beigh <areebbeigh@gmail.com>
| **GitHub Repo:** https://github.com/areebbeigh/anime-scraper
