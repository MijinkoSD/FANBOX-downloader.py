import os
import re
import json
from typing import Any
from time import sleep

import requests

from .fanbox import BASE_LOCAL_DIR, BASE_LOCAL_PROFILE_DIR, WAIT_TIME
from .session import Session
from .file_type import ExtractFileURLData


class File(Session):
    """FANBOXの投稿の内、ファイルや画像を取得するクラスです。"""

    def download(self) -> None:
        "添付ファイルのダウンロードから保存までを全部自動でやってくれるありがたい関数。"
        data = self.get_profile()
        self.download_files_on_profile(profiledata=data)
        # data = self.get_postlist()
        self.download_files_all()

    def __search_latest_filename(
            self, path: str = BASE_LOCAL_DIR, pattern: str = ""
    ) -> str:
        """
        指定したパターンに合致するファイルの中で一番新しいものを返します。

        Params
        --------
        path:
            検索するファイルが存在するディレクトリ。
        pattern:
            検索パターン。
        """
        def isfile(basedir: str, filename: str) -> bool:
            """パスがファイルかどうかを判別する"""
            return os.path.isfile(os.path.join(basedir, filename))

        files = os.listdir(path=path)
        patten = re.compile(pattern)
        files = [f for f in files if isfile(path, f) and bool(patten.match(f))]
        if files:
            return sorted(files, reverse=True)[0]
        else:
            raise FileNotFoundError(
                "保存済みのファイルが見つかりませんでした。\n"
                "  検索場所：%s\n"
                "  検索パターン：%s"
                % (path, pattern)
            )

    def get_postdata(self, postid: str) -> Any:
        """最新の投稿データを読み込み、そのデータを返します。"""
        pattern = r"^\d{14}\.json$"
        parentdir = os.path.join(
            BASE_LOCAL_DIR, self.creator_id, postid, "post")
        filename = self.__search_latest_filename(
            path=parentdir, pattern=pattern)
        filedir = os.path.join(parentdir, filename)
        with open(filedir, mode="rt", encoding="utf-8") as f:
            return json.load(f)

    def get_postlist(self) -> Any:
        """最新の投稿一覧のデータを読み込み、そのデータを返します。"""
        pattern = "^" + re.escape(self.creator_id) + r"_\d{14}\.json$"
        filedir = os.path.join(BASE_LOCAL_DIR,
                               self.__search_latest_filename(pattern=pattern))
        with open(filedir, mode="rt", encoding="utf-8") as f:
            return json.load(f)

    def get_profile(self) -> Any:
        """最新のプロフィールデータを読み込み、そのデータを返します。"""
        pattern = "^" + re.escape(self.creator_id) + r"_profile_\d{14}\.json$"
        filedir = os.path.join(
            BASE_LOCAL_PROFILE_DIR,
            self.__search_latest_filename(
                path=BASE_LOCAL_PROFILE_DIR,
                pattern=pattern))
        with open(filedir, mode="rt", encoding="utf-8") as f:
            return json.load(f)

    def __extract_file_url(self, data: Any) -> ExtractFileURLData:
        """
        投稿データからダウンロード可能なURL（主に画像やファイルのもの）を返します。

        なお、ブログタイプの投稿に含まれるファイル・埋め込み、
        テキストタイプ、動画・音楽タイプの投稿に含まれるファイルは未確認のため対応していません。

        Return
        -------
        ```json
        {
            "id"   :<post_id>,
            "image":[<URL>],
            "cover":[<URL>],
            "thumb":[<URL>],
            "file" :[<URL>]
        }
        ```
        """

        d = data["body"]
        body = d["body"]
        image, cover, thumb, file = [], [], [], []  # 空であろうと必ずリスト型を保つ。
        if d["coverImageUrl"] is not None:
            cover += [d["coverImageUrl"]]
        if body is not None:  # bodyの中身が空の場合は何もしない。
            if "files" in body:
                file = [u["url"] for u in body["files"] if "url" in u]
            if "images" in body:
                image = [u["originalUrl"]
                         for u in body["images"] if "originalUrl" in u]
                thumb = [u["thumbnailUrl"]
                         for u in body["images"] if "thumbnailUrl" in u]
            if "imageMap" in body:
                image = [u["originalUrl"]
                         for u in body["imageMap"].values()
                         if "originalUrl" in u]
                thumb = [u["thumbnailUrl"]
                         for u in body["imageMap"].values()
                         if "thumbnailUrl" in u]
            if "fileMap" in body:
                file = [u["url"]
                        for u in body["fileMap"].values() if "url" in u]
            # if "embedMap" in body:
            # if "urlEmbedMap" in body:
        return {
            "id": d["id"],
            "image": image,
            "cover": cover,
            "thumb": thumb,
            "file": file}

    def __extract_profile_url(self, data: Any) -> dict[str, list[str]]:
        """
        プロフィールデータからダウンロード可能なURL（主に画像やファイルのもの）を返します。

        Return
        --------
        ```json
        {
            "image":[<URL>],
            "cover":[<URL>],
            "thumb":[<URL>],
            "icon" :[<URL>]
        }
        ```
        """
        image, cover, thumb, icon = [], [], [], []  # 空であろうと必ずリスト型を保つ。
        body = data["body"]
        if body["user"]["iconUrl"] is not None:
            icon += [body["user"]["iconUrl"]]
        if body["coverImageUrl"] is not None:
            cover += [body["coverImageUrl"]]
        image = [u["imageUrl"]
                 for u in body["profileItems"] if "imageUrl" in u]
        thumb = [u["thumbnailUrl"]
                 for u in body["profileItems"] if "thumbnailUrl" in u]
        return {"image": image, "cover": cover, "thumb": thumb, "icon": icon}

    def __get_urls_len(
        self,
        urls: dict[str, dict[str, list[str]]]
        | dict[str, list[str]]
        | list[str]
        | str
    ) -> int:
        """URLをまとめた変数の中にある要素の数を数えます。"""
        count = 0
        if type(urls) is dict:
            for v in urls.values():
                count += self.__get_urls_len(v)
        elif type(urls) is list:
            for url in urls:
                count += self.__get_urls_len(url)
        elif type(urls) is str:
            count += 1
        return count

    def download_files_all(self) -> None:
        """最新の投稿一覧のデータを読み込み、全ての添付ファイルや画像等をダウンロードします。"""
        postlist = self.get_postlist()
        ids = [d["id"] for d in postlist]
        for i, id in enumerate(ids):
            self._log("投稿(%s)のダウンロードを開始(%d/%d件)" % (id, i+1, len(ids)))
            self.download_files(postid=id)

    def download_files(self, postid: str) -> None:
        """投稿データから添付ファイルや画像等をダウンロードします。"""
        def __get_filetype_name(filetype: str) -> str:
            """filetypeから日本語の名前を返す"""
            if filetype == "images":
                return "画像"
            elif filetype == "cover":
                return "カバー画像"
            elif filetype == "thumbnails":
                return "サムネイル画像"
            elif filetype == "files":
                return "ファイル"
            else:
                return "不明なファイル"

        def save(urls: list[str], postid: str, filetype: str) -> None:
            """画像をダウンロードして保存する"""
            if not urls:
                return
            dir = os.path.join(
                BASE_LOCAL_DIR, self.creator_id, postid, filetype)
            os.makedirs(dir, exist_ok=True)
            for url in urls:
                if (os.path.isfile(os.path.join(dir, os.path.basename(url)))
                        and not self.args.force_update):
                    self._log("%sのダウンロードをスキップ" % __get_filetype_name(filetype))
                    continue
                self._log("%sをダウンロード中..." % __get_filetype_name(filetype))
                try:
                    r = self.session.get(url, timeout=(6.0, 12.0))
                except requests.exceptions.Timeout:
                    self._log("接続がタイムアウトしました。"
                              "  URL: " + url)
                    sleep(WAIT_TIME)
                    continue
                except ConnectionError as e:
                    self._log("通信が切断されました。"
                              f"  URL: {url}"
                              f"  例外: {e}")
                    sleep(WAIT_TIME)
                    continue

                try:
                    r.raise_for_status()
                except requests.RequestException:
                    self._log("ファイルの取得に失敗しました。"
                              f"  ステータスコード: {str(r.status_code)}")
                with open(
                    os.path.join(dir, os.path.basename(url)), mode="wb"
                ) as f:
                    f.write(r.content)
                sleep(WAIT_TIME)

        postdata = self.get_postdata(postid=postid)
        t = self.__extract_file_url(data=postdata)
        # FIXME: mypyがt周りでエラーを吐いてしまっているので後日解消する
        if self.__get_urls_len({
                "image": t["image"],
                "cover": t["cover"],
                "thumb": t["thumb"],
                "file": t["file"]
        }) == 0:
            return
        os.makedirs(os.path.join(BASE_LOCAL_DIR,
                    self.creator_id, postid), exist_ok=True)
        save(t["image"], postid=t["id"], filetype="images")
        save(t["cover"], postid=t["id"], filetype="cover")
        save(t["thumb"], postid=t["id"], filetype="thumbnails")
        save(t["file"], postid=t["id"], filetype="files")

    def download_files_on_profile(self, profiledata: Any) -> None:
        """プロフィールに含まれるファイルをダウンロードします。"""
        def save(urls: list[str], filetype: str, count: int) -> int:
            """画像をダウンロードして保存する"""
            if not urls:
                return count
            dir = os.path.join(BASE_LOCAL_PROFILE_DIR,
                               self.creator_id, filetype)
            os.makedirs(dir, exist_ok=True)
            for url in urls:
                count += 1
                if (os.path.isfile(os.path.join(dir, os.path.basename(url)))
                        and not self.args.force_update):
                    self._log("プロフィール画像のダウンロードをスキップ(%d/%d件)" %
                              (count, max_count))
                    continue
                self._log("プロフィール画像をダウンロード中...(%d/%d件)" % (count, max_count))
                try:
                    r = self.session.get(url, timeout=(6.0, 12.0))
                except requests.exceptions.Timeout:
                    self._log("接続がタイムアウトしました。"
                              f"  URL: {url}")
                    sleep(WAIT_TIME)
                    continue
                except ConnectionError as e:
                    self._log("通信が切断されました。"
                              f"  URL: {url}"
                              f"  例外: {e}")
                    sleep(WAIT_TIME)
                    continue
                try:
                    r.raise_for_status()
                except requests.RequestException:
                    self._log("ファイルの取得に失敗しました。")
                    self._log("  ステータスコード: " + str(r.status_code))
                with open(
                        os.path.join(dir, os.path.basename(url)), mode="wb"
                ) as f:
                    f.write(r.content)
                sleep(WAIT_TIME)
            return count
        count = 0
        urls = self.__extract_profile_url(data=profiledata)
        max_count = self.__get_urls_len(urls)
        os.makedirs(os.path.join(BASE_LOCAL_PROFILE_DIR,
                    self.creator_id), exist_ok=True)
        count = save(urls["image"], filetype="images", count=count)
        count = save(urls["cover"], filetype="cover", count=count)
        count = save(urls["thumb"], filetype="thumbnails", count=count)
        count = save(urls["icon"], filetype="icon", count=count)
