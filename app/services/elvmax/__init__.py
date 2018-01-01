#!/usr/bin/env python
# -*- coding: utf-8 -*-

from maxcube.cube import MaxCube
from maxcube.connection import MaxCubeConnection

import socket
from datetime import datetime

from ... import db
from ...models import Hosts

serverIP = None
minuteCounter = 1000

def check_maxdevices(app):
    if not serverIP:
        return

    # only check every 15 minutes
    global minuteCounter
    minuteCounter = minuteCounter + 1
    if minuteCounter > 15:
        minuteCounter = 0
    if minuteCounter != 0:
        return

    try:
        cube = MaxCube(MaxCubeConnection(serverIP, 62910))
    except socket.timeout:
        print "MAX: Timeout..."
        return

    with app.app_context():
        for device in cube.devices:
            if device.linkStatusError != 0:
                statusOk = False
            else:
                statusOk = True

            record = Hosts.query.filter_by(fqdn=device.name).first()
            if record:    # update if MAX! device already exists
                record.status = statusOk
                record.last_checked = datetime.utcnow()
            else:       # otherwise create a new entry
                host = Hosts(fqdn=device.name, friendly_name=None, status=statusOk, last_checked=datetime.utcnow(), type='MAX', idle_duration=60)
                db.session.add(host)
        db.session.commit()

def setup(app):
    global serverIP
    serverIP = app.config['ELVMAX_SERVER']
