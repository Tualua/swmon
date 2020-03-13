import json
import socket
import time
from ..extensions import celery
from celery import group
import re


def netcat(hostname, port, command):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((hostname, port))
    sock.sendall(command.encode())
    time.sleep(0.5)
    sock.shutdown(socket.SHUT_WR)

    res = ''

    while 1:
        data = sock.recv(1024)
        if (not data):
            break
        res += data.decode()
    sock.close()
    return res.replace("}{", "},{").replace("\x00", '')


def GetDevicesInfo(addrlist):
    job = group([GetASICInfo.s(ip) for ip in addrlist if ip != ''])
    run = job.apply_async()
    result = run.get()

    return result


@celery.task(bind=True)
def GetASICInfo(self, ipaddress):
    result = json.loads(netcat(ipaddress, 4028, "{\"command\":\"stats\",\"parameter\":\"0\"}"))
    if result:
        asictype = result['STATS'][0]['Type']
        hr = result['STATS'][1]['GHS av']
        if 'chain_power' in result['STATS'][1]:
            power = float(result['STATS'][1]['chain_power'].partition(" ")[0])
        else:
            power = 0.0
    return [ipaddress, asictype, hr, power]


@celery.task
def dummy_task():
    return 'OK'
