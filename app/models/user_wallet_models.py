from sqlalchemy import Column, Integer, String, ForeignKey, Float, DateTime, func
from ..database import Base
from sqlalchemy.orm import relationship
from cuid2 import Cuid

cuid = Cuid()



class Wallet(Base):
    __tablename__ = "wallets"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False)
    balance_usd = Column(Float, default=0.0)
    balance_trx = Column(Float, default=0.0)
    address = Column(String(50), unique=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    owner = relationship("User", back_populates="wallet")