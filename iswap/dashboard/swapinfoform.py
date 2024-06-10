from flask_wtf import FlaskForm
from flask_wtf.file import FileField
from wtforms import SelectField, StringField, IntegerField
from wtforms.validators import DataRequired
from iswap.models import Teacher
from wtforms.validators import ValidationError, EqualTo
from wtforms import PasswordField
from flask_login import current_user
from iswap.staticdata import subject_comb, school_category, school_gender, \
    school_type, countylist

teaching_level = ['Primary', 'Secondary']

class CurrentInfoForm(FlaskForm):
    school_name = StringField('School Name', validators=
                [DataRequired(message='You must provide your current school name!')]) 
    teaching_level = SelectField('Teaching Level', 
                choices=[('', 'Teaching Level', {'disabled': True}), 
                ('Primary', 'Primary'), ('Secondary', 'Secondary')])
    
    counties = SelectField('County', choices=countylist)
    school_category = SelectField('School Category', choices=school_category)
    school_type = SelectField('School Type', choices=school_type)
    school_gender = SelectField('School Gender', choices=school_gender)
    subject_combination = SelectField('Subject Combination', choices=subject_comb)

class ProfileUpdateForm(FlaskForm):
    username = StringField('Username')
    phone = StringField('Phone')
    profile_photo = FileField('Upload profile Photo')

    def validate_username(self, username):
    # check if the entered username is already in the database. 
        if Teacher.query.filter_by(username=username.data).first():
            raise ValidationError('This username is already taken!')
        
class UpdatePassword(FlaskForm):
    current_pwd = PasswordField('Current Password', validators=[DataRequired(message='Please enter current password!')])
    new_pwd = PasswordField('New Password', validators=[DataRequired(message='Please enter new password!')])
    confirm_pwd = PasswordField('Confirm Password', validators=
            [DataRequired(message='Please confirm new password!'), EqualTo('new_pwd', message="Password didn't match!")])
    
