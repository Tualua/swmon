import ssl
from sqlalchemy.orm.exc import NoResultFound
from puresnmp import bulkwalk
from librouteros import connect
from librouteros.login import plain
from librouteros.query import Key
from .extensions import db


class Router(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ipaddress = db.Column(db.String(15), index=True, unique=True, nullable=False)
    port = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return '{}'.format(self.ipaddress)

    def get_leases(self, username, password):
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE

        method = plain

        api = connect(
            username=username,
            password=password,
            host=self.ipaddress,
            ssl_wrapper=ctx.wrap_socket,
            port=self.port,
            login_method=method
        )
        ipaddress = Key('active-address')
        macaddress = Key('mac-address')
        hostname = Key('host-name')
        status = Key('status')
        data = api.path('/ip/dhcp-server/lease').select(
            ipaddress, macaddress, hostname).where(status == 'bound')
        leases = (
            (l['mac-address'], l['active-address'], l['host-name']) if 'host-name' in l.keys() else (
                l['mac-address'], l['active-address'], '') for l in data)
        return leases

    @staticmethod
    def get_router():
        try:
            router = Router.query.one()
        except NoResultFound:
            return None
        return router


class Switch(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ipaddress = db.Column(db.String(15), index=True, unique=True, nullable=False)
    vendor = db.Column(db.String(16), index=True, nullable=False)
    uplinkports = db.Column(db.String(32), nullable=False)
    community = db.Column(db.String(32), nullable=False)

    def __repr__(self):
        return '{}'.format(self.ipaddress)

    def fdb(self, vlanrange):
        swNumber = int(self.ipaddress.rpartition('.')[2])
        if self.vendor == 'cisco':
            def portnumber(interfacename, quantity):
                if interfacename[0] == 'F':
                    return int(interfacename.rpartition('/')[2])
                elif interfacename[0] == 'G':
                    return int(interfacename.rpartition('/')[2])+quantity

            dot1dTpFdbPort = ['.1.3.6.1.2.1.17.4.3.1.2']
            dot1dBasePortIfIndex = ['.1.3.6.1.2.1.17.1.4.1.2']
            vtpVlanState = ['.1.3.6.1.4.1.9.9.46.1.3.1.1.2.1']
            oidifName = ['.1.3.6.1.2.1.31.1.1.1.1']
            swIfaces = bulkwalk(self.ipaddress, self.community, oidifName)
            swVlans = set(int(vlan.oid[-1]) for vlan in bulkwalk(
                self.ipaddress, self.community, vtpVlanState)) & set(vlanrange)
            swIfNames = {int(i.oid[-1]): i.value.decode('utf-8') for i in swIfaces}
            swMappings = {
                int(m.oid[-1]): swIfNames[int(m.value)]
                for v in swVlans
                for m in bulkwalk(self.ipaddress, "@".join([self.community, str(v)]), dot1dBasePortIfIndex)}
            swFDB = (
                (swNumber, portnumber(swMappings[m.value], 48), ":".join(
                    ["{:02X}".format(int(octet)) for octet in m.oid[-6:]]), v) for v in swVlans for m in bulkwalk(
                    self.ipaddress, "@".join(
                        [self.community, str(v)]), dot1dTpFdbPort) if swMappings[m.value] not in self.uplinkports)
            return swFDB
        elif self.vendor == 'dlink':
            oiddot1qTpFdbEntry = ['.1.3.6.1.2.1.17.7.1.2.2.1.2']
            swFDB = (
                (swNumber, int(m.value), ":".join(
                    ["{:02X}".format(int(octet)) for octet in m.oid[-6:]]), int(m.oid[-7]))
                for m in bulkwalk(self.ipaddress, self.community, oiddot1qTpFdbEntry)
                if int(m.oid[-7]) in vlanrange if str(m.value) not in self.uplinkports)
            return swFDB
        else:
            return None

    @staticmethod
    def get_switch(id):
        return Switch.query.get(int(id))

    @staticmethod
    def get_all():
        return Switch.query.all()


class Settings(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), index=True, unique=True)
    value = db.Column(db.String(64))

    def __repr__(self):
        return '{} = {}'.format(self.name, self.value)
