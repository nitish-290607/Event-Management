from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import random
from typing import List

from .. import models, schemas
from ..database import get_db
from ..utils.auth import get_current_user

router = APIRouter()

@router.post("/{event_id}", response_model=schemas.RegistrationResponse)
def register_for_event(
    event_id: int, 
    db: Session = Depends(get_db), 
    current_user: models.User = Depends(get_current_user)
):
    # Retrieve the event
    event = db.query(models.Event).with_for_update().filter(models.Event.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
        
    # Check if already registered
    existing_reg = db.query(models.Registration).filter(
        models.Registration.user_id == current_user.id,
        models.Registration.event_id == event_id,
        models.Registration.status == "registered"
    ).first()
    
    if existing_reg:
        raise HTTPException(status_code=400, detail="Already registered for this event")
        
    if event.current_attendees >= event.capacity:
        raise HTTPException(status_code=400, detail="Event is full")
        
    # Simulate Payment Processing (10% chance to fail)
    payment_status = "success"
    if random.random() < 0.1:
        payment_status = "failed"
        
    payment = models.Payment(
        user_id=current_user.id,
        event_id=event_id,
        amount=event.ticket_price,
        status=payment_status
    )
    db.add(payment)
    
    if payment_status == "failed":
        db.commit() # Save failed payment
        raise HTTPException(status_code=402, detail="Payment processing failed, please try again")

    # Proceed with transaction
    new_reg = models.Registration(user_id=current_user.id, event_id=event_id)
    db.add(new_reg)
    
    # Simulating trigger: UPDATE Events SET current_attendees = current_attendees + 1
    event.current_attendees += 1
    
    # Notification
    notif = models.Notification(user_id=current_user.id, message=f"Successfully registered for event: {event.title}")
    db.add(notif)
    
    db.commit()
    db.refresh(new_reg)
    return new_reg

@router.get("/my-registrations", response_model=List[schemas.RegistrationResponse])
def get_user_registrations(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    return db.query(models.Registration).filter(models.Registration.user_id == current_user.id).all()

@router.delete("/{event_id}")
def cancel_registration(event_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    reg = db.query(models.Registration).filter(
        models.Registration.user_id == current_user.id,
        models.Registration.event_id == event_id,
        models.Registration.status == "registered"
    ).first()
    
    if not reg:
        raise HTTPException(status_code=404, detail="Registration not found")
        
    reg.status = "cancelled"
    
    # Update event attendees
    event = db.query(models.Event).filter(models.Event.id == event_id).first()
    if event:
        event.current_attendees -= 1
        
    notif = models.Notification(user_id=current_user.id, message=f"Registration for {event.title} has been cancelled.")
    db.add(notif)
    
    db.commit()
    return {"detail": "Registration cancelled successfully"}
