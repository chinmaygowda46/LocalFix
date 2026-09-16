from fastapi import APIRouter, HTTPException, Depends
from database import bookings_collection, providers_collection
from pydantic import BaseModel
from bson import ObjectId
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
import os
from dotenv import load_dotenv

load_dotenv()

router = APIRouter(prefix="/bookings", tags=["Bookings"])

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"

security = HTTPBearer()


class Booking(BaseModel):
    user_id: str
    provider_id: str
    service: str
    date: str
    time: str
    address: str
    description: str


class BookingStatus(BaseModel):
    status: str


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    token = credentials.credentials

    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        return payload

    except JWTError:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token"
        )


# =========================================
# CREATE BOOKING
# =========================================

@router.post("/")
def create_booking(
    booking: Booking,
    current_user=Depends(get_current_user)
):

    booking_data = booking.model_dump()

    booking_data["user_id"] = current_user["user_id"]
    booking_data["status"] = "Pending"

    result = bookings_collection.insert_one(
        booking_data
    )

    return {
        "message": "Booking created successfully",
        "booking_id": str(result.inserted_id)
    }


# =========================================
# GET MY BOOKINGS
# =========================================

@router.get("/")
def get_my_bookings(
    current_user=Depends(get_current_user)
):

    bookings = list(
        bookings_collection.find(
            {
                "user_id": current_user["user_id"]
            }
        )
    )

    for booking in bookings:

        booking["_id"] = str(
            booking["_id"]
        )

        # Get provider details
        provider = providers_collection.find_one(
            {
                "_id": ObjectId(
                    booking["provider_id"]
                )
            }
        )

        if provider:

            booking["provider"] = {
                "name": provider.get("name"),
                "phone": provider.get("phone"),
                "location": provider.get("location"),
                "experience": provider.get("experience"),
                "price": provider.get("price")
            }

        else:

            booking["provider"] = None

    return bookings


# =========================================
# UPDATE BOOKING STATUS
# =========================================

@router.put("/{booking_id}/status")
def update_booking_status(
    booking_id: str,
    booking_status: BookingStatus,
    current_user=Depends(get_current_user)
):

    allowed_statuses = [
        "Pending",
        "Confirmed",
        "Completed",
        "Cancelled"
    ]

    if booking_status.status not in allowed_statuses:

        raise HTTPException(
            status_code=400,
            detail=f"Invalid status. Use one of: {allowed_statuses}"
        )

    try:

        object_id = ObjectId(
            booking_id
        )

    except Exception:

        raise HTTPException(
            status_code=400,
            detail="Invalid booking ID"
        )

    result = bookings_collection.update_one(

        {
            "_id": object_id,
            "user_id": current_user["user_id"]
        },

        {
            "$set": {
                "status": booking_status.status
            }
        }

    )

    if result.matched_count == 0:

        raise HTTPException(
            status_code=404,
            detail="Booking not found"
        )

    return {

        "message":
            "Booking status updated successfully",

        "status":
            booking_status.status

    }


# =========================================
# CANCEL BOOKING
# =========================================

@router.delete("/{booking_id}")
def cancel_booking(
    booking_id: str,
    current_user=Depends(get_current_user)
):

    try:

        object_id = ObjectId(
            booking_id
        )

    except Exception:

        raise HTTPException(
            status_code=400,
            detail="Invalid booking ID"
        )

    booking = bookings_collection.find_one(

        {
            "_id": object_id,
            "user_id": current_user["user_id"]
        }

    )

    if not booking:

        raise HTTPException(
            status_code=404,
            detail="Booking not found"
        )

    if booking.get("status") == "Completed":

        raise HTTPException(
            status_code=400,
            detail="Completed bookings cannot be cancelled"
        )

    if booking.get("status") == "Cancelled":

        raise HTTPException(
            status_code=400,
            detail="Booking is already cancelled"
        )

    result = bookings_collection.update_one(

        {
            "_id": object_id,
            "user_id": current_user["user_id"]
        },

        {
            "$set": {
                "status": "Cancelled"
            }
        }

    )

    if result.modified_count == 0:

        raise HTTPException(
            status_code=400,
            detail="Could not cancel booking"
        )

    return {

        "message":
            "Booking cancelled successfully",

        "booking_id":
            booking_id,

        "status":
            "Cancelled"

    }