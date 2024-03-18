import pytz
from datetime import datetime
import sqlite3
import pandas as pd
from datetime import timedelta
from flask import render_template, request, flash, redirect, url_for, send_file, Response
from __init__ import create_app, db
from forms import QRCodeData, Mine, User, Note, Reg, Filters, Tasks, Orgdata, Production, Exhibition, Seat
import secrets
import qrcode
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user
from flask_socketio import SocketIO, emit
import pandas as pd
import os
import io
import requests
from bs4 import BeautifulSoup
# from pywinauto.application import Application
app = create_app()
# notification section
socketio = SocketIO(app)


@socketio.on('assign user')
def assign_user(message):
    emit('notification', {
         'data': 'User ' + message['user'] + ' has been assigned a new post'}, broadcast=True)


# end of notification section
# Time section
now_utc = datetime.now(pytz.utc)
tz = pytz.timezone('Asia/Tashkent')
now_uz = now_utc.astimezone(tz).strftime('%Y-%m-%d %H:%M:%S')
#


@app.route("/", methods=["GET", "POST"])
@app.route("/index", methods=["GET", "POST"])
def index():
    return render_template("index.html", user=current_user)


@app.route('/view_report', methods=['GET', 'POST'])
@login_required
def view_report():
    if request.method == 'POST':
        start_date = datetime.strptime(request.form.get(
            'start_date'), '%d/%m/%Y').strftime('%Y-%m-%d')
        end_date = datetime.strptime(request.form.get(
            'end_date'), '%d/%m/%Y').strftime('%Y-%m-%d')
        person_name = request.form.get('person_name')
        person_id = request.form.get('person_id')
        conn = sqlite3.connect(
            'C:/Users/Public/SmartPSSLite/Data/User/ExternalDatabase/ExternalDataManager.db')
        query = f"SELECT * FROM AttendanceRecordInfo WHERE DATE(AttendanceDateTime/1000, 'unixepoch') BETWEEN '{start_date}' AND '{end_date}' AND PersonName LIKE '%{person_name}%' AND PersonID LIKE '%{person_id}%'"

        df = pd.read_sql_query(query, conn)
        df['AttendanceDateTime'] = pd.to_datetime(
            df['AttendanceDateTime'], unit='ms')
        df['AttendanceDateTime'] = df['AttendanceDateTime'] + \
            timedelta(hours=5)
        df['AttendanceDateTime'] = df['AttendanceDateTime'].dt.strftime(
            '%d/%m/%Y %H:%M:%S')
        df['Handler'] = df['DeviceIPAddress'].apply(lambda x: 'Вход' if x in [
                                                    '10.210.122.4', '10.210.122.5'] else ('Уход' if x in ['10.210.122.2', '10.210.122.3'] else ''))
        df['AttendanceMethod'] = df['AttendanceMethod'].apply(
            lambda x: 'Лицо' if x in [15] else ('Отпечатка' if x in [4] else ''))
        df['AttendanceDateTime'] = pd.to_datetime(
            df['AttendanceDateTime'], format='%d/%m/%Y %H:%M:%S')
        df = df.sort_values('AttendanceDateTime')
        df = df.drop(
            columns=['PerSonCardNo', 'AttendanceState', 'DeviceIPAddress', 'DeviceName', 'SnapshotsPath', 'AttendanceUtcTime', 'Remarks'])
        html_table = df.to_html(index=False)
        conn.close()
        return html_table
    return render_template('view_report.html', user=current_user)


