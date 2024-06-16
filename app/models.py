from app.extensions import db
from flask_login import UserMixin
from datetime import datetime

class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.String(256), primary_key=True, comment='使用者ID')
    passwd = db.Column(db.String(256), unique=False, nullable=False, comment='使用者密碼')
    name = db.Column(db.String(256), unique=False, nullable=False, comment='使用者名稱')
    email = db.Column(db.String(256), unique=False, nullable=False, comment='使用者信箱')
    tel = db.Column(db.String(256), unique=False, nullable=True, comment='使用者電話')
    type = db.Column(db.String(256), comment='使用者類別：管理員、導師、學生、房東')

    __mapper_args__ = {
        'polymorphic_identity': 'user',
        'polymorphic_on': type
    }

class Administrator(User):
    __tablename__ = 'administrator'
    id = db.Column(db.String(256), db.ForeignKey('user.id'), primary_key=True, comment='管理員ID')

    __mapper_args__ = {
        'polymorphic_identity': 'administrator'
    }

class Advisor(User):
    __tablename__ = 'advisor'
    id = db.Column(db.String(256), db.ForeignKey('user.id'), primary_key=True, comment='導師ID')
    dept = db.Column(db.String(256), unique=False, nullable=False, comment='導師所屬系所')
    rank = db.Column(db.String(256), unique=False, nullable=False, comment='導師職級：教授、副教授、助理教授')
    office_addr = db.Column(db.String(256), unique=False, nullable=False, comment='導師辦公室位址')
    office_tel = db.Column(db.String(256), unique=False, nullable=False, comment='導師辦公室電話')

    __mapper_args__ = {
        'polymorphic_identity': 'advisor'
    }

class Student(User):
    __tablename__ = 'student'
    id = db.Column(db.String(256), db.ForeignKey('user.id'), primary_key=True, comment='學生學號')
    dept = db.Column(db.String(256), unique=False, nullable=False, comment='學生所屬系所')
    enroll_year = db.Column(db.Integer, unique=False, nullable=False, comment='學生入學年分')
    sex = db.Column(db.Boolean, unique=False, nullable=True, comment='學生性別')
    home_addr = db.Column(db.String(256), unique=False, nullable=True, comment='學生家中地址')
    home_tel = db.Column(db.String(256), unique=False, nullable=True, comment='學生家裡電話')
    contact_name = db.Column(db.String(256), unique=False, nullable=True, comment='家裡聯絡人姓名')
    contact_tel = db.Column(db.String(256), unique=False, nullable=True, comment='家裡聯絡人電話')
    advisor_id = db.Column(db.String(256), db.ForeignKey('advisor.id'), unique=False, nullable=False, comment='學生的導師')

    __mapper_args__ = {
        'polymorphic_identity': 'student'
    }

class Landlord(User):
    __tablename__ = 'landlord'
    id = db.Column(db.String(256), db.ForeignKey('user.id'), primary_key=True, comment='房東ID')

    __mapper_args__ = {
        'polymorphic_identity': 'landlord'
    }

