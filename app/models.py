#!/usr/bin/env python
# -*- coding: utf-8 -*-

from . import db


class Hosts(db.Model):
    __tablename__ = 'hosts'
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String())
    fqdn = db.Column(db.String(), unique=True)
    friendly_name = db.Column(db.String())
    status = db.Column(db.Boolean, default=False)
    last_checked = db.Column(db.DateTime)
    idle_duration = db.Column(db.Integer, default=60)
    
    def __repr__(self):
        return '<Host {0}>'.format(self.fqdn)
