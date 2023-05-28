from typing import TypedDict, Literal


class Cover(TypedDict):
    """カバー画像の情報。"""

    type: Literal["cover_image"]
    url: str
