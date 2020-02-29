# Playlist-Sync (incomplete)

- Python script to sync songs from multiple playlists into one. Helps to make sure your
bigger playlist has all the songs your smaller, more stylised playlists without 
personally having to add to both each time. 

# Setup

- You must create your own app at [Spotify for Developers](https://developer.spotify.com/), follow their instructions provided.
- After creating your app, you must export the following variables into your environment 
(either in bashrc, your PATH, or some other location for your variables): 
1. SPOTIFY_USERNAME : Your spotify username (if Facebook-connected, your username is the id number in your share link)
2. SPOTIFY_CLIENT_SECRET : Client secret provided for your created spotify app.
3. SPOTIFY_CLIENT_ID : Client ID provided for your created spotify app
4. SPOTIFY_REDIRECT_URI : Redirect URI used for your created app, can be something like http://localhost:3000/callback/

- Afterwards, while in the cloned directory, run the install script: 

`sudo ./install.sh`

* You should now be good to go, use command psync to start the script. If you ever want to reset after setup, 
just go ahead and delete the .playlist_sync.json file in your home directory to clean the configurations.
