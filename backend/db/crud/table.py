import json
from typing import List, Optional
from core.config import settings

TABLES_FILE = settings.TABLES_FILE


def load_tables_from_file() -> List[dict]:
    try:
        with open(TABLES_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        raise ValueError("Malformed JSON in tables file.")


def save_tables_to_file(tables: List[dict]):
    with open(TABLES_FILE, "w", encoding="utf-8") as f:
        json.dump(tables, f, indent=2, ensure_ascii=False)


def get_user_table_names(user_id: int) -> List[dict]:
    tables = load_tables_from_file()
    result = []
    for table in tables:
        if table.get("user") == user_id:
            result.append({"ID": table.get("ID"), "name": table.get("name"), "columns_structure": table.get("data").get("columns")})
    return result


def get_table_by_id(user_id: int, table_id: int) -> Optional[dict]:
    tables = load_tables_from_file()
    for table in tables:
        if table.get("user") == user_id and table.get("ID") == table_id:
            return table
    return None


def is_valid_table_json(table_json: dict) -> bool:
    if not isinstance(table_json, dict):
        return False
    if "name" not in table_json or not isinstance(table_json["name"], str):
        return False
    if "data" not in table_json or not isinstance(table_json["data"], dict):
        return False
    if "columns" not in table_json["data"] or "rows" not in table_json["data"]:
        return False
    return True


def add_table(user_id: int, table_json: dict) -> dict:
    if not is_valid_table_json(table_json):
        raise ValueError("Invalid table JSON format.")

    tables = load_tables_from_file()

    existing_ids = [table.get("ID", 0) for table in tables]
    new_id = max(existing_ids) + 1 if existing_ids else 1

    new_table = {
        "user": user_id,
        "ID": new_id,
        **table_json
    }

    tables.append(new_table)
    save_tables_to_file(tables)
    return new_table


def delete_table(user_id: int, table_id: int) -> bool:
    tables = load_tables_from_file()
    initial_len = len(tables)
    tables = [t for t in tables if not (t.get("user") == user_id and t.get("ID") == table_id)]
    if len(tables) == initial_len:
        return False 
    save_tables_to_file(tables)
    return True


def save_table_by_id(user_id: int, table_id: int, updated_table: dict) -> bool:
    tables = load_tables_from_file()
    updated = False
    for i, table in enumerate(tables):
        if table.get("user") == user_id and table.get("ID") == table_id:
            tables[i] = updated_table
            updated = True
            break
    if updated:
        save_tables_to_file(tables)
    return updated
