# Playlist-Sync (incomplete)

- Python script to sync songs from multiple playlists into one. Makes it easier for me to 
make sure my bigger playlist has all the songs from my smaller, more stylised playlists without 
personally having to add to both each time. Makes sure to avoid duplicate songs.

# Setup

- You must create your own app at [Spotify for Developers](https://developer.spotify.com/), follow their instructions provided.
- After creating your app, you must export the following variables into your environment: 
1. SPOTIFY_USERNAME : Your spotify username 
2. SPOTIFY_CLIENT_SECRET : Client secret provided for your created spotify app.
3. SPOTIFY_CLIENT_ID : Client ID provided for your created spotify app
4. SPOTIFY_REDIRECT_URI : Redirect URI used for your created app, can be something like http://localhost:3000/callback/
