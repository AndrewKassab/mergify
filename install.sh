# Installation script for Playlist-Sync
echo "Installing Playlist-Sync"
cp sync_playlist.py psync
chmod u+x psync 
sudo mv psync /usr/local/bin
echo "Installation complete, restart terminal and run psync to get started."
