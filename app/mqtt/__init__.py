#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

# sudo pip install paho-mqtt
import paho.mqtt.client as mqtt

from datetime import datetime

from .. import db
from ..models import Hosts


# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, app, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("#")

def on_disconnect(client, userdata, rc):
    print("Disconnected with result code "+str(rc))

def printUnknowMessage(msg):
    print('### '+str(datetime.utcnow())+" "+msg.topic+" "+str(msg.payload))

def on_message(client, app, msg):
    topic = msg.topic
    if topic.endswith('/json'):
        topic = topic[:-5]
    print(str(datetime.utcnow())+" "+topic+" "+str(msg.payload))
    with app.app_context():
        record = Hosts.query.filter_by(fqdn=topic).first()
        if record:    # update if MQTT topic already exists
            record.status = True
            record.last_checked = datetime.utcnow()
        else:       # otherwise create a new entry
            host = Hosts(fqdn=topic, port=None, friendly_name=None, status=True, last_checked=datetime.utcnow())
            db.session.add(host)
        db.session.commit()

def add_mqtt_listener(app):
    print 'Connecting to MQTT server'
    mqttc = mqtt.Client(userdata=app)
    mqttc.on_connect = on_connect
    mqttc.on_disconnect = on_disconnect
    mqttc.on_message = on_message
    mqttc.username_pw_set('pi', 'raspberry')
    mqttc.connect("hassio.local", 1883, 60)
    mqttc.loop_start()
