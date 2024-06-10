from werkzeug.utils import secure_filename
from PIL import Image
from secrets import token_hex
import os 
from iswap import app
from iswap.models import Teacher
from flask_login import current_user

def edit_picture(uploaded_image):
  profile_pic = uploaded_image.profile_photo.data

  if profile_pic is None:
    current_pic = Teacher.query.filter_by( \
      id=current_user.id).first().profile_pic
    if current_pic is None:
      return 'default_pic.PNG'
    return current_pic
  
  # Sanitize the uploaded filename of the photo.
  sanitized_name = secure_filename(profile_pic.filename)

  _, ext = os.path.splitext(sanitized_name)
  filename = token_hex(32) + ext.upper()
  
  # Resize the photo into a square of 300px.
  edited_profile_photo = Image.open(profile_pic)
  edited_profile_photo = edited_profile_photo.resize(size=(300, 300))

  # save the picture
  edited_profile_photo.save(os.path.join(
      app.root_path, 'static', 'images', 'profile_pictures', filename
    ))
  
  return filename
  

  


