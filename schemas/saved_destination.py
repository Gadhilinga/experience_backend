from pydantic import BaseModel, Field


class SavedDestinationRequest(BaseModel):
    destination_id: str = Field(min_length=1)


class SavedDestinationResponse(BaseModel):
    destination_id: str