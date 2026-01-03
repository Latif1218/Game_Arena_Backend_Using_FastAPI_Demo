from sqlalchemy import Column, Integer, Enum, ForeignKey, Float, String, Text, DateTime, func
from ..database import Base
from sqlalchemy.orm import relationship
from cuid2 import Cuid
import datetime
import enum

cuid = Cuid()



# Enum for transaction types
class TransactionType(enum.Enum):
    DEPOSIT = "Deposit"
    WITHDRAW = "Withdraw"
    ENTRY_FEE = "EntryFee"
    PRIZE = "Prize"
    REFUND = "Refund"
    
    
# Enum for transaction status
class TransactionStatus(enum.Enum):
    PENDING = "Pending"
    COMPLETED = "Completed"
    FAILED = "Failed"
    REJECTED = "Rejected"


class Transaction(Base):
    __tablename__="transactions"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"))
    amount = Column(Float, nullable=False)
    type = Column(Enum(TransactionType, name="transactiontype"), nullable=False)
    status = Column(Enum(TransactionStatus), default=TransactionStatus.PENDING)
    transaction_id = Column(String(50), unique=True, nullable=False)
    description = Column(Text)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    
    
    user = relationship("User", back_populates="transactions")