from fastapi import FastAPI
from .database import Base, engine
from .routes import register_user, user, admin, forgot, wallet, matches

Base.metadata.create_all(bind=engine)

app = FastAPI()



app.include_router(user.router)
app.include_router(register_user.router)
app.include_router(admin.router)
app.include_router(forgot.router)
app.include_router(wallet.router)
app.include_router(matches.router)