from typing import TypedDict, TypeAlias, Literal, Optional

PostBodyBlocks: TypeAlias = "P" | "Header" | "Image" | "File" | "UrlEmbed"

Style: TypeAlias = "StyleBold"


class P(TypedDict):
    """文章"""
    type: Literal["p"]
    text: str
    styles: Optional[list[Style]]
    links: Optional[list["Link"]]


class Header(TypedDict):
    """見出し"""
    type: Literal["header"]
    text: str


class StyleBold(TypedDict):
    """文字装飾（太字）"""
    type: Literal["bold"]
    offset: int
    """太字の開始位置（0文字目～）"""
    length: int
    """太字にする文字数"""


class Link(TypedDict):
    """リンク文字"""
    offset: int
    """リンクの開始位置（0文字目～）"""
    length: int
    """リンクにする文字数"""
    url: str
    """リンク先"""


class Image(TypedDict):
    """画像"""
    type: Literal["image"]
    imageId: str


class File(TypedDict):
    """ファイル"""
    type: Literal["file"]
    fileId: str


class UrlEmbed(TypedDict):
    """埋め込み"""
    type: Literal["url_embed"]
    urlEmbedId: str
