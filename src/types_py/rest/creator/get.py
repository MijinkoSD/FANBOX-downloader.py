from typing import TypedDict

from ...response.user import ProfileItem, User


class Get(TypedDict):
    coverImageUrl: str
    creatorId: str
    description: str
    hasAdultContent: bool
    hasBoothShop: bool
    isAcceptingRequest: bool
    isFollowed: bool
    isStopped: bool
    isSupported: bool
    profileItems: ProfileItem
    profileLinks: list[str]
    user: User
