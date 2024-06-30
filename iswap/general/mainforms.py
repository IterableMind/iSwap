from iswap import FlaskForm, SearchField, DataRequired
from wtforms import TextAreaField, StringField
from wtforms.validators import DataRequired, Email

class SearchForm(FlaskForm):
  search_input = SearchField(validators=[DataRequired(message=
                "Please type a county or sub-county to search!")])
  
  # validate county/sub-county queried
  def isvalidquery(self, val):
    pass # validation mechanism

class FeedbackForm(FlaskForm):
  email = StringField('Email', validators=[DataRequired('Please type a valid email address'), Email()])
  feedbackinput = TextAreaField(validators=[DataRequired('Please type your message to continue')])