#訪視紀錄
class VisitRecord(db.Model):
    __tablename__ = 'visit_record'
    id = db.Column(db.String(256), db.ForeignKey('student.id'), primary_key=True, comment='學生學號')
    semester = db.Column(db.String(256), primary_key=True, comment='學年及學期') # 學年+學期

    visit_date_time = db.Column(db.DateTime, unique=False, nullable=False, comment='訪視時間')

    # 校外賃居資料（學生填寫）
    landlord_name = db.Column(db.String(256), unique=False, nullable=False, comment='房東姓名')
    landlord_tel = db.Column(db.String(256), unique=False, nullable=False, comment='房東電話')
    addr = db.Column(db.String(256), unique=False, nullable=False, comment='租賃地址')
    building_type = db.Column(db.String(256), unique=False, nullable=False, comment='租屋型態')
    room_type = db.Column(db.String(256), unique=False, nullable=False, comment='房間類型')
    rent = db.Column(db.Integer, unique=False, nullable=False, comment='每月租金')
    deposit = db.Column(db.Integer, unique=False, nullable=False, comment='押金')
    recommand = db.Column(db.Boolean, unique=False, nullable=False, comment='是否值得推薦其他同學租賃')
    
    # 賃居安全自主管理檢視資料（學生填寫）
    safe_manage1 = db.Column(db.Boolean, unique=False, nullable=False, comment='木造隔間或鐵皮加蓋')
    safe_manage2 = db.Column(db.Boolean, unique=False, nullable=False, comment='有火警警報器或偵煙器')
    safe_manage3 = db.Column(db.Boolean, unique=False, nullable=False, comment='逃生通道暢通且標示清楚')
    safe_manage4 = db.Column(db.Boolean, unique=False, nullable=False, comment='門禁及鎖具良好管理')
    safe_manage5 = db.Column(db.Boolean, unique=False, nullable=False, comment='有安裝照明設備(停車場及周邊)')
    safe_manage6 = db.Column(db.Boolean, unique=False, nullable=False, comment='瞭解熟悉電路安全及逃生要領')
    safe_manage7 = db.Column(db.Boolean, unique=False, nullable=False, comment='熟悉派出所、醫療、消防隊、學校校安專線電話')
    safe_manage8 = db.Column(db.Boolean, unique=False, nullable=False, comment='使用多種電器(高耗能)，是否同時插在同一條延長線')
    safe_manage9 = db.Column(db.Boolean, unique=False, nullable=False, comment='有滅火器且功能正常')
    safe_manage10 = db.Column(db.Boolean, unique=False, nullable=False, comment='熱水器(電熱式及瓦斯式)安全良好，無一氧化碳中毒疑慮')
    safe_manage11 = db.Column(db.Boolean, unique=False, nullable=False, comment='分間6個以上房間或10個以上床位')
    safe_manage12 = db.Column(db.Boolean, unique=False, nullable=False, comment='有安裝監視器設備')
    safe_manage13 = db.Column(db.Boolean, unique=False, nullable=False, comment='使用<內政部定型化租賃契約>')

    # 環境作息及評估（導師填寫）
    deposit_demand = db.Column(db.Boolean, unique=False, nullable=False, comment='押金要求。 True:合理 False:不合理')
    water_electric_bill_demand = db.Column(db.Boolean, unique=False, nullable=False, comment='水電費要求。 True:合理 False:不合理')
    environment = db.Column(db.Integer, unique=False, nullable=False, comment='居家環境。 0:佳 1:適中 2:欠佳')
    environment_description = db.Column(db.String(256), unique=False, nullable=True, comment='居家環境欠佳說明')
    facility = db.Column(db.Integer, unique=False, nullable=False, comment='生活設施。 0:佳 1:適中 2:欠佳')
    faclity_description = db.Column(db.String(256), unique=False, nullable=True, comment='生活設施欠佳說明')
    situation = db.Column(db.Integer, unique=False, nullable=False, comment='訪視現況。 0:生活規律 1:適中 2:待加強')
    situation_description = db.Column(db.String(256), unique=False, nullable=True, comment='訪視現況待加強說明')
    is_get_along_with = db.Column(db.Boolean, unique=False, nullable=False, comment='主客相處。 True:和睦 False:欠佳')

    # 訪視結果（導師填寫）
    result = db.Column(db.Integer, unique=False, nullable=False, comment='訪視結果。 0:整體賃居狀況良好 1:聯繫家長關注 2:安全堪慮請協助 3:其他')
    result_description = db.Column(db.String(256), unique=False, nullable=True, comment='其他說明')
    others1 = db.Column(db.String(256), unique=False, nullable=True, comment='其他紀載或建議事項')

    # 關懷宣導項目（懇請導師賃居訪視時多予關懷叮嚀）
    traffic_safty = db.Column(db.Boolean, unique=False, nullable=False, comment='交通安全')
    smoke = db.Column(db.Boolean, unique=False, nullable=False, comment='拒絕菸害')
    drug = db.Column(db.Boolean, unique=False, nullable=False, comment='拒絕毒品')
    dengue = db.Column(db.Boolean, unique=False, nullable=False, comment='登革熱防治')
    others2 = db.Column(db.String(256), unique=False, nullable=True, comment='其他說明')

