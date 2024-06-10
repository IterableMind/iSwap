from iswap import FlaskForm, SearchField, DataRequired

class SearchForm(FlaskForm):
  search_input = SearchField(validators=[DataRequired(message=
                "Please type a county or sub-county to search!")])
  
  # validate county/sub-county queried
  def isvalidquery(self, val):
    pass # validation mechanism