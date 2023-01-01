"""Routes for film info"""
from fastapi import APIRouter, Request, HTTPException, Depends
from app.models import FilmResponse
from app.messageRPC import Response, State
from app.security import get_session_key, Session
from typing import List
from app.functions.cdnURL import location_to_cdn

router = APIRouter()


@router.get("/id/{film_id}", response_model=FilmResponse)
async def get_film_by_id(request: Request, film_id: str, security_profile: Session = Depends(get_session_key)):
    response: Response = await request.app.mq.call("film-id", {"id": film_id})
    if response.status == State.VALID:
        film = response.properties["film"]
        return {
            "id": film["id"],
            "name": film["name"],
            "tags": film["tags"],
            "categories": film["categories"],
            "thumbnail_url": location_to_cdn(film["thumbnail_location"]),
            "description": film["description"],
            "tag_line": film["tag_line"]
        }
    else:
        if response.error == "NOT-FOUND":
            raise HTTPException(status_code=404, detail="Film not found")
        else:
            raise HTTPException(status_code=500, detail="Internal Error")


@router.get("/tag/{tag}", response_model=List[FilmResponse])
async def get_tag_film(request: Request, tag: str, security_profile: Session = Depends(get_session_key)):
    response: Response = await request.app.mq.call("film-tag", {"tag": tag})
    if response.status == State.VALID:
        films = response.properties["films"]
        return [{
            "id": film["id"],
            "name": film["name"],
            "tags": film["tags"],
            "categories": film["categories"],
            "thumbnail_url": location_to_cdn(film["thumbnail_location"]),
            "description": film["description"],
            "tag_line": film["tag_line"]
        } for film in films]
    else:
        if response.error == "NOT-FOUND":
            raise HTTPException(status_code=404, detail="Films not found")
        else:
            raise HTTPException(status_code=500, detail="Internal Error")


@router.get("/category/{category}", response_model=List[FilmResponse])
async def get_category_film(request: Request, category: str, security_profile: Session = Depends(get_session_key)):
    response: Response = await request.app.mq.call("film-cat", {"category": category})
    if response.status == State.VALID:
        films = response.properties["films"]
        return [{
            "id": film["id"],
            "name": film["name"],
            "tags": film["tags"],
            "categories": film["categories"],
            "thumbnail_url": location_to_cdn(film["thumbnail_location"]),
            "description": film["description"],
            "tag_line": film["tag_line"]
        } for film in films]
    else:
        if response.error == "NOT-FOUND":
            raise HTTPException(status_code=404, detail="Films not found")
        else:
            raise HTTPException(status_code=500, detail="Internal Error")


@router.get("/search/{query}", response_model=List[FilmResponse])
async def search_films(request: Request, query: str, security_profile: Session = Depends(get_session_key)):
    response: Response = await request.app.mq.call("film-search", {"query": query})
    if response.status == State.VALID:
        films = response.properties["films"]
        return [{
            "id": film["id"],
            "name": film["name"],
            "tags": film["tags"],
            "categories": film["categories"],
            "thumbnail_url": location_to_cdn(film["thumbnail_location"]),
            "description": film["description"],
            "tag_line": film["tag_line"]
        } for film in films]
    else:
        if response.error == "NOT-FOUND":
            return []
        else:
            raise HTTPException(status_code=500, detail="Internal Error")


@router.get("/all", response_model=List[FilmResponse])
async def get_all_film(request: Request, security_profile: Session = Depends(get_session_key)):
    response: Response = await request.app.mq.call("film-all", {})
    if response.status == State.VALID:
        films = response.properties["films"]
        return [{
            "id": film["id"],
            "name": film["name"],
            "tags": film["tags"],
            "categories": film["categories"],
            "thumbnail_url": location_to_cdn(film["thumbnail_location"]),
            "description": film["description"],
            "tag_line": film["tag_line"]
        } for film in films]
    else:
        if response.error == "NOT-FOUND":
            raise HTTPException(status_code=404, detail="Films not found")
        else:
            raise HTTPException(status_code=500, detail="Internal Error")
