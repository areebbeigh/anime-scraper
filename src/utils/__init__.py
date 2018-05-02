import re
# https://blog.codinghorror.com/sorting-for-humans-natural-sort-order/
def sort_nicely( l ):
    """ Sort the given list in the way that humans expect. """
    convert = lambda text: int(text) if text.isdigit() else text
    alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ]
    l.sort( key=alphanum_key )