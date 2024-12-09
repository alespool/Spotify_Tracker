import spotipy
import spotipy.util as util
import pandas as pd
import seaborn as sns
import os
import matplotlib.pyplot as plt

cid = ''
secret = ''
redirect_uri = ''

scope = 'user-top-read'
ranges = ['short_term', 'medium_term', 'long_term']

token = util.prompt_for_user_token('ale.nespolo',scope,client_id=cid,client_secret=secret,redirect_uri=redirect_uri)
spotify = spotipy.Spotify(auth=token)

data = []

for sp_range in ranges:
    print(f"Fetching top artists for range: {sp_range}")

    results = spotify.current_user_top_artists(time_range=sp_range, limit=15)

    for item in results['items']:
        artist_genres = item['genres']

        # Append each genre separately
        for genre in artist_genres:
            data.append({'time_range': sp_range, 'genre': genre})

genres_df = pd.DataFrame(data)
print(genres_df.head())

categories = {
    'Rock and Metal': [
        'alternative metal', 'nu metal', 'post-grunge', 'groove metal', 'metal',
        'hard rock', 'stoner metal', 'death metal', 'speed metal',
        'thrash metal', 'modern rock', 'alternative rock', 'funk metal',
        'virginia metal', 'french death metal', 'nu-metalcore', 'metalcore', 
        'french metal', 'progressive groove metal'
    ],
    'Mandopop': [
        'mandopop', 'c-pop', 'taiwan pop', 'zhongguo feng', 'cantopop', 
        'singaporean pop', 'singaporean mandopop', 'classic mandopop', 
        'chinese viral pop', 'chinese r&b', 'cantopop'
    ],
    'Hip Hop and Rap': [
        'rap metal', 'alternative hip hop', 'detroit hip hop', 'hip hop', 'rap'
    ],
    'Pop' : [
        'pop', 'pop rock'
    ],
    'Electronic and Techno': [
        'german house', 'german techno', 'high-tech minimal', 'minimal techno'
    ],
    'Folk and World Music': [
        'mongolian folk', 'throat singing'
    ],
    'Other/Uncategorized': [
        'ukrainian post-punk', 'grunge', 'stoner rock', 
    ]
}

def categorize_genre(genre):
    for category, genres in categories.items():
        if genre in genres:
            return category
    return 'Other/Uncategorized'

genres_df['category'] = genres_df['genre'].apply(categorize_genre)
genres_df['count'] = 1

category_summary = genres_df.groupby(['time_range','category'])['count'].sum().reset_index()
category_summary = category_summary.sort_values(by='count', ascending=False)

print(category_summary)

## Heatmap plot
heatmap_df = category_summary.pivot(index='category', columns='time_range', values='count').fillna(0)

plt.figure(figsize=(10, 6))
sns.heatmap(heatmap_df, annot=True, fmt=".0f", cmap="coolwarm", linewidths=0.5)
plt.title('Category Counts Across Time Ranges')
plt.ylabel('Category')
plt.xlabel('Time Range')
plt.tight_layout()
plt.show()

## Area plot
stacked_df = category_summary.pivot(index='time_range', columns='category', values='count').fillna(0)

stacked_df.plot(kind='area', stacked=True, figsize=(12, 8), colormap='tab10', alpha=0.8)
plt.title('Category Trends Over Time Ranges')
plt.xlabel('Time Range')
plt.ylabel('Count')
plt.legend(title='Category', loc='upper left')
plt.grid(True)
plt.tight_layout()
plt.show()

## Facet grids plot
facet_df = category_summary.copy()
facet_df['count'] = facet_df['count'].astype(int)

g = sns.FacetGrid(facet_df, col="time_range", sharex=True, sharey=True, height=4, aspect=1.5)
g.map(sns.barplot, "count", "category", order=facet_df['category'].unique(), hue=facet_df["category"], legend=False, palette="viridis")
g.set_titles("{col_name}")
g.set_axis_labels("Count", "Category")
g.figure.subplots_adjust(top=0.9)
g.figure.suptitle("Category Counts by Time Range")
plt.show()
