#!/usr/bin/env python
# -*- coding: utf-8 -*-

import mqtt
import ping

def setup(app):
    mqtt.setup(app)
    ping.setup(app)
