from fastapi import APIRouter, HTTPException, Depends
from database import reviews_collection
from pydantic import BaseModel
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
import os
from dotenv import load_dotenv

load_dotenv()

router = APIRouter(
    prefix="/reviews",
    tags=["Reviews"]
)

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"

security = HTTPBearer()


class Review(BaseModel):
    user_id: str
    provider_id: str
    rating: int
    comment: str


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
# CREATE REVIEW
# =========================================

@router.post("/")
def create_review(
    review: Review,
    current_user=Depends(get_current_user)
):

    # Check rating
    if review.rating < 1 or review.rating > 5:
        raise HTTPException(
            status_code=400,
            detail="Rating must be between 1 and 5"
        )


    # Check if user already reviewed provider
    existing_review = reviews_collection.find_one(
        {
            "user_id": current_user["user_id"],
            "provider_id": review.provider_id
        }
    )


    if existing_review:
        raise HTTPException(
            status_code=400,
            detail="You have already reviewed this provider"
        )


    # Create review
    review_data = review.model_dump()

    # Use logged-in user's ID
    review_data["user_id"] = current_user["user_id"]


    result = reviews_collection.insert_one(
        review_data
    )


    return {
        "message": "Review created successfully",
        "review_id": str(result.inserted_id)
    }


# =========================================
# GET PROVIDER REVIEWS
# =========================================

@router.get("/{provider_id}")
def get_provider_reviews(
    provider_id: str
):

    reviews = list(
        reviews_collection.find(
            {
                "provider_id": provider_id
            }
        )
    )


    for review in reviews:
        review["_id"] = str(review["_id"])


    return reviews