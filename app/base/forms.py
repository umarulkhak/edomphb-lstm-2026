# -*- encoding: utf-8 -*-


from flask_wtf import FlaskForm
from wtforms import PasswordField, SelectField, StringField, TextAreaField
from wtforms.validators import DataRequired, Email, Length

## login and registration


class LoginForm(FlaskForm):
    username = StringField('Username', id='username_login', validators=[DataRequired()])
    password = PasswordField('Password', id='pwd_login', validators=[DataRequired()])


class CreateAccountForm(FlaskForm):
    username = StringField('Username', id='username_create', validators=[DataRequired(), Length(max=32)])
    nama = StringField('Nama', id='nama_create', validators=[DataRequired(), Length(max=120)])
    email = StringField('Email', id='email_create', validators=[DataRequired(), Email(), Length(max=120)])
    semester = SelectField(
        'Semester',
        id='semester_create',
        choices=[(str(value), str(value)) for value in (2, 4, 6, 8)],
        validators=[DataRequired()],
    )
    kelas = SelectField(
        'Kelas',
        id='kelas_create',
        choices=[(value, value) for value in 'ABCD'],
        validators=[DataRequired()],
    )
    password = PasswordField(
        'Password',
        id='pwd_create',
        validators=[DataRequired(), Length(min=8, max=128)],
    )


class CreateMataKuliahForm(FlaskForm):
    matakuliah = StringField('MataKuliah', id='matakuliah_create', validators=[DataRequired()])
    namadosen = StringField('NamaDosen', id='namadosen_create', validators=[DataRequired()])
    semester = StringField('Semester', id='semester_create', validators=[DataRequired()])


class ReviewForm(FlaskForm):
    nama = SelectField('Dosen', validators=[DataRequired()])
    review = TextAreaField('Komentar', validators=[DataRequired(), Length(max=2000)])


class AdminReviewForm(ReviewForm):
    nim = StringField('NIM', validators=[DataRequired(), Length(max=32)])
    semester = SelectField(
        'Semester',
        choices=[(str(value), str(value)) for value in range(1, 9)],
        validators=[DataRequired()],
    )
