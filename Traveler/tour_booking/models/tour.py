from datetime import datetime
from models import db


class Tour(db.Model):
    __tablename__ = "tours"

    id = db.Column(db.Integer, primary_key=True)
    destination_id = db.Column(db.Integer, db.ForeignKey("destinations.id", ondelete="CASCADE"), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    short_description = db.Column(db.String(500))
    description = db.Column(db.Text)
    departure_location = db.Column(db.String(200))
    departure_date = db.Column(db.Date, nullable=False)
    departure_time = db.Column(db.Time)
    return_date = db.Column(db.Date)
    return_time = db.Column(db.Time)
    duration = db.Column(db.String(100))
    price = db.Column(db.Numeric(10, 2), nullable=False)
    total_seats = db.Column(db.Integer, default=0)
    available_seats = db.Column(db.Integer, default=0)
    transport_details = db.Column(db.Text)
    hotel_details = db.Column(db.Text)
    food_details = db.Column(db.Text)
    included_services = db.Column(db.Text)
    excluded_services = db.Column(db.Text)
    itinerary = db.Column(db.Text)
    rules = db.Column(db.Text)
    cancellation_policy = db.Column(db.Text)
    cover_image = db.Column(db.String(255))
    status = db.Column(db.Enum("upcoming", "ongoing", "completed", "cancelled"), default="upcoming")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Tour {self.title}>"
