from flask import Blueprint, render_template, url_for, redirect, flash, request, current_app as app
from flask_login import login_user, logout_user, login_required, current_user
from app.AIMS.login_management import role_required
from app.models import Advertisement, Landlord, Test
from app.extensions import db
from sqlalchemy import func, desc
from datetime import datetime
from werkzeug.utils import secure_filename
from distutils.util import strtobool
import os
import pathlib
import re
import random
import json

rental_advertisement = Blueprint('rental_advertisement', __name__)

# 取得目前檔案所在的資料夾 
SRC_PATH =  pathlib.Path(__file__).parent.parent.absolute()
UPLOAD_FOLDER = os.path.join(SRC_PATH,  'static', 'uploads')

# 瀏覽所有廣告
@rental_advertisement.route('/<int:page>')
@login_required
def index(page):
    advertisements = Advertisement.query.filter_by(status=1).order_by(desc(Advertisement.timestamp)).paginate(page=page, per_page=10, error_out=False)
    return render_template('/RIMS/rental_advertisement.html', ads=advertisements)

# 瀏覽廣告詳細頁面
@rental_advertisement.route('/advertisement/<int:adid>')
@login_required
def advertisement(adid):
    advertisement = Advertisement.query.filter_by(id=adid).one()
    equips = advertisement.get_equip_list()
    public_equips = advertisement.get_public_equip_list()
    heaters = advertisement.get_heater_list()
    safety_equips = advertisement.get_safety_equip_list()
    docs = advertisement.get_document_list()
    combined_list = {'equips':equips, 'public_equips':public_equips, 'heaters':heaters, 'safety_equips':safety_equips, 'docs':docs}
    landlord = Landlord.query.filter_by(id=advertisement.landlord_id).one()
    return render_template('/RIMS/rental_advertisement_detail.html', ad=advertisement, combined_list=combined_list, landlord=landlord)

