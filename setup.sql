CREATE DATABASE hotel_booking;
USE hotel_booking;
CREATE TABLE rooms (
id INT AUTO_INCREMENT PRIMARY KEY ,
room_number V ARCHAR(10),
room_type V ARCHAR(50),
price_per_night DECIMAL(10, 2),
availability BOOLEAN DEFAULT TRUE
);
CREATE TABLE bookings (
id INT AUTO_INCREMENT PRIMARY KEY ,
customer_name V ARCHAR(100),
room_id INT,
check_in DA TE,
check_out DA TE,
FOREIGN KEY (room_id) REFERENCES rooms(id)
);
INSERT INTO rooms (room_number, room_type, price_per_night, availability)
VALUES
('101', 'Single', 50.00, TRUE),
('102', 'Double', 80.00, TRUE),
('201', 'Suite', 150.00, TRUE);
