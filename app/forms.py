from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, TextAreaField, BooleanField, DateTimeField, SubmitField, RadioField
from wtforms.validators import DataRequired, Length, Optional, NumberRange, InputRequired

class AdvertisementForm(FlaskForm):
    title = StringField('廣告標題', validators=[DataRequired(), Length(max=256)])
    building_age = IntegerField('屋齡', validators=[InputRequired("請輸入數字"), NumberRange(min=0)])
    building_type = StringField('建物類型', validators=[DataRequired(), Length(max=256)])
    addr = StringField('地址', validators=[DataRequired(), Length(max=256)])
    rental_limit = StringField('限租條件', validators=[DataRequired(), Length(max=256)])
    rent = IntegerField('月租金', validators=[InputRequired("請輸入數字"), NumberRange(min=0)])
    image_urls = TextAreaField('廣告圖檔路徑', validators=[Optional()])
    pulish_date = DateTimeField('刊登日期', validators=[Optional()])
    due_date = DateTimeField('截止日期', validators=[Optional()])
    suite = IntegerField('套房數量', validators=[InputRequired("請輸入數字"), NumberRange(min=0)])
    room = IntegerField('雅房數量', validators=[InputRequired("請輸入數字"), NumberRange(min=0)])
    smoke = RadioField('無菸租屋', choices=[('True','是'),('False','否')], validators=[DataRequired()])
    electricity_meter = RadioField('獨立電表', choices=[('True','有'),('False','無')], validators=[DataRequired()])
    wash_machine = RadioField('洗衣機', choices=[('True','有'),('False','無')], validators=[DataRequired()])
    water_dispenser = RadioField('飲水機', choices=[('True','有'),('False','無')], validators=[DataRequired()])
    internet = RadioField('網路', choices=[('True','有'),('False','無')], validators=[DataRequired()])
    parking = RadioField('停車位', choices=[('True','有'),('False','無')], validators=[DataRequired()])
    air_con = RadioField('冷氣', choices=[('True','有'),('False','無')], validators=[DataRequired()])
    water_heater = RadioField('熱水器', choices=[('True','有'),('False','無')], validators=[DataRequired()])
    description = TextAreaField('屋況簡述', validators=[Optional()])
    timestamp = DateTimeField('送出刊登請求的時間', validators=[Optional()])
    status = IntegerField('審核狀態', validators=[Optional()])
    landlord_id = StringField('房東ID', validators=[Optional(), Length(max=10)])
    submit = SubmitField('提交')