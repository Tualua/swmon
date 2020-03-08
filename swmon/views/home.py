from flask import Blueprint, render_template
from ..models import Switch

home_bp = Blueprint('home', __name__)


@home_bp.route('/')
def home():
    switches = Switch.get_all()
    return render_template('index.html', title='Switches', data=switches)
