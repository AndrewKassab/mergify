from flask_wtf import FlaskForm
from wtforms import SelectMultipleField, SelectField, SubmitField
from wtforms import validators, ValidationError


class PlaylistForm(FlaskForm):

    submit_button = SubmitField("Sync")
    source_playlists = SelectMultipleField("Source Playlists", validators=[validators.DataRequired(
        "Please enter at least one source playlist")], choices=[])
    destination_playlist = SelectField("Destination Playlist", validators=[validators.DataRequired(
        "Please enter a destination playlist")], choices=[])
