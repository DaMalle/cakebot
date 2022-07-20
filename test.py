import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

client_id = "3a1bb44c79e5465198d87d7264418758"
client_secret = "6b0add94e43647c39ce76b7d6a29c3e2"
spotify_api = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
    client_id=client_id, client_secret=client_secret)
)
raw_query = "https://open.spotify.com/album/4Rt7yYIgA9wfud6wQCzQWs?si=zKqac2d1R5upMOjYurKBPg"

query = raw_query.split("/")[-1]
# result = spotify_api.search(q="artist: tobias rahim", type="artist")
result = spotify_api.album_tracks(
        album_id=query,
        market="DK"
)
test = result["tracks"]["items"]

print([f'{track["artists"][0]["name"]} {track["name"]}' for track in result["tracks"]["items"]])
