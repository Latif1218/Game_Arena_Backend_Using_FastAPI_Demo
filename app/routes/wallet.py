from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
from typing import List
from ..models import user_models, user_transaction_models
from ..schemas import user_wallet_schemas, user_transaction_schemas
from ..Authentication import user_auth
from ..Wallet_helper import wallet_helper
from ..database import get_db
import uuid

router = APIRouter(
    prefix="/wallet",
    tags=["Wallet"]
)

@router.get("/me", status_code=status.HTTP_200_OK, response_model=user_wallet_schemas.WalletOut)
def get_wallet(
    user: user_models.User = Depends(user_auth.get_current_user),
    db: Session = Depends(get_db)
):
    wallet = wallet_helper.get_user_wallet(db, user.id)
    if not wallet:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail= "Walet not found"
        )
    return wallet


@router.get("/transactions", status_code=status.HTTP_200_OK, response_model=List[user_transaction_schemas.TransactionOut])
def get_transactions(
    user: user_models.User = Depends(user_auth.get_current_user),
    db: Session = Depends(get_db)
):
    return wallet_helper.get_user_transactions(db, user.id)


@router.post("/deposit", status_code=status.HTTP_200_OK)
def deposit(
    amount: float, 
    user: user_models.User = Depends(user_auth.get_current_user),
    db: Session = Depends(get_db)
):
    wallet_helper.add_balance_trx(db, user.id, amount)
    tx_id = "DEP_" + str(uuid.uuid4())[:8]
    wallet_helper.create_transaction(
        db,
        user.id,
        amount,
        user_transaction_models.TransactionType.DEPOSIT,
        user_transaction_models.TransactionStatus.COMPLETED,
        tx_id
    )
    return {"message": f"Deposited {amount} TRX"}
    
    
@router.post("/withdraw", status_code=status.HTTP_200_OK)
def withdeaw(
    amount: float, 
    user: user_models.User = Depends(user_auth.get_current_user),
    db: Session = Depends(get_db)
):
    wallet = wallet_helper.get_user_wallet(db, user.id)
    if not wallet:
        raise HTTPException(
            status_code=404,
            detail="Wallet not found"
        )

    if wallet.balance_trx < amount:
        raise HTTPException(
            status_code=400,
            detail="Insufficient balance"
        )
        
    tx_id = "WD_" + str(uuid.uuid4())[:8]
    wallet_helper.create_transaction(
        db,
        user.id,
        -amount,
        user_transaction_models.TransactionType.WITHDRAW,
        user_transaction_models.TransactionStatus.PENDING,
        tx_id
    )
    return {
        "message": "Withdraw request submitted"
    }