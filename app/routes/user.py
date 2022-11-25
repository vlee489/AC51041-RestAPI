"""Routes for user info"""
from fastapi import APIRouter, Request, HTTPException, Depends
from app.security import get_session_key, Session
from app.models import UserResponse
from app.messageRPC import Response, State

router = APIRouter()


@router.get("/", response_model=UserResponse)
async def login(request: Request, security_profile: Session = Depends(get_session_key)):
    """User Login"""
    response: Response = await request.app.mq.call("user", {"user_id": security_profile.user_id})
    if response.status == State.VALID:
        return response.properties['user']
    else:
        if response.error in ["NO-USER"]:
            raise HTTPException(status_code=401, detail="Invalid User")
        elif response.error == "MISSING-FIELD":
            raise HTTPException(status_code=422, detail="Validation Error")
        else:
            raise HTTPException(status_code=500, detail="Internal Error")
