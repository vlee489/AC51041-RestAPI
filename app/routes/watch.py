"""Routes for film position info"""
from fastapi import APIRouter, Request, HTTPException, Depends, BackgroundTasks
from app.messageRPC import Response, State
from app.security import get_session_key, Session
from app.models import FilmPosition, FilmPositionHistory
from typing import List

router = APIRouter()


@router.post("/film/{film_id}", status_code=202)
async def update_film_position(request: Request, film_id: str, pos: FilmPosition, background_tasks: BackgroundTasks,
                               security_profile: Session = Depends(get_session_key)):
    """Update position in a film for a user"""
    data = pos.dict()
    data["user_oid"] = security_profile.oid
    data["film_id"] = film_id
    background_tasks.add_task(request.app.mq.call,routing_key="film-pos-update", payload=data)
    return


@router.delete("/film/{film_id}", status_code=202)
async def remove_film_position(request: Request, film_id: str, background_tasks: BackgroundTasks,
                               security_profile: Session = Depends(get_session_key)):
    """Remove position in a film for a user"""
    background_tasks.add_task(request.app.mq.call, routing_key="film-pos-remove",
                              payload={"user_oid": security_profile.oid, "film_id": film_id})
    return


@router.get("/film/{film_id}", response_model=FilmPosition)
async def get_film_position(request: Request, film_id: str, security_profile: Session = Depends(get_session_key)):
    response: Response = await request.app.mq.call("film-pos", {"user_oid": security_profile.oid, "film_id": film_id})
    if response.status == State.VALID:
        film = response.properties["film"]
        return {
            "pos": film["pos"]
        }
    else:
        if response.error == "NOT-FOUND":
            raise HTTPException(status_code=404, detail="Film not found")
        else:
            raise HTTPException(status_code=500, detail="Internal Error")

@router.get("/history", response_model=List[FilmPositionHistory])
async def get_film_history(request: Request, security_profile: Session = Depends(get_session_key)):
    """Get up to the last 4 films watched by user to resume"""
    response: Response = await request.app.mq.call("film-history", {"user_oid": security_profile.oid})
    if response.status == State.VALID:
        films = response.properties["films"]
        return [{"film_id":film["film_id"], "pos": film["pos"]} for film in films]
    else:
        raise HTTPException(status_code=500, detail="Internal Error")
