from typing import TypedDict, Literal

from ...response.user import User


class ListCreator(TypedDict):
    """プランに関する型"""

    coverImageUrl: str
    """カバー画像。"""
    creatorId: str
    """クリエイターのID。URLにも使われている。"""
    description: str
    """プロフィール詳細。"""
    fee: int
    """プランの月額料金。"""
    hasAdultContent: bool
    """R-18コンテンツの投稿フラグが有効になっていればtrue。"""
    id: str
    """プランのID。"""
    paymentMethod: None | str | Literal["paypal"]  # paypalのみ確認
    """プランに加入済みの場合は、支払い方法。"""
    title: str
    """プランの名称。"""
    user: User
    """クリエイター情報。"""
