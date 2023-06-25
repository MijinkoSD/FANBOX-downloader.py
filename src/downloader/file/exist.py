from os import path, scandir
from typing import Final

from .common import POST_FILE_ROOT


def is_exist_post(creator_id: str, post_id: str) -> bool:
    """保存済みの投稿データが既に存在しているかを確認します。

    Args:
        creator_id (str): クリエイターID。
        post_id (str): 投稿ID。

    Returns:
        bool: 存在していればTrue。
    """
    SEARCH_DIR: Final[str] = path.join(
        POST_FILE_ROOT, creator_id, post_id, "post")
    if not path.isdir(SEARCH_DIR):
        # フォルダ自体が見つからなかった場合
        return False
    with scandir(path=SEARCH_DIR) as entries:
        for entry in entries:
            if entry.name.endswith(".json") and entry.is_file():
                # jsonファイルが見つかった場合はTrueを返却
                return True
    # 何も見つからずに終わった場合
    return False
