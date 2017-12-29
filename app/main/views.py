from datetime import datetime
from flask import render_template, redirect, url_for, jsonify, request
from . import main, report
from .. import db
from ..models import Hosts


@main.route('/', methods=['GET', 'POST'])
def index():
    hosts = Hosts.query.filter(Hosts.type != None).order_by(Hosts.status.asc()).order_by(Hosts.last_checked.asc()).all()
    if len(hosts) == 0:
        perc_up = 0
    else:
        total_hosts = len(hosts)
        up_hosts = len(Hosts.query.filter_by(status=True).all())
        perc_up = float("%.2f" % (up_hosts / float(total_hosts)))
    return render_template('index.html', hosts=hosts, percent_up=perc_up)

@main.route('/check-hosts', methods=['GET', 'POST'])
def check_hosts():
    hosts = Hosts.query.all()
    if request.method == 'POST':
        if len(hosts) == 0:
            return jsonify({}, 204)
        return_data = report.check_hosts()
        return jsonify(return_data, 202)
    else:
        if len(hosts) == 0:
            return redirect(url_for('main.index'))
        report.check_hosts()
    return redirect(url_for('main.index'))
