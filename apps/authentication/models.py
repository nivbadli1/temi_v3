# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""
import pandas as pd
from flask_login import UserMixin
from datetime import datetime

import pandas as pd
from pytz import lazy
from sqlalchemy import inspect

from apps import db, login_manager

from apps.authentication.util import hash_pass


class Users(db.Model, UserMixin):
    __tablename__ = 'Users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True)
    email = db.Column(db.String(64), unique=True)
    password = db.Column(db.LargeBinary)
    patients = db.relationship('Patient', back_populates='department', lazy='select')
    events = db.relationship('Event', back_populates='department', lazy='select')
    user_times = db.relationship('UserTime', back_populates='user', lazy='select')

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
    department_id = db.Column(db.Integer, db.ForeignKey('Users.id', ondelete='CASCADE', onupdate='CASCADE'), index=True)
    max_calls = db.Column(db.Integer)
    contacts = db.relationship('Contact', back_populates='patient', lazy='select')
    events = db.relationship('Event', back_populates='patient', lazy='select')
    department = db.relationship('Users', back_populates='patients', lazy='select')

    # def __init__(self, patient_id, f_name, l_name, bed, department, max_calls):
    #     self.patient_id = patient_id
    #     self.f_name = f_name
    #     self.l_name = l_name
    #     self.bed = bed
    #     self.department = department
    #     self.max_calls = max_calls


    @classmethod
    def to_dict(cls, with_relationships=True):
        d = {}
        for column in cls.__table__.columns:
            if with_relationships and len(column.foreign_keys) > 0:
                # Skip foreign keys
                continue
            d[column.name] = getattr(cls, column.name)

        if with_relationships:
            for relationship in inspect(cls).relationships:
                val = getattr(cls, relationship.key)
                d[relationship.key] = cls.to_dict(val) if val else None
        return d

    def get_patient_contacts(self):
        for contact in self.contacts:
            print(contact.id, contact.f_name)

    def __repr__(self):
        return "Patient(patient_id='%s', l_name='%s', f_name='%s', bed='%s', department='%s', max_calls='%s')" % (
            self.patient_id, self.l_name, self.f_name, self.bed, self.department, self.max_calls)

        # return cols,pk
        # tuplefield_list = [(getattr(item, col) for col in cols) for item in db.query(cls).all()]
        # df = pd.DataFrame.from_records(tuplefield_list, index=pk, columns=cols)
        # return df


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
    patient = db.relationship('Patient', back_populates='contacts')
    events = db.relationship('Event', back_populates='contact', lazy='select')
    contact_time = db.relationship('ContactTime', back_populates='contact', lazy='select')

    def __init__(self, patient_id, f_name, l_name, phone, mail, priority):
        self.patient_id = patient_id
        self.f_name = f_name
        self.l_name = l_name
        self.phone = phone
        self.mail = mail
        self.priority = priority

    def __repr__(self):
        return '<Contact: %s, %s, %s, %s, %s>' % (self.f_name, self.l_name, self.phone, self.mail, self.priority)


class ContactTime(db.Model):
    __tablename__ = 'contacts_times'

    id = db.Column(db.Integer, primary_key=True)
    day = db.Column(db.Integer)
    contact_id = db.Column(db.Integer, db.ForeignKey('contacts.contact_id', ondelete='CASCADE', onupdate='CASCADE'),
                           index=True)
    from_hour = db.Column(db.Time)
    to_hour = db.Column(db.Time)

    contact = db.relationship('Contact', back_populates='contact_time', lazy='select')
    def __init__(self, contact_id, day, from_hour, to_hour):
        self.contact_id = contact_id
        self.day = day
        self.from_hour = from_hour
        self.to_hour = to_hour

    def __repr__(self):
        return '<Time: %s, %s, %s, %s, %s>' % (self.day, self.from_hour, self.to_hour, self.id, self.contact_id)


class UserTime(db.Model):
    __tablename__ = 'users_times'

    id = db.Column(db.Integer, primary_key=True)
    day = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('Users.id', ondelete='CASCADE', onupdate='CASCADE'),
                        index=True)
    from_hour = db.Column(db.Time)
    to_hour = db.Column(db.Time)
    user = db.relationship('Users', back_populates='user_times', lazy='select')

    def __init__(self, user_id, day, from_hour, to_hour):
        self.user_id = user_id
        self.day = day
        self.from_hour = from_hour
        self.to_hour = to_hour

    def __repr__(self):
        return '<Time: %s, %s, %s, %s, %s>' % (self.day, self.from_hour, self.to_hour, self.id, self.user_id)


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
    department_id = db.Column(db.Integer, db.ForeignKey('Users.id'))
    start_time = db.Column(db.TIMESTAMP)
    status = db.Column(db.Integer)
    row_created_time = db.Column(db.TIMESTAMP, default=datetime.now())

    # Relationships
    contact = db.relationship('Contact', back_populates='events', lazy='select')
    patient = db.relationship('Patient', back_populates='events', lazy='select')
    department = db.relationship('Users', back_populates='events', lazy='select')

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
