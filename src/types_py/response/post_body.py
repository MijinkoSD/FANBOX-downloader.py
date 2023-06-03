from typing import TypedDict

from .post_body_blocks import PostBodyBlocks
from .post_body_map import ImageMap, FileMap, EmbedMap, UrlEmbedMap, \
    ImageMapInfo, FileMapInfo
from .video_service_provider import ServiceProvider


class PostBodyArticle(TypedDict):
    blocks: PostBodyBlocks
    imageMap: ImageMap
    fileMap: FileMap
    embedMap: EmbedMap
    urlEmbedMap: UrlEmbedMap


class PostBodyImage(TypedDict):
    text: str
    images: list[ImageMapInfo]


class PostBodyFile(TypedDict):
    text: str
    files: list[FileMapInfo]


class PostBodyText(TypedDict):
    text: str


class PostBodyVideo(TypedDict):
    text: str
    video: "_VideoItem"


class _VideoItem(TypedDict):
    serviceProvider: ServiceProvider
    videoId: str
