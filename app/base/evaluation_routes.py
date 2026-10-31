from flask import flash, render_template
from flask_login import current_user, login_required

from app.extensions import db
from app.base import blueprint
from app.base.forms import AdminReviewForm, ReviewForm
from app.base.models import EdomModel
from app.base.permissions import admin_required
from app.base.services.edom import (
    INSTRUCTOR_CHOICES,
    instructors_for,
    predict_sentiment,
)


@blueprint.route('/sentiment_prediction', methods=['POST'])
@admin_required
def admin_sentiment_prediction():
    return _save_prediction(AdminReviewForm())


@blueprint.route('/submit-review', methods=['POST'])
@login_required
def submit_review():
    if current_user.is_admin:
        return render_template('errors/403.html'), 403
    return _submit_student_review()


def _submit_student_review():
    form = ReviewForm()
    form.nama.choices = [
        (name, name)
        for name in instructors_for(current_user.semester, current_user.kelas)
    ]
    if not form.validate_on_submit():
        return render_template('Analysis.html', form=form), 400
    return _persist_review(
        nim=current_user.username,
        semester=current_user.semester,
        name=form.nama.data,
        review=form.review.data.strip(),
        form=form,
    )


def _save_prediction(form):
    form.nama.choices = [(name, name) for name in INSTRUCTOR_CHOICES]
    if not form.validate_on_submit():
        return render_template('Analysis.html', form=form), 400
    return _persist_review(
        nim=form.nim.data.strip(),
        semester=form.semester.data,
        name=form.nama.data,
        review=form.review.data.strip(),
        form=form,
    )


def _persist_review(nim, semester, name, review, form):
    if not name or not review:
        flash('Pilih dosen dan isi komentar sebelum mengirim.', 'error')
        return render_template('Analysis.html', form=form), 400

    slug = nim + name
    if EdomModel.query.filter_by(slug=slug).first():
        flash('Anda sudah mengirim evaluasi untuk dosen ini.', 'warning')
        return render_template('Analysis.html', form=form), 409

    sentiment, confidence = predict_sentiment(review)
    evaluation = EdomModel(
        nim=nim,
        nama=name,
        semester=semester,
        review=review,
        sentiment=sentiment,
        probability=str(confidence),
        amount=1,
        slug=slug,
    )
    db.session.add(evaluation)
    db.session.commit()
    flash('Evaluasi berhasil dikirim. Terima kasih atas masukan Anda.', 'success')
    return render_template(
        'Analysis.html',
        form=form,
        result={
            'review': review,
            'sentiment': sentiment,
            'confidence': confidence,
        },
    )
