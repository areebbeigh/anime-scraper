from src.scrape_utils.servers import StreamServers

class UserConfig:
    DEBUG_MESSAGES = True
    STREAM_SERVER = StreamServers.MP4UPLOAD # Prefered streaming host


class TimeoutConfig:
    # Timeout values in seconds for...
    FETCHING_EPISODE_LIST = 15
    FETCHING_EPISODE_STREAM = 15
    KILLING_EXTRA_TABS = 5
