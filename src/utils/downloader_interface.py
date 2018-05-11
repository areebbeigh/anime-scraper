import os

from src.utils import printd

# Windows
class IDM:
    def __str__(self):
        return "Internet Download Manager"

    def add_to_queue(self, directory, filename, url):
        """
        Uses the IDM comand line interface to add files to the main download queue
        """
        command = 'idman /d "{0}" /p "{1}" /f "{2}" /a'.format(url, directory, filename)
        printd(command)
        os.system(command)

# Linux
class uGet:
    def __str__(self):
        return "uGet Download Manager"

    def add_to_queue(self, directory, filename, url):
        """
        Uses the uGet comand line interface to add files to the main download queue
        """
        command = 'uget-gtk --quiet --folder="{1}" --filename="{2}" "{0}"'.format(url, directory, filename)
        printd(command)
        os.system(command)

