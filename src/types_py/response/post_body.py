from typing import TypedDict

from .post_body_blocks import PostBodyBlocks
from .post_body_map import ImageMap, FileMap, EmbedMap, UrlEmbedMap


class PostBody(TypedDict):
    blocks: PostBodyBlocks
    imageMap: ImageMap
    fileMap: FileMap
    embedMap: EmbedMap
    urlEmbedMap: UrlEmbedMap
