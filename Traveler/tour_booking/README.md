# Traveler - Tour Booking Website

Flask + MySQL tour group booking project.

## Features
- Customer registration, login and logout
- Public tour list, search and tour details
- Tour cost, dates, time, seats, hotel, food, transport, itinerary and rules
- Customer booking and My Bookings page
- Admin dashboard
- Destination management
- Add, edit and delete tours
- Booking/payment-status management

## Setup (Windows PowerShell)
1. Open the project folder:
   `cd E:\Project\Traveler\tour_booking`
2. Create/activate a virtual environment (or use your existing one).
3. Install packages:
   `python -m pip install -r requirements.txt`
4. Put your MySQL credentials in `.env`.
5. Import `database/schema.sql` into MySQL.
6. Run:
   `python app.py`
7. Open `http://127.0.0.1:5000`

## Make a user admin
Run in MySQL:
`UPDATE users SET role='admin' WHERE email='your-email@example.com';`
Then logout and login again.
