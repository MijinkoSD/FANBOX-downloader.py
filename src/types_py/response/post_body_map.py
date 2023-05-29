from typing import TypedDict, TypeAlias, Literal

ImageMap: TypeAlias = dict[str, "_ImageMapInfo"]
FileMap: TypeAlias = dict[str, "_FileMapInfo"]
EmbedMap: TypeAlias = dict[str, "_EmbedMapInfo"]
UrlEmbedMap: TypeAlias = dict[str, "_UrlEmbedMapInfo"]


class _ImageMapInfo(TypedDict):
    id: str
    extension: Literal["jpeg", "gif", "png"]
    width: int
    height: int
    originalUrl: str
    thumbnailUrl: str


class _FileMapInfo(TypedDict):
    id: str
    name: str
    extension: str  # Literalで拡張子網羅するのめんどくさかった
    width: int
    height: int
    originalUrl: str
    thumbnailUrl: str


class _EmbedMapInfo(TypedDict):
    """未確認"""
    pass


class _UrlEmbedMapInfo(TypedDict):
    id: str
    type: Literal["html"]
    html: str
    """埋め込みの際に使われるhtml要素"""
