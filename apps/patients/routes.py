# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from flask import render_template, redirect, request, url_for, session, flash, jsonify
from flask_login import (
    current_user,
    login_user,
    logout_user, login_required
)
from apps.patients import blueprint
from apps.patients.forms import PatientForm, ContactForm, ContactTimeForm
from apps.authentication.models import Users, Patient, Contact, ContactTime
from apps import db
from apps.authentication.util import verify_pass


# Patients functions
@blueprint.route('/patients_list', methods=['GET', 'POST'])
@login_required
def patients_list():
    # flash('You have subscribed to the newsletter!', 'success')
    form = PatientForm()
    patients = Patient.query.all()
    return render_template('patients/patients_list.html', patients=patients, patient_form=form)


@blueprint.route("/update_patient/<int:patient_id>", methods=['GET', 'POST'])
@login_required
def update_patient(patient_id):
    form = PatientForm()
    # Get all attributes of the patient
    p = Patient.query.filter_by(patient_id=patient_id).first_or_404()

    if request.method == 'POST':
        p.f_name = form.f_name.data
        p.l_name = form.l_name.data
        p.bed = form.bed.data
        p.department = current_user.id
        p.department = current_user.id
        p.max_calls = form.max_calls.data
        db.session.commit()
        flash("מטופל {} עודכן בהצלחה".format(p.f_name))
        if 'patients_list' in request.form:
            return redirect(url_for('patients_blueprint.patients_list'))
    # If request.method == 'GET' get patient information
    elif request.method == 'GET':
        form.patient_id.data = p.patient_id
        form.f_name.data = p.f_name
        form.l_name.data = p.l_name
        form.bed.data = p.bed
        form.department.data = p.department
        form.max_calls.data = p.max_calls
        # contacts = Patient.query.get(patient_id).contacts
        # session.query(ContactsTime).filter_by(patient_id=4).all()
    return redirect(url_for('patients_blueprint.patient_info', patient_id=patient_id, form=form))


@blueprint.route("/add_patient", methods=['GET', 'POST'])
@login_required
def add_patient():
    form = PatientForm()
    # # Get all attributes of the patient
    # p = Patient.query.filter_by(patient_id=patient_id).first_or_404()

    # If request.method == 'POST' update patient information
    if request.method == 'POST':
        p = Patient(
            patient_id=form.patient_id.data,
            f_name=form.f_name.data,
            l_name=form.l_name.data,
            bed=form.bed.data,
            department_id=int(current_user.username),
            max_calls=form.max_calls.data
        )
        db.session.add(p)
        db.session.commit()
        return redirect(url_for('patients_blueprint.patient_info', patient_id=form.patient_id.data))
        # return redirect(url_for('patients_blueprint.patient_info', patient_id=p.patient_id))
        # flash("מטופל {} עודכן בהצלחה".format(p.f_name))
    return render_template('patients/add_patient.html', form=form)

    # return render_template('patients/patient_info.html',form=form, patient_id=patient_id)


@blueprint.route("/<int:patient_id>/delete_patient", methods=['GET', 'POST'])
@login_required
def delete_patient(patient_id):
    try:
        patient_id = Patient.query.get(patient_id)
        db.session.delete(patient_id)
        db.session.commit()
    except:
        print("Error")
        # flash("מטופל לא קיים")
    return redirect(url_for('patients_blueprint.patients_list'))


@blueprint.route("/<int:patient_id>/patient_info", methods=['GET', 'POST'])
@login_required
def patient_info(patient_id):
    patient_form = PatientForm()
    contact_form = ContactForm()
    contact_time_form = ContactTimeForm()
    contact_time_form.day.default = "3"
    # Get all attributes of the patient
    patient = Patient.query.filter_by(patient_id=patient_id).first_or_404()
    # contacts = p.contacts
    if request.method == 'GET':
        patient_form.patient_id.data = patient.patient_id
        patient_form.f_name.data = patient.f_name
        patient_form.l_name.data = patient.l_name
        patient_form.bed.data = patient.bed
        patient_form.department.data = patient.department
        patient_form.max_calls.data = patient.max_calls
        # contacts = p.contacts
    return render_template('patients/patient_info.html', patient_form=patient_form,
                           patient=patient, contact_form=contact_form, contact_time_form=contact_time_form)


# Contacts functions

