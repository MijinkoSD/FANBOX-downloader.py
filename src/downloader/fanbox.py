#!/usr/bin/env python3
from time import sleep
from typing import Any, Optional
import os
import json
import argparse
import datetime
import re
import urllib.parse

import requests


BASE_URL = "https://api.fanbox.cc/"
BASE_LOCAL_DIR = "./posts/"
BASE_LOCAL_PROFILE_DIR = "./profile/"


def save_json(data: Any, dir: str) -> None:
    """変数の中身をjsonファイルに保存します。"""
    os.makedirs(os.path.dirname(dir), exist_ok=True)
    with open(dir, mode="wt", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def time_now(utc_add: int = 9) -> int:
    """現在時刻を表す数値を返す"""
    now = datetime.datetime.now(datetime.timezone(
        datetime.timedelta(hours=utc_add)))
    return int(now.strftime('%Y%m%d%H%M%S'))


def print_with_timestamp(value: str, utc_add: int = 9) -> None:
    """頭に時刻表記を追加した上でprintする。"""
    now = datetime.datetime.now(datetime.timezone(
        datetime.timedelta(hours=utc_add)))
    timestamp = now.strftime('[%Y/%m/%d %H:%M:%S] ')
    text = value.splitlines()
    if len(text) > 1:
        # 2行目以降は日付ではなく空白を入れる
        text = [text[0], *[' '*22 + t for t in text[1:]]]
    print(timestamp+"\n".join(text))


WAIT_TIME = 0.2


class Session:
    def __init__(self, creator_id: str,
                 args: argparse.Namespace = argparse.Namespace(),
                 FANBOXSESSID: str = "", log_to_stdout: bool = False):
        """APIと通信するための基本的な枠組みを提供する基底クラスです。"""
        self.creator_id = creator_id
        self.args = args
        self.session = requests.Session()
        if FANBOXSESSID:
            self.sessid = FANBOXSESSID
        else:
            self.sessid = ""
        self.session.headers = {
            "accept": "application/json, text/plain, */*",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "ja,en-US;q=0.9,en;q=0.8",
            "origin": "https://www.fanbox.cc",
            "referer": "https://www.fanbox.cc/",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 "
            "Safari/537.36"
        }
        self.is_print_log = log_to_stdout

    @property
    def sessid(self) -> Any:
        """FANBOXSESSID"""
        return self.session.cookies.get("FANBOXSESSID")

    @sessid.setter
    def sessid(self, value: str) -> None:
        """FANBOXSESSID"""
        self.session.cookies.set("FANBOXSESSID", value, domain='.fanbox.cc')

    def _log(self, value: str, utc_add: int = 9) -> None:
        """タイムスタンプをつけてログを出力する。"""
        if self.is_print_log:
            print_with_timestamp(value=value, utc_add=utc_add)


class Post(Session):
    """FANBOXの投稿の内、ファイル以外の要素（文章やページを構成するデータ）を取得するクラスです。"""

    def download(self, page_limit: Optional[int] = None) -> None:
        "投稿データのダウンロードから保存までを全部自動でやってくれるありがたい関数。"
        # クリエイター情報の取得
        data = self.get_creator_get()
        self.save_postlist(data, parentdir=BASE_LOCAL_PROFILE_DIR,
                           filename="%s_profile_%d.json")
        # 投稿データ一覧の取得
        if page_limit is not None:
            if page_limit == 0:
                return
        data = self.download_postlist(
            self.get_paginateCreator(), limit=page_limit)
        self.save_postlist(data)
        # 投稿データのダウンロード＆保存
        self.download_postdata_all(postlist=data)

    def get_paginateCreator(self) -> Any:
        """post.paginateCreatorを叩いて全ページのURLを取得する。"""
        self._log("投稿データを確認中...")
        url = BASE_URL+"post.paginateCreator"
        payload = {"creatorId": self.creator_id}
        return self.__download_json(url, params=payload)

    def get_listCreator(self, **kwargs: str) -> Any:
        """post.listCreatorを叩いてページ一覧の情報を取得する。"""
        url = BASE_URL+"post.listCreator"
        payload = kwargs
        return self.__download_json(url, params=payload)

    def get_creator_get(self) -> Any:
        """creator.getを叩いてクリエイターのFANBOX上のプロフィールなどを取得する。"""
        self._log("プロフィール情報をダウンロード中...")
        url = BASE_URL+"creator.get"
        payload = {"creatorId": self.creator_id}
        return self.__download_json(url, params=payload)

    def __query_parse(self, url: str) -> dict[str, str]:
        """URLについているパラメータを返す"""
        query = urllib.parse.parse_qs(urllib.parse.urlparse(url).query)
        result: dict[str, str] = {}
        for k in query:
            result[k] = query[k][0]
        return result

    def __download_json(self, url: str, **kwargs: Any) -> Any:
        """指定されたURLからJSONをダウンロードする。"""
        r = self.session.get(url, **kwargs)
        try:
            r.raise_for_status()
        except requests.RequestException:
            print("Error: HTTP Status Code: " + str(r.status_code))
            return {}
        return r.json()

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

    def download_postlist(
            self, paginate: Any, limit: Optional[int] = None
    ) -> list[Any]:
        """投稿データ一覧を全てダウンロードして返します。"""
        posts = []
        if limit is None:
            limit = len(paginate["body"])
        for i in range(limit):
            self._log("投稿データ一覧を取得中...(%d/%d件)" % (i+1, limit))
            param = self.__query_parse(paginate["body"][i])
            posts += self.get_listCreator(**param)["body"]["items"]
            sleep(WAIT_TIME/3)
        return posts

    def download_postdata_all(self, postlist: list[Any]) -> None:
        """投稿データ一覧を元に投稿データを取得して保存します。"""
        ids = [d["id"] for d in postlist]
        for i, id in enumerate(ids):
            filename = str(time_now()) + ".json"
            filedir = os.path.join(BASE_LOCAL_DIR, self.creator_id, id, "post")
            filepath = os.path.join(filedir, filename)
            try:
                self.__search_latest_filename(
                    path=filedir, pattern="^\d{14}\.json$")
            except FileNotFoundError:
                pass
            else:
                if not self.args.update_posts:
                    self._log("投稿データのダウンロードをスキップ(%d/%d件)" % (i+1, len(ids)))
                    continue

            self._log("投稿データをダウンロード中...(%d/%d件)" % (i+1, len(ids)))
            data = self.download_postdata(id)
            save_json(data, filepath)
            sleep(WAIT_TIME/3)

    def download_postdata(self, id: list[str]) -> Any:
        """投稿IDを元に投稿データを取得して返します。"""
        url = BASE_URL+"post.info"
        payload = {"postId": id}
        return self.__download_json(url, params=payload)

    def save_postlist(
            self,
            data: list[Any],
            parentdir: str = BASE_LOCAL_DIR,
            filename: str = "%s_%d.json"
    ) -> None:
        """
        ダウンロードした投稿データ一覧をローカルに保存します。

        Params
        -------
        data:
            保存するデータ。
        filename:
            保存するときのファイル名。
        """
        filedir = os.path.join(parentdir, filename %
                               (self.creator_id, time_now()))
        save_json(data, filedir)


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
        pattern = "^" + re.escape(self.creator_id) + "_\d{14}\.json$"
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

    def __extract_file_url(self, data: Any) -> dict[str, list[str] | str]:
        """
        投稿データからダウンロード可能なURL（主に画像やファイルのもの）を返します。

        なお、ブログタイプの投稿に含まれるファイル・埋め込み、
        テキストタイプ、動画・音楽タイプの投稿に含まれるファイルは未確認のため対応していません。

        Return
        -------
        ```json
        {
            "id"   :[<post_id>],
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
                with open(os.path.join(dir, os.path.basename(url)), mode="wb") as f:
                    f.write(r.content)
                sleep(WAIT_TIME)

        postdata = self.get_postdata(postid=postid)
        t = self.__extract_file_url(data=postdata)
        # TODO: mypyがt周りでエラーを吐いてしまっているので後日解消する
        if self.__get_urls_len(t) == 0:
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
