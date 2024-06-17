from flask import *
from flask_login import *
from app.AIMS.login_management import role_required
from app.extensions import db
from sqlalchemy.sql import text
from app.models import AccommodationInfo

accommodation_management = Blueprint('accommodation_management', __name__)

@accommodation_management.route('/')
@login_required
def index():
    data = AccommodationInfo.query.all()
    return render_template('/AIVS/accommodation_management.html', data=data)

@accommodation_management.route('/edit')
@login_required
def edit():
    sql = f"""
    SELECT SS.dept AS dept, user_student.id AS id, user_student.name AS student_name,
        user_student.tel AS tel, user_advisor.id AS advisor_id, user_advisor.name AS advisor_name
    FROM (SELECT * FROM user WHERE type = 'student') AS user_student JOIN student AS SS ON user_student.id = SS.id
        JOIN (SELECT * FROM user WHERE type = 'advisor') AS user_advisor JOIN advisor ON user_advisor.id = advisor.id
    WHERE advisor_id = user_advisor.id AND user_student.id = '{current_user.id}'
    """

    acc_data = AccommodationInfo.query.filter_by(id=current_user.id).first()
    if(acc_data == None):
        data = db.session.execute(text(sql)).first()
        return render_template('/AIVS/accommodation_management.html', data=data)
    else:
        return render_template('/AIVS/accommodation_management.html', data=acc_data)

@accommodation_management.route('/update', methods=['POST'])
@login_required
def update():
    data = AccommodationInfo.query.filter_by(id=request.form.get('id')).first()
    # tmpdata = AccommodationInfo(id=request.form.get('id'), semester=request.form.get('semester'), where_to_live=request.form.get('where_to_live'),
    #                     addr=request.form.get('addr'), landlord_name=request.form.get('landlord_name'),
    #                     landlord_tel=request.form.get('landlord_tel'), rent=request.form.get('rent'), roommate_id=request.form.get('roommate_id'))
    tmpdata = AccommodationInfo()
    tmpdata.id = current_user.id
    tmpdata.semester = request.form.get('semester')
    tmpdata.where_to_live = where_to_live=request.form.get('where_to_live')
    tmpdata.addr=request.form.get('addr')
    tmpdata.landlord_name=request.form.get('landlord_name')
    tmpdata.landlord_tel=request.form.get('landlord_tel')
    tmpdata.rent=request.form.get('rent')
    if request.form.get('roommate_id') != None  or request.form.get('roommate_id') != '':
        tmpdata.roommate_id=request.form.get('roommate_id')
    else:
        data.roommate_id = None

    
    if(data == None):
        db.session.add(tmpdata)
    else:
        data.semester = request.form.get('semester')
        data.where_to_live = request.form.get('where_to_live')
        data.addr = request.form.get('addr')
        data.landlord_name = request.form.get('landlord_name')
        data.landlord_tel = request.form.get('landlord_tel')
        data.rent = request.form.get('rent')
        if request.form.get('roommate_id') != None or request.form.get('roommate_id') != '':
            data.roommate_id = request.form.get('roommate_id')
        else:
            data.roommate_id = None
    db.session.commit()
    if current_user.type == 'student':
        return redirect(url_for('accommodation_management.edit'))
    return redirect(url_for('accommodation_management.index'))