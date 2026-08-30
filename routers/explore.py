from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from core.database import get_db
from core.security import get_current_user
from schemas.saved_destination import (
    SavedDestinationRequest,
    SavedDestinationResponse,
)
from services.saved_destination_service import (
    get_saved_destinations,
    save_destination,
)


router = APIRouter(
    prefix="/yatrivo/api/v1",
    tags=["Explore"],
)


def get_user_id(current_user: dict) -> int:
    return int(current_user["sub"])


@router.post("/saved", response_model=SavedDestinationResponse)
def save_destination_for_user(
    payload: SavedDestinationRequest,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return save_destination(get_user_id(current_user), payload.destination_id, db)


@router.get("/saved", response_model=list[SavedDestinationResponse])
def list_saved_destinations(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return get_saved_destinations(get_user_id(current_user), db)