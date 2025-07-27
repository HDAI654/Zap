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

def is_valid_table_json(table_json: dict) -> bool:
    """
    ## review the json
    """
    if not isinstance(table_json, dict):
        return False
    if "name" not in table_json or "data" not in table_json:
        return False
    if not isinstance(table_json["name"], str):
        return False
    if not isinstance(table_json["data"], dict):
        return False
    return True

def add_table(db: Session, user_id: int, table_json: dict):
    if not is_valid_table_json(table_json):
        raise ValueError("Invalid table JSON format. Must contain 'name' (str) and 'data' (dict).")

    # Convert to compact JSON string then parse back to dict
    compact_json_str = json.dumps(table_json, separators=(",", ":"))
    compact_json_dict = json.loads(compact_json_str)

    new_table = TableData(
        user_id=user_id,
        table_json=compact_json_dict
    )
    db.add(new_table)
    db.commit()
    db.refresh(new_table)
    return new_table

