import smtplib
from email.mime.text import MIMEText
from functools import wraps
from flask import Blueprint, render_template, url_for, request,redirect, flash, current_app
from flask_login import current_user, login_required
from flask_admin import BaseView, AdminIndexView, expose, Admin
from blog import db
import os
from blog.models import Post2, Incident
from werkzeug.utils import secure_filename
main = Blueprint('main', __name__)





main = Blueprint('main', __name__)

@main.route('/post/new', methods=['POST'])
def form():
    location = request.form['incident-location']
    description = request.form['incident-description']
    phone_number = request.form['phone-number']
    full_name = request.form['full-name']
    email = request.form['email']
    is_foundation_employee = request.form['is_foundation_employee']
    dep = request.form['department']
    status=request.form['status']
    photo = None
    if 'photo' in request.files:
        file = request.files['photo']
        if file.filename != '':
            filename = secure_filename(file.filename)
            file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
            photo = filename

    form_data = Incident(location=location, description=description, phone_number=phone_number, full_name=full_name, email=email, is_foundation_employee=is_foundation_employee, dep=dep, status=status, photo=photo)

    db.session.add(form_data)
    db.session.commit()

    return redirect(url_for('admin.index'))


@main.route('/')
def home():
   return render_template('index.html', title = 'UMC')

@main.route('/incidents')
@login_required
def incidents():
    incidents = Incident.query.all()
    return render_template('incidents.html', incidents=incidents)

@main.route('/incidents_hoz')
@login_required
def incidents_hoz():
    incidents = Incident.query.all()
    return render_template('incidents_hoz.html', incidents=incidents)

@main.route('/incidents_med')
@login_required
def incidents_med():
    incidents = Incident.query.all()
    return render_template('incidents_med.html', incidents=incidents)

@main.route("/forward/<string:user>/<string:phone>/<string:email>", methods=['GET', 'POST'])
def smail(user, phone, email):
    sender = "salomat423@gmail.com"
    password = "221502Ernur@"
    server = smtplib.SMTP("smtp.office365.com", 587)

    server.starttls()

    message = request.form['message']

    try:
        server.login(sender, password)
        msg = MIMEText(message, _charset='utf-16')
        msg["Subject"] = "University Medical Center"
        server.sendmail(sender, email, msg.as_string())

        return redirect("/")
    except Exception as _ex:
        return f"{_ex}\nCheck your login or password please!"

        # обновление статуса заявки на "Закрыта"
    incident_id = request.form.get('incident_id')
    incident = Incident.query.get(incident_id)
    incident.status = 'Закрыта'
    db.session.commit()

    return redirect(url_for('main.gla'))




@main.route('/update_status/<int:incident_id>', methods=['POST'])
@login_required
def update_status(incident_id):
    incident = Incident.query.get_or_404(incident_id)
    incident.status = request.form['status']
    print(db.session.query(Incident).filter_by(id=incident_id).update({'status': request.form['status']}))
    db.session.commit()
    flash('Статус заявки изменен успешно', 'success')
    return redirect(url_for('main.incidents'))