@blueprint.route('/<int:patient_id>/add_contact', methods=['GET', 'POST'])
@login_required
def add_contact(patient_id):
    form = ContactForm()
    print(patient_id)
    if request.method == 'POST':
        contact = Contact(patient_id=patient_id, f_name=form.f_name.data, l_name=form.l_name.data,
                          mail=form.mail.data, phone=form.phone.data,
                          priority=form.priority.data)
        # patient_id = contact.patient_id
        db.session.add(contact)
        db.session.commit()
        flash("איש הקשר נוסף בהצלחה")
    return redirect(url_for('patients_blueprint.patient_info', patient_id=patient_id))


@blueprint.route('/delete_contact/<int:contact_id>', methods=['GET', 'POST'])
@login_required
def delete_contact(contact_id):
    contact = Contact.query.get(contact_id)
    patient_id = contact.patient_id
    print(f"contact is is:{contact_id} and patient_id is:{patient_id}")
    db.session.delete(contact)
    db.session.commit()
    flash("contact Deleted Successfully")

    return redirect(url_for('patients_blueprint.patient_info', patient_id=patient_id))


@blueprint.route('/update_contact/<int:contact_id>', methods=['GET', 'POST'])
def update_contact(contact_id):
    contact_form = ContactForm()
    contact = Contact.query.get(contact_id)
    patient_id = contact.patient_id
    if request.method == 'POST':
        contact.f_name = contact_form.f_name.data
        contact.l_name = contact_form.l_name.data
        contact.mail = contact_form.mail.data
        contact.phone = contact_form.phone.data
        contact.priority = contact_form.priority.data

        db.session.commit()
        flash("איש הקשר עודכן בהצלחה")

    return redirect(url_for('patients_blueprint.patient_info', patient_id=patient_id))


# Contactime functions
@blueprint.route("/<int:contact_id>/add_contact_time", methods=['GET', 'POST'])
@login_required
def add_contact_time(contact_id):
    contact_time_form = ContactTimeForm()
    contact = contact = Contact.query.get(contact_id)
    if request.method == 'POST':
        time = ContactTime(contact_id=contact.contact_id,
                           day=contact_time_form.day.data,
                           from_hour=dict(contact_time_form.from_hour.choices).get(contact_time_form.from_hour.data),
                           to_hour=dict(contact_time_form.to_hour.choices).get(contact_time_form.to_hour.data))
        db.session.add(time)
        db.session.commit()
        flash("זמן איש הקשר הוסף בהצלחה")
    return redirect(url_for('patients_blueprint.patient_info', patient_id=contact.patient.patient_id))


@blueprint.route('/<int:time_id>/update_contact_time', methods=['GET', 'POST'])
@login_required
def update_contact_time(time_id):
    contact_time_form = ContactTimeForm()
    time = ContactTime.query.filter_by(id=time_id).first_or_404()
    patient_id = Contact.query.filter_by(contact_id=time.contact_id).first_or_404().patient_id
    if request.method == 'POST':
        time.day = contact_time_form.day.data
        time.from_hour = dict(contact_time_form.from_hour.choices).get(contact_time_form.from_hour.data)
        time.to_hour = dict(contact_time_form.to_hour.choices).get(contact_time_form.to_hour.data)
        time.contact_id = time.contact_id
        db.session.commit()
        flash("איש הקשר עודכן בהצלחה")
        return redirect(url_for('patients_blueprint.patient_info', patient_id=patient_id))

    if request.method == "GET":
        # contact_time_form.day.data.selected = time.day
        # contact_time_form.from_hour.data.selected = time.from_hour
        # contact_time_form.to_hour.data.selected = time.to_hour
        return jsonify(data={"day": "17", "from_hour": "10:00:00", "to_hour": "12:00:00"})

    return redirect(url_for('patients_blueprint.patient_info', patient_id=patient_id))


@blueprint.route('/<int:time_id>/delete_contact_time', methods=['GET', 'POST'])
@login_required
def delete_contact_time(time_id):
    contact_time = ContactTime.query.get(time_id)
    patient_id = contact_time.contact.patient.patient_id
    print(f"contact_time is:{contact_time} and patient_id is:{patient_id} and contact is {contact_time.contact}")
    db.session.delete(contact_time)
    db.session.commit()
    flash("contact time deleted Successfully")

    return redirect(url_for('patients_blueprint.patient_info', patient_id=patient_id))
