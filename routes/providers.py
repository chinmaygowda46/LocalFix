from fastapi import APIRouter
from database import providers_collection
from pydantic import BaseModel

router = APIRouter(
    prefix="/providers",
    tags=["Providers"]
)


class Provider(BaseModel):
    name: str
    phone: str
    service: str
    experience: int
    location: str
    price: float


@router.post("/")
def create_provider(provider: Provider):
    provider_data = provider.model_dump()

    result = providers_collection.insert_one(provider_data)

    return {
        "message": "Provider created successfully",
        "provider_id": str(result.inserted_id)
    }


@router.get("/")
def get_providers():
    providers = list(providers_collection.find())

    for provider in providers:
        provider["_id"] = str(provider["_id"])

    return providers