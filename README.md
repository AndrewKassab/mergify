# Mergify

- Merge and sync up your spotify playlists!

# Development 

- Branch off of the development branch 
- You must create your own app at [Spotify for Developers](https://developer.spotify.com/), follow their instructions provided. 
- After creating your app, you will receive a Client ID and Client Secret. 
You must create a .env file in the app directory with the following fields:
1. MERGIFY_CLIENT_SECRET : Client secret provided for your created spotify app.
2. MERGIFY_CLIENT_ID : Client ID provided for your created spotify app
3. MERGIFY_REDIRECT_URI : Redirect URI used for your created app, can be something like http://localhost:5000/callback/

- After cloning the repostory, make sure you have dependencies installed by typing the following into root: 

`python3 -m pip install -r requirements.txt`

- After that, go ahead and execute `python3 __init__.py` from within the app directory

- Open `login.html` with VSCode Live Server 

