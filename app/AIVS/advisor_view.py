from flask import Blueprint, render_template
from flask_login import login_required, current_user
from app.models import VisitRecord, Student

advisor_view = Blueprint('advisor_view', __name__)

@advisor_view.route('/')
@login_required
def index():
    if current_user.type == 'administrator' or current_user.type == 'advisor':
        data = VisitRecord.query.all()
    else:
        data = VisitRecord.query.filter_by(id=current_user.id).all()
        
    student_name = [Student.query.filter_by(id=record.id).first().name for record in data]
    return render_template('/AIVS/visitation_management.html', data=data, student_name=student_name)

@advisor_view.route('/view/<int:id>')
@login_required
def view(id):
    visit_data = VisitRecord.query.filter_by(id=id).first()
    student_name = Student.query.filter_by(id=id).first().name
    if visit_data is None:
        return render_template('/AIVS/visitation_management.html', data=None)
    return render_template('/AIVS/visitation_management.html', data=visit_data, student_name=student_name)

@advisor_view.route('/my_visits')
@login_required
def my_visits():
    data = VisitRecord.query.filter_by(id=current_user.id).all()
    student_name = Student.query.filter_by(id=current_user.id).first().name
    return render_template('/AIVS/visitation_management.html', data=data, student_name=student_name)
