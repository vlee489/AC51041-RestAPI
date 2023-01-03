"""Routes for film recommendation info"""
from fastapi import APIRouter, Request, HTTPException, Depends, BackgroundTasks
from app.messageRPC import Response, State
from app.security import get_session_key, Session
from app.models import Recommendation, RecommendationResponse

router = APIRouter()

@router.post("", status_code=202)
async def update_film_recommendation(request: Request, data: Recommendation, background_tasks: BackgroundTasks,
                               security_profile: Session = Depends(get_session_key)):
    """Update position in a film for a user"""
    data = data.dict()
    data["user_oid"] = security_profile.oid
    background_tasks.add_task(request.app.mq.call,routing_key="film-rec-update", payload=data)
    return

@router.get("", response_model=RecommendationResponse)
async def get_film_recommendation(request: Request, security_profile: Session = Depends(get_session_key)):
    response: Response = await request.app.mq.call("film-rec", {"user_oid": security_profile.oid})
    if response.status == State.VALID:
        recommendation = response.properties["recommendation"]
        return {
            "tags": dict(reversed(sorted(recommendation["tags"].items(), key=lambda x: x[1]))),
            "categories": dict(reversed(sorted(recommendation["categories"].items(), key=lambda x: x[1]))),
        }
    else:
        if response.error == "NOT-FOUND":
            raise HTTPException(status_code=404, detail="User not found")
        else:
            raise HTTPException(status_code=500, detail="Internal Error")
