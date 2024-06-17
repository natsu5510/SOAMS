from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from datetime import datetime
from app.extensions import db
from app.models import VisitRecord

visit_form = Blueprint('visit_form', __name__)

@visit_form.route('/edit')
@login_required
def edit():
    visit_data = VisitRecord.query.filter_by(id=current_user.id).first()
    return render_template('/AIVS/visitation_management.html', data=visit_data)

@visit_form.route('/update', methods=['POST'])
@login_required
def update():
    id = request.form.get('id')
    data = VisitRecord.query.filter_by(id=id).first()
    
    visit_date_time_str = request.form.get('visit_date_time')
    visit_date_time = datetime.strptime(visit_date_time_str, '%Y-%m-%d') if visit_date_time_str else None

    new_data = {
        'id': id,
        'semester': request.form.get('semester'),
        'visit_date_time': visit_date_time,
        'landlord_name': request.form.get('landlord_name'),
        'landlord_tel': request.form.get('landlord_tel'),
        'addr': request.form.get('addr'),
        'building_type': request.form.get('building_type'),
        'room_type': request.form.get('room_type'),
        'rent': request.form.get('rent'),
        'deposit': request.form.get('deposit'),
        'recommand': bool(int(request.form.get('recommand', 0))),
        'safe_manage1': bool(int(request.form.get('safe_manage1', 0))),
        'safe_manage2': bool(int(request.form.get('safe_manage2', 0))),
        'safe_manage3': bool(int(request.form.get('safe_manage3', 0))),
        'safe_manage4': bool(int(request.form.get('safe_manage4', 0))),
        'safe_manage5': bool(int(request.form.get('safe_manage5', 0))),
        'safe_manage6': bool(int(request.form.get('safe_manage6', 0))),
        'safe_manage7': bool(int(request.form.get('safe_manage7', 0))),
        'safe_manage8': bool(int(request.form.get('safe_manage8', 0))),
        'safe_manage9': bool(int(request.form.get('safe_manage9', 0))),
        'safe_manage10': bool(int(request.form.get('safe_manage10', 0))),
        'safe_manage11': bool(int(request.form.get('safe_manage11', 0))),
        'safe_manage12': bool(int(request.form.get('safe_manage12', 0))),
        'safe_manage13': bool(int(request.form.get('safe_manage13', 0))),
        'deposit_demand': bool(int(request.form.get('deposit_demand', 0))),
        'water_electric_bill_demand': bool(int(request.form.get('water_electric_bill_demand', 0))),
        'environment': bool(int(request.form.get('environment', 0))),
        'environment_description': request.form.get('environment_description', ''),
        'facility': bool(int(request.form.get('facility', 0))),
        'faclity_description': request.form.get('faclity_description', ''),
        'situation': bool(int(request.form.get('situation', 0))),
        'situation_description': request.form.get('situation_description', ''),
        'is_get_along_with': bool(int(request.form.get('is_get_along_with', 1))),
        'result': bool(int(request.form.get('result', 0))),
        'result_description': request.form.get('result_description', ''),
        'others1': request.form.get('others1', ''),
        'traffic_safty': bool(int(request.form.get('traffic_safty', 0))),
        'smoke': bool(int(request.form.get('smoke', 0))),
        'drug': bool(int(request.form.get('drug', 0))),
        'dengue': bool(int(request.form.get('dengue', 0))),
        'others2': request.form.get('others2', '')
    }

    if data is None:
        tmpdata = VisitRecord(**new_data)
        db.session.add(tmpdata)
    else:
        for key, value in new_data.items():
            setattr(data, key, value)

    db.session.commit()
    return redirect(url_for('advisor_view.my_visits'))
