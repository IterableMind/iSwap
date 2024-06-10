from flask import Blueprint, render_template, url_for, flash, redirect, request
from sqlalchemy.orm.exc import FlushError
from .forms import LoginForm, SignupForm
from iswap.models import Teacher, db
from flask_login import current_user, login_user, logout_user
from urllib.parse import urlsplit

auth_bp = Blueprint('auth_bp', __name__, static_folder='static', 
          template_folder='templates')

# Login logistics.
@auth_bp.route('/login', methods=['GET','POST'])
def login():
  if current_user.is_authenticated:
    return redirect(url_for('dashboard_bp.timeline'))
  login_form = LoginForm()
  if login_form.validate_on_submit():  
    teacher = Teacher.query.filter_by(username=login_form.username.data).first()
    if teacher is None or not teacher.is_correct_password(login_form.password.data):
      flash('Invalid username or password!', 'danger')
      return redirect(url_for('auth_bp.login'))
    login_user(teacher, remember=login_form.remember_me.data)
    next_page = request.args.get('next')
    if not next_page or urlsplit(next_page).netloc != '':
      next_page = url_for('dashboard_bp.timeline')
    return redirect(next_page)
  return render_template('login.html', login_form=login_form, page_title='Login')

# Create new Account
@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup(): 
  signup_form = SignupForm()
  if signup_form.validate_on_submit():
    # insert new teacher into the database.
    tr = Teacher(username=signup_form.username.data.strip(), 
                email=signup_form.email.data.strip(),
                phone=signup_form.phone.data)
    tr.set_password(signup_form.password.data.strip())
    try:
      db.session.add(tr)
      db.session.commit()
      flash('Accounty created successfully', 'success')
      return redirect(url_for('auth_bp.login'))
    except FlushError as e:
      db.session.rollback()
      flash('An error occurred while processing your request.', 'danger')
      return redirect(url_for('auth_bp.signup'))
    except Exception as e:
      db.session.rollback()
      flash('An error occurred. Please try again later.', 'danger')
      return redirect(url_for('auth_bp.signup'))
  return render_template('signup.html', signup_form=signup_form, page_title='Sign up')

@auth_bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('auth_bp.login'))
