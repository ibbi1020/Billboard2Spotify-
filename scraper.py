from bs4 import BeautifulSoup
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os
from dotenv import load_dotenv

load_dotenv()
CLIENT_ID = os.getenv('client_id')
CLIENT_SECRET = os.getenv('client_secret')
URI = os.getenv('uri')

URL = "https://www.billboard.com/charts/hot-100/2001-09-11/"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
}
html_doc = requests.get(URL, headers=headers)

soup = BeautifulSoup(html_doc.text, 'html.parser')
titles_1 = soup.find('h3', class_ = 'c-title a-no-trucate a-font-primary-bold-s u-letter-spacing-0021 u-font-size-23@tablet lrv-u-font-size-16 u-line-height-125 u-line-height-normal@mobile-max a-truncate-ellipsis u-max-width-245 u-max-width-230@tablet-only u-letter-spacing-0028@tablet')
titles_99 = soup.find_all('h3', class_ = 'c-title a-no-trucate a-font-primary-bold-s u-letter-spacing-0021 lrv-u-font-size-18@tablet lrv-u-font-size-16 u-line-height-125 u-line-height-normal@mobile-max a-truncate-ellipsis u-max-width-330 u-max-width-230@tablet-only')

titles = []
titles.append(titles_1.get_text(strip=True))

for title in titles_99:
    titles.append(title.get_text(strip = True))

#auth manager
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id = CLIENT_ID,
    client_secret = CLIENT_SECRET,
    redirect_uri=URI,
    scope = 'playlist-modify-private playlist-modify-public'
))

#get user information
user = sp.current_user()
print(f"Logged in as: {user['display_name']}")

#find track_uris
track_uris = []
for title in titles:
    result = sp.search(q=title, limit=1, type='track')
    if result['tracks']['items']:
        track = result['tracks']['items'][0]
        track_uris.append(track['uri'])
    else:
        print(f"Track URI for {title} not found")
        track_uris.append("spotify:track:4PTG3Z6ehGkBFwjybzWkR8")

print(f"Track URIs: {track_uris}")

#create playlist
playlist_name = 'Billboard Top 100 on 11-9-2001'
playlist_desc = 'Songs on Billboards Top 100 list on 11-9-2001. Hello Shaheera :)'
user_id = sp.current_user()['id']

playlist = sp.user_playlist_create(
    user = user_id,
    name = playlist_name,
    description= playlist_desc,
    public=True
)

print(f"Playlist {playlist['name']} created")

sp.playlist_add_items(playlist_id=playlist['id'], items = track_uris)
print(f"Tracks added to playlist {playlist_name}")




