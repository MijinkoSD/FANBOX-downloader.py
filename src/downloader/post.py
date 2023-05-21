import os
import re
import urllib.parse as urlparse
from typing import Any, Optional
from time import sleep

import requests

from .fanbox import BASE_URL, BASE_LOCAL_DIR, BASE_LOCAL_PROFILE_DIR, WAIT_TIME
from .util import time_now, save_json
from .session import Session


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
        query = urlparse.parse_qs(urlparse.urlparse(url).query)
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
                    path=filedir, pattern=r"^\d{14}\.json$")
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
