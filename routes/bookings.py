from fastapi import (
    APIRouter,
    Depends,
    HTTPException
)

from sqlalchemy.orm import Session

from database import SessionLocal

from models.booking import Booking
from models.room import Room
from models.user import User

from schemas.booking import BookingCreate

from services.booking_service import valid_booking

router = APIRouter(
    prefix="/bookings",
    tags=["Bookings"]
)


def get_db():

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()


@router.post("/")
def create_booking(
    booking: BookingCreate,
    db: Session = Depends(get_db)
):

    room = db.query(Room).filter(
        Room.id == booking.room_id
    ).first()

    if not room:

        raise HTTPException(
            status_code=404,
            detail="Room not found"
        )

    if not room.is_available:

        raise HTTPException(
            status_code=400,
            detail="Room unavailable"
        )

    employee = db.query(User).filter(
        User.id == booking.employee_id
    ).first()

    if not employee:

        raise HTTPException(
            status_code=404,
            detail="Employee not found"
        )

    if not valid_booking(
        booking.start_time,
        booking.end_time
    ):

        raise HTTPException(
            status_code=400,
            detail="Invalid booking time"
        )

    overlap = db.query(Booking).filter(
        Booking.room_id == booking.room_id,
        Booking.booking_date == booking.booking_date,
        Booking.status == "Scheduled"
    ).all()

    for item in overlap:

        if (
            booking.start_time < item.end_time
            and booking.end_time > item.start_time
        ):

            raise HTTPException(
                status_code=400,
                detail="Room already booked for this time"
            )

    new_booking = Booking(
        room_id=booking.room_id,
        employee_id=booking.employee_id,
        meeting_title=booking.meeting_title,
        booking_date=booking.booking_date,
        start_time=booking.start_time,
        end_time=booking.end_time,
        status="Scheduled"
    )

    db.add(new_booking)

    db.commit()

    db.refresh(new_booking)

    return new_booking


@router.get("/")
def get_bookings(
    booking_date: str = None,
    room_id: int = None,
    meeting_title: str = None,
    page: int = 1,
    limit: int = 10,
    db: Session = Depends(get_db)
):

    query = db.query(Booking)

    if booking_date:
        query = query.filter(
            Booking.booking_date == booking_date
        )

    if room_id:
        query = query.filter(
            Booking.room_id == room_id
        )

    if meeting_title:
        query = query.filter(
            Booking.meeting_title.contains(meeting_title)
        )

    total = query.count()

    bookings = query.offset(
        (page - 1) * limit
    ).limit(limit).all()

    return {
        "total_records": total,
        "current_page": page,
        "limit": limit,
        "data": bookings
    }


@router.get("/{booking_id}")
def get_booking(
    booking_id: int,
    db: Session = Depends(get_db)
):

    booking = db.query(Booking).filter(
        Booking.id == booking_id
    ).first()

    if not booking:

        raise HTTPException(
            status_code=404,
            detail="Booking not found"
        )

    return booking


@router.put("/{booking_id}")
def update_booking(
    booking_id: int,
    booking: BookingCreate,
    db: Session = Depends(get_db)
):

    db_booking = db.query(Booking).filter(
        Booking.id == booking_id
    ).first()

    if not db_booking:

        raise HTTPException(
            status_code=404,
            detail="Booking not found"
        )

    if not valid_booking(
        booking.start_time,
        booking.end_time
    ):

        raise HTTPException(
            status_code=400,
            detail="Invalid booking time"
        )

    db_booking.room_id = booking.room_id
    db_booking.employee_id = booking.employee_id
    db_booking.meeting_title = booking.meeting_title
    db_booking.booking_date = booking.booking_date
    db_booking.start_time = booking.start_time
    db_booking.end_time = booking.end_time

    db.commit()

    return {
        "message": "Booking updated"
    }


@router.delete("/{booking_id}")
def cancel_booking(
    booking_id: int,
    db: Session = Depends(get_db)
):

    booking = db.query(Booking).filter(
        Booking.id == booking_id
    ).first()

    if not booking:

        raise HTTPException(
            status_code=404,
            detail="Booking not found"
        )

    booking.status = "Cancelled"

    db.commit()

    return {
        "message": "Booking cancelled"
    }
