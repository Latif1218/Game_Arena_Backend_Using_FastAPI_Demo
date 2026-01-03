from sqlalchemy.orm import Session
from ..models import user_wallet_models, user_transaction_models
from ..schemas import user_transaction_schemas


def get_user_wallet(db:Session, user_id: int):
    return db.query(user_wallet_models.Wallet).filter(
        user_wallet_models.Wallet.user_id == user_id
    ).first()
    
    
def add_balance_trx(db: Session, user_id: int, amount: float):
    wallet = get_user_wallet(db, user_id)
    if wallet:
        wallet.balance_trx += amount
        db.commit()


def deduct_balance_trx(db: Session, user_id: int, amount: float):
    wallet = get_user_wallet(db, user_id)
    if wallet and wallet.balance_trx >= amount:
        wallet.balance_trx -= amount
        db.commit()
        return True
    return False


def get_user_transactions(db: Session, user_id: int):
    return db.query(user_transaction_models.Transaction).filter(
        user_transaction_models.Transaction.user_id == user_id
    ).order_by(
        user_transaction_models.Transaction.timestamp.desc()
    ).all()
    
    
def create_transaction(
    db: Session,
        user_id: int,
        amount: float,
        type: user_transaction_models.TransactionType,
        status: user_transaction_models.TransactionStatus,
        transaction_id: str,
        description: str = None
):
    tx = user_transaction_models.Transaction(
        user_id=user_id,
        amount=amount,
        type=type,       
        status=status,   
        transaction_id=transaction_id,
        description=description
    )
    db.add(tx)
    db.commit()
    db.refresh(tx)
    return tx


def get_pending_withdrawals(db: Session):
    return db.query(user_transaction_models.Transaction).filter(
        user_transaction_models.Transaction.type == user_transaction_models.TransactionType.WITHDRAW, 
        user_transaction_models.Transaction.status == user_transaction_models.TransactionStatus.PENDING
    ).all()



def approve_withdrawal(db: Session, transaction_id: str):
    tx = db.query(user_transaction_models.Transaction).filter(
        user_transaction_models.Transaction.transaction_id == transaction_id
    ).first()
    if tx:
        tx.status = user_transaction_models.TransactionStatus.COMPLETED
        db.commit()