from flask_wtf import FlaskForm
from wtforms import SelectMultipleField, SelectField, SubmitField


class PlaylistForm(FlaskForm):

    submit_button = SubmitField("Sync")
    source_playlists = SelectMultipleField("Source Playlists", choices=[])
    destination_playlist = SelectField("Destination Playlist", choices=[])
