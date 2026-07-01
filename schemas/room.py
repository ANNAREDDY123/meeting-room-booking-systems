from pydantic import BaseModel


class RoomCreate(BaseModel):

    room_name: str

    capacity: int

    floor: str

    amenities: str

    is_available: bool = True
