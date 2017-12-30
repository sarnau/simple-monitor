#!/usr/bin/env python

import os
import subprocess
import platform
import socket
from datetime import datetime

from ... import db
from ...models import Hosts


def check_hosts():
    """
    Function to check all hosts
    
    If host is up returns true, else will return false
    """
    return_data = {}
    hosts = Hosts.query.all()
    for host in hosts:
        fqdn = host.fqdn
        if host.type == 'CONNECT':
            port = host.port
            if port is not None:
                port = 80
            return_name = fqdn + ':' + str(port)
            test = check_sock(fqdn, port)
        elif host.type == 'PING':
            return_name = fqdn
            test = ping_host(fqdn)
        else:
            continue
        timestamp = datetime.utcnow()
        host.status = test
        host.last_checked = timestamp
        db.session.add(host)
        return_data[return_name] = test
    return return_data


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


if __name__ == '__main__':
    check_hosts()
