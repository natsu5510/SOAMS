from flask import *
from flask_login import *
from app.AIMS.login_management import role_required
from app.extensions import db
from sqlalchemy.sql import text
from app.models import VisitRecord
from app.models import Student

visitation_management = Blueprint('visitation_management', __name__)

@visitation_management.route('/')
@login_required
def index():
    data = VisitRecord.query.all()
    student_name = []
    
    for i in data:
        student_name.append(Student.query.filter_by(id=i.id).first().name)
    return render_template('/AIVS/visitation_management.html', data=data, student_name=student_name)

@visitation_management.route('/edit')
@login_required
def edit():

    visit_data = VisitRecord.query.filter_by(id=current_user.id).first()
    if(visit_data == None):
        return render_template('/AIVS/visitation_management.html', data=None)
    else:
        return render_template('/AIVS/visitation_management.html', data=visit_data)
    
@visitation_management.route('/update', methods=['POST'])
@login_required
def update():
    print(request.form)
    data = VisitRecord.query.filter_by(id=request.form.get('id')).first()
    if current_user.type == 'student':
        tmpdata = VisitRecord(
            id=request.form.get('id'), semester=request.form.get('semester'), visit_date_time=request.form.get('visit_date_time'),
            landlord_name=request.form.get('landlord_name'), landlord_tel=request.form.get('landlord_tel'), addr=request.form.get('addr'),
            building_type=request.form.get('building_type'), room_type=request.form.get('room_type'), rent=request.form.get('rent'),
            deposit=request.form.get('deposit'), recommand=int(request.form.get('recommand')), 
            safe_manage1=bool(int(request.form.get('safe_manage1'))), safe_manage2=bool(int(request.form.get('safe_manage2'))),
            safe_manage3=bool(int(request.form.get('safe_manage3'))), safe_manage4=bool(int(request.form.get('safe_manage4'))),
            safe_manage5=bool(int(request.form.get('safe_manage5'))), safe_manage6=bool(int(request.form.get('safe_manage6'))),
            safe_manage7=bool(int(request.form.get('safe_manage7'))), safe_manage8=bool(int(request.form.get('safe_manage8'))),
            safe_manage9=bool(int(request.form.get('safe_manage9'))), safe_manage10=bool(int(request.form.get('safe_manage10'))),
            safe_manage11=bool(int(request.form.get('safe_manage11'))), safe_manage12=bool(int(request.form.get('safe_manage12'))),
            safe_manage13=bool(int(request.form.get('safe_manage13'))),
            deposit_demand=bool(0), water_electric_bill_demand=bool(0),
            environment=bool(0),environment_description="",
            facility=bool(0),faclity_description="",
            situation=bool(0),situation_description="",
            others1="", result=0, result_description="",
            is_get_along_with=bool(1),
            traffic_safty=bool(0), smoke=bool(0), drug=bool(0),
            dengue=bool(0), others2=""
        )
        if(data == None):
            db.session.add(tmpdata)
        else:
            data.semester = request.form.get('semester')
            data.visit_date_time = request.form.get('visit_date_time')
            data.landlord_name = request.form.get('landlord_name')
            data.landlord_tel = request.form.get('landlord_tel')
            data.addr = request.form.get('addr')
            data.building_type = request.form.get('building_type')
            data.room_type = request.form.get('room_type')
            data.rent = request.form.get('rent')
            data.deposit = request.form.get('deposit')
            data.recommand = bool(int(request.form.get('recommand')))
            data.safe_manage1 = bool(int(request.form.get('safe_manage1')))
            data.safe_manage2 = bool(int(request.form.get('safe_manage2')))
            data.safe_manage3 = bool(int(request.form.get('safe_manage3')))
            data.safe_manage4 = bool(int(request.form.get('safe_manage4')))
            data.safe_manage5 = bool(int(request.form.get('safe_manage5')))
            data.safe_manage6 = bool(int(request.form.get('safe_manage6')))
            data.safe_manage7 = bool(int(request.form.get('safe_manage7')))
            data.safe_manage8 = bool(int(request.form.get('safe_manage8')))
            data.safe_manage9 = bool(int(request.form.get('safe_manage9')))
            data.safe_manage10 = bool(int(request.form.get('safe_manage10')))
            data.safe_manage11 = bool(int(request.form.get('safe_manage11')))
            data.safe_manage12 = bool(int(request.form.get('safe_manage12')))
            data.safe_manage13 = bool(int(request.form.get('safe_manage13')))
        db.session.commit()
        return redirect(url_for('visitation_management.edit'))
    data.deposit_demand = bool(int(request.form.get('deposit_demand')))
    data.water_electric_bill_demand = bool(int(request.form.get('water_electric_bill_demand')))
    data.environment = bool(int(request.form.get('environment')))
    data.environment_description = request.form.get('environment_description')
    data.facility = bool(int(request.form.get('facility')))
    data.faclity_description = request.form.get('faclity_description')
    data.situation = bool(int(request.form.get('situation')))
    data.situation_description = request.form.get('situation_description')
    data.is_get_along_with = bool(int(request.form.get('is_get_along_with')))
    data.result = bool(int(request.form.get('result')))
    data.result_description = request.form.get('result_description')
    data.others1 = request.form.get('others1')
    # 關懷宣導項目
    traffic_safty = bool(0)
    if request.form.get('traffic_safty') == '1':
        traffic_safty = bool(1)
    data.traffic_safty = traffic_safty
    smoke = bool(0)
    if request.form.get('smoke') == '1':
        smoke = bool(1)
    data.smoke = smoke
    drug = bool(0)
    if request.form.get('drug') == '1':
        drug = bool(1)
    data.drug = drug
    dengue = bool(0)
    if request.form.get('dengue') == '1':
        dengue = bool(1)
    data.dengue = dengue
    data.others2 = request.form.get('others2')
    db.session.commit()
    return redirect(url_for('visitation_management.index'))