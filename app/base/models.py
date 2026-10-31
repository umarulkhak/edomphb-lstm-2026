# -*- encoding: utf-8 -*-
"""
License: MIT
Copyright (c) 2019 - present AppSeed.us
"""

from flask_login import UserMixin
from sqlalchemy import LargeBinary, Column, Integer, String

from app.extensions import db, login_manager

from app.base.util import hash_pass


class User(db.Model, UserMixin):

    __tablename__ = 'User'

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    nama = Column(String)
    email = Column(String, unique=True)
    semester = Column(String)
    kelas = Column(String)
    password = Column(LargeBinary)

    def __init__(
        self,
        username: str,
        nama: str,
        email: str,
        semester: str,
        kelas: str,
        password: str,
    ) -> None:
        self.username = username
        self.nama = nama
        self.email = email
        self.semester = semester
        self.kelas = kelas
        self.password = hash_pass(password)

    def __repr__(self):
        return str(self.username)

    @property
    def is_admin(self):
        return self.nama == 'Administrator'


@login_manager.user_loader
def user_loader(id):
    return User.query.filter_by(id=id).first()

# Mata Kuliah Table


class MataKuliah(db.Model):

    __tablename__ = 'MataKuliah'

    id = Column(Integer, primary_key=True)
    matakuliah = Column(String, unique=True)
    namadosen = Column(String, unique=True)
    semester = Column(String, unique=True)


class EdomModel(db.Model):
    __tablename__ = "edom"

    id = db.Column(db.Integer, primary_key=True)
    nim = db.Column(db.String())
    nama = db.Column(db.String())
    semester = db.Column(db.String())
    review = db.Column(db.String())
    sentiment = db.Column(db.String())
    probability = db.Column(db.String())
    amount = db.Column(db.Integer, nullable=False)
    slug = db.Column(db.String())

    def __init__(self, nim, nama, semester, review, sentiment, probability, amount, slug):
        self.nim = nim
        self.nama = nama
        self.semester = semester
        self.review = review
        self.sentiment = sentiment
        self.probability = probability
        self.amount = amount
        self.slug = slug

    def __repr__(self):
        return f"{self.nama}:{self.sentiment}"
