from flask import Blueprint

switch_bp = Blueprint('switch', __name__)


@switch_bp.route('/')
def switch():
    return 'Switch View'
