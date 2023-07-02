from typing import TypedDict

from .file import ProfileSubDir, PostSubDir


class UrlsInProfile(TypedDict):
    type: ProfileSubDir
    url: str


class UrlsInPost(TypedDict):
    type: PostSubDir
    url: str
