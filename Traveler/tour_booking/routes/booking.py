from decimal import Decimal
from uuid import uuid4
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from models import db
from models.tour import Tour
from models.booking import Booking


booking_bp = Blueprint("booking", __name__, url_prefix="/booking")


def new_booking_code():
    return "TB-" + uuid4().hex[:10].upper()


@booking_bp.route("/tour/<int:tour_id>", methods=["GET", "POST"])
@login_required
def create(tour_id):
    tour = Tour.query.get_or_404(tour_id)

    if tour.status != "upcoming" or tour.available_seats <= 0:
        flash("This tour is not available for booking.", "warning")
        return redirect(url_for("tour.details", tour_id=tour.id))

    if request.method == "POST":
        customer_name = request.form.get("customer_name", "").strip()
        customer_email = request.form.get("customer_email", "").strip().lower()
        customer_phone = request.form.get("customer_phone", "").strip()
        total_persons = request.form.get("total_persons", type=int) or 1
        special_request = request.form.get("special_request", "").strip()

        if not customer_name or not customer_phone:
            flash("Name and phone are required.", "danger")
            return render_template("booking.html", tour=tour)

        if total_persons < 1:
            flash("Number of persons must be at least 1.", "danger")
            return render_template("booking.html", tour=tour)

        if total_persons > tour.available_seats:
            flash(f"Only {tour.available_seats} seat(s) are available.", "danger")
            return render_template("booking.html", tour=tour)

        total_amount = Decimal(tour.price) * total_persons
        booking = Booking(
            booking_code=new_booking_code(),
            user_id=current_user.id,
            tour_id=tour.id,
            customer_name=customer_name,
            customer_email=customer_email or current_user.email,
            customer_phone=customer_phone,
            total_persons=total_persons,
            total_amount=total_amount,
            special_request=special_request,
            booking_status="pending",
            payment_status="unpaid"
        )

        tour.available_seats -= total_persons
        db.session.add(booking)
        db.session.commit()

        return redirect(url_for("booking.success", booking_code=booking.booking_code))

    return render_template("booking.html", tour=tour)


@booking_bp.route("/success/<booking_code>")
@login_required
def success(booking_code):
    booking = Booking.query.filter_by(booking_code=booking_code, user_id=current_user.id).first_or_404()
    return render_template("booking_success.html", booking=booking)


@booking_bp.route("/my-bookings")
@login_required
def my_bookings():
    bookings = Booking.query.filter_by(user_id=current_user.id).order_by(Booking.created_at.desc()).all()
    return render_template("my_bookings.html", bookings=bookings)
