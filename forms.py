from wtforms import StringField, SubmitField, IntegerField, SelectField
from wtforms.fields import DateField
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, Length
from __init__ import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class QRCodeData(FlaskForm):
    dat = StringField("Data", validators=[
                      DataRequired(), Length(min=3, max=500)])
    submit = SubmitField("Generate QRCode")


class Mine(FlaskForm):
    con_note = IntegerField("Consignment")
    client_id = IntegerField("client_id")
    client = StringField("Client")
    address = StringField("Address")
    mark = SelectField("Mark", choices=[" ", "B7.5(M100)", "B10(M150)", "B15(M200)",
                       "B20(M250)", "B22.5(M300)", "B25(M350)", "B30(M400)", "B35(M450)"])
    quantity = IntegerField("Meter cube?")
    quantity_tray = StringField("How many trays?")
    s_rep = SelectField("Sales repr.", choices=[
                        "", "Seller1", "Seller2", "Seller3", "Seller4"])
    quantity_fbs1 = StringField("Quantity of ФБС-0.6")
    quantity_fbs2 = StringField("Quantity of ФБС-0.8")
    quantity_fbs3 = StringField("Quantity of ФБС-0.9")
    quantity_fbs4 = StringField("Quantity of ФБС-1.2")
    quantity_fbs5 = StringField("Quantity of ФБС-2.4")
    precast1 = StringField("Precast1")
    precast2 = StringField("Precast2")
    precast3 = StringField("Precast3")
    precast4 = StringField("Precast4")
    precast5 = StringField("Precast5")
    length1 = StringField("Quantity1")
    length2 = StringField("Quantity2")
    length3 = StringField("Quantity3")
    length4 = StringField("Quantity4")
    length5 = StringField("Quantity5")
    pre_width1 = SelectField("Width1", choices=[
                             "", "1m 6 Pressure", "1m 8 Pressure", "1.2m 6 Pressure", "1.2m 8 Pressure", "1.2m(uncertified)"])
    pre_width2 = SelectField("Width2", choices=[
                             "", "1m 6 Pressure", "1m 8 Pressure", "1.2m 6 Pressure", "1.2m 8 Pressure", "1.2m(uncertified)"])
    pre_width3 = SelectField("Width3", choices=[
                             "", "1m 6 Pressure", "1m 8 Pressure", "1.2m 6 Pressure", "1.2m 8 Pressure", "1.2m(uncertified)"])
    pre_width4 = SelectField("Width4", choices=[
                             "", "1m 6 Pressure", "1m 8 Pressure", "1.2m 6 Pressure", "1.2m 8 Pressure", "1.2m(uncertified)"])
    pre_width5 = SelectField("Width5", choices=[
                             "", "1m 6 Pressure", "1m 8 Pressure", "1.2m 6 Pressure", "1.2m 8 Pressure", "1.2m(uncertified)"])
    type1 = StringField("Type1")
    type2 = StringField("Type2")
    type3 = StringField("Type3")
    type4 = StringField("Type4")
    type5 = StringField("Type5")
    price = IntegerField("Total")
    currency = SelectField("Currency", choices=["UZS", "Transfer"])
    price_rm = IntegerField("Price per cube")
    price_tray = IntegerField("Price per tray")
    price_fbs06 = IntegerField("Price FBS06")
    price_fbs08 = IntegerField("Price FBS08")
    price_fbs09 = IntegerField("Price FBS09")
    price_fbs12 = IntegerField("Price FBS12")
    price_fbs24 = IntegerField("Price FBS24")
    price_pre1 = IntegerField("Price for pr.1")
    price_pre2 = IntegerField("Price for pr.2")
    price_pre3 = IntegerField("Price for pr.3")
    price_pre4 = IntegerField("Price for pr.4")
    price_pre5 = IntegerField("Price for pr.5")
    paid = IntegerField("Paid")
    driver = StringField("Driver")
    date = StringField("Date")
    due_precast = StringField("Due Date")
    due_fbs = StringField("Due Date")
    due_tray = StringField("Due Date")
    due_rm = StringField("Due Date")
    user_fullname = StringField("User_fullname")
    submit = SubmitField("Confirm")


