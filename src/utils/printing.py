def fetching_episode(episode_name, stream_page):
    tag = "[ FETCHING ]"
    print(tag, episode_name, stream_page)

def fetched_episode(episode_name, stream_url, success):
    tag = "[ SUCCESS ] " if success else "[ FAILED  ] "
    print(tag, episode_name, stream_url, end="\n\n")

def fetching_list(anime_url):
    print("Fetching episode list ;", anime_url, end="\n\n")
