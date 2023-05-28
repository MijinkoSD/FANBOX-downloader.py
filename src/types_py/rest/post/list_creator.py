from typing import TypedDict

from ...response.post_item import PostItem


class ListCreator(TypedDict):
    items: list[PostItem]
    """投稿データの一覧。"""
    nextUrl: str
    """次ページのデータを取得するためのURL。"""
