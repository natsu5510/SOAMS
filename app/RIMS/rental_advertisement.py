from flask import Blueprint, render_template, url_for, redirect, flash, request, current_app as app
from flask_login import login_user, logout_user, login_required, current_user
from app.AIMS.login_management import role_required
from app.models import Advertisement
from app.forms import AdvertisementForm
from app.extensions import db
from sqlalchemy import func
from datetime import datetime
from werkzeug.utils import secure_filename
from distutils.util import strtobool
import os
import pathlib

rental_advertisement = Blueprint('rental_advertisement', __name__)

# 取得目前檔案所在的資料夾 
SRC_PATH =  pathlib.Path(__file__).parent.parent.absolute()
UPLOAD_FOLDER = os.path.join(SRC_PATH,  'static', 'uploads')

@rental_advertisement.route('/')
@login_required
def index():
    advertisements = Advertisement.query.all()
    return render_template('/RIMS/rental_advertisement.html', ads=advertisements)

# 房東刊登廣告
@rental_advertisement.route('/advertise', methods=['GET', 'POST'])
@login_required
@role_required('landlord')
def advertise():
    form = AdvertisementForm()
    if request.method == 'POST' and form.validate():
        new_ad = Advertisement(
            electricity_meter=strtobool(form.electricity_meter.data),
            smoke=strtobool(form.smoke.data),
            wash_machine=strtobool(form.wash_machine.data),
            water_dispenser=strtobool(form.water_dispenser.data),
            internet=strtobool(form.internet.data),
            parking=strtobool(form.parking.data),
            air_con=strtobool(form.air_con.data),
            water_heater=strtobool(form.water_heater.data),
        )
        new_ad.title=form.title.data
        new_ad.building_age=form.building_age.data
        new_ad.building_type=form.building_type.data
        new_ad.addr=form.addr.data
        new_ad.rental_limit=form.rental_limit.data
        new_ad.rent=form.rent.data
        new_ad.suite=form.suite.data
        new_ad.room=form.room.data
        new_ad.description=form.description.data
        new_ad.timestamp=datetime.now()
        new_ad.status=0 # 待審核
        new_ad.landlord_id=current_user._get_current_object().id

        with app.app_context():
            # 查詢目前廣告編號最大值
            max_id = db.session.query(func.max(Advertisement.id)).scalar()
            if max_id is None:
                max_id = 0

        # 處理圖檔
        if 'filename' in request.files:
            max_id += 1
            count = 1
            image_urls = ''
            files = request.files.getlist('filename')
            for file in files:
                if file and file.filename:
                    name, extension = os.path.splitext(file.filename)
                    new_filename = f'{max_id}_{count}{extension}'
                    filepath = os.path.join(UPLOAD_FOLDER, new_filename)
                    file.save(filepath)
                    image_urls += new_filename + ','
                    count += 1
            new_ad.image_urls=image_urls
        
        
        db.session.add(new_ad)
        db.session.commit()

        flash('刊登請求已送出！請等待管理員審核', 'success')
        return redirect(url_for('rental_advertisement.index'))
    # else:
    #     for fieldName, errorMessages in form.errors.items():
    #         for err in errorMessages:
    #             print(f'Error in {fieldName}: {err}')
    return render_template('/RIMS/advertise.html', form=form)