# 房東刊登廣告
@rental_advertisement.route('/advertise', methods=['GET', 'POST'])
@login_required
@role_required('landlord')
def advertise():
    if request.method == 'POST':
        new_ad = Advertisement(
            electricity_meter = strtobool(request.form.get('electricity_meter')),
            smoke = strtobool(request.form.get('smoke')),
            sofa = 0 if request.form.get('sofa') == None else 1,
            telephone = 0 if request.form.get('telephone') == None else 1,
            bookcase = 0 if request.form.get('bookcase') == None else 1,
            wardrobe = 0 if request.form.get('wardrobe') == None else 1,
            central_air_conditioning = 0 if request.form.get('central_air_conditioning') == None else 1,
            fiber_optic_network1 = 0 if request.form.get('fiber_optic_network') == None else 1,
            washing_machine = 0 if request.form.get('washing_machine') == None else 1,
            single_bed = 0 if request.form.get('single_bed') == None else 1,
            dehydrator = 0 if request.form.get('dehydrator') == None else 1,
            cable_television = 0 if request.form.get('cable_television') == None else 1,
            dryer = 0 if request.form.get('dryer') == None else 1,
            desk_and_chair = 0 if request.form.get('desk_and_chair') == None else 1,
            refrigerator = 0 if request.form.get('refrigerator') == None else 1,
            double_bed = 0 if request.form.get('double_bed') == None else 1,
            water_dispenser = 0 if request.form.get('water_dispenser') == None else 1,
            television = 0 if request.form.get('television') == None else 1,
            air_conditioner = 0 if request.form.get('air_conditioner') == None else 1,
            table_lamp = 0 if request.form.get('table_lamp') == None else 1,
            broadband_network = 0 if request.form.get('broadband_network') == None else 1,
            fire_extinguishers_smoke_detectors_and_monitors_per_floor = 0 if request.form.get('fire_extinguishers_smoke_detectors_and_monitors_per_floor') == None else 1,
            parking_lot = 0 if request.form.get('parking_lot') == None else 1,
            kitchen = 0 if request.form.get('kitchen') == None else 1,
            laundry_area = 0 if request.form.get('laundry_area') == None else 1,
            parking_lot_elevator = 0 if request.form.get('parking_lot_elevator') == None else 1,
            public_balcony = 0 if request.form.get('public_balcony') == None else 1,
            courtyard = 0 if request.form.get('courtyard') == None else 1,
            elevator = 0 if request.form.get('elevator') == None else 1,
            fiber_optic_network2 = 0 if request.form.get('fiber_optic_network_2') == None else 1,
            courtyard_parking_lot = 0 if request.form.get('courtyard_parking_lot') == None else 1,
            lounge = 0 if request.form.get('lounge') == None else 1,
            electric_water_heater = 0 if request.form.get('electric_water_heater') == None else 1,
            gas_water_heater = 0 if request.form.get('gas_water_heater') == None else 1,
            solar_water_heater = 0 if request.form.get('solar_water_heater') == None else 1,
            natural_gas = 0 if request.form.get('natural_gas') == None else 1,
            bottled_gas = 0 if request.form.get('bottled_gas') == None else 1,
            escape_ladder = 0 if request.form.get('escape_ladder') == None else 1,
            security_personnel = 0 if request.form.get('security_personnel') == None else 1,
            slow_descend_device = 0 if request.form.get('slow_descend_device') == None else 1,
            carbon_monoxide_detector = 0 if request.form.get('carbon_monoxide_detector') == None else 1,
            electric_water_heater_power_cut_off_device = 0 if request.form.get('electric_water_heater_power_cut_off_device') == None else 1,
            gas_water_heater_forced_exhaust_device = 0 if request.form.get('gas_water_heater_forced_exhaust_device') == None else 1,
            fire_extinguisher = 0 if request.form.get('fire_extinguisher') == None else 1,
            smoke_detector = 0 if request.form.get('smoke_detector') == None else 1,
            escape_route_clear_and_marked = 0 if request.form.get('escape_route_clear_and_marked') == None else 1,
            lighting_equipment = 0 if request.form.get('lighting_equipment') == None else 1,
            surveillance_system = 0 if request.form.get('surveillance_system') == None else 1,
            access_control_system = 0 if request.form.get('access_control_system') == None else 1,
            firefighting_system = 0 if request.form.get('firefighting_system') == None else 1,
            landlord_identification_documents = 0 if request.form.get('landlord_identification_documents') == None else 1,
            power_of_attorney = 0 if request.form.get('power_of_attorney') == None else 1,
            property_ownership_certificate = 0 if request.form.get('property_ownership_certificate') == None else 1,
            property_tax_bill = 0 if request.form.get('property_tax_bill') == None else 1,
            meets_ministry_of_education_safety_standards =  0 if request.form.get('meets_ministry_of_education_safety_standards') == None else 1
        )
        new_ad.title=request.form.get('title')
        new_ad.rent_lower=request.form.get('rent_lower')
        new_ad.rent_upper=request.form.get('rent_upper')
        new_ad.addr=request.form.get('addr')
        new_ad.suite_num=request.form.get('suite_num')
        new_ad.room_num=request.form.get('room_num')
        new_ad.suite_empty=request.form.get('suite_empty')
        new_ad.room_empty=request.form.get('room_empty')
        new_ad.suite_size=request.form.get('suite_size')
        new_ad.room_size=request.form.get('room_size')
        new_ad.building_type=request.form.get('building_type')
        new_ad.building_age=request.form.get('building_age')
        new_ad.floor1 = request.form.get('floor1')
        new_ad.floor2 = request.form.get('floor2')
        new_ad.size = request.form.get('size')
        new_ad.rental_type = request.form.get('rental_type')
        new_ad.electricity_meter = request.form.get('electricity_meter')
        new_ad.partition_material = request.form.get('partition_material')
        new_ad.deposit = request.form.get('deposit')
        new_ad.sex_limit=request.form.get('sex_limit')
        new_ad.identity_limit = request.form.get('identity_limit')
        new_ad.others_fee = request.form.get('others_fee')
        new_ad.description=request.form.get('description')
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
                    new_filename = f'{max_id}x{count}{extension}'
                    filepath = os.path.join(UPLOAD_FOLDER, new_filename)
                    file.save(filepath)
                    image_urls += new_filename + ','
                    count += 1
            # 移除最後一個逗號
            if image_urls.endswith(','):
                image_urls = image_urls[:-1]
            new_ad.image_urls=image_urls
        
        db.session.add(new_ad)
        test = Test(fuck = strtobool(request.form.get('electricity_meter')))
        db.session.add(test)

        db.session.commit()

        flash('刊登請求已送出！請等待管理員審核', 'success')
        return redirect(url_for('rental_advertisement.index', page=1))
    # else:
    #     for fieldName, errorMessages in form.errors.items():
    #         for err in errorMessages:
    #             print(f'Error in {fieldName}: {err}')
    return render_template('/RIMS/advertise.html')

