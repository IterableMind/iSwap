from flask_login import current_user
from iswap.models import TargetLoc, db
import logging
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import FlushError
from iswap.staticdata import subject_comb, school_gender,\
                school_type, countylist

# Validate current teacher location details.
def validate_select_fields(sub_data):
  if sub_data.get('sub_comb') is not None and \
    sub_data['sub_comb'] not in subject_comb: 
    return False
  if sub_data.get('tchin_level') is not None and \
    sub_data['tchin_level'] not in ('Primary', 'Secondary'): 
    return False
  if sub_data['county'] not in countylist: 
    return False
  if sub_data.get('sch_gender') is not None and \
    sub_data['sch_gender'] not in school_gender: 
    return False 
  if sub_data.get('sch_type') is not None and \
    sub_data['sch_type'] not in school_type: 
    return False
  return True


"""
# Insert target location into the database.
# """
def insertlocinfo(data):
    try:
        # Fetch the existing record
        usertarinfo = TargetLoc.query.filter_by(teacher_id=current_user.id).first()

        if usertarinfo:
            # Update the existing record with new values
            usertarinfo.county1 = data[0]
            usertarinfo.subcounty1 = data[1]
            usertarinfo.county2 = data[2]
            usertarinfo.subcounty2 = data[3]
            usertarinfo.county3 = data[4]
            usertarinfo.subcounty3 = data[5]
            logging.info(f"Updated TargetLoc for teacher_id {current_user.id}")
        else:
            # Create a new TargetLoc instance with the provided data
            loc = TargetLoc(
                county1=data[0], 
                subcounty1=data[1],
                county2=data[2], 
                subcounty2=data[3],
                county3=data[4], 
                subcounty3=data[5],
                teacher_id=current_user.id
            )
            db.session.add(loc)
            logging.info(f"Inserted new TargetLoc for teacher_id {current_user.id}")
        db.session.commit()

    except IntegrityError as ie:
        logging.error(f"IntegrityError occurred: {ie}")
        db.session.rollback()
    except FlushError as fe:
        logging.error(f"FlushError occurred: {fe}")
        db.session.rollback()
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        db.session.rollback()
    finally:
        usertarinfo = TargetLoc.query.filter_by(teacher_id=current_user.id).first() 
        db.session.close()
