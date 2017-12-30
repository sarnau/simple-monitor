#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import subprocess
import platform
import socket
from datetime import datetime

from ... import db
from ...models import Hosts

# import BackgroundScheduler
from apscheduler.schedulers.background import BackgroundScheduler


def check_hosts():
    hosts = Hosts.query.all()
    for host in hosts:
        fqdn = host.fqdn
        if host.type == 'CONNECT':
            port = host.port
            if port is not None:
                port = 80
            test = check_sock(fqdn, port)
        elif host.type == 'PING':
            test = ping_host(fqdn)
        else:
            continue
        timestamp = datetime.utcnow()
        host.status = test
        host.last_checked = timestamp
        db.session.add(host)
    db.session.commit()


def ping_host(hostname):
    os_type = platform.platform()
    with open(os.devnull, 'w'):
        try:
            if 'Windows' in os_type:
                response = subprocess.check_output(['ping', '-n', '1', hostname],
                                                   stderr=subprocess.STDOUT,
                                                   universal_newlines=True
                                                   )
            else:
                response = subprocess.check_output(['ping', '-c', '1', hostname],
                                                   stderr=subprocess.STDOUT,
                                                   universal_newlines=True
                                                   )
            if 'host unreachable' in response:
                is_up = False
            else:
                is_up = True
        except subprocess.CalledProcessError:
            is_up = False
    return is_up


def check_sock(hostname, port):
    try:
        r = socket.create_connection((hostname, port), 2)
    except socket.error:
        return False
    if r:
        return True

def setup(app):
    if not app.debug or os.environ.get('WERKZEUG_RUN_MAIN') == 'true': # avoid launching the scheduler twice in debug
        print "Initializing ping..."

        # init BackgroundScheduler job
        def update_hosts():
            with app.app_context():
                check_hosts()

        scheduler = BackgroundScheduler()
        scheduler.add_job(update_hosts,'interval',minutes=1)
        scheduler.start()

        def goodbye():
            # shutdown if app occurs except 
            print "Exiting ping..."
            scheduler.shutdown()

        import atexit
        atexit.register(goodbye)
