from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import date, time, datetime

# User Schemas
class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    role: str = "Attendee"

class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    role: str
    created_at: datetime
    
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

# Event Schemas
class EventBase(BaseModel):
    title: str
    description: Optional[str] = None
    event_date: date
    event_time: time
    venue_id: int
    capacity: int
    ticket_price: float = 100.0
    status: str = "upcoming"
    image_url: Optional[str] = None

class EventCreate(EventBase):
    pass

class EventResponse(EventBase):
    id: int
    current_attendees: int
    ticket_price: float
    organizer_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

# Registration Schemas
class RegistrationResponse(BaseModel):
    id: int
    user_id: int
    event_id: int
    status: str
    created_at: datetime
    event: Optional[EventResponse] = None

    class Config:
        from_attributes = True

# Notification
class NotificationResponse(BaseModel):
    id: int
    message: str
    is_read: bool

    class Config:
        from_attributes = True
