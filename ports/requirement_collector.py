from typing import Protocol, Any


class RequirementCollector(Protocol):

    def find_requirement_names(self) -> None:
        pass

    def find_requirement_values(self) -> None:
        pass

    def get(self, name: str) -> Any:
        pass

    def new_requirement(self, news: dict) -> None:
        pass
