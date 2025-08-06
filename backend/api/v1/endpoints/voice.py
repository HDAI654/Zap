from fastapi import APIRouter, UploadFile, File, Depends, Form
from fastapi.responses import JSONResponse
from services.voice_to_text import transcribe_audio
from core.logger import logger
from auth import dependencies
from sqlalchemy.orm import Session
from db.session import get_db
from services.manager import manager

router = APIRouter()

@router.post("/transcribe")
async def transcribe(
    audio: UploadFile = File(None),
    table_name: str = Form(None),
    text: str = Form(None),
    user=Depends(dependencies.get_current_user),
):
    """
    Receive audio file and return transcribed text.
    """
    try:
        if text == None and audio == None:
            return JSONResponse(content={"error": "One of the audio or text is requerd to use this api"}, status_code=400)
        # use text if exist
        if text and isinstance(text, str):
            res = manager(user_text=text, user_id=user.id, table=table_name)
            return JSONResponse(content={"text": res})

        # speech to text
        contents = await audio.read()
        user_text = transcribe_audio(contents)

        res = manager(user_text=user_text, user_id=user.id, table=table_name)
        return JSONResponse(content={"text":res})
    except Exception as e:
        logger.error(f"Error in transcribe endpoint: {e}")
        return JSONResponse(content={"error": str(e)}, status_code=500)
