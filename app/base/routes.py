from flask import redirect, url_for
from flask_login import current_user

from app.base import blueprint


@blueprint.route('/')
def route_default():
    if current_user.is_authenticated:
        return redirect(url_for('home_blueprint.index'))
    return redirect(url_for('base_blueprint.login'))
