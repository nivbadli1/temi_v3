# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from flask_login import UserMixin
from datetime import datetime

from apps import db, login_manager

from apps.authentication.util import hash_pass


class Users(db.Model, UserMixin):
    __tablename__ = 'Users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True)
    email = db.Column(db.String(64), unique=True)
    password = db.Column(db.LargeBinary)

    def __init__(self, **kwargs):
        for property, value in kwargs.items():
            # depending on whether value is an iterable or not, we must
            # unpack it's value (when **kwargs is request.form, some values
            # will be a 1-element list)
            if hasattr(value, '__iter__') and not isinstance(value, str):
                # the ,= unpack of a singleton fails PEP8 (travis flake8 test)
                value = value[0]

            if property == 'password':
                value = hash_pass(value)  # we need bytes here (not plain str)

            setattr(self, property, value)

    def __repr__(self):
        return str(self.username)


class Patient(db.Model):
    __tablename__ = "patients"

    patient_id = db.Column(db.Integer, primary_key=True)
    f_name = db.Column(db.String(50))
    l_name = db.Column(db.String(50))
    bed = db.Column(db.Integer)
    department = db.Column(db.Integer, db.ForeignKey('Users.id'), nullable=False)
    max_calls = db.Column(db.Integer)
    contacts = db.relationship('Contact', backref='patient', lazy='select')
    events = db.relationship('Event', backref='patient', lazy='dynamic')

    def __init__(self, patient_id, f_name, l_name, bed, department, max_calls):
        self.patient_id = patient_id
        self.f_name = f_name
        self.l_name = l_name
        self.bed = bed
        self.department = department
        self.max_calls = max_calls

    def get_patient_contacts(self):
        for contact in self.contacts:
            print(contact.id, contact.f_name)

    def __repr__(self):
        return "Patient(patient_id='%s', l_name='%s', f_name='%s', bed='%s', department='%s', max_calls='%s')" % (
            self.patient_id, self.l_name, self.f_name, self.bed, self.department, self.max_calls)


class Contact(db.Model):
    __tablename__ = 'contacts'


    contact_id = db.Column(db.Integer, primary_key=True)
    f_name = db.Column(db.String(50))
    l_name = db.Column(db.String(50))
    phone = db.Column(db.String(50))
    mail = db.Column(db.String(50))
    priority = db.Column(db.Integer)
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.patient_id', ondelete='CASCADE', onupdate='CASCADE'),
                           index=True)
    events = db.relationship('Event', backref='contact', lazy='dynamic')
    contacts_times = db.relationship('ContactsTime', backref='contact', lazy='select')

    def __init__(self, patient_id, f_name, l_name, phone, mail, priority):
        self.patient_id = patient_id
        self.f_name = f_name
        self.l_name = l_name
        self.phone = phone
        self.mail = mail
        self.priority = priority


    def __repr__(self):
        return '<Contact: %s, %s, %s, %s, %s>' % (self.f_name, self.l_name, self.phone, self.mail, self.priority)

class ContactsTime(db.Model):
    __tablename__ = 'contacts_times'

    id = db.Column(db.Integer, primary_key=True)
    day = db.Column(db.Integer)
    contact_id = db.Column(db.Integer,db.ForeignKey('contacts.contact_id', ondelete='CASCADE', onupdate='CASCADE'),
                           index=True)
    from_hour = db.Column( db.Time)
    to_hour = db.Column(db.Time)
    contacts = db.relationship(Contact,backref='contact')
    def __init__(self, contact_id, day, from_hour, to_hour):
        self.contact_id = contact_id
        self.day = day
        self.from_hour = from_hour
        self.to_hour = to_hour

    def __repr__(self):
        return '<Time: %s, %s, %s, %s, %s>' % (self.day, self.from_hour, self.to_hour, self.id, self.contact_id)

class DepartmentsTimes(db.Model):
    __tablename__ = 'departments_times'

    deprtment_id = db.Column(db.Integer, db.ForeignKey('Users.id'), nullable=False)
    _from = db.Column('from', db.Time, primary_key=True, nullable=False)
    to = db.Column(db.Time, primary_key=True, nullable=False)
    day = db.Column(db.Integer, primary_key=True, nullable=False)

    def __init__(self, num, _from, to, day):
        self.num = num
        self._from = _from
        self.to = to
        self.day = day


class LogMng(db.Model):
    __tablename__ = 'log_mng'

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    subject = db.Column(db.String(100), primary_key=True, nullable=False)
    desc = db.Column(db.String(100))

    def __init__(self, subject, desc):
        self.subject = subject
        self.desc = desc


class Event(db.Model):
    __tablename__ = 'events'

    event_id = db.Column(db.String(100), primary_key=True)
    url = db.Column(db.String(256))
    contact_id = db.Column(db.Integer, db.ForeignKey('contacts.contact_id'))
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.patient_id'))
    start_time = db.Column(db.TIMESTAMP)
    status = db.Column(db.Integer)
    row_created_time = db.Column(db.TIMESTAMP, default=datetime.now())

    def __init__(self, event_id, url, start_time, status, patient_id, contact_id):
        self.url = url
        self.event_id = event_id
        self.start_time = start_time
        self.status = status
        self.patient_id = patient_id
        self.contact_id = contact_id


@login_manager.user_loader
def user_loader(id):
    return Users.query.filter_by(id=id).first()


@login_manager.request_loader
def request_loader(request):
    username = request.form.get('username')
    user = Users.query.filter_by(username=username).first()
    return user if user else None
