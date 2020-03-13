from flask import Blueprint, render_template, redirect, url_for, jsonify, current_app
from pandas import DataFrame
import time
from ..extensions import db
from ..models import Switch, Router
from ..forms import AddSwitchForm, EditSwitchForm
from ..tasks import GetDevicesInfo


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


@switch_bp.route('/<int:id>/getdata')
def getdata(id):
    switch = Switch.get_switch(id)
    router = Router.query.get(1)
    start_time = time.time()
    dfFDB = DataFrame.from_records(switch.fdb(range(10, 35)), columns=['Switch', 'Port', 'MAC', 'VLAN'])
    print(time.time() - start_time)
    start_time = time.time()

    dfLeases = DataFrame.from_records(
        router.get_leases(
            current_app.config['ROS_USER'], current_app.config['ROS_PASSWORD']),
        index='MAC', columns=['MAC', 'IP', 'Hostname'])

    print(time.time() - start_time)
    start_time = time.time()
    dfDevices = dfFDB.join(dfLeases, on='MAC')
    print(time.time() - start_time)
    iplist = dfDevices['IP'].dropna().tolist()
    start_time = time.time()
    status = GetDevicesInfo(iplist)
    print(status)
    dfStatus = DataFrame.from_records(status, index='IP', columns=['IP', 'Type', 'HR', 'Power'])
    dfResult = dfDevices.join(dfStatus, on='IP').sort_values(by=['Port']).fillna('')
    print(time.time() - start_time)

    return jsonify(data=tuple(dfResult.itertuples(index=False)))


@switch_bp.route('/<int:id>/show')
def show(id):
    return render_template('switch/show.html', id=id, ip=Switch.get_switch(id).ipaddress)
