from ports.requirement_collector import RequirementCollector
import json
from typing import Any
from pathlib import Path

class LocalRequirementCollector(RequirementCollector):
    JSON_PATH = Path(__file__).resolve().parent / "req.json"

    def find_requirement_names(self) -> None:
        with open(self.JSON_PATH, "r", encoding="utf-8") as jf:
            return tuple(dict(json.load(jf)).keys())

    def find_requirement_values(self) -> None:
        with open(self.JSON_PATH, "r", encoding="utf-8") as jf:
            return dict(json.load(jf))

    def get(self, name: str) -> Any:
        with open(self.JSON_PATH, "r", encoding="utf-8") as jf:
            return dict(json.load(jf)).get(name)

    def new_requirement(self, news: dict) -> None:
        with open(self.JSON_PATH, "r", encoding="utf-8") as jf:
            req = json.load(jf)

        with open(self.JSON_PATH, "w", encoding="utf-8") as jf:
            json.dump(req | news, jf, indent=2, ensure_ascii=True)
