from typing import Optional

from .read import read_postlist


def extract_post_id(
    creator_id: str, date: Optional[int] = None
) -> list[str]:
    """保存済みの投稿一覧のデータから投稿IDを取得します。

    Args:
        creator_id (str): クリエイターID。
        date (Optional[int], optional): 読み込むファイルの日付。省略した場合は最新のファイルを取得する。

    Returns:
        list[str]: 取得した投稿ID。
    """
    post_list = read_postlist(creator_id, date)
    post_ids: list[str] = []
    for item in post_list:
        post_ids.append(item["id"])
    return post_ids
