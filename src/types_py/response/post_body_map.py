from typing import TypedDict, TypeAlias, Literal

ImageMap: TypeAlias = dict[str, "ImageMapInfo"]
"""ブログタイプの投稿に埋め込まれた画像ファイルの情報を格納する型"""
FileMap: TypeAlias = dict[str, "FileMapInfo"]
"""ブログタイプの投稿に埋め込まれたファイル（画像以外）の情報を格納する型"""
EmbedMap: TypeAlias = dict[str, "EmbedMapInfo"]
"""未確認"""
UrlEmbedMap: TypeAlias = dict[str, "UrlEmbedMapInfo"]
"""ブログタイプの投稿に埋め込まれたURLの情報を格納する型"""


class ImageMapInfo(TypedDict):
    """ブログタイプの投稿に埋め込まれた画像ファイルの情報を格納する型"""
    id: str
    extension: Literal["jpeg", "gif", "png"]
    width: int
    height: int
    originalUrl: str
    thumbnailUrl: str


class FileMapInfo(TypedDict):
    """ブログタイプの投稿に埋め込まれたファイル（画像以外）の情報を格納する型"""
    id: str
    name: str
    extension: str  # Literalで拡張子網羅するのめんどくさかった
    size: int
    url: str


class EmbedMapInfo(TypedDict):
    """未確認"""
    pass


class UrlEmbedMapInfo(TypedDict):
    """ブログタイプの投稿に埋め込まれたURLの情報を格納する型"""
    id: str
    type: Literal["html"]
    html: str
    """埋め込みの際に使われるhtml要素"""
