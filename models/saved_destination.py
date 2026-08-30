from sqlalchemy import Column, ForeignKey, Integer, String, UniqueConstraint

from core.database import Base


class SavedDestination(Base):
    __tablename__ = "saved_destinations"
    __table_args__ = (
        UniqueConstraint("user_id", "destination_id", name="uq_saved_destination_user_destination"),
    )

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    destination_id = Column(String, nullable=False)