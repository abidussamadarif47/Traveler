from datetime import datetime
from models import db


class Booking(db.Model):
    __tablename__ = "bookings"

    id = db.Column(db.Integer, primary_key=True)
    booking_code = db.Column(db.String(50), unique=True, nullable=False, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="SET NULL"))
    tour_id = db.Column(db.Integer, db.ForeignKey("tours.id", ondelete="CASCADE"), nullable=False)
    customer_name = db.Column(db.String(120), nullable=False)
    customer_email = db.Column(db.String(120))
    customer_phone = db.Column(db.String(20), nullable=False)
    total_persons = db.Column(db.Integer, default=1, nullable=False)
    total_amount = db.Column(db.Numeric(10, 2), nullable=False)
    special_request = db.Column(db.Text)
    booking_status = db.Column(db.Enum("pending", "confirmed", "cancelled", "completed"), default="pending")
    payment_status = db.Column(db.Enum("unpaid", "partial", "paid", "refunded"), default="unpaid")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    tour = db.relationship("Tour", backref="bookings")
    user = db.relationship("User", backref="bookings")
