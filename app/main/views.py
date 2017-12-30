from datetime import datetime
from flask import render_template, redirect, url_for, jsonify, request
from . import main
from .. import db
from ..models import Hosts


@main.route('/', methods=['GET'])
def index():
    hosts = Hosts.query.filter(Hosts.type != None).order_by(Hosts.status.asc()).order_by(Hosts.last_checked.asc()).all()
    if len(hosts) == 0:
        perc_up = 0
    else:
        total_hosts = len(hosts)
        up_hosts = len(Hosts.query.filter_by(status=True).all())
        perc_up = float("%.2f" % (up_hosts / float(total_hosts)))
    return render_template('index.html', hosts=hosts, percent_up=perc_up)
