from ports.tool import Tool
from typing import Protocol


class ToolPkg(Protocol):
    tools: list[Tool]

    def run(name: str):
        pass
