from flask_wtf import Form
from wtforms import SelectMultipleField, SelectField, SubmitField


class PlaylistForm(Form):

    submit_button = SubmitField("Sync")
    source_playlists = SelectMultipleField("Source Playlists", choices=[])
    destination_playlist = SelectField("Destination Playlist", choices=[])
