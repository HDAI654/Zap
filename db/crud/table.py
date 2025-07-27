from sqlalchemy.orm import Session
from db.models.table_data import TableData
import json

def get_user_table_names(db: Session, user_id: int):
    # Get all tables of user
    tables = db.query(TableData).filter(TableData.user_id == user_id).all()

    # find IDs and Names
    # ! name saved in filed named 'name' in json
    result = []
    for table in tables:
        table_data = table.table_json
        table_name = table_data.get("name") if isinstance(table_data, dict) else None
        result.append({"id": table.id, "name": table_name})
    return result


def get_table_by_id(db: Session, table_id: int):
    table = db.query(TableData).filter(TableData.id == table_id).first()
    if not table:
        return None
    
    table_data = table.table_json
    return table_data
