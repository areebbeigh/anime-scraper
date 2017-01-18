anime-scraper 
=============

This is a simple collection of simple web scrapers that extracts the MP4 download URLs from anime stream/download websites. I made it because of my love for anime and put it on GitHub to share with my IRL friends who are crazy about anime like me.

It doesn't work for all the series on animeland.tv because of the different DOM structure in some of them. It should work for most of them
though.

This doesn't download the episodes, it only creates a new text file with the download URLs. I use IDM to batch download after and run 
``rename.py`` after the downloads are complete. Works perfectly good for me so far. 

**Note:** The files created after running ``prepare_download_list.py`` should not be deleted until you have downloaded the episodes using IDM and then ran the ``rename.py`` script.

Dependencies
------------

- BeautifulSoup
- cfscrape (for websites using CloadFare DDoS protection)
- demjson

Additional Info
---------------

| **Developer:** Areeb Beigh <areebbeigh@gmail.com>
| **GitHub Repo:** https://github.com/areebbeigh/anime-scraperhttps