# 住宿資料
class AccommodationInfo(db.Model):
    __tablename__ = 'accommodation_info'
    id = db.Column(db.String(256), db.ForeignKey('student.id'), primary_key=True, comment='學生學號')
    semester = db.Column(db.String(256), primary_key=True, comment='學年及學期')
    
    where_to_live = db.Column(db.Integer, unique=False, nullable=False, comment='住宿地。 0:住家裡 1:寄居親友家 2:住校 3:在外租屋')
    addr = db.Column(db.String(256), unique=False, nullable=True, comment='住宿地址')
    landlord_name = db.Column(db.String(256), unique=False, nullable=True, comment='房東姓名')
    landlord_tel = db.Column(db.String(256), unique=False, nullable=True, comment='房東電話')
    rent = db.Column(db.Integer, unique=False, nullable=True, comment='租金')
    roommate_id = db.Column(db.String(256), db.ForeignKey('student.id'), unique=False, nullable=True, comment='同住室友學號')
    


class Advertisement(db.Model):
    __tablename__ = 'advertisement'
    id = db.Column(db.Integer, primary_key=True, comment='租屋廣告編號')
    title = db.Column(db.String(256), unique=False, nullable=False, comment='租屋廣告標題')
    rent_lower = db.Column(db.Integer, unique=False, nullable=False ,comment='月租金下限')
    rent_upper = db.Column(db.Integer, unique=False, nullable=False ,comment='月租金上限')
    addr = db.Column(db.String(256), unique=False, nullable=False, comment='地址')

    suite_num = db.Column(db.Integer, unique=False, nullable=False, comment='套房總數')
    room_num = db.Column(db.Integer, unique=False, nullable=False, comment='雅房總數')
    suite_empty = db.Column(db.Integer, unique=False, nullable=False, comment='空套房數量')
    room_empty = db.Column(db.Integer, unique=False, nullable=False, comment='空雅房數量')
    suite_size = db.Column(db.Integer, unique=False, nullable=False, comment='套房坪數')
    room_size = db.Column(db.Integer, unique=False, nullable=False, comment='雅房坪數')

    building_type = db.Column(db.String(256), unique=False, nullable=False, comment='房屋類型')
    building_age = db.Column(db.Integer, unique=False, nullable=False ,comment='屋齡')
    floor1 = db.Column(db.Integer, unique=False, nullable=False ,comment='樓')
    floor2 = db.Column(db.Integer, unique=False, nullable=False ,comment='層')
    size = db.Column(db.Integer, unique=False, nullable=False ,comment='坪數')

    rental_type = db.Column(db.String(256), unique=False, nullable=False, comment='出租類型')
    electricity_meter = db.Column(db.Integer, unique=False, nullable=True, comment='有無獨立電表')
    partition_material = db.Column(db.String(256), unique=False, nullable=False, comment='隔間材質')
    deposit = db.Column(db.String(256), unique=False, nullable=False ,comment='押金')
    sex_limit = db.Column(db.String(256), unique=False, nullable=False, comment='性別要求')
    identity_limit = db.Column(db.String(256), unique=False, nullable=False, comment='身分要求')
    others_fee = db.Column(db.String(256), unique=False, nullable=False, comment='其他費用')
    smoke = db.Column(db.Integer, unique=False, nullable=True, comment='無菸租屋')

    # 屋內設備
    sofa = db.Column(db.Integer, unique=False, nullable=True, comment='沙發')
    telephone = db.Column(db.Integer, unique=False, nullable=True, comment='電話')
    bookcase = db.Column(db.Integer, unique=False, nullable=True, comment='書櫃')
    wardrobe = db.Column(db.Integer, unique=False, nullable=True, comment='衣櫃')
    central_air_conditioning = db.Column(db.Integer, unique=False, nullable=True, comment='中央空調')
    fiber_optic_network1 = db.Column(db.Integer, unique=False, nullable=True, comment='光纖網路')
    washing_machine = db.Column(db.Integer, unique=False, nullable=True, comment='洗衣機')
    single_bed = db.Column(db.Integer, unique=False, nullable=True, comment='單人床')
    dehydrator = db.Column(db.Integer, unique=False, nullable=True, comment='脫水機')
    cable_television = db.Column(db.Integer, unique=False, nullable=True, comment='第四台')
    dryer = db.Column(db.Integer, unique=False, nullable=True, comment='烘乾機')
    desk_and_chair = db.Column(db.Integer, unique=False, nullable=True, comment='書桌(椅)')
    refrigerator = db.Column(db.Integer, unique=False, nullable=True, comment='電冰箱')
    double_bed = db.Column(db.Integer, unique=False, nullable=True, comment='雙人床')
    water_dispenser = db.Column(db.Integer, unique=False, nullable=True, comment='飲水機')
    television = db.Column(db.Integer, unique=False, nullable=True, comment='電視機')
    air_conditioner = db.Column(db.Integer, unique=False, nullable=True, comment='冷氣機')
    table_lamp = db.Column(db.Integer, unique=False, nullable=True, comment='檯燈')
    broadband_network = db.Column(db.Integer, unique=False, nullable=True, comment='寬頻網路')

    # 公共設施
    fire_extinguishers_smoke_detectors_and_monitors_per_floor = db.Column(db.Integer, unique=False, nullable=True, comment='每層樓滅火器及煙霧偵測器及監視器')
    parking_lot = db.Column(db.Integer, unique=False, nullable=True, comment='停車場')
    kitchen = db.Column(db.Integer, unique=False, nullable=True, comment='廚房')
    laundry_area = db.Column(db.Integer, unique=False, nullable=True, comment='晒衣場')
    parking_lot_elevator = db.Column(db.Integer, unique=False, nullable=True, comment='停車場電梯')
    public_balcony = db.Column(db.Integer, unique=False, nullable=True, comment='公共陽台')
    courtyard = db.Column(db.Integer, unique=False, nullable=True, comment='中庭')
    elevator = db.Column(db.Integer, unique=False, nullable=True, comment='電梯')
    fiber_optic_network2 = db.Column(db.Integer, unique=False, nullable=True, comment='光纖網路')
    courtyard_parking_lot = db.Column(db.Integer, unique=False, nullable=True, comment='中庭停車場')
    lounge = db.Column(db.Integer, unique=False, nullable=True, comment='交誼廳')

    description = db.Column(db.Text, unique=False, nullable=True, comment='屋況說明')

    # 熱水器
    electric_water_heater = db.Column(db.Integer, unique=False, nullable=False, comment='電熱水器')
    gas_water_heater = db.Column(db.Integer, unique=False, nullable=False, comment='瓦斯熱水器')
    solar_water_heater = db.Column(db.Integer, unique=False, nullable=False, comment='太陽能熱水器')
    natural_gas = db.Column(db.Integer, unique=False, nullable=False, comment='天然瓦斯')
    bottled_gas = db.Column(db.Integer, unique=False, nullable=False, comment='桶裝瓦斯')

    # 安全設施
    escape_ladder = db.Column(db.Integer, unique=False, nullable=False, comment='逃生梯')
    security_personnel = db.Column(db.Integer, unique=False, nullable=False, comment='保全人員')
    slow_descend_device = db.Column(db.Integer, unique=False, nullable=False, comment='緩降梯')
    carbon_monoxide_detector = db.Column(db.Integer, unique=False, nullable=False, comment='一氧化碳警報器')
    electric_water_heater_power_cut_off_device = db.Column(db.Integer, unique=False, nullable=False, comment='電用熱水器斷電設備')
    gas_water_heater_forced_exhaust_device = db.Column(db.Integer, unique=False, nullable=False, comment='瓦斯熱水器強制排氣設備')
    fire_extinguisher = db.Column(db.Integer, unique=False, nullable=False, comment='滅火器')
    smoke_detector = db.Column(db.Integer, unique=False, nullable=False, comment='偵煙設備')
    escape_route_clear_and_marked = db.Column(db.Integer, unique=False, nullable=False, comment='逃生路線暢通及標示')
    lighting_equipment = db.Column(db.Integer, unique=False, nullable=False, comment='照明設備')
    surveillance_system = db.Column(db.Integer, unique=False, nullable=False, comment='監視錄影設備(系統)')
    access_control_system = db.Column(db.Integer, unique=False, nullable=False, comment='門禁系統')
    firefighting_system = db.Column(db.Integer, unique=False, nullable=False, comment='消防系統')

    # 證明文件
    landlord_identification_documents = db.Column(db.Integer, unique=False, nullable=False, comment='房東身分證明文件')
    power_of_attorney = db.Column(db.Integer, unique=False, nullable=False, comment='委託書')
    property_ownership_certificate = db.Column(db.Integer, unique=False, nullable=False, comment='房屋所有權狀')
    property_tax_bill = db.Column(db.Integer, unique=False, nullable=False, comment='房屋稅單')

    # 安全訪評
    meets_ministry_of_education_safety_standards = db.Column(db.Integer, unique=False, nullable=False, comment='符合教育部安全訪評規範')
    
    image_urls = db.Column(db.Text, unique=False, nullable=True, comment='廣告圖檔路徑')
    pulish_date = db.Column(db.DateTime, unique=False, nullable=True, comment='刊登日期')
    update_date = db.Column(db.DateTime, unique=False, nullable=True, comment='更新日期')
    due_date = db.Column(db.DateTime, unique=False, nullable=True, comment='截止日期')
    timestamp = db.Column(db.DateTime, unique=False, nullable=False, comment='送出刊登請求的時間')
    status = db.Column(db.Integer, unique=False, nullable=False, comment='審核狀態。 0:待審核 1:通過 2:未通過')
    landlord_id = db.Column(db.String(10), db.ForeignKey('landlord.id'), unique=False, nullable=False, comment='房東ID')

    def __init__(self,
                electricity_meter,
                smoke,
                sofa,
                telephone,
                bookcase,
                wardrobe,
                central_air_conditioning,
                fiber_optic_network1,
                washing_machine,
                single_bed,
                dehydrator,
                cable_television,
                dryer,
                desk_and_chair,
                refrigerator,
                double_bed,
                water_dispenser,
                television,
                air_conditioner,
                table_lamp,
                broadband_network,
                fire_extinguishers_smoke_detectors_and_monitors_per_floor,
                parking_lot,
                kitchen,
                laundry_area,
                parking_lot_elevator,
                public_balcony,
                courtyard,
                elevator,
                fiber_optic_network2,
                courtyard_parking_lot,
                lounge,
                electric_water_heater,
                gas_water_heater,
                solar_water_heater,
                natural_gas,
                bottled_gas,
                escape_ladder,
                security_personnel,
                slow_descend_device,
                carbon_monoxide_detector,
                electric_water_heater_power_cut_off_device,
                gas_water_heater_forced_exhaust_device,
                fire_extinguisher,
                smoke_detector,
                escape_route_clear_and_marked,
                lighting_equipment,
                surveillance_system,
                access_control_system,
                firefighting_system,
                landlord_identification_documents,
                power_of_attorney,
                property_ownership_certificate,
                property_tax_bill,
                meets_ministry_of_education_safety_standards,
                ):
        self.electricity_meter = electricity_meter
        self.smoke = smoke
        # 屋內設備
        self.sofa = sofa
        self.telephone = telephone
        self.bookcase = bookcase
        self.wardrobe = wardrobe
        self.central_air_conditioning = central_air_conditioning
        self.fiber_optic_network1 = fiber_optic_network1
        self.washing_machine = washing_machine
        self.single_bed = single_bed
        self.dehydrator = dehydrator
        self.cable_television = cable_television
        self.dryer = dryer
        self.desk_and_chair = desk_and_chair
        self.refrigerator = refrigerator
        self.double_bed = double_bed
        self.water_dispenser = water_dispenser
        self.television = television
        self.air_conditioner = air_conditioner
        self.table_lamp = table_lamp
        self.broadband_network = broadband_network
        # 公共設施
        self.fire_extinguishers_smoke_detectors_and_monitors_per_floor = fire_extinguishers_smoke_detectors_and_monitors_per_floor
        self.parking_lot = parking_lot
        self.kitchen = kitchen
        self.laundry_area = laundry_area
        self.parking_lot_elevator = parking_lot_elevator
        self.public_balcony = public_balcony
        self.courtyard = courtyard
        self.elevator = elevator
        self.fiber_optic_network2 = fiber_optic_network2
        self.courtyard_parking_lot = courtyard_parking_lot
        self.lounge = lounge
        # 熱水器
        self.electric_water_heater = electric_water_heater
        self.gas_water_heater = gas_water_heater
        self.solar_water_heater = solar_water_heater
        self.natural_gas = natural_gas
        self.bottled_gas = bottled_gas
        # 安全設施
        self.escape_ladder = escape_ladder
        self.security_personnel = security_personnel
        self.slow_descend_device = slow_descend_device
        self.carbon_monoxide_detector = carbon_monoxide_detector
        self.electric_water_heater_power_cut_off_device = electric_water_heater_power_cut_off_device
        self.gas_water_heater_forced_exhaust_device = gas_water_heater_forced_exhaust_device
        self.fire_extinguisher = fire_extinguisher
        self.smoke_detector = smoke_detector
        self.escape_route_clear_and_marked = escape_route_clear_and_marked
        self.lighting_equipment = lighting_equipment
        self.surveillance_system = surveillance_system
        self.access_control_system = access_control_system
        self.firefighting_system = firefighting_system
        # 證明文件
        self.landlord_identification_documents = landlord_identification_documents
        self.power_of_attorney = power_of_attorney
        self.property_ownership_certificate = property_ownership_certificate
        self.property_tax_bill = property_tax_bill
        # 安全訪評
        self.meets_ministry_of_education_safety_standards = meets_ministry_of_education_safety_standards
    
    
    def get_equip_list(self):
        equip_list = []
        equip_list.append('沙發') if self.sofa == 1 else None
        equip_list.append('電話') if self.telephone == 1 else None
        equip_list.append('書櫃') if self.bookcase == 1 else None
        equip_list.append('衣櫃') if self.wardrobe == 1 else None
        equip_list.append('中央空調') if self.central_air_conditioning == 1 else None
        equip_list.append('光纖網路') if self.fiber_optic_network1 == 1 else None
        equip_list.append('洗衣機') if self.washing_machine == 1 else None
        equip_list.append('單人床') if self.single_bed == 1 else None
        equip_list.append('脫水機') if self.dehydrator == 1 else None
        equip_list.append('第四台') if self.cable_television == 1 else None
        equip_list.append('烘乾機') if self.dryer == 1 else None
        equip_list.append('書桌(椅)') if self.desk_and_chair == 1 else None
        equip_list.append('電冰箱') if self.refrigerator == 1 else None
        equip_list.append('雙人床') if self.double_bed == 1 else None
        equip_list.append('飲水機') if self.water_dispenser == 1 else None
        equip_list.append('電視機') if self.television == 1 else None
        equip_list.append('冷氣機') if self.air_conditioner == 1 else None
        equip_list.append('檯燈') if self.table_lamp == 1 else None
        equip_list.append('寬頻網路') if self.broadband_network == 1 else None
        return equip_list
    
    def get_public_equip_list(self):
        public_equip_list = []
        public_equip_list.append('每層樓滅火器及煙霧偵測器及監視器') if self.fire_extinguishers_smoke_detectors_and_monitors_per_floor == 1 else None
        public_equip_list.append('停車場') if self.parking_lot == 1 else None
        public_equip_list.append('廚房') if self.kitchen == 1 else None
        public_equip_list.append('晒衣場') if self.laundry_area == 1 else None
        public_equip_list.append('停車場電梯') if self.parking_lot_elevator == 1 else None
        public_equip_list.append('公共陽台') if self.public_balcony == 1 else None
        public_equip_list.append('中庭') if self.courtyard == 1 else None
        public_equip_list.append('電梯') if self.elevator == 1 else None
        public_equip_list.append('光纖網路') if self.fiber_optic_network2 == 1 else None
        public_equip_list.append('中庭停車場') if self.courtyard_parking_lot == 1 else None
        public_equip_list.append('交誼廳') if self.lounge == 1 else None
        return public_equip_list
    
    def get_heater_list(self):
        heater_list = []
        heater_list.append('電熱水器') if self.electric_water_heater == 1 else None
        heater_list.append('瓦斯熱水器') if self.gas_water_heater == 1 else None
        heater_list.append('太陽能熱水器') if self.solar_water_heater == 1 else None
        heater_list.append('天然瓦斯') if self.natural_gas == 1 else None
        heater_list.append('桶裝瓦斯') if self.bottled_gas == 1 else None
        return heater_list
    
    def get_safety_equip_list(self):
        safety_equip_list = []
        safety_equip_list.append('逃生梯') if self.escape_ladder == 1 else None
        safety_equip_list.append('保全人員') if self.security_personnel == 1 else None
        safety_equip_list.append('緩降梯') if self.slow_descend_device == 1 else None
        safety_equip_list.append('一氧化碳警報器') if self.carbon_monoxide_detector == 1 else None
        safety_equip_list.append('電用熱水器斷電設備') if self.electric_water_heater_power_cut_off_device == 1 else None
        safety_equip_list.append('瓦斯熱水器強制排氣設備') if self.gas_water_heater_forced_exhaust_device == 1 else None
        safety_equip_list.append('滅火器') if self.fire_extinguisher == 1 else None
        safety_equip_list.append('偵煙設備') if self.smoke_detector == 1 else None
        safety_equip_list.append('逃生路線暢通及標示') if self.escape_route_clear_and_marked == 1 else None
        safety_equip_list.append('照明設備') if self.lighting_equipment == 1 else None
        safety_equip_list.append('監視錄影設備(系統)') if self.surveillance_system == 1 else None
        safety_equip_list.append('門禁系統') if self.access_control_system == 1 else None
        safety_equip_list.append('消防系統') if self.firefighting_system == 1 else None
        return safety_equip_list
    
    def get_document_list(self):
        doc_list = []
        doc_list.append('房東身分證明文件') if self.landlord_identification_documents == 1 else None
        doc_list.append('委託書') if self.power_of_attorney == 1 else None
        doc_list.append('房屋所有權狀') if self.property_ownership_certificate == 1 else None
        doc_list.append('房屋稅單') if self.property_tax_bill == 1 else None
        return doc_list

