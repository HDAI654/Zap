from fastapi import APIRouter, UploadFile, File, Depends
from fastapi.responses import JSONResponse
from services.voice_to_text import transcribe_audio
from core.logger import logger
from services.intent_analyzer import extract_tables_from_question
from services.llm_client import get_answer_and_sql_queries
from db.crud.table import get_user_table_names, get_table_by_id
from auth import dependencies
from sqlalchemy.orm import Session
from db.session import get_db

router = APIRouter()

@router.post("/transcribe")
async def transcribe(audio: UploadFile = File(...), user=Depends(dependencies.get_current_user), db: Session = Depends(get_db), table_name=None):
    """
    Receive audio file and return transcribed text.
    """
    try:
        # speech to text
        contents = await audio.read()
        user_text = transcribe_audio(contents)

        # get names of user's tables
        tables = get_user_table_names(db=db, user_id=user.id)


        # get the focused table if exist
        if table_name != None and table_name in tables:
            extracted_tables = [table_name]

        else:
            # extract tables from user question
            extracted_tables = extract_tables_from_question(tables_names=tables, question=user_text)

        # extract table data
        tables_data = [get_table_by_id(db=db, table_id=t["id"]) for t in extracted_tables]

        # get final response
        res = get_answer_and_sql_queries(user_question=user_text, table_data=tables_data)
        return JSONResponse(content={"text": str(res["answer"])})
    except Exception as e:
        logger.error(f"Error in transcribe endpoint: {e}")
        return JSONResponse(content={"error": str(e)}, status_code=500)
