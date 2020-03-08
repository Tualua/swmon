from flask import Blueprint, render_template, redirect, url_for
from ..models import Switch, db
from ..forms import AddSwitchForm


switch_bp = Blueprint('switch', __name__)


@switch_bp.route('/')
def switch():
    return 'Switch View'


@switch_bp.route('/add', methods=['GET', 'POST'])
def add():
    form = AddSwitchForm()
    if form.validate_on_submit():
        switch = Switch(
            ipaddress=form.ipaddress.data, vendor=form.vendor.data, uplinkports=form.uplinkports.data,
            community=form.community.data)
        db.session.add(switch)
        db.session.commit()
        return redirect(url_for('home.home'))
    return render_template('switch/add.html', form=form)
