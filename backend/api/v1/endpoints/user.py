from fastapi import Depends, APIRouter, HTTPException
from auth import dependencies
from pydantic import BaseModel, validator
from sqlalchemy.orm import Session
from db.crud.table import add_table, get_user_table_names, get_table_by_id
from db.session import get_db
from core.logger import logger


router = APIRouter()

# Simple secure path
@router.get("/me")
def read_me(user=Depends(dependencies.get_current_user)):
    return {"email": user.email, "username": user.username}




# endpoint for Add table
class TableCreateSchema(BaseModel):
    table_json: dict

    @validator("table_json")
    def validate_format(cls, v):
        # Check if 'name' key exists and is a string
        if "name" not in v or not isinstance(v["name"], str):
            raise ValueError("Missing or invalid 'name' in table_json")
        # Check if 'data' key exists and is a dict
        if "data" not in v or not isinstance(v["data"], dict):
            raise ValueError("Missing or invalid 'data' in table_json")
        return v

@router.post("/add-table")
def create_table_endpoint(
    table_json: dict,
    db: Session = Depends(get_db),
    user = Depends(dependencies.get_current_user)
):
    try:
        new_table = add_table(db=db, user_id=user.id, table_json=table_json)
        return new_table
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error in create_table_endpoint: {e}")
        raise HTTPException(status_code=500, detail="Internal Error")
    

@router.get("/tables-names")
def read_user_table_names(
    current_user=Depends(dependencies.get_current_user),
    db: Session = Depends(get_db),
):

    if not current_user.id:
        raise HTTPException(status_code=403, detail="Forbidden")

    tables = get_user_table_names(db, current_user.id)
    return {"tables": tables}


@router.get("/tables/{table_id}")
def read_table_data(
    table_id: int,
    current_user=Depends(dependencies.get_current_user),
    db: Session = Depends(get_db),
):
    table = get_table_by_id(db, table_id)
    if not table:
        raise HTTPException(status_code=404, detail="Table not found")

    return {"table": table}



