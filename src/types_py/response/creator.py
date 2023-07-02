from typing import TypedDict

from .user import User
from .profile_item import ProfileItem


class Creator(TypedDict):
    """クリエイター情報。"""

    coverImageUrl: str
    """カバー画像。"""
    creatorId: str
    """クリエイターのID。URLにも使われている。"""
    description: str
    """プロフィール詳細。"""
    hasAdultContent: bool
    """R-18コンテンツの投稿フラグが有効になっていればtrue。"""
    hasBoothShop: bool
    """BOOTHのショップが登録されていればtrue。"""
    isAcceptingRequest: bool
    """Pixivでリクエストを送れる状態になっていればtrue。"""
    isFollowed: bool
    """ログイン中のアカウントがフォローしていればtrue。"""
    isStopped: bool
    """不明。falseのみ確認。"""
    isSupported: bool
    """ログイン中のアカウントが支援していればtrue。"""
    profileItems: list[ProfileItem]
    """プロフィール欄のポートフォリオ。"""
    profileLinks: list[str]
    """プロフィールの外部リンクのURL文字列。"""
    user: User
    """クリエイター情報。"""
