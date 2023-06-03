from typing import TypedDict, TypeAlias, Literal

ImageMap: TypeAlias = dict[str, "ImageMapInfo"]
FileMap: TypeAlias = dict[str, "FileMapInfo"]
EmbedMap: TypeAlias = dict[str, "EmbedMapInfo"]
UrlEmbedMap: TypeAlias = dict[str, "UrlEmbedMapInfo"]


class ImageMapInfo(TypedDict):
    id: str
    extension: Literal["jpeg", "gif", "png"]
    width: int
    height: int
    originalUrl: str
    thumbnailUrl: str


class FileMapInfo(TypedDict):
    id: str
    name: str
    extension: str  # Literalで拡張子網羅するのめんどくさかった
    size: int
    url: str


class EmbedMapInfo(TypedDict):
    """未確認"""
    pass


class UrlEmbedMapInfo(TypedDict):
    id: str
    type: Literal["html"]
    html: str
    """埋め込みの際に使われるhtml要素"""
