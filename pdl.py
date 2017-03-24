# Prepare download list
import os
import argparse
import json

from src import scraper

parser = argparse.ArgumentParser()
parser.add_argument("url", help="URL to the page of the list of episodes of the anime")
parser.add_argument("--start", "-s", type=int, help="The episode number to start fetching from")
parser.add_argument("--end", "-e", type=int, help="The episode number to stop fetching at")

args = parser.parse_args()

start = 0 if not args.start else args.start
end = 0 if not args.end else args.end

res = scraper.get_episodes_dictionary(args.url, start, end)
episodes_dict = res[0]
failed_episodes = res[1]

print("\nSuccessfuly fetched", str(len(episodes_dict)), "episodes.")
print("Failed to fetch", str(len(failed_episodes)), "episodes.")

print("\nWriting download_list.txt...")
with open("download_list.txt", "w") as f:
    for url in episodes_dict:
        f.write(url + "\n")

if failed_episodes:
    print("\nWriting failed.txt...")
    with open("failed.txt", "w") as f:
        for ep in failed_episodes:
            f.write(ep + "\n")

print("\nWriting hash_map.json...")
with open("hash_map.json", "w") as f:
    f.write(json.dumps(episodes_dict, indent=4, separators=(',', ': ')))

print("\nDo you want to add the fetched download URLs to IDM? (Y/N)")
response = input("> ")

if response.lower() in ["y", "yes"]:
    print("\nEnter the path to the location where you want to save the episodes:")
    local_path = input("> ")
    while not os.path.isdir(local_path):
        print("The given path is not a directory or it does not exist.")
        local_path = input("> ")

    scraper.add_to_idm(episodes_dict, local_path)
