from pydantic import BaseModel
from datetime import date, time


class BookingCreate(BaseModel):

    room_id: int

    employee_id: int

    meeting_title: str

    booking_date: date

    start_time: time

    end_time: time
