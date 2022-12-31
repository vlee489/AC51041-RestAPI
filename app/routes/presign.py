"""Routes for pre-signed URLs"""
from fastapi import APIRouter, Request, HTTPException, Depends
from app.messageRPC import Response, State
from app.security import get_session_key, Session
from app.models import UrlResponse

router = APIRouter()

@router.get("/film/id/{film_id}", response_model=UrlResponse)
async def get_film_url(request: Request, film_id: str, security_profile: Session = Depends(get_session_key)):
    film_response: Response = await request.app.mq.call("film-id", {"id": film_id})
    if film_response.status == State.VALID:
        url_response: Response = await request.app.mq.call("film-url",
                                                           {"location": film_response.properties["film"]["file_location"]})
        if url_response.status == State.VALID:
            return {
                "url": url_response.properties["url"]
            }
        else:
            raise HTTPException(status_code=500, detail=f"{url_response.error}")
    else:
        if film_response.error == "NOT-FOUND":
            raise HTTPException(status_code=404, detail="Film not found")
        else:
            raise HTTPException(status_code=500, detail="Internal Error")