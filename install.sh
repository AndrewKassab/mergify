# Installation script for Playlist-Sync

PYTHON_PATH="$(which python3)"
if [ -z "$PYTHON_PATH" ] 
then
  echo "Error, python3 not found, please before continuing."
  echo "Exiting installation..."
  exit
fi

HASH_BANG="#!${PYTHON_PATH}"

echo "Installing Playlist-Sync..."
cp sync_playlist.py psync
echo "Pointing script to python3."
(echo $HASH_BANG && cat psync) > psynctmp && mv psynctmp psync
chmod u+x psync 
echo "Installing and verifying dependencies..."
python3 -m pip install -r requirements.txt
echo "Moving script to PATH /usr/local/bin"
sudo mv psync /usr/local/bin
echo "Installation complete, run psync to get started."

