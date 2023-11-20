from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, IntegerField, DecimalField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign In')

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(),Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

class ImageAlbumForm(FlaskForm):
    name = StringField('Image Album Name')
    thumbnail = StringField('Thumbnail Img url', validators=[DataRequired()])
    submit = SubmitField('Add Photo to Album')

class UpdateAlbumForm(FlaskForm):
    name = StringField('Image Album Name')
    thumbnail = StringField('Thumbnail Img url', validators=[DataRequired()])
    submit = SubmitField('Update Album')


class ImageForm(FlaskForm):
    name = StringField('Image Name')
    thumbnail = StringField('Img url', validators=[DataRequired()])
    submit = SubmitField('Add Photo to Album')

class UpdateImageForm(FlaskForm):
    name = StringField('Image Album Name')
    thumbnail = StringField('Thumbnail Img url', validators=[DataRequired()])
    submit = SubmitField('Update Image')