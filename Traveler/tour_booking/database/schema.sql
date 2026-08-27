CREATE DATABASE IF NOT EXISTS tour_booking;

USE tour_booking;


-- =========================
-- USERS TABLE
-- =========================
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,

    full_name VARCHAR(100) NOT NULL,

    email VARCHAR(120) NOT NULL UNIQUE,

    phone VARCHAR(20),

    password VARCHAR(255) NOT NULL,

    role ENUM('customer', 'admin') DEFAULT 'customer',

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


-- =========================
-- ADMINS TABLE
-- =========================
CREATE TABLE IF NOT EXISTS admins (
    id INT AUTO_INCREMENT PRIMARY KEY,

    user_id INT NOT NULL UNIQUE,

    designation VARCHAR(100),

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (user_id)
        REFERENCES users(id)
        ON DELETE CASCADE
);


-- =========================
-- DESTINATIONS TABLE
-- =========================
CREATE TABLE IF NOT EXISTS destinations (
    id INT AUTO_INCREMENT PRIMARY KEY,

    name VARCHAR(150) NOT NULL,

    district VARCHAR(100),

    division VARCHAR(100),

    description TEXT,

    image VARCHAR(255),

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


-- =========================
-- TOURS TABLE
-- =========================
CREATE TABLE IF NOT EXISTS tours (
    id INT AUTO_INCREMENT PRIMARY KEY,

    destination_id INT NOT NULL,

    title VARCHAR(200) NOT NULL,

    short_description VARCHAR(500),

    description TEXT,

    departure_location VARCHAR(200),

    departure_date DATE NOT NULL,

    departure_time TIME,

    return_date DATE,

    return_time TIME,

    duration VARCHAR(100),

    price DECIMAL(10,2) NOT NULL,

    total_seats INT DEFAULT 0,

    available_seats INT DEFAULT 0,

    transport_details TEXT,

    hotel_details TEXT,

    food_details TEXT,

    included_services TEXT,

    excluded_services TEXT,

    itinerary TEXT,

    rules TEXT,

    cancellation_policy TEXT,

    cover_image VARCHAR(255),

    status ENUM(
        'upcoming',
        'ongoing',
        'completed',
        'cancelled'
    ) DEFAULT 'upcoming',

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (destination_id)
        REFERENCES destinations(id)
        ON DELETE CASCADE
);


-- =========================
-- BOOKINGS TABLE
-- =========================
CREATE TABLE IF NOT EXISTS bookings (
    id INT AUTO_INCREMENT PRIMARY KEY,

    booking_code VARCHAR(50) NOT NULL UNIQUE,

    user_id INT,

    tour_id INT NOT NULL,

    customer_name VARCHAR(120) NOT NULL,

    customer_email VARCHAR(120),

    customer_phone VARCHAR(20) NOT NULL,

    total_persons INT NOT NULL DEFAULT 1,

    total_amount DECIMAL(10,2) NOT NULL,

    special_request TEXT,

    booking_status ENUM(
        'pending',
        'confirmed',
        'cancelled',
        'completed'
    ) DEFAULT 'pending',

    payment_status ENUM(
        'unpaid',
        'partial',
        'paid',
        'refunded'
    ) DEFAULT 'unpaid',

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (user_id)
        REFERENCES users(id)
        ON DELETE SET NULL,

    FOREIGN KEY (tour_id)
        REFERENCES tours(id)
        ON DELETE CASCADE
);


-- =========================
-- PAYMENTS TABLE
-- =========================
CREATE TABLE IF NOT EXISTS payments (
    id INT AUTO_INCREMENT PRIMARY KEY,

    booking_id INT NOT NULL,

    payment_method ENUM(
        'cash',
        'bkash',
        'nagad',
        'rocket',
        'card',
        'bank'
    ),

    transaction_id VARCHAR(150),

    amount DECIMAL(10,2) NOT NULL,

    payment_status ENUM(
        'pending',
        'successful',
        'failed',
        'refunded'
    ) DEFAULT 'pending',

    paid_at DATETIME,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (booking_id)
        REFERENCES bookings(id)
        ON DELETE CASCADE
);


-- =========================
-- REVIEWS TABLE
-- =========================
CREATE TABLE IF NOT EXISTS reviews (
    id INT AUTO_INCREMENT PRIMARY KEY,

    user_id INT,

    tour_id INT NOT NULL,

    rating INT NOT NULL,

    comment TEXT,

    status ENUM(
        'pending',
        'approved',
        'rejected'
    ) DEFAULT 'pending',

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (user_id)
        REFERENCES users(id)
        ON DELETE SET NULL,

    FOREIGN KEY (tour_id)
        REFERENCES tours(id)
        ON DELETE CASCADE,

    CHECK (rating >= 1 AND rating <= 5)
);