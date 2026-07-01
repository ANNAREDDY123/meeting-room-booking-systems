from fastapi import (
    APIRouter,
    Depends,
    HTTPException
)

from sqlalchemy.orm import Session

from database import SessionLocal

from models.room import Room

from schemas.room import RoomCreate

router = APIRouter(
    prefix="/rooms",
    tags=["Rooms"]
)


def get_db():

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()


@router.post("/")
def create_room(
    room: RoomCreate,
    db: Session = Depends(get_db)
):

    new_room = Room(
        room_name=room.room_name,
        capacity=room.capacity,
        floor=room.floor,
        amenities=room.amenities,
        is_available=room.is_available
    )

    db.add(new_room)

    db.commit()

    db.refresh(new_room)

    return new_room


@router.get("/")
def get_rooms(
    db: Session = Depends(get_db)
):

    return db.query(Room).all()


@router.get("/{room_id}")
def get_room(
    room_id: int,
    db: Session = Depends(get_db)
):

    room = db.query(Room).filter(
        Room.id == room_id
    ).first()

    if not room:

        raise HTTPException(
            status_code=404,
            detail="Room not found"
        )

    return room


@router.put("/{room_id}")
def update_room(
    room_id: int,
    room: RoomCreate,
    db: Session = Depends(get_db)
):

    db_room = db.query(Room).filter(
        Room.id == room_id
    ).first()

    if not db_room:

        raise HTTPException(
            status_code=404,
            detail="Room not found"
        )

    db_room.room_name = room.room_name
    db_room.capacity = room.capacity
    db_room.floor = room.floor
    db_room.amenities = room.amenities
    db_room.is_available = room.is_available

    db.commit()

    return {
        "message": "Room updated"
    }


@router.delete("/{room_id}")
def delete_room(
    room_id: int,
    db: Session = Depends(get_db)
):

    room = db.query(Room).filter(
        Room.id == room_id
    ).first()

    if not room:

        raise HTTPException(
            status_code=404,
            detail="Room not found"
        )

    room.is_available = False

    db.commit()

    return {
        "message": "Room deactivated"
    }
