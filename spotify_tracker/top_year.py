from daily_tracker import combined_df


combined_df['count_played'] = 1
top_songs_year = combined_df.groupby(['track'], 
                                as_index=False)['count_played'].sum().sort_values(by='count_played',
                                ascending=False).reset_index(drop=True).head(10)

print(top_songs_year)

top_artist_year = combined_df.groupby(['artist'],
                                as_index=False)['count_played'].sum().sort_values(by='count_played',
                                ascending=False).reset_index(drop=True).head(10)

print(top_artist_year)

top_albums_year = combined_df.groupby(['album'], 
                                as_index=False)['count_played'].sum().sort_values(by='count_played',
                                ascending=False).reset_index(drop=True).head(10)

print(top_albums_year)