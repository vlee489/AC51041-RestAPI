"""Routes for user login & logout"""
from fastapi import APIRouter, Request, HTTPException, Depends
from app.models import LoginResponse, LoginCredentials, BoolResponse
from app.messageRPC import Response, State
from app.security import get_session_key, Session

router = APIRouter()


@router.post("/login", response_model=LoginResponse)
async def login(request: Request, credentials: LoginCredentials):
    """User Login"""
    response: Response = await request.app.mq.call("login", credentials.dict())
    if response.status == State.VALID:
        return {"session_id": response.properties['login']["session"],
                "expiry": response.properties['login']['expiry']}
    else:
        if response.error in ["NO-USER", "PASSWORD"]:
            raise HTTPException(status_code=401, detail="Invalid Username/Password")
        elif response.error == "MISSING-FIELD":
            raise HTTPException(status_code=422, detail="Validation Error")
        else:
            raise HTTPException(status_code=500, detail="Internal Error")


@router.get("/logout", response_model=BoolResponse)
async def logout(request: Request, security_profile: Session = Depends(get_session_key)):
    """User Logout"""
    response: Response = await request.app.mq.call("logout", {"session_id": security_profile.session_id})
    if response.status == State.VALID:
        return {"status": True}
    else:
        if response.error == "NO-SESSION":
            raise HTTPException(status_code=404, detail="Session not found")
        elif response.error in ["NO-USER"]:
            raise HTTPException(status_code=401, detail="Invalid User")
        elif response.error == "MISSING-FIELD":
            raise HTTPException(status_code=422, detail="Validation Error")
        else:
            raise HTTPException(status_code=500, detail="Internal Error")

