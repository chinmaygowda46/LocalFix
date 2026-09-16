from fastapi import APIRouter
from database import services_collection
from pydantic import BaseModel

router = APIRouter(
    prefix="/services",
    tags=["Services"]
)


class Service(BaseModel):
    name: str
    description: str
    price: float
    category: str


@router.post("/")
def create_service(service: Service):
    service_data = service.model_dump()

    result = services_collection.insert_one(service_data)

    return {
        "message": "Service created successfully",
        "service_id": str(result.inserted_id)
    }


@router.get("/")
def get_services():
    services = list(services_collection.find())

    for service in services:
        service["_id"] = str(service["_id"])

    return services