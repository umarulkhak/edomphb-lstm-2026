from flask import abort, render_template
from flask_login import current_user, login_required

from app.extensions import db
from app.base.forms import AdminReviewForm, ReviewForm
from app.base.models import EdomModel, User
from app.base.services.edom import INSTRUCTOR_CHOICES, instructors_for
from app.home import blueprint

SENTIMENT_LABELS = ('Baik', 'Cukup', 'Kurang', 'Sangat Baik')


@blueprint.route('/index')
@login_required
def index():
    is_admin = current_user.is_admin
    if is_admin:
        counts = dict(
            db.session.query(
                EdomModel.sentiment, db.func.sum(EdomModel.amount)
            ).group_by(EdomModel.sentiment).all()
        )
        return render_template(
            'Dashboard.html',
            is_admin=True,
            total_users=User.query.count(),
            total_reviews=int(
                db.session.query(db.func.coalesce(db.func.sum(EdomModel.amount), 0)).scalar()
            ),
            total_instructors=db.session.query(
                db.func.count(db.func.distinct(EdomModel.nama))
            ).scalar(),
            latest_reviews=EdomModel.query.order_by(EdomModel.id.desc()).limit(6).all(),
            chart_labels=list(SENTIMENT_LABELS),
            chart_values=[int(counts.get(label) or 0) for label in SENTIMENT_LABELS],
        )

    return render_template(
        'Dashboard.html',
        is_admin=False,
        submitted_count=EdomModel.query.filter_by(nim=current_user.username).count(),
    )


@blueprint.route('/Analysis')
@login_required
def analysis():
    if current_user.is_admin:
        form = AdminReviewForm()
        form.nama.choices = [(name, name) for name in INSTRUCTOR_CHOICES]
    else:
        form = ReviewForm()
        form.nama.choices = [
            (name, name)
            for name in instructors_for(current_user.semester, current_user.kelas)
        ]
    return render_template('Analysis.html', form=form)


@blueprint.route('/<template>')
@login_required
def route_template(template):
    if template not in {'About', 'Data'}:
        abort(404)
    if template == 'Data' and not current_user.is_admin:
        abort(403)
    return render_template(template + '.html')
