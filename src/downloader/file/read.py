from os import path
from typing import Optional, Final

from src.types_py.rest.creator import Get as CreatorGet
from src.types_py.rest.post import Info
from src.types_py.response.post_item import PostItem
from .common import POST_FILE_ROOT, PROFILE_FILE_ROOT
from .util import read_json, get_latest_filename


def read_creator_profile(
    creator_id: str, date: Optional[int] = None
) -> CreatorGet:
    """保存済みのクリエイター情報を取得します。
    取得先：`profiles/<クリエイターID>/<日付>.json`
    なお、取得するデータの型チェックは行わない。

    Args:
        creator_id (str): クリエイター情報
        date (Optional[int], optional): 読み込むファイルの日付。省略した場合は最新のファイルを取得する。

    Returns:
        CreatorGet: 取得したクリエイター情報。

    Raises:
        ValueError: creator_idの値が有効ではない場合に発生。
    """
    if not creator_id:
        raise ValueError("クリエイターIDが無効です。" +
                         "  渡されたクリエイターID: %s"
                         % (creator_id))

    CREATOR_DIR: Final[str] = path.join(
        PROFILE_FILE_ROOT, creator_id)
    file_name: str
    if date is None:
        file_name = get_latest_filename(CREATOR_DIR, r"\d{14}\.json")
    else:
        file_name = str(date) + ".json"
    READ_FILE_PATH: Final[str] = path.join(
        CREATOR_DIR, file_name)

    # ファイル読み込み
    data: CreatorGet = read_json(READ_FILE_PATH)
    return data


def read_postlist(
    creator_id: str, date: Optional[int] = None
) -> list[PostItem]:
    """保存済みの投稿一覧のデータを取得します。
    取得先：`posts/<クリエイターID>/postlist/<日付>.json`
    なお、取得するデータの型チェックは行わない。

    Args:
        creator_id (str): クリエイターID。
        date (Optional[int], optional): 読み込むファイルの日付。省略した場合は最新のファイルを取得する。

    Returns:
        list[PostItem]: 取得した投稿一覧のデータ。

    Raises:
        ValueError: creator_idの値が有効ではない場合に発生。
    """
    if not creator_id:
        raise ValueError("クリエイターIDが無効です。" +
                         "  渡されたクリエイターID: %s"
                         % (creator_id))

    POSTLIST_DIR: Final[str] = path.join(
        POST_FILE_ROOT, creator_id, "postlist")
    file_name: str
    if date is None:
        file_name = get_latest_filename(POSTLIST_DIR, r"\d{14}\.json")
    else:
        file_name = str(date) + ".json"
    READ_FILE_PATH: Final[str] = path.join(
        POSTLIST_DIR, file_name)

    # ファイル読み込み
    data: list[PostItem] = read_json(READ_FILE_PATH)
    return data


def read_postinfo(
    creator_id: str, post_id: str, date: Optional[int] = None
) -> Info:
    """保存済みの詳細な投稿データを取得します。
    取得先：`posts/<クリエイターID>/<投稿ID>/post/<日付>.json`

    Args:
        creator_id (str): クリエイターID。
        post_id (str): 投稿ID。
        date (Optional[int], optional): 読み込むファイルの日付。省略した場合は最新のファイルを取得する。

    Returns:
        Info: 取得した投稿データ。

    Raises:
        ValueError: creator_idまたはpost_idの値が有効ではない場合に発生。
    """
    if not creator_id:
        raise ValueError("クリエイターIDが無効です。" +
                         "  渡されたクリエイターID: %s"
                         % (creator_id))
    elif not post_id:
        raise ValueError("投稿IDが無効です。" +
                         "  渡された投稿ID: %s"
                         % (post_id))

    POST_DIR: Final[str] = path.join(
        POST_FILE_ROOT, creator_id, post_id, "post")
    file_name: str
    if date is None:
        file_name = get_latest_filename(POST_DIR, r"\d{14}\.json")
    else:
        file_name = str(date) + ".json"
    READ_FILE_PATH: Final[str] = path.join(
        POST_DIR, file_name)

    # ファイル読み込み
    data: Info = read_json(READ_FILE_PATH)
    return data
