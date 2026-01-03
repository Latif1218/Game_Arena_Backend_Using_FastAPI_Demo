from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from ..models import user_models, user_match_models
from ..schemas import user_match_schemas
from ..database import get_db
from ..Authentication import user_auth
from typing import List
from ..Match_helper import match_helper


router = APIRouter(
    prefix="/matches", 
    tags=["Matches"]
)



@router.get("/live", status_code=status.HTTP_200_OK, response_model=List[user_match_schemas.MatchOut])
def get_live_matches(db: Session = Depends(get_db)):
    return match_helper.get_live_matches(db)

@router.get("/my-ongoing", status_code=status.HTTP_200_OK, response_model=List[user_match_schemas.MatchOut])
def get_my_ongoing(current_user: user_models.User = Depends(user_auth.get_current_user), db: Session = Depends(get_db)):
    return match_helper.get_user_ongoing_matches(db, current_user.id)

@router.get("/history", status_code=status.HTTP_200_OK, response_model=List[user_match_schemas.MatchHistoryOut])
def get_match_history(current_user: user_models.User = Depends(user_auth.get_current_user), db: Session = Depends(get_db)):
    return match_helper.get_user_match_history(db, current_user.id)

@router.post("/{match_id}/join", status_code=status.HTTP_200_OK,)
def join_match(match_id: int, current_user: user_models.User = Depends(user_auth.get_current_user), db: Session = Depends(get_db)):
    match_helper.join_match(db, match_id, current_user.id)
    return {"message": "Joined match successfully"}