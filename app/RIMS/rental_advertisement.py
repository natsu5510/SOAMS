from flask import Blueprint, render_template, url_for, redirect, flash, request, current_app as app
from flask_login import login_user, logout_user, login_required, current_user
from app.AIMS.login_management import role_required
from app.models import Advertisement, Landlord
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

# 瀏覽所有廣告
@rental_advertisement.route('/<int:page>')
@login_required
def index(page):
    advertisements = Advertisement.query.filter_by(status=1).paginate(page=page, per_page=10, error_out=False)
    return render_template('/RIMS/rental_advertisement.html', ads=advertisements)

# 瀏覽廣告
@rental_advertisement.route('/advertisement/<int:adid>')
@login_required
def advertisement(adid):
    advertisement = Advertisement.query.filter_by(id=adid).one()
    landlord = Landlord.query.filter_by(id=advertisement.landlord_id).one()
    return render_template('/RIMS/rental_advertisement_detail.html', ad=advertisement, landlord=landlord)

# 房東刊登廣告
@rental_advertisement.route('/advertise', methods=['GET', 'POST'])
@login_required
@role_required('landlord')
def advertise():
    form = AdvertisementForm()
    if form.validate_on_submit():
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
        new_ad.rent_lower=form.rent_lower.data
        new_ad.rent_upper=form.rent_upper.data
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
            # 移除最後一個逗號
            if image_urls.endswith(','):
                image_urls = image_urls[:-1]
            new_ad.image_urls=image_urls
        
        
        db.session.add(new_ad)
        db.session.commit()

        flash('刊登請求已送出！請等待管理員審核', 'success')
        return redirect(url_for('rental_advertisement.index', page=1))
    # else:
    #     for fieldName, errorMessages in form.errors.items():
    #         for err in errorMessages:
    #             print(f'Error in {fieldName}: {err}')
    return render_template('/RIMS/advertise.html', form=form)

# 房東編輯廣告
@rental_advertisement.route('/edit_advertisement')
@login_required
@role_required('landlord')
def edit_advertisement():
    ads = Advertisement.query.filter_by(landlord_id=current_user.id)
    return render_template('/RIMS/edit_advertisement.html', ads=ads)

# 房東編輯廣告
@rental_advertisement.route('/edit_advertisement/<int:adid>', methods=['GET', 'POST'])
@login_required
@role_required('landlord')
def edit_advertisement_detail(adid):
    ad = Advertisement.query.get_or_404(adid)
    # 確保房東不能透過直接在路由輸入參數來編輯其他人的廣告
    if ad.landlord_id != current_user.id:
        return redirect(url_for('login_management.login'))
    form = AdvertisementForm(obj=ad)
    if form.validate_on_submit():
        form.populate_obj(ad)
        ad.electricity_meter=strtobool(form.electricity_meter.data)
        ad.smoke=strtobool(form.smoke.data)
        ad.wash_machine=strtobool(form.wash_machine.data)
        ad.water_dispenser=strtobool(form.water_dispenser.data)
        ad.internet=strtobool(form.internet.data)
        ad.parking=strtobool(form.parking.data)
        ad.air_con=strtobool(form.air_con.data)
        ad.water_heater=strtobool(form.water_heater.data)
        db.session.add(ad)
        db.session.commit()
        flash('編輯成功', 'success')
        return redirect(url_for('rental_advertisement.edit_advertisement'))
    return render_template('/RIMS/edit_advertisement_detail.html', form=form)

# 管理員審核廣告
@rental_advertisement.route('/review_advertisement')
@login_required
@role_required('administrator')
def review_advertisement():
    ads = Advertisement.query.filter_by(status=0)
    return render_template('/RIMS/review_advertisement.html', ads=ads)

# 管理員審核廣告
@rental_advertisement.route('/review_advertisement/<int:adid>', methods=['GET', 'POST'])
@login_required
@role_required('administrator')
def review_advertisement_detail(adid):
    ad = Advertisement.query.get_or_404(adid)
    # 確保房東不能透過直接在路由輸入參數來編輯其他人的廣告
    form = AdvertisementForm(obj=ad)
    if request.method == 'POST':
        form.populate_obj(ad)
        ad.electricity_meter=strtobool(form.electricity_meter.data)
        ad.smoke=strtobool(form.smoke.data)
        ad.wash_machine=strtobool(form.wash_machine.data)
        ad.water_dispenser=strtobool(form.water_dispenser.data)
        ad.internet=strtobool(form.internet.data)
        ad.parking=strtobool(form.parking.data)
        ad.air_con=strtobool(form.air_con.data)
        ad.water_heater=strtobool(form.water_heater.data)

        if request.form.get('action') == '核准':
            ad.status = 1
        elif request.form.get('action') == '駁回':
            ad.status = 2

        db.session.add(ad)
        db.session.commit()
        flash('審核成功', 'success')
        return redirect(url_for('rental_advertisement.review_advertisement'))
    return render_template('/RIMS/review_advertisement_detail.html', form=form)