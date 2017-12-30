#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import subprocess
import platform
import socket
from datetime import datetime

from ... import db
from ...models import Hosts


def check_hosts():
    for host in Hosts.query.all():
        fqdn = host.fqdn
        if host.type == 'CONNECT':
            port = host.port
            if port is not None:
                port = 80
            test = check_socket(fqdn, port)
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


def check_socket(hostname, port):
    try:
        r = socket.create_connection((hostname, port), 2)
    except socket.error:
        return False
    if r:
        return True

def setup(app):
    pass
