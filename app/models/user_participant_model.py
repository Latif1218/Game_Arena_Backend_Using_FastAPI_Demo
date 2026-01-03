from sqlalchemy import Column, Integer, ForeignKey, Float, UniqueConstraint, DateTime, func
from ..database import Base
from sqlalchemy.orm import relationship
from cuid2 import Cuid


cuid = Cuid()

class MatchParticipant(Base):
    __tablename__ = "match_participants"
    __table_args__ = (UniqueConstraint('match_id', 'user_id', name='unique_user_per_match'),)

    id = Column(Integer, primary_key=True, index=True)
    match_id = Column(Integer, ForeignKey("matches.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    joined_at = Column(DateTime(timezone=True), server_default=func.now())
    position = Column(Integer, nullable=True) 
    earnings = Column(Float, default=0.0)  
    
    
    match = relationship("Match", back_populates="participants")
    user = relationship("User", back_populates="match_participants")