# 房東編輯廣告
@rental_advertisement.route('/edit_advertisement')
@login_required
@role_required('landlord')
def edit_advertisement():
    ads = Advertisement.query.filter_by(landlord_id=current_user.id).order_by(desc(Advertisement.timestamp))
    return render_template('/RIMS/edit_advertisement.html', ads=ads)

# 房東編輯廣告詳細頁面
@rental_advertisement.route('/edit_advertisement/<int:adid>', methods=['GET', 'POST'])
@login_required
@role_required('landlord')
def edit_advertisement_detail(adid):
    ad = Advertisement.query.get_or_404(adid)
    # 確保房東不能透過直接在路由輸入參數來編輯其他人的廣告
    if ad.landlord_id != current_user.id:
        return redirect(url_for('login_management.login'))
    if request.method == 'POST':
        ad.electricity_meter = strtobool(request.form.get('electricity_meter')),
        ad.smoke = strtobool(request.form.get('smoke')),
        ad.sofa = 0 if request.form.get('sofa') == None else 1,
        ad.telephone = 0 if request.form.get('telephone') == None else 1,
        ad.bookcase = 0 if request.form.get('bookcase') == None else 1,
        ad.wardrobe = 0 if request.form.get('wardrobe') == None else 1,
        ad.central_air_conditioning = 0 if request.form.get('central_air_conditioning') == None else 1,
        ad.fiber_optic_network1 = 0 if request.form.get('fiber_optic_network') == None else 1,
        ad.washing_machine = 0 if request.form.get('washing_machine') == None else 1,
        ad.single_bed = 0 if request.form.get('single_bed') == None else 1,
        ad.dehydrator = 0 if request.form.get('dehydrator') == None else 1,
        ad.cable_television = 0 if request.form.get('cable_television') == None else 1,
        ad.dryer = 0 if request.form.get('dryer') == None else 1,
        ad.desk_and_chair = 0 if request.form.get('desk_and_chair') == None else 1,
        ad.refrigerator = 0 if request.form.get('refrigerator') == None else 1,
        ad.double_bed = 0 if request.form.get('double_bed') == None else 1,
        ad.water_dispenser = 0 if request.form.get('water_dispenser') == None else 1,
        ad.television = 0 if request.form.get('television') == None else 1,
        ad.air_conditioner = 0 if request.form.get('air_conditioner') == None else 1,
        ad.table_lamp = 0 if request.form.get('table_lamp') == None else 1,
        ad.broadband_network = 0 if request.form.get('broadband_network') == None else 1,
        ad.fire_extinguishers_smoke_detectors_and_monitors_per_floor = 0 if request.form.get('fire_extinguishers_smoke_detectors_and_monitors_per_floor') == None else 1,
        ad.parking_lot = 0 if request.form.get('parking_lot') == None else 1,
        ad.kitchen = 0 if request.form.get('kitchen') == None else 1,
        ad.laundry_area = 0 if request.form.get('laundry_area') == None else 1,
        ad.parking_lot_elevator = 0 if request.form.get('parking_lot_elevator') == None else 1,
        ad.public_balcony = 0 if request.form.get('public_balcony') == None else 1,
        ad.courtyard = 0 if request.form.get('courtyard') == None else 1,
        ad.elevator = 0 if request.form.get('elevator') == None else 1,
        ad.fiber_optic_network2 = 0 if request.form.get('fiber_optic_network_2') == None else 1,
        ad.courtyard_parking_lot = 0 if request.form.get('courtyard_parking_lot') == None else 1,
        ad.lounge = 0 if request.form.get('lounge') == None else 1,
        ad.electric_water_heater = 0 if request.form.get('electric_water_heater') == None else 1,
        ad.gas_water_heater = 0 if request.form.get('gas_water_heater') == None else 1,
        ad.solar_water_heater = 0 if request.form.get('solar_water_heater') == None else 1,
        ad.natural_gas = 0 if request.form.get('natural_gas') == None else 1,
        ad.bottled_gas = 0 if request.form.get('bottled_gas') == None else 1,
        ad.escape_ladder = 0 if request.form.get('escape_ladder') == None else 1,
        ad.security_personnel = 0 if request.form.get('security_personnel') == None else 1,
        ad.slow_descend_device = 0 if request.form.get('slow_descend_device') == None else 1,
        ad.carbon_monoxide_detector = 0 if request.form.get('carbon_monoxide_detector') == None else 1,
        ad.electric_water_heater_power_cut_off_device = 0 if request.form.get('electric_water_heater_power_cut_off_device') == None else 1,
        ad.gas_water_heater_forced_exhaust_device = 0 if request.form.get('gas_water_heater_forced_exhaust_device') == None else 1,
        ad.fire_extinguisher = 0 if request.form.get('fire_extinguisher') == None else 1,
        ad.smoke_detector = 0 if request.form.get('smoke_detector') == None else 1,
        ad.escape_route_clear_and_marked = 0 if request.form.get('escape_route_clear_and_marked') == None else 1,
        ad.lighting_equipment = 0 if request.form.get('lighting_equipment') == None else 1,
        ad.surveillance_system = 0 if request.form.get('surveillance_system') == None else 1,
        ad.access_control_system = 0 if request.form.get('access_control_system') == None else 1,
        ad.firefighting_system = 0 if request.form.get('firefighting_system') == None else 1,
        ad.landlord_identification_documents = 0 if request.form.get('landlord_identification_documents') == None else 1,
        ad.power_of_attorney = 0 if request.form.get('power_of_attorney') == None else 1,
        ad.property_ownership_certificate = 0 if request.form.get('property_ownership_certificate') == None else 1,
        ad.property_tax_bill = 0 if request.form.get('property_tax_bill') == None else 1,
        ad.meets_ministry_of_education_safety_standards = 0 if request.form.get('meets_ministry_of_education_safety_standards') == None else 1
        ad.title=request.form.get('title')
        ad.rent_lower=request.form.get('rent_lower')
        ad.rent_upper=request.form.get('rent_upper')
        ad.addr=request.form.get('addr')
        ad.suite_num=request.form.get('suite_num')
        ad.room_num=request.form.get('room_num')
        ad.suite_empty=request.form.get('suite_empty')
        ad.room_empty=request.form.get('room_empty')
        ad.suite_size=request.form.get('suite_size')
        ad.room_size=request.form.get('room_size')
        ad.building_type=request.form.get('building_type')
        ad.building_age=request.form.get('building_age')
        ad.floor1 = request.form.get('floor1')
        ad.floor2 = request.form.get('floor2')
        ad.size = request.form.get('size')
        ad.rental_type = request.form.get('rental_type')
        ad.electricity_meter = request.form.get('electricity_meter')
        ad.partition_material = request.form.get('partition_material')
        ad.deposit = request.form.get('deposit')
        ad.sex_limit=request.form.get('sex_limit')
        ad.identity_limit = request.form.get('identity_limit')
        ad.others_fee = request.form.get('others_fee')
        ad.description=request.form.get('description')

        image_urls = ad.image_urls.split(',')
        new_image_urls = []
        for img in image_urls:
            if request.form.get(img) != None:
                # 刪除圖片
                filepath = os.path.join(UPLOAD_FOLDER, img)
                os.remove(filepath)
            else:
                new_image_urls.append(img)
        
        match = re.search(r'x(\d+)', new_image_urls[-1])
        if match:
            number_after_x = match.group(1)
        else:
            number_after_x = 0

        image_urls = ','.join(new_image_urls)
        # 處理圖檔
        if 'filename' in request.files:
            count = int(number_after_x) + 1
            files = request.files.getlist('filename')
            for file in files:
                if file and file.filename:
                    name, extension = os.path.splitext(file.filename)
                    new_filename = f'{ad.id}x{count}{extension}'
                    filepath = os.path.join(UPLOAD_FOLDER, new_filename)
                    file.save(filepath)
                    image_urls += ',' + new_filename
                    count += 1
            # 移除最後一個逗號
            if image_urls.endswith(','):
                image_urls = image_urls[:-1]
        
        ad.image_urls=image_urls

        ad.update_time=datetime.now()


        db.session.add(ad)
        db.session.commit()
        flash('編輯成功', 'success')
        return redirect(url_for('rental_advertisement.edit_advertisement'))
    return render_template('/RIMS/edit_advertisement_detail.html', ad=ad)