@app.route('/download_report', methods=['GET', 'POST'])
@login_required
def download_report():
    if request.method == 'POST':
        start_date = datetime.strptime(request.form.get(
            'start_date'), '%d/%m/%Y').strftime('%Y-%m-%d')
        end_date = datetime.strptime(request.form.get(
            'end_date'), '%d/%m/%Y').strftime('%Y-%m-%d')
        person_name = request.form.get('person_name')
        person_id = request.form.get('person_id')
        conn = sqlite3.connect(
            'C:/Users/Public/SmartPSSLite/Data/User/ExternalDatabase/ExternalDataManager.db')
        query = f"SELECT * FROM AttendanceRecordInfo WHERE DATE(AttendanceDateTime/1000, 'unixepoch') BETWEEN '{start_date}' AND '{end_date}' AND PersonName LIKE '%{person_name}%' AND PersonID LIKE '%{person_id}%'"

        df = pd.read_sql_query(query, conn)
        df['AttendanceDateTime'] = pd.to_datetime(
            df['AttendanceDateTime'], unit='ms')
        df['AttendanceDateTime'] = df['AttendanceDateTime'] + \
            timedelta(hours=5)
        df['AttendanceDateTime'] = df['AttendanceDateTime'].dt.strftime(
            '%d/%m/%Y %H:%M:%S')
        df['Handler'] = df['DeviceIPAddress'].apply(lambda x: 'Вход' if x in [
                                                    '10.210.122.5', '10.210.122.6'] else ('Уход' if x in ['10.210.122.2', '10.210.122.3'] else ''))
        df['AttendanceMethod'] = df['AttendanceMethod'].apply(
            lambda x: 'Лицо' if x in [15] else ('Отпечатка' if x in [4] else ''))

        df['AttendanceDateTime'] = pd.to_datetime(
            df['AttendanceDateTime'], format='%d/%m/%Y %H:%M:%S')
        df = df.sort_values('AttendanceDateTime')
        df = df.drop(
            columns=['PerSonCardNo', 'AttendanceState', 'DeviceIPAddress', 'DeviceName', 'SnapshotsPath', 'AttendanceUtcTime', 'Remarks'])
        output = io.BytesIO()
        # Write the DataFrame to the output stream & Save DataFrame to an Excel file
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df.to_excel(writer, index=False)
        output.seek(0)
        conn.close()
        # Create a response with the output stream & Send the Excel file to the client
        response = send_file(
            output, mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', as_attachment=True, download_name='report.xlsx')
        # Set the filename for the download
        response.headers["Content-Disposition"] = "attachment; filename=report.xlsx"
        return response
    return render_template('view_report.html', user=current_user)


@app.route("/sign_up/", methods=["GET", "POST"])
@app.route("/sign_up", methods=["GET", "POST"])
def sign_up():
    if request.method == "POST":
        email = request.form.get("email")
        fullname = request.form.get("fullname")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")
        comment = str(password1)
        role = request.form.get("role")
        user = User.query.filter_by(email=email).first()
        if user:
            flash("This email is already taken. Use another!", category="error")
        elif len(email) < 5:
            flash("At least 6 characters for email, please!", category="error")
        elif password1 != password2:
            flash("Passwords don't match", category="error")
        elif len(password1) < 5:
            flash("At least 6 characters for password, please", category="error")
        else:
            new_user = User(email=email, fullname=fullname, comment=comment, role=role,
                            password=generate_password_hash(password1, method="scrypt"))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash("Account created successfully!", category="success")
            return redirect(url_for("login"))
    return render_template("sign_up.html", user=current_user)


@app.route("/login/", methods=["GET", "POST"])
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash("Logged in successfully", category="success")
                login_user(user, remember=True)
                return redirect(url_for("index"))
            else:
                flash("Incorrect password", category="error")
        else:
            flash("This user doesn't exist", category="error")
    return render_template("login.html", user=current_user)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))


@app.route('/logout_all')
def logout_all():
    app.config['SECRET_KEY'] = os.urandom(24)
    return redirect(url_for('login'))


@app.route("/users/")
@app.route("/users")
def users():
    users = User.query.filter_by(email=User.email).all()
    return render_template("users.html", user=current_user, users=users)


@app.route("/create_all")
def create_all():
    db.create_all()
    return "All tables are created!!!"
