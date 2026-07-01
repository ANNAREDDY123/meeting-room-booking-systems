from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean
)

from database import Base


class Room(Base):
    __tablename__ = "rooms"

    id = Column(
        Integer,
        primary_key=True
    )

    room_name = Column(String)

    capacity = Column(Integer)

    floor = Column(String)

    amenities = Column(String)

    is_available = Column(
        Boolean,
        default=True
    )
