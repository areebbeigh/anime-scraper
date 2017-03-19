anime-scraper
=============

This is a simple collection of simple web scrapers that extracts the MP4 download URLs from anime stream/download websites. I made it because of my love for anime and put it on GitHub to share with my IRL friends who are crazy about anime like me.

It doesn't work for all the series on animeland.tv because of the different DOM structure in some of them. It should work for most of them
though.

This doesn't download the episodes, it only creates a new text file with the download URLs. I use IDM to batch download after and run
``rename.py`` after the downloads are complete. Works perfectly good for me so far.

**Note 1:** The files created after running ``prepare_download_list.py`` should not be deleted until you have downloaded the episodes using IDM and then ran the ``rename.py`` script.

**Note 2:** After an update on animeland.tv the site now has some of its videos hosted on Google. The scraper can't rename the files anymore. All the videos hosted on Google will be
saved as videoplayback.mp4 now.

**Solution:** New scraper for another dubbed anime website coming soon. (If you have a good website for dubbed anime where episodes are <= 150 MB and not hosted with the same file name email me)

Usage
-----
The usage is straight forward. Everything is hard coded in the script. You have to change only two lines in the script to fetch download links for another anime.

- The line in which the variable for number of episodes is set
- The line in which the name of the anime is set

For example in `animejoy.tv`:

::

    START_EPISODE = 1  # Replace with the episode number to start fetching from
    END_EPISODE = 24  # Replace with the episode number to stop fetching at

    website_base_url = "http://anime-joy.tv/watch/"
    page_url = "http://anime-joy.tv/watch/clannad"  # Replace with the URL to the anime page

In the snippet above you can see ``START_EPISODE``, ``END_EPISODE`` and ``page_url``. These are the values you'll have to change while downloading an anime other than Clannad.

Dependencies
------------

- BeautifulSoup
- cfscrape (for websites using CloadFare DDoS protection)
- demjson

Additional Info
---------------

| **Developer:** Areeb Beigh <areebbeigh@gmail.com>
| **GitHub Repo:** https://github.com/areebbeigh/anime-scraper
