import os

def add_to_idm(hash_map, local_path):
    """
    Uses the IDM comand line utility to add the episode download URLs to the download queue in IDM
        hash_map: A dictionary with episode download URLs mapped to their names
    """
    for url in hash_map:
        os.system('idman /d "{0}" /p "{1}" /f "{2}" /a'.format(url, local_path, hash_map[url] + ".mp4"))
