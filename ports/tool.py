from typing import Protocol


class ToolDef(Protocol):
    defenition: str


class Tool(Protocol):
    tooldef: ToolDef

    def do(*args, **kwargs):
        pass
