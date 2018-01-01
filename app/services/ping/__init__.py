#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import subprocess
import platform
import socket
from datetime import datetime

from ... import db
from ...models import Hosts


def check_hosts(app):
    for host in Hosts.query.all():
        if host.type != 'PING':
            continue
        fqdn = host.fqdn
        if ':' in fqdn: # a ':' denotes the difference between ping and connect
            (fqdn,port) = fqdn.split(':')
            test = check_socket(fqdn, int(port))
        else:
            test = ping_host(fqdn)
        host.status = test
        host.last_checked = datetime.utcnow()
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
