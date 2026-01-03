from sqlalchemy import Column, Integer, Enum, Float, String, DateTime, func
from ..database import Base
from sqlalchemy.orm import relationship
from cuid2 import Cuid
import enum

cuid = Cuid()


# Enum for match status
class MatchStatus(enum.Enum):
    WAITING = "Waiting"
    IN_GAME = "In-Game"
    COMPLETED = "Completed"
    CANCELLED = "Cancelled"



class Match(Base):
    __tablename__ = "matches"

    id = Column(Integer, primary_key=True, index=True)
    room_id = Column(String(20), unique=True, nullable=False)  
    room_name = Column(String(100), nullable=False)
    game_type = Column(String(20), nullable=False) 
    entry_fee = Column(Float, nullable=False, default=10.0)
    prize_pool = Column(Float, default=0.0)
    max_players = Column(Integer, default=10)
    current_players = Column(Integer, default=0)
    status = Column(Enum(MatchStatus), default=MatchStatus.WAITING)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    started_at = Column(DateTime(timezone=True), nullable=True)
    ended_at = Column(DateTime(timezone=True), nullable=True)
    
    
    participants = relationship("MatchParticipant", back_populates="match")