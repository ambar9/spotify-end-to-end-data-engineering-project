import json
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import os
import boto3
from datetime import datetime

def lambda_handler(event, context):
    client_id = os.environ.get('client_id')
    client_secret = os.environ.get('client_secret')
    
    client_credentials_manager = SpotifyClientCredentials(client_id = client_id, client_secret = client_secret)
    playlist_link = "https://open.spotify.com/playlist/37i9dQZEVXbMDoHDwVN2tF"
    
    
    sp = spotipy.Spotify(client_credentials_manager = client_credentials_manager)
    playlist_URI = playlist_link.split('/')[-1]
    
    spotify_data = sp.playlist_tracks(playlist_URI)
    playlists = sp.user_playlists('spotify')
    
    client = boto3.client('s3')
    filename = "spotify_raw_" + str(datetime.now()) + ".json"
    
    client.put_object(
        Bucket = "spotify-etl-project-ambar",
        Key = "raw_data/to_processed/" + filename,
        Body = json.dumps(spotify_data)
        )
    
    
