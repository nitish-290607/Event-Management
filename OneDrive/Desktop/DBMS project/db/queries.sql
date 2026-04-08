-- SQL Queries for Event Management System Project
-- These meet the explicit DBMS project requirements

-- 1. SQL Query for Event Registration
-- Registers a user (id = 4) for an event (id = 1) assuming capacity is available
INSERT INTO Registrations (user_id, event_id, status)
VALUES (4, 1, 'registered');

-- 2. Aggregate Queries for Participant Count
-- Total participant count across all events
SELECT 
    e.title AS event_name, 
    COUNT(r.user_id) AS total_participants
FROM 
    Events e
LEFT JOIN 
    Registrations r ON e.id = r.event_id AND r.status = 'registered'
GROUP BY 
    e.id, e.title;

-- Alternate Aggregate: Count total events and participants per organizer
SELECT 
    u.username AS organizer_name,
    COUNT(DISTINCT e.id) AS total_events_organized,
    SUM(e.current_attendees) AS total_participants_across_events
FROM 
    Users u
JOIN 
    Events e ON u.id = e.organizer_id
WHERE 
    u.role = 'Organizer'
GROUP BY 
    u.id, u.username;

-- 3. Views for Event Schedules
-- Creates a comprehensive view of the event schedule, easily readable by the application or admins
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

-- Querying the newly created view
SELECT * FROM Event_Schedules;
