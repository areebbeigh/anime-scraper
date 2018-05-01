anime-scraper
=============


**New version in development: https://github.com/areebbeigh/anime-scraper/tree/v3.0.0**

**Update: Latest changes made for WatchAnime.me**

**Update: The scraper has been modified according to the latest changes made on WatchAnime.me and AnimeLand.tv and now works without any problems.**

This is a simple collection of web scrapers that extract the MP4 download URLs from anime stream/download websites.
I made it because of my love for anime and put it on GitHub to share with my IRL friends who are crazy about anime like me.

This scraper simply fetches the download URLs for the episodes. It can also add the download URLs directly to IDM (using the idman command line utility) with the correct episode numbers.

**Note**: You must add the directory where IDM is installed (C:/Program Files (x86)/Internet Download Manager by default) to your system
environment variable PATH before trying to use this script to add downloads to IDM.

Usage
-----

::

    usage: pdl.py [-h] [--missing] [--auto] [--start START] [--end END] url

    positional arguments:
      url                   URL to the page of the list of episodes of the anime

    optional arguments:
      -h, --help            show this help message and exit
      --missing, -m         Fetch downloads URLs only for episodes not present in
                            this directory
      --auto, -a            Automatically add the downloads to IDM using the
                            current directory as the download location
      --start START, -s START
                            The episode number to start fetching from
      --end END, -e END     The episode number to stop fetching at

Example:

To fetch episodes 10-20 of the anime Clannad:

``python pdl.py www3.animeland.tv/dub/clannad -s 10 -e 20``

To fetch all the episodes skip the --start and --end parameters.

``python pdl.py www3.animeland.tv/dub/clannad``

To fetch only those episodes which are missing from the current directory use the -m argument.

``python pdl.py www3.animeland.tv/dub/clannad -m``

You could as well add the folder, in which pdl.py is located, to PATH to make it easier to use.

Dependencies
------------

- BeautifulSoup
- cfscrape (for websites using CloudFlare DDoS protection)
- demjson
- jsbeautifier

Supported Sites
-----------------

Here's a list of sites the scraper currently works for:

- `animeland.tv <http://animeland.tv/>`_
- `watchanime.me <http://watchanime.me>`_

Sites that may be added soon:

- `kissanime.ru <http://kissanime.ru/>`_

Additional Info
---------------

| **Developer:** Areeb Beigh <areebbeigh@gmail.com>
| **GitHub Repo:** https://github.com/areebbeigh/anime-scraper
