import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import engine, Base
from .routers import users, events, registrations

# Create DB Tables if they don't exist (useful for SQLite demo, for real deploy use migration tool like Alembic)
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Event Management System API",
    description="A full-stack Event Management System focusing on DBMS principles.",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # For development only
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
app.include_router(users.router, prefix="/api/users", tags=["Users"])
app.include_router(events.router, prefix="/api/events", tags=["Events"])
app.include_router(registrations.router, prefix="/api/registrations", tags=["Registrations"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the Event Management System. Visit /docs for the API Swagger UI."}

if __name__ == "__main__":
    uvicorn.run("backend.main:app", host="127.0.0.1", port=8000, reload=True)
