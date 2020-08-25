from app.models import UserData

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError

# Form class when user wants to register an account
class RegisterUser(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2,max=20)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=5)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        userExit = UserData.query.filter_by(username=username.data).first()
        if userExit:
            raise ValidationError('Username has already been taken')

# Form class when user wants to login to their account
class LoginUser(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2,max=20)])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Log In')

# Form class when user wants to create a post on the forum
class CreatePost(FlaskForm):
    title = StringField('Post Title', validators=[DataRequired(), Length(min=2, max=100)])
    content = TextAreaField('Post Content', validators=[DataRequired(), Length(min=1)])
    submit = SubmitField('Create Post')

# Form class when user wants to create a comment of a post
class CreateComment(FlaskForm):
    content = TextAreaField(validators=[DataRequired()])
    submit = SubmitField('Add Comment')
