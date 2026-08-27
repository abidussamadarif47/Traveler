from datetime import datetime
from models import db


class Payment(db.Model):
    __tablename__ = "payments"

    id = db.Column(db.Integer, primary_key=True)
    booking_id = db.Column(db.Integer, db.ForeignKey("bookings.id", ondelete="CASCADE"), nullable=False)
    payment_method = db.Column(db.Enum("cash", "bkash", "nagad", "rocket", "card", "bank"))
    transaction_id = db.Column(db.String(150))
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    payment_status = db.Column(db.Enum("pending", "successful", "failed", "refunded"), default="pending")
    paid_at = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    booking = db.relationship("Booking", backref="payments")
