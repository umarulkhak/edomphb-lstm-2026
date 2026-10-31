from datetime import datetime
from importlib import import_module
from logging import DEBUG, INFO
from os import path

import click
from flask import Flask, render_template, url_for

from app.extensions import csrf, db, login_manager


def register_extensions(app):
    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)


def register_blueprints(app):
    for module_name in (
        'app.base.auth_routes',
        'app.base.admin_routes',
        'app.base.evaluation_routes',
    ):
        import_module(module_name)

    for module_name in ('app.base.routes', 'app.home.routes'):
        module = import_module(module_name)
        app.register_blueprint(module.blueprint)


def configure_database(app):
    @app.before_first_request
    def initialize_database():
        db.create_all()

    @app.teardown_request
    def shutdown_session(exception=None):
        db.session.remove()


def configure_logs(app):
    app.logger.setLevel(DEBUG if app.debug else INFO)


def register_error_handlers(app):
    @app.errorhandler(403)
    def forbidden(error):
        return render_template('errors/403.html'), 403

    @app.errorhandler(404)
    def not_found(error):
        return render_template('errors/404.html'), 404

    @app.errorhandler(500)
    def internal_error(error):
        return render_template('errors/500.html'), 500


def apply_themes(app):
    @app.context_processor
    def override_url_for():
        return {'url_for': _generate_url_for_theme}

    def _generate_url_for_theme(endpoint, **values):
        if endpoint.endswith('static'):
            theme = values.get('theme') or app.config.get('DEFAULT_THEME')
            theme_file = '{}/{}'.format(theme, values.get('filename', ''))
            if theme and path.isfile(path.join(app.static_folder, theme_file)):
                values['filename'] = theme_file
        return url_for(endpoint, **values)


def create_app(config, selenium=False):
    app = Flask(__name__, static_folder='base/static')
    app.config.from_object(config)
    if not app.config.get('SECRET_KEY') and not app.debug:
        raise RuntimeError('Set SECRET_KEY before starting the production application.')
    if not app.config.get('SQLALCHEMY_DATABASE_URI'):
        raise RuntimeError(
            'Set DATABASE_URL or the APPSEED_DATABASE_* variables before starting production.'
        )

    app.config['SESSION_COOKIE_HTTPONLY'] = True
    app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
    if selenium:
        app.config['LOGIN_DISABLED'] = True

    register_extensions(app)
    register_blueprints(app)
    configure_database(app)
    configure_logs(app)
    register_error_handlers(app)
    apply_themes(app)
    app.context_processor(
        lambda: {
            'current_year': datetime.now().year,
            'app_version': app.config['APP_VERSION'],
        }
    )

    @app.cli.command('create-admin')
    def create_admin():
        """Create an administrator account using interactive terminal prompts."""
        from app.base.models import User

        db.create_all()
        username = click.prompt('Username admin').strip()
        email = click.prompt('Email admin').strip().lower()
        password = click.prompt(
            'Kata sandi admin',
            hide_input=True,
            confirmation_prompt='Ulangi kata sandi admin',
        )

        if not username or not email:
            raise click.ClickException('Username dan email wajib diisi.')
        if len(password) < 8:
            raise click.ClickException('Kata sandi harus memiliki minimal 8 karakter.')
        if User.query.filter(
            (User.username == username) | (User.email == email)
        ).first():
            raise click.ClickException('Username atau email sudah terdaftar.')

        db.session.add(
            User(
                username=username,
                nama='Administrator',
                email=email,
                semester='',
                kelas='',
                password=password,
            )
        )
        db.session.commit()
        click.echo(f'Akun admin {username} berhasil dibuat.')

    return app
