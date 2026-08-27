from datetime import datetime
from functools import wraps
from decimal import Decimal, InvalidOperation

from flask import Blueprint, render_template, request, redirect, url_for, flash, abort
from flask_login import login_required, current_user

from models import db
from models.user import User
from models.destination import Destination
from models.tour import Tour
from models.booking import Booking


admin_bp = Blueprint("admin", __name__, url_prefix="/admin")


def admin_required(function):
    @wraps(function)
    @login_required
    def decorated_function(*args, **kwargs):
        if current_user.role != "admin":
            abort(403)
        return function(*args, **kwargs)
    return decorated_function


def parse_date(value):
    return datetime.strptime(value, "%Y-%m-%d").date() if value else None


def parse_time(value):
    return datetime.strptime(value, "%H:%M").time() if value else None


def get_tour_form_data():
    destination_id = request.form.get("destination_id", type=int)
    title = request.form.get("title", "").strip()
    departure_date_raw = request.form.get("departure_date", "").strip()
    price_raw = request.form.get("price", "").strip()
    total_seats = request.form.get("total_seats", type=int)

    if not destination_id or not title or not departure_date_raw or not price_raw:
        raise ValueError("Destination, title, departure date and price are required.")

    try:
        price = Decimal(price_raw)
    except InvalidOperation:
        raise ValueError("Price must be a valid number.")

    if price < 0:
        raise ValueError("Price cannot be negative.")
    if total_seats is None or total_seats < 0:
        raise ValueError("Total seats must be zero or more.")

    return {
        "destination_id": destination_id,
        "title": title,
        "short_description": request.form.get("short_description", "").strip(),
        "description": request.form.get("description", "").strip(),
        "departure_location": request.form.get("departure_location", "").strip(),
        "departure_date": parse_date(departure_date_raw),
        "departure_time": parse_time(request.form.get("departure_time")),
        "return_date": parse_date(request.form.get("return_date")),
        "return_time": parse_time(request.form.get("return_time")),
        "duration": request.form.get("duration", "").strip(),
        "price": price,
        "total_seats": total_seats,
        "transport_details": request.form.get("transport_details", "").strip(),
        "hotel_details": request.form.get("hotel_details", "").strip(),
        "food_details": request.form.get("food_details", "").strip(),
        "included_services": request.form.get("included_services", "").strip(),
        "excluded_services": request.form.get("excluded_services", "").strip(),
        "itinerary": request.form.get("itinerary", "").strip(),
        "rules": request.form.get("rules", "").strip(),
        "cancellation_policy": request.form.get("cancellation_policy", "").strip(),
        "cover_image": request.form.get("cover_image", "").strip(),
        "status": request.form.get("status", "upcoming")
    }


@admin_bp.route("/")
@admin_required
def dashboard():
    return render_template(
        "admin/dashboard.html",
        total_users=User.query.count(),
        total_destinations=Destination.query.count(),
        total_tours=Tour.query.count(),
        total_bookings=Booking.query.count(),
        upcoming_tours=Tour.query.filter_by(status="upcoming").count(),
        recent_tours=Tour.query.order_by(Tour.created_at.desc()).limit(5).all(),
        recent_bookings=Booking.query.order_by(Booking.created_at.desc()).limit(5).all()
    )


@admin_bp.route("/destinations", methods=["GET", "POST"])
@admin_required
def destinations():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        if not name:
            flash("Destination name is required.", "danger")
            return redirect(url_for("admin.destinations"))

        destination = Destination(
            name=name,
            district=request.form.get("district", "").strip(),
            division=request.form.get("division", "").strip(),
            description=request.form.get("description", "").strip(),
            image=request.form.get("image", "").strip()
        )
        db.session.add(destination)
        db.session.commit()
        flash("Destination added successfully.", "success")
        return redirect(url_for("admin.destinations"))

    destination_list = Destination.query.order_by(Destination.id.desc()).all()
    return render_template("admin/destinations.html", destinations=destination_list)


