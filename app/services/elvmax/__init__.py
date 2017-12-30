#!/usr/bin/env python
# -*- coding: utf-8 -*-

from maxcube.cube import MaxCube
from maxcube.connection import MaxCubeConnection

import socket
from datetime import datetime

from ... import db
from ...models import Hosts

serverIP = '192.168.178.33'

def check_maxdevices(app):
    if not serverIP:
        return

    while True:
        try:
            cube = MaxCube(MaxCubeConnection(serverIP, 62910))
        except socket.timeout:
            print "MAX: Timeout..."
            continue
        break

    # for debugging only:
    if not app:
        for device in cube.devices:
            print(device.linkStatusError, device.lowBattery, device.statusInitialized, device.errorStatus, device.name, device.actual_temperature)
        return

    with app.app_context():
        for device in cube.devices:
#            print device.name,device.linkStatusError
            record = Hosts.query.filter_by(fqdn=device.name).first()
            if device.linkStatusError != 0:
                statusOk = False
            else:
                statusOk = True
            if record:    # update if MAX! device already exists
                record.status = statusOk
                record.last_checked = datetime.utcnow()
            else:       # otherwise create a new entry
                host = Hosts(fqdn=device.name, port=None, friendly_name=None, status=statusOk, last_checked=datetime.utcnow(), type='MAX', idle_duration=60)
                db.session.add(host)
        db.session.commit()

def setup(app):
    global serverIP
    serverIP = app.config['ELVMAX_SERVER']

if __name__ == '__main__':
    check_maxdevices(None)
