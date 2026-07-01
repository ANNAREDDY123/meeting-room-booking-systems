CREATE TABLE users(
    id INTEGER PRIMARY KEY,
    username VARCHAR(100),
    email VARCHAR(100) UNIQUE,
    password VARCHAR(255),
    role VARCHAR(50)
);

CREATE TABLE rooms(
    id INTEGER PRIMARY KEY,
    room_name VARCHAR(100),
    capacity INTEGER,
    floor VARCHAR(50),
    amenities TEXT,
    is_available BOOLEAN
);

CREATE TABLE bookings(
    id INTEGER PRIMARY KEY,
    room_id INTEGER,
    employee_id INTEGER,
    meeting_title VARCHAR(255),
    booking_date DATE,
    start_time TIME,
    end_time TIME,
    status VARCHAR(50)
);
