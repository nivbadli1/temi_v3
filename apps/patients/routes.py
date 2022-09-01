# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from flask import render_template, redirect, request, url_for
from flask_login import (
    current_user,
    login_user,
    logout_user, login_required
)

from apps import db, login_manager
from apps.patients import blueprint
from apps.patients.forms import PatientForm
from apps.authentication.models import Users,Patient

from apps.authentication.util import verify_pass


@blueprint.route("/tables", methods=["GET", "POST"])
@login_required
def list():
    if request.method == "GET":
        patients = Patient.query.all()
        return render_template("tables.html",patients=patients)

# @blueprint.route('/<template>',methods=['GET', 'POST'])
# @login_required
# def route_template(template):
#
#     try:
#         if not template.endswith('.html'):
#             template += '.html'
#
#         # Detect the current page
#         segment = get_segment(request)
#
#         if 'tables' in template:
#             patients = patients = Patient.query.all()
#             return render_template('tables.html', patients=patients)
#
#
#     if 'login' in request.form:
#
#         # Serve the file (if exists) from app/templates/home/FILE.html
#         return render_template("home/" + template, segment=segment)
#
#     except TemplateNotFound:
#         return render_template('home/page-404.html'), 404
#     except:
#         return render_template('home/page-500.html'), 500
#


def get_segment(request):

    try:

        segment = request.path.split('/')[-1]

        if segment == '':
            segment = 'index'

        return segment

    except:
        return None


@blueprint.errorhandler(403)
def access_forbidden(error):
    return render_template('home/page-403.html'), 403


@blueprint.errorhandler(404)
def not_found_error(error):
    return render_template('home/page-404.html'), 404


@blueprint.errorhandler(500)
def internal_error(error):
    return render_template('home/page-500.html'), 500
