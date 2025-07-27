from fastapi import APIRouter, UploadFile, File
from fastapi.responses import JSONResponse
from services.voice_to_text import transcribe_audio

router = APIRouter()

@router.post("/transcribe")
async def transcribe(audio: UploadFile = File(...)):
    """
    Receive audio file and return transcribed text.
    """
    try:
        contents = await audio.read()
        text = transcribe_audio(contents)
        return JSONResponse(content={"text": text})
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