class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))


class Filters(FlaskForm):
    startdate = DateField("From", format="%Y-%m-%d",
                          validators=[DataRequired()])
    enddate = DateField("To", format="%Y-%m-%d", validators=[DataRequired()])
    submit = SubmitField("Filter")


# User Class:
class User(db.Model, UserMixin):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(250), unique=True)
    password = db.Column(db.String(150))
    fullname = db.Column(db.String(250))
    comment = db.Column(db.String(250))
    role = db.Column(db.String())
    notes = db.relationship("Note")
    reg = db.relationship("Reg", backref="user")


class Reg(db.Model):
    __tablename__ = "reg"
    id = db.Column(db.Integer, primary_key=True)
    con_note = db.Column(db.Integer)
    client_id = db.Column(db.Integer)
    client = db.Column(db.String())
    address = db.Column(db.String())
    s_rep = db.Column(db.String())
    mark = db.Column(db.String())
    quantity = db.Column(db.Integer)
    quantity_tray = db.Column(db.String())
    quantity_fbs1 = db.Column(db.String())
    quantity_fbs2 = db.Column(db.String())
    quantity_fbs3 = db.Column(db.String())
    quantity_fbs4 = db.Column(db.String())
    quantity_fbs5 = db.Column(db.String())
    precast1 = db.Column(db.String())
    precast2 = db.Column(db.String())
    precast3 = db.Column(db.String())
    precast4 = db.Column(db.String())
    precast5 = db.Column(db.String())
    length1 = db.Column(db.String())
    length2 = db.Column(db.String())
    length3 = db.Column(db.String())
    length4 = db.Column(db.String())
    length5 = db.Column(db.String())
    pre_width1 = db.Column(db.String())
    pre_width2 = db.Column(db.String())
    pre_width3 = db.Column(db.String())
    pre_width4 = db.Column(db.String())
    pre_width5 = db.Column(db.String())
    type1 = db.Column(db.String())
    type2 = db.Column(db.String())
    type3 = db.Column(db.String())
    type4 = db.Column(db.String())
    type5 = db.Column(db.String())
    price = db.Column(db.Integer)
    price_rm = db.Column(db.Integer)
    price_tray = db.Column(db.Integer)
    price_fbs06 = db.Column(db.Integer)
    price_fbs08 = db.Column(db.Integer)
    price_fbs09 = db.Column(db.Integer)
    price_fbs12 = db.Column(db.Integer)
    price_fbs24 = db.Column(db.Integer)
    price_pre1 = db.Column(db.Integer)
    price_pre2 = db.Column(db.Integer)
    price_pre3 = db.Column(db.Integer)
    price_pre4 = db.Column(db.Integer)
    price_pre5 = db.Column(db.Integer)
    paid = db.Column(db.Integer)
    currency = db.Column(db.String())
    driver = db.Column(db.String())
    date = db.Column(db.String)
    user_fullname = db.Column(db.String(), db.ForeignKey("user.fullname"))

    def __init__(self, con_note, client, address, quantity, mark, price, price_rm, price_tray, price_fbs06, price_fbs08, price_fbs09, price_fbs12, price_fbs24,
                 price_pre1, price_pre2, price_pre3, price_pre4, price_pre5, paid, currency, driver, date, user_fullname, client_id,
                 pre_width1, pre_width2, pre_width3, pre_width4, pre_width5, quantity_tray, s_rep,
                 precast1, precast2, precast3, precast4, precast5,
                 length1, length2, length3, length4, length5, type1, type2, type3, type4, type5,
                 quantity_fbs1, quantity_fbs2, quantity_fbs3, quantity_fbs4, quantity_fbs5):
        self.con_note = con_note
        self.client = client
        self.address = address
        self.quantity = quantity
        self.mark = mark
        self.price = price
        self.price_rm = price_rm
        self.price_tray = price_tray
        self.price_fbs06 = price_fbs06
        self.price_fbs08 = price_fbs08
        self.price_fbs09 = price_fbs09
        self.price_fbs12 = price_fbs12
        self.price_fbs24 = price_fbs24
        self.price_pre1 = price_pre1
        self.price_pre2 = price_pre2
        self.price_pre3 = price_pre3
        self.price_pre4 = price_pre4
        self.price_pre5 = price_pre5
        self.paid = paid
        self.currency = currency
        self.driver = driver
        self.date = date
        self.user_fullname = user_fullname
        self.client_id = client_id
        self.pre_width1 = pre_width1
        self.pre_width2 = pre_width2
        self.pre_width3 = pre_width3
        self.pre_width4 = pre_width4
        self.pre_width5 = pre_width5
        self.quantity_tray = quantity_tray
        self.s_rep = s_rep
        self.precast1 = precast1
        self.precast2 = precast2
        self.precast3 = precast3
        self.precast4 = precast4
        self.precast5 = precast5
        self.length1 = length1
        self.length2 = length2
        self.length3 = length3
        self.length4 = length4
        self.length5 = length5
        self.type1 = type1
        self.type2 = type2
        self.type3 = type3
        self.type4 = type4
        self.type5 = type5
        self.quantity_fbs1 = quantity_fbs1
        self.quantity_fbs2 = quantity_fbs2
        self.quantity_fbs3 = quantity_fbs3
        self.quantity_fbs4 = quantity_fbs4
        self.quantity_fbs5 = quantity_fbs5


