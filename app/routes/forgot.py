from fastapi import APIRouter, Depends, status, HTTPException
from ..Authentication import user_auth
from sqlalchemy.orm import Session 
from ..database import get_db, get_redis
from ..schemas import user_schemas
from ..models import user_models
from ..utils.email_sender import send_otp_email
from ..utils.otp_sender import generate_otp
from ..Authentication import user_auth
from ..utils import hashing
from datetime import datetime, timedelta, timezone


router = APIRouter(
    prefix="/forgot",
    tags=["Forgot Password"]
)

@router.post("/forgot_pass", status_code=status.HTTP_200_OK)
def forgot_password(
    payload: user_schemas.ForgotPasswordRequest, 
    db: Session = Depends(get_db)
):
    user = db.query(user_models.User).filter(
        user_models.User.email == payload.email
    ).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="user with this email dose not exist"
        )
    set_otp = generate_otp()
    db.query(user_models.PasswordResetCode).filter(
        user_models.PasswordResetCode.user_id == user.id,
        user_models.PasswordResetCode.used == False
    ).delete()
    
    otp_record = user_models.PasswordResetCode(
        user_id = user.id,
        otp = set_otp,
        used = False,
        expires_at = datetime.now(timezone.utc)+timedelta(minutes=15)
    )
    db.add(otp_record)
    db.commit()
    
    sent = send_otp_email(to_email= user.email, otp = set_otp)
    
    if not sent:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Faild to send otp email"
        )
        
    return{
        "status": "success",
        "message": f"password reset otp sent to {user.email}"
    }
    
    
    
    
@router.post("/verify_otp", status_code=status.HTTP_200_OK)
def verify_otp(
    payload: user_schemas.OTPVerify, 
    db: Session = Depends(get_db)
):
    user = db.query(user_models.User).filter(
        user_models.User.email == payload.email
    ).first()
    
    if not user: 
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="user with this email dose not exixt"
        )
    otp_record = db.query(user_models.PasswordResetCode).filter(
        user_models.PasswordResetCode.user_id == user.id,
        user_models.PasswordResetCode.otp == payload.otp,
        user_models.PasswordResetCode.used == False,
        user_models.PasswordResetCode.expires_at > datetime.now(timezone.utc)
    ).first()
    
    if not otp_record:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid od expired OTP"
        )
        
        
    otp_record.used = True
    db.commit()
    
    redis_session = get_redis()
    reset_key = redis_session.get_key("password_reset: {}:{}", payload.email, payload.otp)
    redis_session.set_with_expiry(reset_key, "verified", 600)
    
    return {
        "status": "success",
        "message": "OTP verified successfully. you can now reset your password."
    }
    
    
    
@router.put("/update_password_without_token", status_code= status.HTTP_200_OK)
def update_password_without_token(
    payload: user_schemas.PasswoedUpdateWithoutToken,
    db: Session = Depends(get_db)
):
    """
    update password without requireing authentication token(JWT). \n
    User for password reset after OTP verification.
    """
    
    if len(payload.new_password) < 8:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="New password must be at least 8 characters long"
        )
    
    user = db.query(user_models.User).filter(user_models.User.email == payload.email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
        
    redis_session = get_redis()
    reset_key = redis_session.get(f"password_reset: {payload.email}:{payload.otp}")
    
    reset_verified = redis_session.get_key(reset_key)
    if not reset_verified:
        otp_record = db.query(user_models.PasswordResetCode).filter(
            user_models.PasswordResetCode.user_id == user.id,
            user_models.PasswordResetCode.otp == payload.otp,
            user_models.PasswordResetCode.expires_at > datetime.now(timezone.utc)
        ).first()
        
        if not otp_record:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="OTP not verified or expired"
            )
            
    else: 
        redis_session.delete(reset_key)
        
    hashed_password = hashing.hash_password(payload.new_password)
    user.password = hashed_password
    
    db.query(user_models.PasswordResetCode).filter(
        user_models.PasswordResetCode.user_id == user.id,
        user_models.PasswordResetCode.used == False
    ).delete()
    
    try:
        db.commit()
        
        user_session_key = redis_session.get_key("user_session: {}", user.id)
        redis_session.delete(user_session_key)
        
        return {
            "status": "success",
            "message": "Password update successfully"
        }
        
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update password"
        )
    
    
    
@router.put("/update_password", status_code=status.HTTP_200_OK)
def update_password(
    payload: user_schemas.PasswordUpdate,
    user: user_models.User = Depends(user_auth.get_current_user),
    db: Session = Depends(get_db)
):
    user = db.query(user_models.User).filter(
        user_models.User.id == user.id
    ).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="user not found"
        )
    db.commit()
    
    return {
        "status": " Success",
        "message": "Password updated successfully"
    }