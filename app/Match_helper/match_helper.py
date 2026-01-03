from sqlalchemy.orm import Session
from ..models import user_participant_model, user_match_models, user_transaction_models
import uuid
from ..Wallet_helper import wallet_helper

def get_live_matches(db: Session):
    return db.query(user_match_models.Match).filter(
        user_match_models.Match.status.in_([
            user_match_models.MatchStatus.WAITING,
            user_match_models.MatchStatus.IN_GAME
        ])
    ).all()

def get_user_ongoing_matches(db: Session, user_id: int):
    return (
        db.query(user_match_models.Match)
        .join(user_participant_model.MatchParticipant)
        .filter(user_participant_model.MatchParticipant.user_id == user_id)
        .filter(user_match_models.Match.status.in_([
            user_match_models.MatchStatus.WAITING,
            user_match_models.MatchStatus.IN_GAME
        ])).all()
    )

def get_user_match_history(db: Session, user_id: int):
    return (
        db.query(user_match_models.Match)
        .join(user_participant_model.MatchParticipant)
        .filter(user_participant_model.MatchParticipant.user_id == user_id)
        .filter(user_match_models.Match.status == "Completed")
        .order_by(user_match_models.Match.ended_at.desc())
        .all()
    )

def join_match(db: Session, match_id: int, user_id: int):
    match = db.query(user_match_models.Match).filter(user_match_models.Match.id == match_id).first()
    if not match or match.status != user_match_models.MatchStatus.WAITING:
        raise ValueError("Match not available")
    
    
    if not wallet_helper.deduct_balance_trx(db, user_id, match.entry_fee):
        raise ValueError("Insufficient balance")
    
   
    participant = user_participant_model.MatchParticipant(match_id=match_id, user_id=user_id)
    db.add(participant)
    
    match.current_players += 1
    match.prize_pool += match.entry_fee  
    
    
    wallet_helper.create_transaction(
        db,
        user_id,
        -match.entry_fee,
        user_transaction_models.TransactionType.ENTRY_FEE,
        user_transaction_models.TransactionStatus.COMPLETED,
        "ENTRY_" + str(uuid.uuid4())[:8]
    )
    
    db.commit()