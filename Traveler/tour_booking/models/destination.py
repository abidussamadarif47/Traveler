from datetime import datetime
from models import db


class Destination(db.Model):
    __tablename__ = "destinations"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    district = db.Column(db.String(100))
    division = db.Column(db.String(100))
    description = db.Column(db.Text)
    image = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    tours = db.relationship("Tour", backref="destination", lazy=True)

    def __repr__(self):
        return f"<Destination {self.name}>"
