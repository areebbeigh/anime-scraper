import os

# Windows
class IDM:
    def add_to_queue(self, directory, filename, url):
        """
        Uses the IDM comand line interface to add files to the main download queue
        """
        os.system('idman /d "{url}" /p "{directory}" /f "{filename}" /a'.format(url, directory, filename))

# Linux
class uGet:
    def add_to_queue(self, directory, filename, url):
        """
        Uses the uGet comand line interface to add files to the main download queue
        """
        os.system('uget-gtk --folder="{directory}" --filename="{filename} "{url}"" /a'.format(directory, filename, url))

