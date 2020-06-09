from flask_wtf import FlaskForm
from wtforms import SelectMultipleField, SelectField
from wtforms import validators, widgets


class MultiCheckboxField(SelectMultipleField):
    option_widget = widgets.CheckboxInput()
    widget = widgets.ListWidget(prefix_label=False)


class PlaylistForm(FlaskForm):

    source_playlists = MultiCheckboxField("Source Playlists", validators=[validators.DataRequired(
        "Please enter at least one source playlist")], choices=[])
    destination_playlist = SelectField("Destination Playlist", validators=[validators.DataRequired(
        "Please enter a destination playlist")], choices=[])
