# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from flask import render_template, redirect, request, url_for, session, flash
from flask_login import (
    current_user,
    login_user,
    logout_user, login_required
)

from apps.patients import blueprint
from apps.patients.forms import PatientForm
from apps.authentication.models import Users, Patient
from apps import db
from apps.authentication.util import verify_pass

@blueprint.route('/tables', methods=['GET', 'POST'])
@login_required
def tables():
    flash('You have subscribed to the newsletter!', 'success')
    patients = Patient.query.all()
    return render_template('patients/tables.html', patients=patients)

@blueprint.route("/<int:patient_id>/patient_info", methods=['GET', 'POST'])
@login_required
def update(patient_id):
    form = PatientForm()
    # Get all attributes of the patient
    p = Patient.query.filter_by(patient_id=patient_id).first_or_404()

    # If request.method == 'POST' update patient information
    if form.validate_on_submit():
        p.patient_id = form.patient_id.data
        p.f_name = form.f_name.data
        p.l_name = form.l_name.data
        p.bed = form.bed.data
        p.department = form.department.data
        p.max_calls = form.max_calls.data
        db.session.commit()
        # flash("מטופל {} עודכן בהצלחה".format(p.f_name))
        return redirect(url_for('patients.list',patient_id=p.patient_id))
    # If request.method == 'GET' get patient information
    elif request.method == 'GET':
        form.patient_id.data = p.patient_id
        form.f_name.data = p.f_name
        form.l_name.data = p.l_name
        form.bed.data = p.bed
        form.department.data = p.department
        form.max_calls.data = p.max_calls

    return render_template('patients/patient_info.html',form=form, patient_id=patient_id)


@blueprint.route("/add", methods=['GET', 'POST'])
@login_required
def add():
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
            department=form.department.data,
            max_calls=form.max_calls.data
        )
        db.session.add(p)
        db.session.commit()
        return redirect(url_for('patients_blueprint.tables'))
        # return redirect(url_for('patients_blueprint.patient_info', patient_id=p.patient_id))
        # flash("מטופל {} עודכן בהצלחה".format(p.f_name))
    return render_template('patients/add_patient.html',form=form)


    # return render_template('patients/patient_info.html',form=form, patient_id=patient_id)

@blueprint.route("/<int:patient_id>/patient_info", methods=['GET', 'POST'])
@login_required
def patient_info(patient_id):
    form = PatientForm()
    # Get all attributes of the patient
    p = Patient.query.filter_by(patient_id=patient_id).first_or_404()
    if request.method == 'GET':
        form.patient_id.data = p.patient_id
        form.f_name.data = p.f_name
        form.l_name.data = p.l_name
        form.bed.data = p.bed
        form.department.data = p.department
        form.max_calls.data = p.max_calls
        contacts = p.contacts
    return render_template('patients/patient_info.html',form=form, patient_id=patient_id,contacts=contacts)

@blueprint.route("/<int:patient_id>/delete", methods=['GET', 'POST'])
@login_required
def delete(patient_id):
    try:
        patient_id = Patient.query.get(patient_id)
        db.session.delete(patient_id)
        db.session.commit()
    except:
        print("Error")
        # flash("מטופל לא קיים")
    return redirect(url_for('patients_blueprint.tables'))

