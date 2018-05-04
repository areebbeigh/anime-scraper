def extract_episode_number(episode_name):
    episode_number = episode_name.replace("Episode ", "")
    
    if episode_number.isdigit():
        return int(episode_number)
    return ""