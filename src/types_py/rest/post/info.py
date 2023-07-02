from typing import TypeAlias

from ...response.post_info import PostInfo, PostInfoArticle, \
    PostInfoImage, PostInfoFile, PostInfoText, PostInfoVideo

Info: TypeAlias = (
    "_InfoArticle" | "_InfoImage" | "_InfoFile"
    | "_InfoText" | "_InfoVideo")
"""投稿データに関する型"""


class _InfoArticle(PostInfo, PostInfoArticle):
    """ブログタイプの投稿の型"""
    pass


class _InfoImage(PostInfo, PostInfoImage):
    """画像タイプの投稿の型"""
    pass


class _InfoFile(PostInfo, PostInfoFile):
    """ファイルタイプの投稿の型"""
    pass


class _InfoText(PostInfo, PostInfoText):
    """テキストタイプの投稿の型"""
    pass


class _InfoVideo(PostInfo, PostInfoVideo):
    """動画・音楽タイプの投稿の型"""
    pass
