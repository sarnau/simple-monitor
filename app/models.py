from . import db


class Hosts(db.Model):
    __tablename__ = 'hosts'
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String())
    fqdn = db.Column(db.String(), unique=True)
    port = db.Column(db.Integer, default=None, nullable=True)
    friendly_name = db.Column(db.String())
    status = db.Column(db.Boolean, default=False)
    last_checked = db.Column(db.DateTime)
    idle_duration = db.Column(db.Integer, default=60)
    parameter_string = db.Column(db.String(), nullable=True)
    parameter_value_string = db.Column(db.String(), nullable=True)
    
    def __repr__(self):
        return '<Host {0}>'.format(self.fqdn)