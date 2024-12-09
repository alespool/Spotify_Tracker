import spotipy
import spotipy.util as util
import pandas as pd
from datetime import datetime, timedelta
import os

cid = ''
secret = ''
redirect_uri = ''

scope = 'user-read-recently-played'

token = util.prompt_for_user_token('',scope,client_id=cid,client_secret=secret,redirect_uri=redirect_uri)
spotify = spotipy.Spotify(auth=token)

def chunks(tracks, n):
    """Yield successive n-sized chunks from tracks."""
    for i in range(0, len(tracks), n):
         yield tracks[i:i + n]

time_24_hours_ago = int((datetime.now() - timedelta(hours=24)).timestamp() * 1000)

results = spotify.current_user_recently_played(limit=50, after=time_24_hours_ago)
items = results.get('items', [])

tracks = {
    'artist': [],
    'album': [],
    'track': [],
    'release_date': [],
    'song_duration(ms)': [],
    'played_at': []
}

for item in items:
    tracks['artist'].append(item['track']['artists'][0]['name'])
    tracks['album'].append(item['track']['album']['name'])
    tracks['track'].append(item['track']['name'])
    tracks['release_date'].append(item['track']['album']['release_date'])
    tracks['song_duration(ms)'].append(item['track']['duration_ms'])
    tracks['played_at'].append(pd.to_datetime(item['played_at']).strftime('%Y-%m-%d %H:%M:%S'))

songs_df = pd.DataFrame.from_dict(tracks)

songs_df['release_date'] = pd.to_datetime(songs_df['release_date'],format='ISO8601').dt.date
songs_df['played_at'] = pd.to_datetime(songs_df['played_at'])

excel_file = 'songs.xlsx'

if os.path.exists(excel_file):
    existing_df = pd.read_excel(excel_file)
else:
    existing_df = pd.DataFrame()

if not existing_df.empty:
    combined_df = pd.concat([existing_df, songs_df]).drop_duplicates(subset=['played_at'], keep='first')
else:
    combined_df = songs_df

combined_df.to_excel(excel_file, index=False)

print(f"Songs updated. Total songs recorded: {len(combined_df)}")
print(combined_df.head())