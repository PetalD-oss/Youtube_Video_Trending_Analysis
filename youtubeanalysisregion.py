import pandas as pd
import requests
from dotenv import load_dotenv
import os

# Load API key from .env
load_dotenv()
API_KEY = os.getenv('YOUTUBE_API_KEY')

# Regions to fetch trending videos from
regions = ['US', 'GB', 'IN', 'JP']

category_ID = {
    "1": "Film & Animation",
    "2": "Autos & Vehicles",
    "10": "Music",
    "15": "Pets & Animals",
    "17": "Sports",
    "18": "Short Movies",
    "19": "Travel & Events",
    "20": "Gaming",
    "21": "Videoblogging",
    "22": "People & Blogs",
    "23": "Comedy",
    "24": "Entertainment",
    "25": "News & Politics",
    "26": "Howto & Style",
    "27": "Education",
    "28": "Science & Technology",
    "30": "Movies",
    "31": "Anime/Animation",
    "33": "Classics",
    "34": "Comedy",
    "35": "Documentary",
    "36": "Drama",
    "37": "Family",
    "38": "Foreign",
    "39": "Horror",
    "40": "Sci-Fi/Fantasy",
    "41": "Thriller",
    "42": "Shorts",
    "43": "Shows",
    "44": "Trailers",
}

def get_trending_videos(api_key, region, max_results=10):
    url = (
        f'https://www.googleapis.com/youtube/v3/videos?part=snippet,statistics'
        f'&chart=mostPopular&regionCode={region}&maxResults={max_results}&key={api_key}'
    )
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(f"API request failed with status {response.status_code}: {response.text}")
    
    data = response.json()
    videos = []
    for item in data.get('items', []):
        snippet = item['snippet']
        stats = item.get('statistics', {})
        category_name = category_ID.get(snippet.get('categoryId', ''), 'Unknown')
        videos.append({
            'video_id': item['id'],
            'title': snippet.get('title', ''),
            'category': category_name,
            'published_at': snippet.get('publishedAt', ''),
            'view_count': int(stats.get('viewCount', 0)),
            'like_count': int(stats.get('likeCount', 0)),
            'comment_count': int(stats.get('commentCount', 0)),
            'region': region
        })

    return pd.DataFrame(videos)

if __name__ == '__main__':
    all_videos = pd.DataFrame()
    for region_code in regions:
        df = get_trending_videos(API_KEY, region_code, max_results=10)
        all_videos = pd.concat([all_videos, df], ignore_index=True)

    filename = 'youtube_trending_multiple_regions.csv'
    all_videos.to_csv(filename, index=False)
    print(f"Saved {len(all_videos)} records to {filename}")
    print(all_videos.head())
