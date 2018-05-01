import re

from .servers import StreamServers


def get_stream_url_regex(server):
    """
    Returns a list of compiled stream URL regex objects for given server
    """
    patterns = {
        StreamServers.OPENUPLOAD: [r"[\"'](http:\/\/|https:\/\/)*([a-z0-9][a-z0-9\-]*\.)*(oloadcdn)\.net(\/dl\/.+?)[\"']"],
        StreamServers.MP4UPLOAD: [r"[\"'](http:\/\/|https:\/\/)*([a-z0-9][a-z0-9\-]*\.)*(mp4upload)\.com:[0-9]*(\/d\/.+?)[\"']"],
        StreamServers.YOURUPLOAD: [r"[\"'](http:\/\/|https:\/\/)*([a-z0-9][a-z0-9\-]*\.)*(vidcache)\.net:[0-9]*(\/play\/.+?)[\"']"]
    }

    if server in patterns:
        return [re.compile(pattern) for pattern in patterns[server]]

    raise ValueError("Regex for server %s stream url does not exist" % server)
