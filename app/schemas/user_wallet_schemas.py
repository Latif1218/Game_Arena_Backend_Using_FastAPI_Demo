from pydantic import BaseModel



class WalletOut(BaseModel):
    balance_usd: float
    balance_trx: float
    address: str
    
    class Config:
        from_attributes = True