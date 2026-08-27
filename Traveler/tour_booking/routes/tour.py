from flask import Blueprint, render_template, request
from sqlalchemy import or_
from models.tour import Tour
from models.destination import Destination


tour_bp = Blueprint("tour", __name__, url_prefix="/tours")


@tour_bp.route("/")
def list_tours():
    query = Tour.query
    search = request.args.get("q", "").strip()
    destination_id = request.args.get("destination", type=int)

    if search:
        query = query.filter(or_(
            Tour.title.ilike(f"%{search}%"),
            Tour.short_description.ilike(f"%{search}%"),
            Tour.departure_location.ilike(f"%{search}%")
        ))

    if destination_id:
        query = query.filter(Tour.destination_id == destination_id)

    tours = query.order_by(Tour.departure_date.asc()).all()
    destinations = Destination.query.order_by(Destination.name.asc()).all()
    return render_template("tours.html", tours=tours, destinations=destinations, search=search, selected_destination=destination_id)


@tour_bp.route("/<int:tour_id>")
def details(tour_id):
    tour = Tour.query.get_or_404(tour_id)
    return render_template("tour_details.html", tour=tour)
