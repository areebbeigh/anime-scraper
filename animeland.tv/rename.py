import os
import json

with open("hash_map.json", "r") as f:
    episode_mapping = json.loads(f.read())

for url in episode_mapping:
    for file_ in os.listdir():
        if url.endswith(file_):
            os.rename(file_, episode_mapping[url] + ".mp4")
