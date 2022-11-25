"""FastAPI Security Dependencies"""
from fastapi import Request, Security, HTTPException, WebSocket
from fastapi.security.api_key import APIKeyHeader
from typing import Optional
from app.messageRPC import State
from .models import Session

header_authorization = APIKeyHeader(name="Authorization", auto_error=True)


async def get_session_key(request: Request, api_key_header: str = Security(header_authorization)) -> Optional[Session]:
    response = await request.app.mq.call("session", {"session_id": api_key_header})
    if response.status == State.VALID:
        return Session(response.properties["session"])
    else:
        raise HTTPException(status_code=401, detail="Not Authorised")
