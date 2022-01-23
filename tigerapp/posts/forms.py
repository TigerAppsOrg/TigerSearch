from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import (StringField, SubmitField, TextAreaField,
                     SelectMultipleField, HiddenField)
from wtforms.fields.core import RadioField
from wtforms.validators import DataRequired, Length
from wtforms.widgets import ListWidget, CheckboxInput
from tigerapp.config import MAX_TITLE, MAX_DESCRIPTION, MAX_LOCATION
# ----------------------------------------------------------------------


class MultiCheckboxField(SelectMultipleField):
    """
    A multiple-select, except displays a list of checkboxes.

    Iterating the field will produce subfields, allowing 
    custom rendering of the enclosed checkbox fields.
    """
    widget = ListWidget(prefix_label=False)
    option_widget = CheckboxInput()
#----------------------------------------------------------------------


class PostForm(FlaskForm):
    """
    WTForm for creating a post. Does not include the option to choose
    what kind of post it is (lost/found.).
    """
    title = StringField("Title", validators=[DataRequired(),
                                             Length(max=MAX_TITLE)])
    description = TextAreaField("Description",
                                validators=[DataRequired(),
                                            Length(max=MAX_DESCRIPTION)])
    location = StringField("Location",
                           validators=[DataRequired(),
                                       Length(max=MAX_LOCATION)])
    location_tags = MultiCheckboxField("Location Tags")
    type_tags = MultiCheckboxField("Type Tags")
    inout_tags = MultiCheckboxField("Indoors/Outdoors Tags")
    upload = FileField('image', validators=[FileAllowed(
        ['jpg', 'png', 'jpeg'], 'Images only!')])

    submit = SubmitField("Post")
#----------------------------------------------------------------------

class EditForm(FlaskForm):
    """
    Form for editing a post. Difference between this and create form
    is that this allows you to change the type of the post.
    """
    imageCleared = HiddenField("")
    isFoundItem = RadioField(coerce=int,
                             choices=[(0, 'I lost something'),
                                      (1, 'I found something')])
    title = StringField("Title",
                        validators=[DataRequired(),
                                    Length(max=MAX_TITLE)])
    description = TextAreaField("Description",
                                validators=[DataRequired(),
                                            Length(max=MAX_DESCRIPTION)])
    location = StringField("Location",
                           validators=[DataRequired(),
                                       Length(max=MAX_LOCATION)])
    location_tags = MultiCheckboxField("Location Tags")
    type_tags = MultiCheckboxField("Type Tags")
    inout_tags = MultiCheckboxField("Indoors/Outdoors Tags")
    upload = FileField('image', validators=[FileAllowed(
        ['jpg', 'png', 'jpeg'], 'Images only!')])

    submit = SubmitField("Post")
# ----------------------------------------------------------------------
