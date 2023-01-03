"""Routes for film position info"""
from fastapi import APIRouter, Request, HTTPException, Depends, BackgroundTasks
from app.messageRPC import Response, State
from app.security import get_session_key, Session
from app.models import FilmPosition

router = APIRouter()


@router.post("/{film_id}", status_code=202)
async def update_film_position(request: Request, film_id: str, pos: FilmPosition, background_tasks: BackgroundTasks,
                               security_profile: Session = Depends(get_session_key)):
    """Update position in a film for a user"""
    data = pos.dict()
    data["user_oid"] = security_profile.oid
    data["film_id"] = film_id
    background_tasks.add_task(request.app.mq.call,routing_key="film-pos-update", payload=data)
    return


@router.delete("/{film_id}", status_code=202)
async def remove_film_position(request: Request, film_id: str, background_tasks: BackgroundTasks,
                               security_profile: Session = Depends(get_session_key)):
    """Remove position in a film for a user"""
    background_tasks.add_task(request.app.mq.call, routing_key="film-pos-remove",
                              payload={"user_oid": security_profile.oid, "film_id": film_id})
    return


@router.get("/{film_id}", response_model=FilmPosition)
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
