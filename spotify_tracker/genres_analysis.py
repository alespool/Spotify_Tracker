import spotipy
import spotipy.util as util
import pandas as pd
from datetime import datetime, timedelta
import os

cid = ''
secret = ''
redirect_uri = ''

scope = 'user-top-read'
ranges = ['short_term', 'medium_term', 'long_term']

token = util.prompt_for_user_token('ale.nespolo',scope,client_id=cid,client_secret=secret,redirect_uri=redirect_uri)
spotify = spotipy.Spotify(auth=token)

genres = {
    'short_term': [],
    'medium_term': [],
    'long_term': []
}

for sp_range in ['short_term', 'medium_term', 'long_term']:
    print("range:", sp_range)

    results = spotify.current_user_top_artists(time_range=sp_range, limit=10)

    for i, item in enumerate(results['items']):
        print(f"{i+1}) {item['name']} - ({item['genres']})")
        genres[sp_range].append(item['genres']) 
        if item['genres'] in genres[sp_range]:
            continue
    print()

genres_df = pd.DataFrame.from_dict(genres)
print(genres_df)