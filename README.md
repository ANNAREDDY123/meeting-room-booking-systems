# meeting-room-booking-systems
FastAPI Meeting Room Booking System with JWT Authentication, Room Management, Booking Management, Reports, Search, SQLAlchemy ORM, Pagination, and Docker Support.
# Meeting Room Booking System

## Features

- JWT Authentication
- Meeting Room Management
- Booking Management
- Search & Filtering
- Pagination
- Booking Conflict Validation
- SQLAlchemy ORM
- SQLite Database
- Docker Support

## Setup Instructions

1. Install dependencies
pip install -r requirements.txt

2. Run the application
uvicorn main:app --reload

## Environment Variables

SECRET_KEY=meeting_secret_key
ALGORITHM=HS256

## Authentication Flow

- Register using `/auth/register`
- Login using `/auth/login`
- JWT token is returned after successful login.

## API Flow Overview

1. Register/Login
2. Create Rooms
3. Create Bookings
4. View Bookings
5. Update Bookings
6. Cancel Bookings

## Assumptions Made

- One room can have multiple bookings.
- Overlapping bookings are not allowed.
- Rooms use soft delete by setting `is_available` to `False`.
- Booking status supports Scheduled, Completed, and Cancelled.
