import requests
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv('YOUTUBE_API_KEY')

#region code to extract category ID's to understand particular genres of videos 
region_code = 'UK'

url = f"https://www.googleapis.com/youtube/v3/videoCategories?part=snippet&regionCode={region_code}&key={API_KEY}"

response = requests.get(url)
data = response.json()

# Prints the category names corresponding to the ID 
for item in data['items']:
    print(f"{item['id']}: {item['snippet']['title']}")