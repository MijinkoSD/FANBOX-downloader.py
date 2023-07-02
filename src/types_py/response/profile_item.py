from typing import TypedDict, Literal, TypeAlias, Union

from .video_service_provider import ServiceProvider

ProfileItem: TypeAlias = Union["Image", "Video"]
"""プロフィール欄のポートフォリオ"""


class Image(TypedDict):
    """ポートフォリオに掲載された画像。"""

    id: str
    """ID。"""
    imageUrl: str
    """画像のURL。"""
    thumbnailUrl: str
    """サムネイル用の軽量な画像のURL。"""
    type: Literal["image"]
    """ポートフォリオのファイルタイプ。"""


class Video(TypedDict):
    """ポートフォリオの内、動画や音声といった外部サイトに依存しているもの。"""

    id: str
    """ID。"""
    serviceProvider: ServiceProvider
    """動画や音声を提供しているサイトを表す文字列。"""
    videoId: str
    """提供サイトにおけるコンテンツID。"""
    type: Literal["video"]
    """ポートフォリオのファイルタイプ。"""
