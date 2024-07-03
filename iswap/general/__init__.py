from flask import Blueprint, render_template, url_for
from .mainforms import SearchForm, FeedbackForm
from iswap.models import Teacher, db
from iswap.staticdata import fake_data
from sqlalchemy import func

land_bp = Blueprint('land_bp', __name__,
                      static_folder='static',
                      template_folder='templates')


@land_bp.route('/', methods=['GET', 'POST'])
@land_bp.route('/index', methods=['GET', 'POST'])
def index():
  displayinfo = {
    'total_teachers': Teacher.query.count(),
    'matched_teachers': db.session.query(func.count(Teacher.id)).\
        filter_by(matched_status=True).scalar(),
    'fake_data': fake_data[2]
  }
  search_form = SearchForm()
  if search_form.validate_on_submit():
    # Search for posted destination
   search_value = search_form.search_input.data
   all_dest = []
   for teacher in Teacher.query.all():
     teacher_info = teacher.target_info
     if teacher_info:
      all_dest.append(teacher_info.county1)
      all_dest.append(teacher_info.county2)
      all_dest.append(teacher_info.county3)
      all_dest.append(teacher_info.subcounty1)
      all_dest.append(teacher_info.subcounty2)
      all_dest.append(teacher_info.subcounty3)
      destn_upper = [val.upper() for val in all_dest]
      
   return render_template('searchresult.html', 
                          search_value=search_value,
                          total_result = len(destn_upper),
                          percentage = round((all_dest.count(search_value) * len(destn_upper)) % 100, 2),
                          searchresult=destn_upper.count(search_value.upper()))
  return render_template('landingpg.html',
                          page_title='Home', 
                          search_form=search_form, 
                          displayinfo=displayinfo, 
                          feedbackform = FeedbackForm()
                          )
