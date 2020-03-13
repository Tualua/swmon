from flask import Blueprint, render_template, redirect, url_for
from ..models import Switch, db
from ..forms import AddSwitchForm, EditSwitchForm


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


@switch_bp.route('/<int:id>/edit', methods=['GET', 'POST'])
def edit(id):
    switch = Switch.get_switch(id)
    form = EditSwitchForm(obj=switch)
    if form.validate_on_submit():
        switch.ipaddress, switch.vendor, switch.uplinkports, switch.community = \
            form.ipaddress.data, form.vendor.data, form.uplinkports.data, form.community.data
        db.session.commit()
        return redirect(url_for('home.home'))
    else:
        print(form.ipaddress.data)
    return render_template('switch/edit.html', form=form)


@switch_bp.route('/<int:id>/edit', methods=['GET', 'POST'])
def show(id):
    switch = Switch.get_switch(id)
    print(switch)
    return render_template('switch/show.html')
