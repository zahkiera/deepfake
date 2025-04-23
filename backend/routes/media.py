from fastapi import APIRouter, HTTPException
from db import get_media

router = APIRouter()

# return a list of static media sources
@router.get("/{question_id}")
def get_media_from_question(question_id: int):
    urls = get_media(question_id)

    if not urls:
        raise HTTPException(status_code=404, detail="No media was found.")

    url_list = [f"{url[0]}" if not url[0].startswith("/media/") else url[0] for url in urls]

    return {
        "media_urls": url_list
    }