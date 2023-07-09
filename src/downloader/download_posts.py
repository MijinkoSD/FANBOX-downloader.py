from typing import Optional
from time import sleep

from src.types_py.rest.post import ListCreator
from .common import WAIT_TIME_JSON
from .file import save_creator_profile, save_postlist, save_postinfo, \
    is_exist_post
from .rest import Post, Creator


class DownloadPosts(Creator, Post):
    """FANBOXの投稿の内、ファイル以外の要素（文章やページを構成するデータ）を取得するクラスです。"""

    def download(self, page_limit: Optional[int] = None) -> None:
        "投稿データのダウンロードから保存までを全部自動でやってくれるありがたい関数。"
        # TODO: ダウンロード件数を集計して
        # クリエイター情報の取得
        creator_profile = self.get_creator()
        save_creator_profile(creator_profile)

        # 投稿データ一覧の取得
        if page_limit is not None and page_limit == 0:
            return
        self._log("投稿データを確認中...")
        paginate = self.paginate_creator()
        if page_limit is None:
            page_limit = len(paginate)
        postlist: ListCreator = ListCreator({"items": [], "nextUrl": ""})
        for i, url in enumerate(paginate):
            self._log("投稿データ一覧を取得中...(%d/%d件)" % (i+1, page_limit))
            _postlist = self.list_creator_by_full_url(url)
            postlist["items"].extend(_postlist["items"])
            postlist["nextUrl"] = _postlist["nextUrl"]
            sleep(WAIT_TIME_JSON)
            if i+1 >= page_limit:
                # 予め指定された取得上限を突破した場合は中断する。
                break
        save_postlist(
            items=postlist["items"],
            creator_id=self.creator_id
        )

        # 投稿データの取得
        post_item_len = len(postlist["items"])
        for i, post_item in enumerate(postlist["items"]):
            post_id = post_item["id"]
            if (
                not self.args["force_update"]
                and is_exist_post(
                    creator_id=post_item["creatorId"],
                    post_id=post_item["id"])
            ):
                # 強制的に上書きするフラグが無効で、なおかつ取得しようとしたファイルが既に保存されていた場合
                self._log("投稿データのダウンロードをスキップ(%d/%d件)" % (i+1, post_item_len))
                continue
            self._log("投稿データをダウンロード中...(%d/%d件)" % (i+1, post_item_len))
            post_info = self.info(post_id=post_id)
            save_postinfo(postinfo=post_info)
            sleep(WAIT_TIME_JSON)
