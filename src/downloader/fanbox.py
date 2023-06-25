#!/usr/bin/env python3
# FIXME: _post依存をやめる
from ._post import Post
from .file_ import File

BASE_URL = "https://api.fanbox.cc/"
BASE_LOCAL_DIR = "./posts/"
BASE_LOCAL_PROFILE_DIR = "./profile/"

WAIT_TIME = 0.2

__all__ = [
    "Post",
    "File",
]
