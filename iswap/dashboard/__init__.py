from flask import Blueprint, url_for, render_template, redirect, request, flash, jsonify
from flask_login import login_required, current_user 
from .swapinfoform import CurrentInfoForm, ProfileUpdateForm, UpdatePassword
from iswap.staticdata import counties
from iswap.models import Teacher, CurrentInfo, db 
from sqlalchemy.orm.exc import FlushError
from iswap.utils import edit_picture
from .matchalgo import find_potential_swapmates 
from .sendsms import send_sms
from .dashutils import validate_select_fields, insertlocinfo

dashboard_bp = Blueprint('dashboard_bp',
                __name__, 
                static_folder='static',
                template_folder='templates')

"""
Landing page/feed for posted comments and swaps.
"""
@dashboard_bp.route('/home', methods=['GET', 'POST'])
@login_required
def timeline(): 
  all_teachers = Teacher.query.all()
  all_teachers.reverse()
  match_score, match_details = 0, None
  # Run a matching algorithm.
  match_result = find_potential_swapmates(current_user, all_teachers)
  if len(match_result):  
    match_details, match_score = match_result[0].values() 
    # Send notification to the matched teachers.
    teaching_level = current_user.current_info.teaching_level
    if (teaching_level == 'Primary' and match_score > 0) or \
       (teaching_level == 'Secondary' and match_score >= 4):
      send_sms(current_user)
      # Update matched status
      try:
        current_user.matched_status = True
        db.session.commit()
      except:
        pass 
  return render_template(
          'home.html', 
          teacher_swaps=all_teachers,
          match_score=match_score, 
          match_details = match_details
        )


"""
Handle current teacher personal and location information.
"""
@dashboard_bp.route('/swapinfo', methods=['GET', 'POST'])
@login_required
def swapinfo():
  # if the user has already updated current details, 
  # redirect to  target info.
  if current_user.current_info:
    return redirect(url_for('dashboard_bp.targetlocation'))
  form = CurrentInfoForm()
  if request.method == 'POST':
    # extract data from form in the request.
    curr_details = {
      'tchin_level': request.form.get('teaching_level'),
      'sch_name': request.form.get('school_name'),
      'county': request.form.get('county'),
      'subcounty': request.form.get('subcounty'),
      'sch_type': request.form.get('school_type'),
      'sch_gender': request.form.get('school_gender')
    }
    if request.form.get('teaching_level') == 'Secondary':
      # additional fields for secondary option.
      curr_details['sub_comb'] = request.form.get('subject_combination')
      curr_details['sch_category'] = request.form.get('school_category')
    
    # basic form validation
    for field in curr_details:
      if not curr_details[field]:
        flash('Please fill all the fields to continue!', 'danger')
        return redirect(url_for('dashboard_bp.swapinfo'))
    if not validate_select_fields(curr_details):
      flash('One of the values of your field is not valid!', 'danger')
      return redirect(url_for('dashboard_bp.swapinfo'))
     
    teacher_current_details = CurrentInfo(
      teaching_level = curr_details['tchin_level'],
      school_name = curr_details['sch_name'],
      school_type = curr_details.get('sch_type'),
      school_gender = curr_details['sch_gender'],
      school_category = curr_details.get('sch_category'),
      county = curr_details['county'],
      subcounty = curr_details['subcounty'],
      subject_comb = curr_details.get('sub_comb'),
      teacher_id = current_user.id
    )
    try:
      user = CurrentInfo.query.filter_by(teacher_id=current_user.id).first()
      if user:
        db.session.delete(user)
        db.session.commit()
      db.session.add(teacher_current_details)
      db.session.commit()
      flash('Current details updated successfully!', 'success') 
      return redirect(url_for('dashboard_bp.targetlocation')) 
    except FlushError as e:
      db.session.rollback()
      flash('An error occurred while processing your request.', 'danger')
      return redirect(url_for('dashboard_bp.swapinfo'))
    except Exception as e:
      db.session.rollback()
      flash('An error occurred. Please try again later.', 'danger')
      return redirect(url_for('dashboard_bp.swapinfo')) 
  return render_template('currinfo.html', form=form, counties=counties)


"""
Handle target location functionality.
"""
@dashboard_bp.route('/targetlocation', methods=['GET', 'POST'])
@login_required
def targetlocation():
  form = CurrentInfoForm()
  if request.method == 'POST':
    form_data = request.form.to_dict()
    return redirect(url_for('dashboard_bp.timeline'))
  return render_template('targetinfo.html', form=form, counties=counties)

"""
Implement advanced search functionality.
"""
@dashboard_bp.route('/advsearch', methods=['GET', 'POST'])
@login_required
def advsearch():
  return render_template('advsearch.html')

"""
Insert target data into the database.
"""
@dashboard_bp.route('/submitted', methods=['GET', 'POST'])
@login_required
def submitted(): 
  insertlocinfo(request.json) 
  return redirect(url_for('dashboard_bp.timeline'))

"""
Update phone, username and profile picture.
"""
@dashboard_bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
  form = ProfileUpdateForm()
  if form.validate_on_submit():
    phone, username = form.phone.data, form.username.data
    try:
      current_user.profile_pic = edit_picture(form)
      if phone:
        current_user.phone = phone
      if username:
        current_user.username = username
      db.session.commit()
      if any([phone, username, form.profile_photo.data]):
        flash('Profile updated successfully', 'success')
        return redirect(url_for('dashboard_bp.timeline'))
    except:
      db.session.rollback()
      flash('Failured to update profile', 'danger')
  return render_template('profile.html', form=form, page_title='Update Profile')

"""
Upadte user password.
"""
@dashboard_bp.route('/updatepwd', methods=['GET', 'POST'])
@login_required
def updatepwd():
  form = UpdatePassword()
  if form.validate_on_submit():
    if current_user.is_correct_password(form.current_pwd.data):
      try:
        current_user.set_password(form.new_pwd.data.strip()) 
        db.session.commit() 
        flash('Password changed successfully', 'success')
        return redirect(url_for('dashboard_bp.timeline'))
      except:
        db.session.rollback()
        flash('Error updating password. Please try again.','danger')
    else:
      flash('Incorrect current password!', 'danger')                                                      
  return render_template('changepwd.html', form=form, page_title='Update password')


"""
Swapmate Info
"""
@dashboard_bp.route('/matched')
@login_required
def matched(): 
  all_teachers = Teacher.query.all()
  match = find_potential_swapmates(current_user, all_teachers)[0]
  swapmate = None
  match_score = find_potential_swapmates(current_user, all_teachers)[0]['score']
  if current_user.current_info.teaching_level == 'Secondary':
    if match_score >= 4:
      swapmate = match['teacher']
  else:
    if match_score >= 0:
      swapmate = match['teacher']
  return render_template('match.html', swapmate=swapmate)


"""
API to fetch all counties and their subcounties.
"""
@dashboard_bp.route('/fetchsubcounties')
@login_required
def fetchsubcounties(): 
  return jsonify(counties) 


