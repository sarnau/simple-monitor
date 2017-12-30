#!/usr/bin/env python
# -*- coding: utf-8 -*-

import mqtt
import ping

# import BackgroundScheduler
import os
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timedelta
from .. import db
from ..models import Hosts

def setup(app):
    mqtt.setup(app)
    ping.setup(app)

    if not app.debug or os.environ.get('WERKZEUG_RUN_MAIN') == 'true': # avoid launching the scheduler twice in debug
        print "Initializing service timer..."

        # init BackgroundScheduler job
        def check_service_timeout():
            with app.app_context():
                for host in Hosts.query.all():
                    if host.last_checked + timedelta(minutes=host.idle_duration) < datetime.utcnow():
                        host.status = False
                    else:
                        host.status = True
                db.session.commit()

        scheduler = BackgroundScheduler()
        scheduler.add_job(check_service_timeout,'interval',minutes=1)
        check_service_timeout()
        scheduler.start()

        def goodbye():
            # shutdown if app occurs except 
            print "Exiting service timer..."
            scheduler.shutdown()

        import atexit
        atexit.register(goodbye)

