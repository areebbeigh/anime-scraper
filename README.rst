anime-scraper
=============

.. image:: banner.png

This is a simple collection of simple web scrapers that extracts the MP4 download URLs from anime stream/download websites.
I made it because of my love for anime and put it on GitHub to share with my IRL friends who are crazy about anime like me.

This scraper simply fetches the download URLs for the episodes. It can also add the download URLs directly to IDM (using the idman
command line utility) with the correct episode names.

**Note**: You must add the directory where IDM is installed (C:\Program Files (x86)\Internet Download Manager by default) to your system
environment variable PATH before trying to use this script to add downloads to IDM.

Usage
-----

::

    usage: pdl.py [-h] [--missing] [--start START] [--end END] url

    positional arguments:
    url                   URL to the page of the list of episodes of the anime

    optional arguments:
    -h, --help            show this help message and exit
    --missing, -m         Fetch downloads URLs only for episodes not present in
                        this directory
    --start START, -s START
                        The episode number to start fetching from
    --end END, -e END     The episode number to stop fetching at

Example:

To fetch episodes 10-20 of the anime Clannad:

``python pdl.py "www3.animeland.tv/dub/clannad" -s 10 -e 20``

To fetch all the episodes skip the --start and --end parameters.

``python pdl.py "www3.animeland.tv/dub/clannad"``

To fetch only those episodes which are missing from the current directory use the -m argument.

``python pdl.py "www3.animeland.tv/dub/clannad -m"``

Dependencies
------------

- BeautifulSoup
- cfscrape (for websites using CloadFare DDoS protection)
- demjson

Supported Sites
-----------------

Here's a list of sites the scraper currently works for:

- `animeland.tv <http://animeland.tv/>`_
- `animejoy.tv <http://animejoy.tv>`_

Sites that may be added soon:

- `kissanime.ru <http://kissanime.ru/>`_

Additional Info
---------------

| **Developer:** Areeb Beigh <areebbeigh@gmail.com>
| **GitHub Repo:** https://github.com/areebbeigh/anime-scraper
