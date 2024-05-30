from extensions import db

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.String(256), primary_key=True)
    passwd = db.Column(db.String(256), unique=False, nullable=False)
    name = db.Column(db.String(256), unique=False, nullable=False)
    email = db.Column(db.String(256), unique=False, nullable=False)
    tel = db.Column(db.String(256), unique=False, nullable=False)
    type = db.Column(db.String(256))

    __mapper_args__ = {
        'polymorphic_identity': 'user',
        'polymorphic_on': type
    }

class Administrator(User):
    __tablename__ = 'administrator'
    id = db.Column(db.String(256), db.ForeignKey('user.id'), primary_key=True)

    __mapper_args__ = {
        'polymorphic_identity': 'administrator'
    }

class Advisor(User):
    __tablename__ = 'advisor'
    id = db.Column(db.String(256), db.ForeignKey('user.id'), primary_key=True)
    dept = db.Column(db.String(256), unique=False, nullable=False)
    rank = db.Column(db.String(256), unique=False, nullable=False)
    office_addr = db.Column(db.String(256), unique=False, nullable=False)
    office_tel = db.Column(db.String(256), unique=False, nullable=False)

    __mapper_args__ = {
        'polymorphic_identity': 'advisor'
    }

class Student(User):
    __tablename__ = 'student'
    id = db.Column(db.String(256), db.ForeignKey('user.id'), primary_key=True)
    dept = db.Column(db.String(256), unique=False, nullable=False)
    enroll_year = db.Column(db.Integer, unique=False, nullable=False)
    sex = db.Column(db.Boolean, unique=False, nullable=False)
    home_addr = db.Column(db.String(256), unique=False, nullable=False)
    home_tel = db.Column(db.String(256), unique=False, nullable=False)
    contact_name = db.Column(db.String(256), unique=False, nullable=False)
    contact_tel = db.Column(db.String(256), unique=False, nullable=False)
    advisor_id = db.Column(db.String(256), db.ForeignKey('advisor.id'), unique=False, nullable=False)

    __mapper_args__ = {
        'polymorphic_identity': 'student'
    }

class Landlord(User):
    __tablename__ = 'landlord'
    id = db.Column(db.String(256), db.ForeignKey('user.id'), primary_key=True)

    __mapper_args__ = {
        'polymorphic_identity': 'landlord'
    }

#訪視資料
class VisitRecord(db.Model):
    __tablename__ = 'visit_record'
    id = db.Column(db.String(256), primary_key=True)
    semester = db.Column(db.String(256), primary_key=True) # 學年+學期

    visit_date_time = db.Column(db.DateTime, unique=False, nullable=False)

    # 校外賃居資料（學生填寫）
    landlord_name = db.Column(db.String(256), unique=False, nullable=False)
    landlord_tel = db.Column(db.String(256), unique=False, nullable=False)
    addr = db.Column(db.String(256), unique=False, nullable=False)
    landlord_name = db.Column(db.String(256), unique=False, nullable=False)
    building_type = db.Column(db.String(256), unique=False, nullable=False)
    room_type = db.Column(db.String(256), unique=False, nullable=False)
    rent = db.Column(db.Integer, unique=False, nullable=False)
    deposit = db.Column(db.Integer, unique=False, nullable=False)
    recommand = db.Column(db.Boolean, unique=False, nullable=False)
    
    # 賃居安全自主管理檢視資料（學生填寫）
    safe_manage1 = db.Column(db.Boolean, unique=False, nullable=False, comment='木造隔間或鐵皮加蓋')
    safe_manage2 = db.Column(db.Boolean, unique=False, nullable=False, comment='備註')
    safe_manage3 = db.Column(db.Boolean, unique=False, nullable=False, comment='備註')
    safe_manage4 = db.Column(db.Boolean, unique=False, nullable=False, comment='備註')
    safe_manage5 = db.Column(db.Boolean, unique=False, nullable=False, comment='備註')
    safe_manage6 = db.Column(db.Boolean, unique=False, nullable=False, comment='備註')
    safe_manage7 = db.Column(db.Boolean, unique=False, nullable=False, comment='備註')
    safe_manage8 = db.Column(db.Boolean, unique=False, nullable=False, comment='備註')
    safe_manage9 = db.Column(db.Boolean, unique=False, nullable=False, comment='備註')
    safe_manage10 = db.Column(db.Boolean, unique=False, nullable=False, comment='備註')
    safe_manage11 = db.Column(db.Boolean, unique=False, nullable=False, comment='備註')
    safe_manage12 = db.Column(db.Boolean, unique=False, nullable=False, comment='備註')
    safe_manage13 = db.Column(db.Boolean, unique=False, nullable=False, comment='備註')

    # 環境作息及評估（導師填寫）
    deposit_demand = db.Column(db.Boolean, unique=False, nullable=False, comment='備註')
    water_electric_bill_demand = db.Column(db.Boolean, unique=False, nullable=False, comment='備註')
    environment = db.Column(db.String(256), unique=False, nullable=False, comment='備註')
    environment_description = db.Column(db.String(256), unique=False, nullable=True, comment='備註')
    facility = db.Column(db.String(256), unique=False, nullable=False, comment='備註')
    faclity_description = db.Column(db.String(256), unique=False, nullable=True, comment='備註')
    situation = db.Column(db.String(256), unique=False, nullable=False, comment='備註')
    situation_description = db.Column(db.String(256), unique=False, nullable=True, comment='備註')
    is_get_along_with = db.Column(db.Boolean, unique=False, nullable=False, comment='備註')

    # 訪視結果（導師填寫）
    result = db.Column(db.String(256), unique=False, nullable=False, comment='備註')
    result_description = db.Column(db.String(256), unique=False, nullable=True, comment='備註')
    others = db.Column(db.String(256), unique=False, nullable=True, comment='備註')

    # 關懷宣導項目（懇請導師賃居訪視時多予關懷叮嚀）
    traffic_safty = db.Column(db.Boolean, unique=False, nullable=False, comment='備註')
    smoke = db.Column(db.Boolean, unique=False, nullable=False, comment='備註')
    drug = db.Column(db.Boolean, unique=False, nullable=False, comment='備註')
    dengue = db.Column(db.Boolean, unique=False, nullable=False, comment='備註')
    others = db.Column(db.String(256), unique=False, nullable=True, comment='備註')

