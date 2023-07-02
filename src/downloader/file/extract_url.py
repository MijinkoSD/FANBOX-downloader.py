from typing import Optional

from src.types_py.rest.creator import Get as CreatorGet
from src.types_py.rest.post import Info
from ..define.urls import UrlsInProfile, UrlsInPost
from .read import read_creator_profile, read_postinfo


def extract_url_from_profile(
    creator_id: str, date: Optional[int] = None
) -> list[UrlsInProfile]:
    """保存済みのプロフィールデータからダウンロード可能なURLを抽出します。

    Args:
        creator_id (str): クリエイターID。
        date (Optional[int], optional): 読み込むファイルの日付。省略した場合は最新のファイルを取得する。

    Returns:
        list[UrlsInProfile]: 取得したURLの一覧。
    """

    PROFILE: CreatorGet = read_creator_profile(creator_id, date)

    urls: list[UrlsInProfile] = []

    # アイコン画像
    icon_url = PROFILE["user"]["iconUrl"]
    if icon_url is not None:
        urls.append({
            "type": "icon",
            "url": icon_url
        })

    # カバー画像
    cover_url = PROFILE["coverImageUrl"]
    if cover_url is not None:
        urls.append({
            "type": "cover",
            "url": cover_url
        })

    # ポートフォリオ画像
    for item in PROFILE["profileItems"]:
        if item["type"] != "image":
            # 外部サイトの動画・音楽埋め込みのダウンロードには対応していないので、スキップする。
            continue

        # サムネイル画像
        thumb_url = item["thumbnailUrl"]
        urls.append({
            "type": "thumbnails",
            "url": thumb_url
        })

        # 元画像
        image_url = item["imageUrl"]
        urls.append({
            "type": "images",
            "url": image_url
        })

    return urls


def extract_url_from_post(
    creator_id: str, post_id: str, date: Optional[int] = None
) -> list[UrlsInPost]:
    """保存済みの投稿データからダウンロード可能なURLを抽出します。

    Args:
        creator_id (str): クリエイターID。
        post_id (str): 投稿ID。
        date (Optional[int], optional):読み込むファイルの日付。省略した場合は最新のファイルを取得する。

    Returns:
        list[UrlsInPost]: 取得したURLの一覧。
    """
    POST: Info = read_postinfo(creator_id, post_id, date)

    urls: list[UrlsInPost] = []

    # カバー画像
    cover_url = POST["coverImageUrl"]
    if cover_url is not None:
        urls.append({
            "type": "cover",
            "url": cover_url
        })

    if POST["type"] == "article":
        # ブログタイプの投稿
        # 画像
        image_map = POST["body"]["imageMap"]
        for image_item in image_map.values():
            thumbnail = image_item["thumbnailUrl"]
            original = image_item["originalUrl"]
            urls.extend([{
                "type": "thumbnails",
                "url": thumbnail
            }, {
                "type": "images",
                "url": original
            }])

        # ファイル
        file_map = POST["body"]["fileMap"]
        for file_item in file_map.values():
            file = file_item["url"]
            urls.append({
                "type": "files",
                "url": file
            })

    elif POST["type"] == "image":
        # 画像タイプの投稿
        images = POST["body"]["images"]
        for image_item in images:
            thumbnail = image_item["thumbnailUrl"]
            original = image_item["originalUrl"]
            urls.extend([{
                "type": "thumbnails",
                "url": thumbnail
            }, {
                "type": "images",
                "url": original
            }])

    elif POST["type"] == "file":
        files = POST["body"]["files"]
        for file_item in files:
            file = file_item["url"]
            urls.append({
                "type": "files",
                "url": file
            })

    elif POST["type"] == "text":
        # テキストタイプの投稿
        # 取得可能なファイルが無い
        pass

    elif POST["type"] == "video":
        # 動画・音声タイプの投稿
        # 外部サイトの動画・音楽埋め込みのダウンロードには対応していないのでスキップ
        pass

    return urls
