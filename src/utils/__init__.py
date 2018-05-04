import re
import time

from src.config import UserConfig

def printd(*args, **kwargs):
    """ 
        Prints given msg to console if debug is on. Writes to scrape.log either way. 
        override : Prints to console even if debug is off
    """
    kwargs.setdefault("override", False)
    msg = " ".join([str(arg) for arg in args])
    if UserConfig.DEBUG_MESSAGES or kwargs["override"]:
        print(msg)
    timestamp = time.strftime("[%d %h %H:%M:%S]")
    with open("scrape.log", "a") as f:
        f.write(timestamp + " " + msg + "\n")
    

# https://blog.codinghorror.com/sorting-for-humans-natural-sort-order/
def sort_nicely( l ):
    """ Sort the given list in the way that humans expect. """
    convert = lambda text: int(text) if text.isdigit() else text
    alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ]
    l.sort( key=alphanum_key )