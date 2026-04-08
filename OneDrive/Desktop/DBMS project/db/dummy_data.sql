-- Dummy Data for Event Management System

-- Insert Users (Admins, Organizers, Attendees)
-- Passwords are just dummy hashes for illustration (e.g., hashed 'password123')
INSERT INTO Users (role, username, email, password_hash) VALUES ('Admin', 'admin_user', 'admin@example.com', 'hashed_pass_123');
INSERT INTO Users (role, username, email, password_hash) VALUES ('Organizer', 'event_org1', 'org1@example.com', 'hashed_pass_123');
INSERT INTO Users (role, username, email, password_hash) VALUES ('Organizer', 'event_org2', 'org2@example.com', 'hashed_pass_123');
INSERT INTO Users (role, username, email, password_hash) VALUES ('Attendee', 'john_doe', 'john@example.com', 'hashed_pass_123');
INSERT INTO Users (role, username, email, password_hash) VALUES ('Attendee', 'jane_doe', 'jane@example.com', 'hashed_pass_123');

-- Insert Events
-- Organizer is hardcoded to id=2 or id=3
INSERT INTO Events (title, description, event_date, event_time, venue, capacity, organizer_id, status, image_url) 
VALUES ('Tech Conference 2026', 'A major conference on emerging technologies.', '2026-06-15', '09:00:00', 'Convention Center', 500, 2, 'upcoming', 'https://via.placeholder.com/800x400?text=Tech+Conference');

INSERT INTO Events (title, description, event_date, event_time, venue, capacity, organizer_id, status, image_url) 
VALUES ('Music Fest', 'An outdoor music festival featuring top bands.', '2026-07-20', '18:00:00', 'City Park', 2000, 3, 'upcoming', 'https://via.placeholder.com/800x400?text=Music+Fest');

INSERT INTO Events (title, description, event_date, event_time, venue, capacity, organizer_id, status, image_url) 
VALUES ('Local Coding Bootcamp', 'A 2-day intensive coding workshop.', '2026-05-10', '10:00:00', 'Tech Hub Center', 50, 2, 'upcoming', 'https://via.placeholder.com/800x400?text=Coding+Bootcamp');

-- Note: In a real system, registrations and payments would be handled via the API/Procedures to ensure triggers fire.
-- However, we provide some manual inserts for testing analytics immediately.
-- Assuming event 1 and users 4, 5
INSERT INTO Registrations (user_id, event_id, status) VALUES (4, 1, 'registered');
INSERT INTO Payments (user_id, event_id, amount, status) VALUES (4, 1, 150.00, 'success');

INSERT INTO Registrations (user_id, event_id, status) VALUES (5, 1, 'registered');
INSERT INTO Payments (user_id, event_id, amount, status) VALUES (5, 1, 150.00, 'success');

-- Update the attendees count to match dummy data
UPDATE Events SET current_attendees = 2 WHERE id = 1;

-- Add a notification for user 4
INSERT INTO Notifications (user_id, message, is_read) VALUES (4, 'Welcome to the Event Management System!', FALSE);
