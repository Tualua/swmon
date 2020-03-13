from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import DataRequired, NumberRange, IPAddress, ValidationError
from .models import Switch


class SwitchForm(FlaskForm):
    ipaddress = StringField('IP Address', validators=[DataRequired(), IPAddress(
        ipv4=True, ipv6=False, message='Valid IPv4 Address Required'
    )])
    vendor = StringField('Vendor', validators=[DataRequired(message='Enter cisco or dlink')])
    uplinkports = StringField('Uplink ports', validators=[DataRequired(
        message='For D-Link Switches 49,50 or 25,26. For Cisco Gi1/0/4 or Gi0/2'
    )])
    community = StringField('SNMP Community', validators=[DataRequired(
        message='SNMP Community string. Use public by default'
    )])

    def validate_ipaddress(self, ipaddress):
        switch = Switch.query.filter_by(ipaddress=ipaddress.data).first()
        if switch is not None:
            raise ValidationError('Switch with same IP address is already added!')


class AddSwitchForm(SwitchForm):
    submit = SubmitField('Add switch')


class EditSwitchForm(SwitchForm):
    submit = SubmitField('Save')


class EditRouterForm(FlaskForm):
    ipaddress = StringField('IP Address', validators=[DataRequired(), IPAddress(
        ipv4=True, ipv6=False, message='Valid IPv4 Address Required'
    )])
    port = IntegerField('Port', validators=[DataRequired(), NumberRange(
        min=1, max=65535, message='Port range is from 1 to 65535')])
    submitRouter = SubmitField('Save')
