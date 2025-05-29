# Import required packages
import requests
import os

# Download the data required locally and prep the data for analysis.
def get_data(csv_file,filename="airlines-dash.csv"):
    req = requests.get(csv_file)
    with open(filename,"wb") as file:
        file.write(req.content)
        print(f"CSV file successfully downloaded: {filename}")
    if os.path.exists(filename):
        print("CSV file read successfully!")
    return filename

