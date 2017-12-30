#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

from config import config

bootstrap = Bootstrap()
db = SQLAlchemy()
admin = Admin(name='Device Monitor', base_template='layout.html', template_mode='bootstrap3')


class HostModelView(ModelView):
    create_modal = True
    edit_modal = True
    can_export = True
    form_choices = {
        'type': [
            ('PING', 'Ping'),
            ('CONNECT', 'Connect'),
            ('MQTT', 'MQTT')
        ]
    }
    column_list = ['type', 'fqdn', 'port', 'friendly_name', 'idle_duration']
    column_editable_list = ['type', 'fqdn', 'port', 'friendly_name', 'idle_duration']
    form_excluded_columns = ['status', 'last_checked', 'parameter_string', 'parameter_value_string']
    page_size = 100  # the number of entries to display on the list view


# Application factory for the flask application
def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    bootstrap.init_app(app)
    db.init_app(app)

    from .models import Hosts
    
    admin.init_app(app)
    admin.add_view(HostModelView(Hosts, db.session))
    
    # Register blueprints for different functions within the app
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from services import setup
    services.setup(app)

    return app
