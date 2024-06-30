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
    pass
  return render_template('index.html', page_title='Home', search_form=
          search_form, displayinfo=displayinfo, feedbackform = FeedbackForm())
