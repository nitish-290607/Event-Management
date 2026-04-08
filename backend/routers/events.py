from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from sqlalchemy import or_

from .. import models, schemas
from ..database import get_db
from ..utils.auth import get_current_user

router = APIRouter()

class VenueResponse(schemas.BaseModel):
    id: int
    name: str
    location: str
    capacity: int
    class Config:
        from_attributes = True

@router.get("/venues", response_model=List[VenueResponse])
def get_venues(db: Session = Depends(get_db)):
    return db.query(models.Venue).all()

@router.post("/venues", response_model=VenueResponse)
def create_venue(name: str, location: str, capacity: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    if current_user.role not in ["Admin", "Organizer"]:
        raise HTTPException(status_code=403, detail="Not authorized to create venues")
    venue = models.Venue(name=name, location=location, capacity=capacity)
    db.add(venue)
    db.commit()
    db.refresh(venue)
    return venue

@router.get("/", response_model=List[schemas.EventResponse])
def get_events(
    skip: int = 0, limit: int = 10, search: Optional[str] = None, db: Session = Depends(get_db)
):
    query = db.query(models.Event)
    if search:
        query = query.filter(
            or_(
                models.Event.title.ilike(f"%{search}%"),
                models.Event.venue.ilike(f"%{search}%")
            )
        )
    return query.offset(skip).limit(limit).all()

@router.post("/", response_model=schemas.EventResponse)
def create_event(
    event: schemas.EventCreate, 
    db: Session = Depends(get_db), 
    current_user: models.User = Depends(get_current_user)
):
    if current_user.role not in ["Admin", "Organizer"]:
        raise HTTPException(status_code=403, detail="Not authorized to create events")
        
    new_event = models.Event(**event.dict(), organizer_id=current_user.id)
    db.add(new_event)
    db.commit()
    db.refresh(new_event)
    return new_event

@router.put("/{event_id}", response_model=schemas.EventResponse)
def update_event(
    event_id: int, 
    event_update: schemas.EventCreate,
    db: Session = Depends(get_db), 
    current_user: models.User = Depends(get_current_user)
):
    event = db.query(models.Event).filter(models.Event.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
        
    if event.organizer_id != current_user.id and current_user.role != "Admin":
        raise HTTPException(status_code=403, detail="Not authorized to update this event")
        
    # Check if we should notify (Simulating the Trigger in Python for DB portability)
    send_notification = False
    if event.venue != event_update.venue or event.event_date != event_update.event_date:
        send_notification = True

    for key, value in event_update.dict().items():
        setattr(event, key, value)
        
    db.commit()
    db.refresh(event)
    
    if send_notification:
        registrations = db.query(models.Registration).filter(models.Registration.event_id == event.id, models.Registration.status == "registered").all()
        for reg in registrations:
            notif = models.Notification(
                user_id=reg.user_id, 
                message=f"The event {event.title} has been updated. New Date: {event.event_date}, Venue: {event.venue}"
            )
            db.add(notif)
        db.commit()
        
    return event

@router.get("/analytics")
def get_analytics(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    if current_user.role != "Admin":
        raise HTTPException(status_code=403, detail="Not authorized")
        
    from sqlalchemy import func
    total_events = db.query(models.Event).count()
    total_users = db.query(models.User).count()
    total_revenue = db.query(func.sum(models.Payment.amount)).filter(models.Payment.status == "success").scalar() or 0.0
    
    return {
        "total_events": total_events,
        "total_users": total_users,
        "total_revenue": total_revenue
    }

@router.get("/{event_id}/registrations", response_model=List[schemas.UserResponse])
def get_event_registrations(event_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    if current_user.role not in ["Admin", "Organizer"]:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    event = db.query(models.Event).filter(models.Event.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
        
    regs = db.query(models.Registration).filter(models.Registration.event_id == event_id, models.Registration.status == "registered").all()
    users = [reg.user for reg in regs]
    return users

@router.delete("/{event_id}")
def delete_event(
    event_id: int, 
    db: Session = Depends(get_db), 
    current_user: models.User = Depends(get_current_user)
):
    event = db.query(models.Event).filter(models.Event.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
        
    if event.organizer_id != current_user.id and current_user.role != "Admin":
        raise HTTPException(status_code=403, detail="Not authorized to delete this event")
        
    db.delete(event)
    db.commit()
    return {"detail": "Event deleted successfully"}
