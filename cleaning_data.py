import pandas as pd 

df = pd.read_csv("youtube_trending_multiple_regions.csv")
df['published_at'] = pd.to_datetime(df['published_at'])
df[['view_count', 'like_count','comment_count']] = df[['view_count', 'like_count', 'comment_count']].astype(int)

#adding an new column that checks the engagement rate of the particular video 
df['engagement rate'] = (df['like_count'] + df['comment_count']) / df['view_count']

df['hour'] = df['published_at'].dt.hour
df['day_of_week'] = df['published_at'].dt.day_name()

df.to_csv("youtube_trending_region.csv", index=False)
print("Cleaned data saved!")
