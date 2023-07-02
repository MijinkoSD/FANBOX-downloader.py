from typing import TypedDict

from .post_body_blocks import PostBodyBlocks
from .post_body_map import ImageMap, FileMap, EmbedMap, UrlEmbedMap, \
    ImageMapInfo, FileMapInfo
from .video_service_provider import ServiceProvider


class PostBodyArticle(TypedDict):
    """ブログタイプの投稿の本文"""
    blocks: PostBodyBlocks
    imageMap: ImageMap
    fileMap: FileMap
    embedMap: EmbedMap
    urlEmbedMap: UrlEmbedMap


class PostBodyImage(TypedDict):
    """画像タイプの投稿の本文"""
    text: str
    images: list[ImageMapInfo]


class PostBodyFile(TypedDict):
    """ファイルタイプの投稿の本文"""
    text: str
    files: list[FileMapInfo]


class PostBodyText(TypedDict):
    """テキストタイプの投稿の本文"""
    text: str


class PostBodyVideo(TypedDict):
    """動画・音楽タイプの投稿の本文"""
    text: str
    video: "_VideoItem"


class _VideoItem(TypedDict):
    """動画・音楽タイプの投稿内の埋め込み情報"""
    serviceProvider: ServiceProvider
    videoId: str
