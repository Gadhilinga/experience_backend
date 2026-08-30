from sqlalchemy.orm import Session

from models.saved_destination import SavedDestination


def save_destination(user_id: int, destination_id: str, db: Session):
    saved_destination = db.query(SavedDestination).filter(
        SavedDestination.user_id == user_id,
        SavedDestination.destination_id == destination_id,
    ).first()

    if saved_destination:
        return saved_destination

    saved_destination = SavedDestination(
        user_id=user_id,
        destination_id=destination_id,
    )
    db.add(saved_destination)
    db.commit()
    db.refresh(saved_destination)
    return saved_destination


def get_saved_destinations(user_id: int, db: Session):
    return db.query(SavedDestination).filter(
        SavedDestination.user_id == user_id,
    ).order_by(SavedDestination.id).all()