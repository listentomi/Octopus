CREATE TABLE albums ([id], [name], [album_group], [album_type], [release_date], [popularity]);
CREATE TABLE artists ([name], [id], [popularity], [followers]);
CREATE TABLE audio_features ([id], [acousticness], [analysis_url], [danceability], [duration], [energy], [instrumentalness], [key], [liveness], [loudness], [mode], [speechiness], [tempo], [time_signature], [valence]);
CREATE TABLE genres ([id]);
CREATE TABLE r_albums_artists ([album_id], [artist_id]);
CREATE TABLE r_albums_tracks ([album_id], [track_id]);
CREATE TABLE r_artist_genre ([genre_id], [artist_id]);
CREATE TABLE r_track_artist ([track_id], [artist_id]);
CREATE TABLE tracks ([id], [disc_number], [duration], [explicit], [audio_feature_id], [name], [preview_url], [track_number], [popularity], [is_playable]);
