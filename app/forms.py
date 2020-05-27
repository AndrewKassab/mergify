from flask_wtf import Form
from wtforms import SelectMultipleField, SelectField, SubmitField


class PlaylistForm(Form):

    submit_button = SubmitField("Sync")

    def __init__(self, playlist_names):
        self.source_playlists = SelectMultipleField("Source Playlists", choices=playlist_names)
        self.destination_playlist = SelectField("Destination Playlist", choices=playlist_names)
