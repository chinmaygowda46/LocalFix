from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import client
from routes.services import router as services_router
from routes.providers import router as providers_router
from routes.users import router as users_router
from routes.bookings import router as bookings_router
from routes.reviews import router as reviews_router

app = FastAPI(
    title="LocalFix API",
    description="Local Service Booking Platform",
    version="1.0.0"
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(services_router)
app.include_router(providers_router)
app.include_router(users_router)
app.include_router(bookings_router)
app.include_router(reviews_router)

@app.get("/")
def home():
    return {
        "message": "Welcome to LocalFix API",
        "status": "running"
    }


@app.get("/health")
def health():
    try:
        client.admin.command("ping")

        return {
            "status": "healthy",
            "database": "connected"
        }

    except Exception as e:
        return {
            "status": "unhealthy",
            "database": "disconnected",
            "error": str(e)
        }