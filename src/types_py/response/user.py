from typing import TypedDict


class User(TypedDict):
    """クリエイターの基本的な情報"""

    iconUrl: str | None
    name: str
    userId: str
