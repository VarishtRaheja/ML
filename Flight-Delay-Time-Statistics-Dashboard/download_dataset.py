from random import randint
import requests
from pathlib import Path
import time

class File:
    def __init__(self,url):
        self.url = url.content

    def download_file(self,filename):
        file_path = Path(filename)
        if file_path.exists():
            print(f"The file '{filename}' already exists.")
        # Create a time delay.
        time.sleep(randint(1, 5))

        with open(filename,"wb") as f:
            f.write(self.url)
            print(f"The file {filename} has been downloaded.")

url = requests.get('https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-'
                   'SkillsNetwork/Data%20Files/airline_data.csv')

File(url=url).download_file("airline_data.csv")


