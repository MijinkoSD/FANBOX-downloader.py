from typing import TypeAlias

from ...response.post_info import PostInfo, PostInfoArticle

Info: TypeAlias = "_InfoArticle"


class _InfoArticle(PostInfo, PostInfoArticle):
    pass
