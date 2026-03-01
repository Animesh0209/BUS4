from werkzeug.security import generate_password_hash, check_password_hash
from flask import render_template, redirect, url_for, flash, request, session
from app import app
from app import db
from app.forms import RegisterForm, LoginForm, FirstHealthForm, RecurrentHealthForm, CheckupForm
from app.models import User, HealthRecord, Checkup

@app.route('/', methods=['GET', 'POST'])
def index():
    if 'user_id' not in session:
        return redirect(url_for('authenticate_user'))
    return render_template('index.html', session=session)

@app.route('/register', methods=['GET', 'POST'])
def register_user():
    form = RegisterForm()
    if form.validate_on_submit():
        existing_user = User.query.filter_by(email=form.email.data.lower()).first()
        if existing_user:
            flash("Email already registered!")
            return render_template('register.html', form=form)
        hashed_password = generate_password_hash(form.password.data)
        user = User(
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            email=form.email.data,
            password=hashed_password,
            role=form.role.data,
        )
        db.session.add(user)
        db.session.commit()
        flash("Registration successful! Please log in.")
        return redirect(url_for("authenticate_user"))
    return render_template("register.html", form=form)

@app.route('/login', methods=['GET', 'POST'])
def authenticate_user():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password, form.password.data):
            session.permanent = True
            session["user_id"] = user.user_id
            session["user_name"] = f"{user.first_name} {user.last_name}"
            session["user_role"] = user.role
            flash(f"Welcome back, {user.first_name}!")
            return redirect(url_for("index"))
        else:
            flash("Invalid email and/or password - please try again!")
            return render_template('login.html', form=form)
    return render_template('login.html', form=form)

@app.route('/logout')
def logout_user():
    session.clear()
    flash("You have been logged out!")
    return redirect(url_for('authenticate_user'))

# to complete

def get_health_data(user_id=None):
    pass

def update_health_data():
    pass

def generate_auth_code():
    pass

def verify_auth_code():
    pass

@app.route('/check_up', methods=['GET', 'POST'])
def checkup():
    form = CheckupForm()
    if form.validate_on_submit():
        checkup_log = Checkup(
            patient_last_name=form.patient_last_name.data,
            patient_first_name=form.patient_first_name.data,
            checkup_date=form.checkup_date.data,
            medication=form.medication.data,
            dosage=form.dosage.data,
            notes=form.notes.data
        )
        db.session.add(checkup_log)
        db.session.commit()
        flash(f"Check-up details have been successfully logged!")
        return redirect(url_for('checkup'))
    checkups = Checkup.query.all()
    return render_template("checkups.html", form=form, checkups=checkups)

@app.route('/update_check_up/<int:checkup_id>', methods=['GET', 'POST'])
def update_checkup(checkup_id):
    checkup_log = Checkup.query.get_or_404(checkup_id)
    form = CheckupForm(obj=checkup_log)

    if form.validate_on_submit():
        checkup_log.patient_last_name = form.patient_last_name.data
        checkup_log.patient_first_name = form.patient_first_name.data
        checkup_log.checkup_date = form.checkup_date.data
        checkup_log.medication = form.medication.data
        checkup_log.dosage = form.dosage.data
        checkup_log.notes = form.notes.data
        db.session.commit()
        flash(f'Check-up details have been updated successfully!')
        return redirect(url_for('checkup'))
    return render_template('checkups_updating.html', form=form)

@app.route('/delete_check_up/<int:checkup_id>', methods=['GET', 'POST'])
def delete_checkup(checkup_id):
    checkup_log = Checkup.query.get_or_404(checkup_id)
    db.session.delete(checkup_log)
    db.session.commit()
    flash(f'Check-up details have been deleted successfully.')
    return redirect(url_for('checkup'))