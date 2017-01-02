import os

with open("download_list.txt", "r") as f:
    lines = f.read().replace("\n", " ").split()

file_names = {}

count = 1
for line in lines:
    file_names[line.replace(line[0:len(line)-21], "")] = "Episode " + str(count) + ".mp4"
    count += 1

for file in os.listdir():
    if file in file_names:
        os.rename(file, file_names[file])
