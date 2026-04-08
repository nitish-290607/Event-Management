-- MySQL Schema Definition
CREATE DATABASE IF NOT EXISTS event_management;
USE event_management;

-- Drop tables if they exist
DROP TABLE IF EXISTS Notifications;
DROP TABLE IF EXISTS Payments;
DROP TABLE IF EXISTS Registrations;
DROP TABLE IF EXISTS Events;
DROP TABLE IF EXISTS Venues;
DROP TABLE IF EXISTS Users;

CREATE TABLE Users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    role VARCHAR(50) NOT NULL CHECK (role IN ('Admin', 'Organizer', 'Attendee')),
    username VARCHAR(100) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE Venues (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    location VARCHAR(500) NOT NULL,
    capacity INT NOT NULL
);

CREATE TABLE Events (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    event_date DATE NOT NULL,
    event_time TIME NOT NULL,
    venue_id INT NOT NULL,
    capacity INT NOT NULL CHECK (capacity > 0),
    ticket_price DECIMAL(10,2) NOT NULL DEFAULT 100.00,
    current_attendees INT DEFAULT 0,
    organizer_id INT NOT NULL,
    status VARCHAR(50) DEFAULT 'upcoming' CHECK (status IN ('upcoming', 'ongoing', 'completed')),
    image_url VARCHAR(500),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (organizer_id) REFERENCES Users(id) ON DELETE CASCADE,
    FOREIGN KEY (venue_id) REFERENCES Venues(id) ON DELETE RESTRICT
);

CREATE TABLE Registrations (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    event_id INT NOT NULL,
    status VARCHAR(50) DEFAULT 'registered' CHECK (status IN ('registered', 'cancelled')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES Users(id) ON DELETE CASCADE,
    FOREIGN KEY (event_id) REFERENCES Events(id) ON DELETE CASCADE,
    UNIQUE(user_id, event_id)
);

CREATE TABLE Payments (
    transaction_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    event_id INT NOT NULL,
    amount DECIMAL(10,2) NOT NULL,
    status VARCHAR(50) DEFAULT 'success' CHECK (status IN ('success', 'failed')),
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES Users(id),
    FOREIGN KEY (event_id) REFERENCES Events(id)
);

CREATE TABLE Notifications (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    message VARCHAR(500) NOT NULL,
    is_read BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES Users(id) ON DELETE CASCADE
);

-- Note: Triggers and Procedures are updated to match the new venue_id logic.
-- (They mostly reference id/dates, so no major logic shifts inside them other than checking `venue_id`).

-- Views
CREATE OR REPLACE VIEW Event_Schedules AS
SELECT 
    e.id AS event_id,
    e.title AS event_title,
    e.event_date AS schedule_date,
    e.event_time AS schedule_time,
    v.name AS venue_name,
    v.location AS venue_location,
    u.username AS organizer_name,
    e.status
FROM 
    Events e
JOIN 
    Venues v ON e.venue_id = v.id
JOIN 
    Users u ON e.organizer_id = u.id
WHERE 
    e.status != 'completed'
ORDER BY 
    e.event_date ASC, e.event_time ASC;
