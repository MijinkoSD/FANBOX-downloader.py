from typing import TypedDict, Optional
from argparse import Namespace


class Args(TypedDict):
    session_id: Optional[str]
    force_update: bool
    update_posts: bool
    page_limit: Optional[int]
    creator_id: list[str]


def convert_to_args(namespace_args: Namespace) -> Args:
    return Args({
        "session_id": namespace_args.session_id,
        "force_update": namespace_args.force_update,
        "update_posts": namespace_args.update_posts,
        "page_limit": namespace_args.page_limit,
        "creator_id": namespace_args.creator_id,
    })
