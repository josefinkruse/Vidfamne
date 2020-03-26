from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, RadioField, DateField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flaskblog.models import User, Folder


class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')


class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class UpdateAccountForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is taken. Please choose a different one.')


# *** This need to be changed!   More than this?
class PictureForm(FlaskForm):
#    title = StringField('Title', validators=[DataRequired()])
#    content_type = RadioField('Content type', validators=[DataRequired()], choices=[('plain', 'Plain Text'), ('html', 'HTML'), ('markdown', 'Markdown')])
    image_file = FileField('Add an image file', validators=[FileAllowed(['jpg', 'png'])])
#    date_taken = TextAreaField('Date the photo was taken (YYYY-MM-DD)')
    date_taken = DateField('Date the photo was taken')
    place_taken = TextAreaField('Place')
    description = TextAreaField('Description') # , validators=[DataRequired()])
#    image_folder = RadioField('Folder', validators=[DataRequired()], choices=[('plain', 'Plain Text'), ('html', 'HTML'), ('markdown', 'Markdown')])
    submit = SubmitField('Upload')


# *** Add a class for creating a folder   More?
class FolderForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    start_date = TextAreaField( 'Date trip started (YYYY-MM-DD)', validators=[DataRequired()] )
    end_date = TextAreaField( 'Date trip ended (YYYY-MM-DD)', validators=[DataRequired()] )
    destinations = StringField('Destinations', validators=[DataRequired()])
    description = TextAreaField('Description')
    folder_image = FileField('Add a folder image', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Create')

    def validate_folder_title(self, title):
        folder = Folder.query.filter_by(title=title.data).first()
        if folder:
            raise ValidationError('That folder name is taken. Please choose a different one.')

class CommentForm(FlaskForm):
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Send comment')
