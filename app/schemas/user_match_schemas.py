from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class MatchOut(BaseModel):
    id: int
    room_id: str
    room_name: str
    game_type: str
    entry_fee: float
    prize_pool: float
    current_players: int
    max_players: int
    status: str
    created_at: datetime

    class Config:
        from_attributes = True

class MatchHistoryOut(MatchOut):
    position: Optional[int] = None
    earnings: Optional[float] = None