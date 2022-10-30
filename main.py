from bs4 import BeautifulSoup
import requests
import spotipy
from credentials import spotify_client_id, spotify_client_secret, spotify_redirect_url
from spotipy.oauth2 import SpotifyClientCredentials

SPOTIPY_CLIENT_ID = spotify_client_id
SPOTIPY_CLIENT_SECRET = spotify_client_secret
SPOTIPY_REDIRECT_URL = spotify_redirect_url

spotify_auth = spotipy.oauth2.SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID,
                                           client_secret=SPOTIPY_CLIENT_SECRET,
                                           redirect_uri=SPOTIPY_REDIRECT_URL,
                                           scope="playlist-modify-private",
                                           cache_path="token.txt"
                                           )

BB_URL = "https://www.billboard.com/charts/hot-100/"
date = "1981-01-22"  # input("Which year do you want to travel to? Type the date in this format YYYY-MM-DD: ")

dated_url = f"{BB_URL}{date}/"
response = requests.get(dated_url)
billboard_page = response.text

soup = BeautifulSoup(billboard_page, "html.parser")
titles = soup.find_all(class_="o-chart-results-list-row-container")

songs = []
artists = []

for title in titles:
    song_tag = title.select_one("h3")
    song = song_tag.getText()
    songs.append(song.strip())

    artist_tag = song_tag.find_next_sibling()
    artist = artist_tag.getText()
    artists.append(artist.strip())

song_uris = []
year = date.split("-")[0]

sp = spotipy.Spotify(oauth_manager=spotify_auth)

for song in songs:
    result = sp.search(q=f"track:{song} year:{year}", type="track")
    print(result)
    # try:
    #     uri = result["tracks"]
