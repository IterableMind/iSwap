from iswap import FlaskForm, StringField, PasswordField, BooleanField
from iswap import DataRequired, Length, EqualTo, Email, IntegerField
from wtforms.validators import ValidationError
from iswap.models import Teacher 


class LoginForm(FlaskForm):
  username = StringField('Username', 
                          validators=[DataRequired(message=
                          'Please provide a username to login!')])
  password = PasswordField('Password', 
                          validators=[DataRequired(message=
                          'Password field cannot be empty!')])
  remember_me = BooleanField('Remember me')


class SignupForm(FlaskForm):
  username = StringField('Username', 
                         validators=[DataRequired(message=
                         'Username MUST be provided!')])
  password = PasswordField('Password', 
                          validators=[DataRequired(message=
                          'Please Create your password!'), 
                          Length(min=6, message=
                         'Password Must be more than 5 characters long!')])
  confirm_password = PasswordField('Confirm Password',
                          validators=[DataRequired(message=
                          'Please confirm your password!'), 
                          EqualTo('password', message='Password MUST Match!')])
  email = StringField('Email', validators=[DataRequired(), Email()])
  phone = IntegerField('Phone', validators=[DataRequired(message='Phone number is needed!')])

  def validate_username(self, username):
    # check if the entered username is already in the database. 
    if Teacher.query.filter_by(username=username.data).first():
        raise ValidationError('This username is already taken!')
          
  def validate_email(self, email):
    # check if the entered email is already in the database. 
    if Teacher.query.filter_by(email=email.data).first():
        raise ValidationError('There is a teacher registered with this email!')