@admin_bp.route("/tours")
@admin_required
def tours():
    tour_list = Tour.query.order_by(Tour.created_at.desc()).all()
    return render_template("admin/tours.html", tours=tour_list)


@admin_bp.route("/tours/add", methods=["GET", "POST"])
@admin_required
def add_tour():
    destinations = Destination.query.order_by(Destination.name.asc()).all()
    if not destinations:
        flash("Please add a destination first.", "warning")
        return redirect(url_for("admin.destinations"))

    if request.method == "POST":
        try:
            data = get_tour_form_data()
        except ValueError as exc:
            flash(str(exc), "danger")
            return render_template("admin/add_tour.html", destinations=destinations)

        tour = Tour(**data)
        tour.available_seats = tour.total_seats
        db.session.add(tour)
        db.session.commit()
        flash("Tour added successfully.", "success")
        return redirect(url_for("admin.tours"))

    return render_template("admin/add_tour.html", destinations=destinations)


@admin_bp.route("/tours/edit/<int:tour_id>", methods=["GET", "POST"])
@admin_required
def edit_tour(tour_id):
    tour = Tour.query.get_or_404(tour_id)
    destinations = Destination.query.order_by(Destination.name.asc()).all()

    if request.method == "POST":
        old_total = tour.total_seats or 0
        old_available = tour.available_seats or 0
        booked_seats = max(old_total - old_available, 0)

        try:
            data = get_tour_form_data()
        except ValueError as exc:
            flash(str(exc), "danger")
            return render_template("admin/edit_tour.html", tour=tour, destinations=destinations)

        if data["total_seats"] < booked_seats:
            flash(f"Total seats cannot be less than already booked seats ({booked_seats}).", "danger")
            return render_template("admin/edit_tour.html", tour=tour, destinations=destinations)

        for key, value in data.items():
            setattr(tour, key, value)
        tour.available_seats = data["total_seats"] - booked_seats
        db.session.commit()
        flash("Tour updated successfully.", "success")
        return redirect(url_for("admin.tours"))

    return render_template("admin/edit_tour.html", tour=tour, destinations=destinations)


@admin_bp.route("/tours/delete/<int:tour_id>", methods=["POST"])
@admin_required
def delete_tour(tour_id):
    tour = Tour.query.get_or_404(tour_id)
    if tour.bookings:
        flash("A tour with bookings cannot be deleted. Cancel or manage the bookings first.", "danger")
        return redirect(url_for("admin.tours"))
    db.session.delete(tour)
    db.session.commit()
    flash("Tour deleted successfully.", "success")
    return redirect(url_for("admin.tours"))


@admin_bp.route("/bookings")
@admin_required
def bookings():
    booking_list = Booking.query.order_by(Booking.created_at.desc()).all()
    return render_template("admin/bookings.html", bookings=booking_list)


@admin_bp.route("/bookings/<int:booking_id>/status", methods=["POST"])
@admin_required
def update_booking_status(booking_id):
    booking = Booking.query.get_or_404(booking_id)
    new_status = request.form.get("booking_status")
    new_payment_status = request.form.get("payment_status")

    allowed_booking = {"pending", "confirmed", "cancelled", "completed"}
    allowed_payment = {"unpaid", "partial", "paid", "refunded"}

    if new_status not in allowed_booking or new_payment_status not in allowed_payment:
        flash("Invalid booking or payment status.", "danger")
        return redirect(url_for("admin.bookings"))

    old_status = booking.booking_status
    if old_status != "cancelled" and new_status == "cancelled":
        booking.tour.available_seats = min(
            booking.tour.total_seats,
            booking.tour.available_seats + booking.total_persons
        )
    elif old_status == "cancelled" and new_status != "cancelled":
        if booking.tour.available_seats < booking.total_persons:
            flash("Not enough seats to reactivate this booking.", "danger")
            return redirect(url_for("admin.bookings"))
        booking.tour.available_seats -= booking.total_persons

    booking.booking_status = new_status
    booking.payment_status = new_payment_status
    db.session.commit()
    flash("Booking updated successfully.", "success")
    return redirect(url_for("admin.bookings"))
