#!/usr/bin/env python3
from .post import Post
from .file import File

BASE_URL = "https://api.fanbox.cc/"
BASE_LOCAL_DIR = "./posts/"
BASE_LOCAL_PROFILE_DIR = "./profile/"

WAIT_TIME = 0.2

__all__ = [
    "Post",
    "File",
]