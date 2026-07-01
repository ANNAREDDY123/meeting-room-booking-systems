from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database import Base, engine

from models.user import User
from models.room import Room
from models.booking import Booking

from routes.auth import router as auth_router
from routes.rooms import router as rooms_router
from routes.bookings import router as bookings_router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Meeting Room Booking System"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(auth_router)
app.include_router(rooms_router)
app.include_router(bookings_router)


@app.get("/")
def home():

    return {
        "message":
        "Meeting Room Booking System"
    }
