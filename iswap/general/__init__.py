from flask import Blueprint, render_template, url_for
from .searchform import SearchForm
from iswap.models import Teacher
from iswap.staticdata import fake_data

land_bp = Blueprint('land_bp', __name__,
                      static_folder='static',
                      template_folder='templates')


@land_bp.route('/', methods=['GET', 'POST'])
@land_bp.route('/index', methods=['GET', 'POST'])
def index():
  displayinfo = {
    'total_teachers': Teacher.query.count(),
    'fake_data': fake_data[2]
  }
  search_form = SearchForm()
  if search_form.validate_on_submit():
    return 'Validated and submitted successfully!'
  return render_template('index.html', page_title='Home', search_form=
          search_form, displayinfo=displayinfo)
