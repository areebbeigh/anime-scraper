import os
import json

from src import scraper

with open("hash_map.json", "r") as f:
    episodes_dict = json.loads(f.read())

print("\nEnter the path to the location where you want to save the episodes:")
local_path = input("> ")
while not os.path.isdir(local_path):
    print("The given path is not a directory or it does not exist.")
    local_path = input("> ")

scraper.add_to_idm(episodes_dict, local_path)