# 管理員審核廣告
@rental_advertisement.route('/review_advertisement')
@login_required
@role_required('administrator')
def review_advertisement():
    ads = Advertisement.query.filter_by(status=0).order_by(Advertisement.timestamp)
    return render_template('/RIMS/review_advertisement.html', ads=ads)

# 管理員審核廣告詳細頁面
@rental_advertisement.route('/review_advertisement/<int:adid>', methods=['GET', 'POST'])
@login_required
@role_required('administrator')
def review_advertisement_detail(adid):
    advertisement = Advertisement.query.get_or_404(adid)
    equips = advertisement.get_equip_list()
    public_equips = advertisement.get_public_equip_list()
    heaters = advertisement.get_heater_list()
    safety_equips = advertisement.get_safety_equip_list()
    docs = advertisement.get_document_list()
    combined_list = {'equips':equips, 'public_equips':public_equips, 'heaters':heaters, 'safety_equips':safety_equips, 'docs':docs}
    landlord = Landlord.query.filter_by(id=advertisement.landlord_id).one()
    # form = AdvertisementForm(obj=ad)
    if request.method == 'POST':
        if request.form.get('action') == '核准':
            advertisement.status = 1
        elif request.form.get('action') == '駁回':
            advertisement.status = 2
        
        advertisement.pulish_date = datetime.now()
        db.session.add(advertisement)
        db.session.commit()
        flash('審核成功', 'success')
        return redirect(url_for('rental_advertisement.review_advertisement'))
    return render_template('/RIMS/review_advertisement_detail.html',  ad=advertisement, combined_list=combined_list, landlord=landlord)

