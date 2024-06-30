from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
import os
from iswap import db, login
from flask_login import UserMixin
from flask import url_for
from iswap import app

@login.user_loader
def load_user(id):
    return db.session.get(Teacher, int(id))


class Teacher(UserMixin, db.Model):
  __tablename__ = 'teachers'
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(64), index=True, unique=True)
  email = db.Column(db.String(120), index=True, unique=True)
  phone = db.Column(db.Integer)
  pw_hash = db.Column(db.String(128))
  transfer_update_status = db.Column(db.String, default='False')
  current_info = db.relationship('CurrentInfo', backref='teacher', uselist=False)
  target_info = db.relationship('TargetLoc', backref='targetloc', uselist=False)
  profile_pic = db.Column(db.String(200))
  matched_status = db.Column(db.Boolean, default=False)
  
  def set_password(self, password):
    self.pw_hash = generate_password_hash(password)
  
  def is_correct_password(self, password):
    return check_password_hash(self.pw_hash, password)

  @property
  def profile_pic_path(self):
    """Returns the full path to the profile picture."""
    if self.profile_pic: 
      return os.path.join(app.root_path, 'static', 'images', 'profile_pictures', self.profile_pic)
    else:
        # Return a default image path if no profile picture is set
        return os.path.join(app.root_path, 'static', 'images', 'profile_pictures', 'default_profile.pic.png')

  def get_profile_pic_url(self):
    """Returns the URL to load the profile picture in templates.""" 
    if self.profile_pic:
      return url_for('static', filename='images/profile_pictures/' + self.profile_pic)
    else:
       return url_for('static', filename='images/profile_pictures/default_pic.PNG')
  
  def __repr__(self):
    # For debugging purposes only.
    return '<User {}>'.format(self.username)
  

class CurrentInfo(db.Model):
  __tablename__ = 'currentinfo'
  id = db.Column(db.Integer, primary_key=True)
  school_name = db.Column(db.String(200), nullable=False)
  county = db.Column(db.String(64), nullable=False)
  subcounty = db.Column(db.String(64), nullable=False)
  teaching_level = db.Column(db.String(64), nullable=False)
  school_category = db.Column(db.String(64), default=None)
  school_type = db.Column(db.String(64), default=None)
  school_gender = db.Column(db.String(64))
  subject_comb = db.Column(db.String(64), default=None)
  teacher_id = db.Column(db.Integer, db.ForeignKey('teachers.id'), unique=True, nullable=False)
  

class TargetLoc(db.Model):
  __tablename__ = 'targetlocs'
  id = db.Column(db.Integer, primary_key=True)
  county1 = db.Column(db.String(64), nullable=False)
  subcounty1 = db.Column(db.String(64), nullable=False)
  county2 = db.Column(db.String(64), nullable=False)
  subcounty2 = db.Column(db.String(64), nullable=False)
  county3 = db.Column(db.String(64), nullable=False)
  subcounty3 = db.Column(db.String(64), nullable=False)
  teacher_id = db.Column(db.Integer, db.ForeignKey('teachers.id'), unique=True, nullable=False)
  updated_on = db.Column(db.DateTime, default=datetime.utcnow)

