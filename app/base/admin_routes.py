from flask import abort, flash, redirect, render_template, request, url_for
from flask_login import current_user

from app.extensions import db
from app.base import blueprint
from app.base.forms import CreateMataKuliahForm
from app.base.models import EdomModel, MataKuliah, User
from app.base.permissions import admin_required
from app.base.services.edom import INSTRUCTOR_CHOICES

SENTIMENT_LABELS = ('Baik', 'Cukup', 'Kurang', 'Sangat Baik')


def _render_report(teacher=None):
    query = EdomModel.query
    if teacher:
        query = query.filter_by(nama=teacher)
    entries = query.order_by(EdomModel.id.desc()).all()
    totals = {label: 0 for label in SENTIMENT_LABELS}
    totals_query = db.session.query(
        EdomModel.sentiment, db.func.sum(EdomModel.amount)
    ).group_by(EdomModel.sentiment)
    if teacher:
        totals_query = totals_query.filter(EdomModel.nama == teacher)
    for sentiment, count in totals_query.all():
        if sentiment in totals:
            totals[sentiment] = int(count or 0)
    return render_template(
        'Rekap.html',
        edom=entries,
        chart_labels=list(SENTIMENT_LABELS),
        chart_values=[totals[label] for label in SENTIMENT_LABELS],
        instructors=INSTRUCTOR_CHOICES,
        selected_teacher=teacher,
    )


@blueprint.route('/DataUser')
@admin_required
def datauser():
    users = User.query.order_by(User.nama.asc()).all()
    return render_template('DataUser.html', user=users)


@blueprint.route('/<int:id>/delete', methods=['GET', 'POST'])
@admin_required
def deleteuser(id):
    user = User.query.get_or_404(id)
    if request.method == 'POST':
        if user.id == current_user.id:
            flash('Akun yang sedang digunakan tidak dapat dihapus.', 'error')
            return redirect(url_for('base_blueprint.datauser'))
        db.session.delete(user)
        db.session.commit()
        flash('Akun pengguna berhasil dihapus.', 'success')
        return redirect(url_for('base_blueprint.datauser'))
    return render_template('delete.html', user=user)


@blueprint.route('/DataEdom')
@admin_required
def dataedom():
    edom = EdomModel.query.order_by(EdomModel.id.desc()).all()
    return render_template('DataEdom.html', edom=edom)


@blueprint.route('/Rekap')
@admin_required
def rekapedom():
    return _render_report()


@blueprint.route('/Rekap<int:teacher_id>')
@admin_required
def rekap_by_teacher(teacher_id):
    if not 1 <= teacher_id <= len(INSTRUCTOR_CHOICES):
        abort(404)
    return _render_report(INSTRUCTOR_CHOICES[teacher_id - 1])


@blueprint.route('/RekapDosen')
@admin_required
def rekapdosen():
    return _render_report('Taufiq Abidin, M.Kom.')


@blueprint.route('/<int:id>/deleteedom', methods=['GET', 'POST'])
@admin_required
def delete(id):
    edom = EdomModel.query.get_or_404(id)
    if request.method == 'POST':
        db.session.delete(edom)
        db.session.commit()
        flash('Data evaluasi berhasil dihapus.', 'success')
        return redirect(url_for('base_blueprint.dataedom'))
    return render_template('deleteedom.html', edom=edom)


@blueprint.route('/Maktul', methods=['GET', 'POST'])
@admin_required
def maktul():
    form = CreateMataKuliahForm()
    if form.validate_on_submit():
        course = MataKuliah(
            matakuliah=form.matakuliah.data.strip(),
            namadosen=form.namadosen.data.strip(),
            semester=form.semester.data.strip(),
        )
        db.session.add(course)
        db.session.commit()
        flash('Mata kuliah berhasil disimpan.', 'success')
        return redirect(url_for('base_blueprint.maktul'))
    return render_template('Maktul.html', form=form)
