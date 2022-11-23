"""Routes for user login & logout"""
from fastapi import APIRouter, Request, HTTPException
from app.models import LoginResponse, LoginCredentials
from app.messageRPC import Response, State

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