@rental_advertisement.route('/import_db', methods=['GET', 'POST'])
def import_db():
    # 读取JSON文件
    with open('house_data.json', 'r', encoding='utf-8') as file:
        data = json.load(file)

    for house in data[32:]:
        # 屋內設備
        equip = {'檯燈':0, '第四台':1, '中央空調':2, '光纖網路':3, '書櫃':4, '洗衣機':5, '電冰箱':6,
                '電話':7, '烘乾機':8, '脫水機':9, '飲水機':10, '衣櫃':11, '沙發':12, '冷氣機':13, '電視機':14,
                '單人床':15, '書桌(椅)':16, '寬頻網路':17, '雙人床':18}
        el = [0]*19
        split_list = house['屋內設備'].split(',')
        split_list_with_comma = [item for item in split_list]
        es = set(split_list_with_comma)
        if '' in es:
            es.remove('')
        for e in es:
            el[equip[e]] = 1

        # 公共設施
        equip2 = {'中庭':0, '每層樓滅火器及煙霧偵測器及監視器':1, '電梯':2, '廚房':3, '光纖網路':4,
                '公共陽台':5, '晒衣場':6, '停車場電梯':7, '停車場':8, '交誼廳':9, '中庭停車場':10}
        el2 = [0]*11
        split_list = house['公共設施'].split(',')
        # Add a comma at the end of each element
        split_list_with_comma = [item for item in split_list]
        es = set(split_list_with_comma)
        if '' in es:
            es.remove('')
        for e in es:
            el2[equip2[e]] = 1
        
        # 熱水器
        heater = {'桶裝瓦斯':0, '電熱水器':1, '瓦斯熱水器':2, '太陽能熱水器':3, '天然瓦斯':4}
        el3 = [0]*5
        split_list = house['熱水器'].split(',')
        # Add a comma at the end of each element
        split_list_with_comma = [item for item in split_list]
        es = set(split_list_with_comma)
        if '' in es:
            es.remove('')
        for e in es:
            el3[heater[e]] = 1
        
        # 安全設施
        safee = {'監視錄影設備(系統)':0, '偵煙設備':1, '一氧化碳警報器':2, '瓦斯熱水器強制排氣設備':3,
                '消防系統':4, '保全人員':5, '門禁系統':6, '逃生梯':7, '滅火器':8, '逃生路線暢通及標示':9,
                '緩降梯':10, '照明設備':11, '電用熱水器斷電設備':12}
        el4 = [0]*13
        split_list = house['安全設施'].split(',')
        # Add a comma at the end of each element
        split_list_with_comma = [item for item in split_list]
        es = set(split_list_with_comma)
        if '' in es:
            es.remove('')
        for e in es:
            el4[safee[e]] = 1

        # 證明文件
        doc = {'房屋稅單':0, '委託書':1, '房屋所有權狀':2, '房東身分證明文件':3}
        docl = [0]*4
        split_list = house['證明文件'].split(',')
        # Add a comma at the end of each element
        split_list_with_comma = [item for item in split_list]
        es = set(split_list_with_comma)
        if '' in es:
            es.remove('')
        for e in es:
            docl[doc[e]] = 1

        if house['安全訪評'] != '':
            has_safe = 1
        else:
            has_safe = 0
        
        if house['獨立電表'] == '有':
            electricity = 1
        else:
            electricity = 0
        
        if house['無菸租屋'] == '是':
            no_smoke = 1
        else:
            no_smoke = 0

        new_ad = Advertisement(
            electricity_meter = electricity,
            smoke = no_smoke,

            table_lamp = el[0],
            cable_television = el[1],
            central_air_conditioning = el[2],
            fiber_optic_network1 = el[3],
            bookcase = el[4],
            washing_machine = el[5],
            refrigerator = el[6],
            telephone = el[7],
            dryer = el[8],
            dehydrator = el[9],
            water_dispenser = el[10],
            wardrobe = el[11],
            sofa = el[12],
            air_conditioner = el[13],
            television = el[14],
            single_bed = el[15],
            desk_and_chair = el[16],
            broadband_network = el[17],
            double_bed = el[18],

            courtyard = el2[0],
            fire_extinguishers_smoke_detectors_and_monitors_per_floor = el2[1],
            elevator = el2[2],
            kitchen = el2[3],
            fiber_optic_network2 = el2[4],
            public_balcony = el2[5],
            laundry_area = el2[6],
            parking_lot_elevator = el2[7],
            parking_lot = el2[8],
            lounge = el2[9],
            courtyard_parking_lot = el2[10],

            bottled_gas = el3[0],
            electric_water_heater = el3[1],
            gas_water_heater = el3[2],
            solar_water_heater = el3[3],
            natural_gas = el3[4],

            surveillance_system = el4[0],
            smoke_detector = el4[1],
            carbon_monoxide_detector = el4[2],
            gas_water_heater_forced_exhaust_device = el4[3],
            firefighting_system = el4[4],
            security_personnel = el4[5],
            access_control_system = el4[6],
            escape_ladder = el4[7],
            fire_extinguisher = el4[8],
            escape_route_clear_and_marked = el4[9],
            slow_descend_device = el4[10],
            lighting_equipment = el4[11],
            electric_water_heater_power_cut_off_device = el4[12],
            
            property_tax_bill = docl[0],
            power_of_attorney = docl[1],
            property_ownership_certificate = docl[2],
            landlord_identification_documents = docl[3],
            meets_ministry_of_education_safety_standards = has_safe
        )
        new_ad.title=house['標題']

        # Extract numbers using regular expressions
        numbers = re.findall(r'\d+', house['租金'])
        # Convert the extracted numbers to integers
        numbers_list = [int(num) for num in numbers]

        new_ad.rent_lower=numbers_list[0]
        if len(numbers_list) == 1:
            new_ad.rent_upper=numbers_list[0]
        else:
            new_ad.rent_upper=numbers_list[1]

        new_ad.addr=house['地址']

        # Extract numbers using regular expressions
        numbers = re.findall(r'\d+', house['出租房數'])
        # Convert the extracted numbers to integers
        numbers_list = [int(num) for num in numbers]
        new_ad.suite_size=numbers_list[0]
        new_ad.suite_num=numbers_list[1]
        new_ad.suite_empty=numbers_list[2]
        new_ad.room_size=numbers_list[3]
        new_ad.room_num=numbers_list[4]
        new_ad.room_empty=numbers_list[5]

        new_ad.building_type=house['房屋類型']

        new_ad.building_age=random.randrange(0, 20, 1)

        # Extract numbers using regular expressions
        numbers = re.findall(r'\d+', house['建物樓層'])
        # Convert the extracted numbers to integers
        numbers_list = [int(num) for num in numbers]

        new_ad.floor1 = numbers_list[0]
        new_ad.floor2 = numbers_list[1]
        new_ad.size = numbers_list[2]

        new_ad.rental_type = house['出租類型']

        new_ad.electricity_meter = house['獨立電表'] == '有'

        new_ad.partition_material = house['隔間材質']
        new_ad.deposit = house['押金']
        new_ad.sex_limit=house['性別要求']
        new_ad.identity_limit = house['身份要求']
        new_ad.others_fee = house['其他費用']
        new_ad.description=house['屋況說明']
        new_ad.timestamp=datetime.now()
        new_ad.status=0 # 待審核
        new_ad.landlord_id='landlord'

        with app.app_context():
            # 查詢目前廣告編號最大值
            max_id = db.session.query(func.max(Advertisement.id)).scalar()
            if max_id is None:
                max_id = 0
        
        # 設定要搜尋的目錄路徑
        source_directory = 'downloaded_images/'
        dest_directory = 'C:/FlaskProject/SOAMS/app/RIMS/uploads'
        import os
        import shutil
        # 取得目錄下所有檔案名稱
        file_names = os.listdir(source_directory)

        # 篩選出以 '123' 開頭的檔案名稱
        image_files = [f for f in file_names if f.startswith(house['id']) and f.endswith(('.jpg', '.png', '.jpeg', '.gif'))]
        image_urls = ''
        print(image_files)
        # 遍歷篩選出的圖片檔案
        for i, image_file in enumerate(image_files):
            # 建立新的檔案名稱
            new_file_name = f'{max_id+1}x{i+1}.{image_file.split(".")[-1]}'
            
            # 組合源檔案路徑和目標檔案路徑
            source_path = os.path.join(source_directory, image_file)
            dest_path = os.path.join(dest_directory, new_file_name)
            if not os.path.exists('uploads'):
                os.mkdir('uploads')
            
            # 複製檔案
            shutil.copyfile(source_path, dest_path)
            print(f'Copied {image_file} to {new_file_name}')
            image_urls += new_file_name + ','

        # 移除最後一個逗號
        if image_urls.endswith(','):
            image_urls = image_urls[:-1]
        new_ad.image_urls=image_urls

        # 處理圖檔
        # if 'filename' in request.files:
        #     max_id += 1
        #     count = 1
        #     image_urls = ''
        #     files = request.files.getlist('filename')
        #     for file in files:
        #         if file and file.filename:
        #             name, extension = os.path.splitext(file.filename)
        #             new_filename = f'{max_id}_{count}{extension}'
        #             filepath = os.path.join(UPLOAD_FOLDER, new_filename)
        #             file.save(filepath)
        #             image_urls += new_filename + ','
        #             count += 1
        #     # 移除最後一個逗號
        #     if image_urls.endswith(','):
        #         image_urls = image_urls[:-1]
        #     new_ad.image_urls=image_urls

        db.session.add(new_ad)
        db.session.commit()
    
    return "<h1>fuck</h1>"