class Test(db.Model):
    __tablename__ = 'test'
    id = db.Column(db.Integer, primary_key=True, comment='Po文編號')
    fuck = db.Column(db.Boolean, unique=False, nullable=False, comment='房東身分證明文件')

    def __init__(self, fuck):
        self.fuck = fuck

class Post(db.Model):
    __tablename__ = 'post'
    id = db.Column(db.Integer, primary_key=True, comment='Po文編號')
    title = db.Column(db.String(50), unique=False, nullable=False, comment='Po文標題')
    text = db.Column(db.Text, unique=False, nullable=False, comment='Po文內容')
    timestamp = db.Column(db.DateTime, unique=False, nullable=False, default=datetime.utcnow, comment='Po文時間')
    image_urls = db.Column(db.Text, unique=False, nullable=True, comment='Po文圖檔路徑')
    user_id = db.Column(db.String(10), db.ForeignKey('user.id'), unique=False, nullable=False, comment='Po文者ID')

    def __init__(self, title, text, user_id, image_urls=None):
        self.title = title
        self.text = text
        self.image_urls = image_urls
        self.user_id = user_id

class Comment(db.Model):
    __tablename__ = 'comment'
    id = db.Column(db.Integer, primary_key=True, comment='留言編號')
    text = db.Column(db.Text, unique=False, nullable=False, comment='留言內容')
    timestamp = db.Column(db.DateTime, unique=False, nullable=False, default=datetime.utcnow, comment='留言時間')
    image_urls = db.Column(db.Text, unique=False, nullable=True, comment='留言圖檔路徑')
    user_id = db.Column(db.String(256), db.ForeignKey('user.id'), unique=False, nullable=False, comment='留言者ID')
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), unique=False, nullable=False, comment='文章ID')

    def __init__(self, text, user_id, post_id, image_urls=None):
        self.text = text
        self.user_id = user_id
        self.post_id = post_id
        self.image_urls = image_urls