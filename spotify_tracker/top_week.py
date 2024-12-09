from daily_tracker import combined_df
from datetime import datetime, timedelta

combined_df['count_played'] = 1

today = datetime.today()

start_of_week = today - timedelta(days=today.weekday())
end_of_week = start_of_week + timedelta(days=6)

week_df = combined_df[(combined_df['played_at'] >= start_of_week) & (combined_df['played_at'] <= end_of_week)]

top_songs_week = week_df.groupby(['track'], 
                                as_index=False)['count_played'].sum().sort_values(by='count_played',
                                ascending=False).reset_index(drop=True).head(10)

print(top_songs_week)

top_artist_week = week_df.groupby(['artist'],
                                as_index=False)['count_played'].sum().sort_values(by='count_played',
                                ascending=False).reset_index(drop=True).head(10)

print(top_artist_week)

top_albums_week = week_df.groupby(['album'], 
                                as_index=False)['count_played'].sum().sort_values(by='count_played',
                                ascending=False).reset_index(drop=True).head(10)

print(top_albums_week)