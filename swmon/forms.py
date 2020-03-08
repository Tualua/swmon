from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, IPAddress, ValidationError
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