class Stock(db.Model):
    __tablename__ = "stock"
    id = db.Column(db.Integer, primary_key=True)
    s_tray = db.Column(db.String())
    s_quantity_tray = db.Column(db.String())

    def __init__(self, s_tray, s_quantity_tray):
        self.s_tray = s_tray
        self.s_quantity_tray = s_quantity_tray


class Production(db.Model):
    __tablename__ = "production"
    id = db.Column(db.Integer, primary_key=True)
    mark = db.Column(db.String())
    quantity = db.Column(db.Integer)
    quantity_tray = db.Column(db.String())
    quantity_fbs1 = db.Column(db.String())
    quantity_fbs2 = db.Column(db.String())
    quantity_fbs3 = db.Column(db.String())
    quantity_fbs4 = db.Column(db.String())
    quantity_fbs5 = db.Column(db.String())
    precast1 = db.Column(db.String())
    precast2 = db.Column(db.String())
    precast3 = db.Column(db.String())
    precast4 = db.Column(db.String())
    precast5 = db.Column(db.String())
    length1 = db.Column(db.String())
    length2 = db.Column(db.String())
    length3 = db.Column(db.String())
    length4 = db.Column(db.String())
    length5 = db.Column(db.String())
    pre_width1 = db.Column(db.String())
    pre_width2 = db.Column(db.String())
    pre_width3 = db.Column(db.String())
    pre_width4 = db.Column(db.String())
    pre_width5 = db.Column(db.String())


class Tasks(db.Model):
    __tablename__ = "tasks"
    id = db.Column(db.Integer, primary_key=True)
    task_name = db.Column(db.String(5000))
    task_taker = db.Column(db.String)
    assigned_user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    assigned_user = db.relationship('User', backref='tasks')
    company = db.Column(db.String)
    companies = db.Column(db.String)
    deadline = db.Column(db.String)
    now_time = db.Column(db.String)


class Orgdata(db.Model):
    __tablename__ = "orgdata"
    id = db.Column(db.Integer, primary_key=True)
    orgresults = db.Column(db.String)


class Exhibition(db.Model):
    __talename__ = "exhibition"
    id = db.Column(db.Integer, primary_key=True)
    exh_datetime = db.Column(db.String)
    exh_name = db.Column(db.String)
    x_number = db.Column(db.Integer)
    x = db.Column(db.Float)
    seats = db.relationship('Seat', backref='exhibition', lazy=True)


class Seat(db.Model):
    __tablename__ = "seat"
    id = db.Column(db.Integer, primary_key=True)
    seat_number = db.Column(db.Integer)
    is_booked = db.Column(db.Boolean, default=False)
    price = db.Column(db.Float)
    exhibition_id = db.Column(db.Integer, db.ForeignKey('exhibition.id'))
