from .home import home_bp
from .switch import switch_bp
from .settings import settings_bp


def init_app(app):
    app.register_blueprint(home_bp)
    app.register_blueprint(switch_bp, url_prefix='/switch')
    app.register_blueprint(settings_bp, url_prefix='/settings')
