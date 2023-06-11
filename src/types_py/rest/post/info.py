from typing import TypeAlias

from ...response.post_info import PostInfo, PostInfoArticle, \
    PostInfoImage, PostInfoFile, PostInfoText, PostInfoVideo

Info: TypeAlias = (
    "_InfoArticle" | "_InfoImage" | "_InfoFile"
    | "_InfoText" | "_InfoVideo")


class _InfoArticle(PostInfo, PostInfoArticle):
    pass


class _InfoImage(PostInfo, PostInfoImage):
    pass


class _InfoFile(PostInfo, PostInfoFile):
    pass


class _InfoText(PostInfo, PostInfoText):
    pass


class _InfoVideo(PostInfo, PostInfoVideo):
    pass