# 住宿資料
class AccommodationInfo(db.Model):
    __tablename__ = 'accommodation_info'
    id = db.Column(db.String(256), db.ForeignKey('student.id'), primary_key=True)
    semester = db.Column(db.String(256), primary_key=True) # 學年+學期
    
    where_to_live = db.Column(db.String(256), unique=False, nullable=False) # 家裡、宿舍、租屋
    addr = db.Column(db.String(256), unique=False, nullable=False)
    landlord_name = db.Column(db.String(256), unique=False, nullable=True)
    landlord_tel = db.Column(db.String(256), unique=False, nullable=True)
    rent = db.Column(db.Integer, unique=False, nullable=True)
    roommate_id = db.Column(db.String(256), db.ForeignKey('student.id'), unique=False, nullable=True)
    


class Advertisement(db.Model):
    __tablename__ = 'advertisement'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(256), unique=False, nullable=False)
    building_age = db.Column(db.Integer)
    building_type = db.Column(db.String(256), unique=False, nullable=False)
    addr = db.Column(db.String(256), unique=False, nullable=False)
    rental_limit = db.Column(db.String(256), unique=False, nullable=False)
    rent = db.Column(db.Integer)
    image_urls = db.Column(db.Text, unique=False, nullable=False)
    pulish_date = db.Column(db.DateTime, unique=False, nullable=False)
    due_date = db.Column(db.DateTime, unique=False, nullable=False)
    
    suite = db.Column(db.Integer, unique=False, nullable=False) # 套房
    room = db.Column(db.Integer, unique=False, nullable=False) # 雅房

    electricity_meter = db.Column(db.Boolean, unique=False, nullable=False)
    smoke = db.Column(db.Boolean, unique=False, nullable=False)
    wash_machine = db.Column(db.Boolean, unique=False, nullable=False)
    water_dispenser = db.Column(db.Boolean, unique=False, nullable=False)
    internet = db.Column(db.Boolean, unique=False, nullable=False)
    parking = db.Column(db.Boolean, unique=False, nullable=False)
    air_con = db.Column(db.Boolean, unique=False, nullable=False)
    water_heater = db.Column(db.Boolean, unique=False, nullable=False)
    
    description = db.Column(db.Text, unique=False, nullable=True)
    timestamp = db.Column(db.DateTime, unique=False, nullable=False)
    landlord_id = db.Column(db.String(10), db.ForeignKey('user.id'), unique=False, nullable=False)

class Post(db.Model):
    __tablename__ = 'post'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), unique=False, nullable=False)
    text = db.Column(db.Text, unique=False, nullable=False)
    timestamp = db.Column(db.DateTime, unique=False, nullable=False)
    image_urls = db.Column(db.Text, unique=False, nullable=False)
    user_id = db.Column(db.String(10), db.ForeignKey('user.id'), unique=False, nullable=False)

class Comment(db.Model):
    __tablename__ = 'comment'
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, unique=False, nullable=False)
    timestamp = db.Column(db.DateTime, unique=False, nullable=False)
    image_urls = db.Column(db.Text, unique=False, nullable=False)
    user_id = db.Column(db.String(256), db.ForeignKey('user.id'), unique=False, nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), unique=False, nullable=False)