from flask import flash, redirect, render_template, url_for
from flask_login import current_user, login_user, logout_user

from app.extensions import db
from app.base import blueprint
from app.base.forms import CreateAccountForm, LoginForm
from app.base.models import User
from app.base.util import verify_pass


@blueprint.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data.strip()).first()
        if user and verify_pass(form.password.data, user.password):
            login_user(user)
            return redirect(url_for('home_blueprint.index'))
        flash('Username atau kata sandi tidak sesuai.', 'error')
    if current_user.is_authenticated:
        return redirect(url_for('home_blueprint.index'))
    return render_template('login/login.html', form=form)


@blueprint.route('/create_user', methods=['GET', 'POST'])
def create_user():
    if current_user.is_authenticated:
        return redirect(url_for('home_blueprint.index'))

    form = CreateAccountForm()
    if form.validate_on_submit():
        username = form.username.data.strip()
        email = form.email.data.strip().lower()
        name = form.nama.data.strip()
        if name.casefold() == 'administrator':
            flash('Nama tersebut tidak dapat digunakan untuk pendaftaran mahasiswa.', 'error')
        elif User.query.filter_by(username=username).first():
            flash('NIM tersebut sudah terdaftar.', 'error')
        elif User.query.filter_by(email=email).first():
            flash('Email tersebut sudah terdaftar.', 'error')
        else:
            user = User(
                username=username,
                nama=name,
                email=email,
                semester=form.semester.data,
                kelas=form.kelas.data,
                password=form.password.data,
            )
            db.session.add(user)
            db.session.commit()
            flash('Akun berhasil dibuat. Silakan masuk.', 'success')
            return redirect(url_for('base_blueprint.login'))
    return render_template('login/register.html', form=form)


@blueprint.route('/logout', methods=['POST'])
def logout():
    logout_user()
    flash('Anda telah keluar dari akun.', 'info')
    return redirect(url_for('base_blueprint.login'))
