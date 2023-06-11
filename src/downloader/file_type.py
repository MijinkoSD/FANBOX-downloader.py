from typing import TypedDict


class ExtractFileURLData(TypedDict):
    id: str
    image: list[str]
    cover: list[str]
    thumb: list[str]
    file: list[str]
