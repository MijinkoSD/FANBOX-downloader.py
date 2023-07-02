from typing import TypedDict


class FileDownloadStats(TypedDict):
    try_count: int
    success: int
    failure: int
    skip: int
