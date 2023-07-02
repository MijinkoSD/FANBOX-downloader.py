from os import path
from typing import Final, Any

from src.types_py.rest.creator import Get as CreatorGet
from src.types_py.rest.post import Info
from src.types_py.response.post_item import PostItem
from ..util import time_now
from .common import POST_FILE_ROOT, PROFILE_FILE_ROOT
from .util import save_json


def save_creator_profile(profile: CreatorGet, date: int = time_now()) -> None:
    """クリエイター情報を保存します。
    保存先：`profiles/<クリエイターID>/<日付>.json`

    Args:
        profile (CreatorGet): 保存するクリエイター情報。
        date (int): ファイル名に記入する保存日時。既定では現在日時になる。
    """
    CREATOR_ID: Final[str] = profile["creatorId"]
    SAVE_FILE_PATH: Final[str] = path.join(
        PROFILE_FILE_ROOT, CREATOR_ID, str(date) + ".json")
    save_json(profile, SAVE_FILE_PATH)


def save_postlist(
    items: list[PostItem], creator_id: str, date: int = time_now()
) -> None:
    """投稿一覧のデータを保存します。
    保存先：`posts/<クリエイターID>/postlist/<日付>.json`

    Args:
        items (list[PostItem]): 保存する投稿一覧のデータ。
        creator_id (str): クリエイターID。
        date (int): ファイル名に記入する保存日時。既定では現在日時になる。
    """
    SAVE_FILE_PATH: Final[str] = path.join(
        POST_FILE_ROOT, creator_id, "postlist", str(date) + ".json")
    save_json(items, SAVE_FILE_PATH)


def save_postinfo(postinfo: Info, date: int = time_now()) -> None:
    """詳細な投稿データを保存します。
    保存先：`posts/<クリエイターID>/<投稿ID>/post/<日付>.json`

    Args:
        postinfo (Info): 保存する投稿データ。
        date (int, optional): ファイル名に記入する保存日時。既定では現在日時になる。
    """
    CREATOR_ID: Final[str] = postinfo["user"]["userId"]
    POST_ID: Final[str] = postinfo["id"]
    SAVE_FILE_PATH: Final[str] = path.join(
        POST_FILE_ROOT, CREATOR_ID, POST_ID, "post", str(date) + ".json")
    save_json(postinfo, SAVE_FILE_PATH)


def save_file_by_profile(
    data: Any, creator_id: str, file_type: str, file_name: str
) -> None:
    """プロフィールのファイルを保存します。
    保存先：`profiles/<クリエイターID>/<ファイル種別>/<ファイル名>`

    Args:
        data (Any): 保存するデータ。
        creator_id (str): クリエイターID。
        file_type (str): ファイル種別。
        file_name (str): ファイル名。
    """
    FILE_PATH: Final[str] = path.join(
        PROFILE_FILE_ROOT, creator_id, file_type, file_name)
    with open(FILE_PATH, mode="bw") as f:
        f.write(data)


def save_file_by_post(
    data: Any, creator_id: str, post_id: str, file_type: str, file_name: str
) -> None:
    """投稿データのファイルを保存します。
    保存先：`post/<クリエイターID>/<投稿ID>/<ファイル種別>/<ファイル名>`

    Args:
        data (Any): 保存するデータ。
        creator_id (str): クリエイターID。
        file_type (str): ファイル種別。
        file_name (str): ファイル名。
    """
    FILE_PATH: Final[str] = path.join(
        POST_FILE_ROOT, creator_id, post_id, file_type, file_name)
    with open(FILE_PATH, mode="bw") as f:
        f.write(data)
