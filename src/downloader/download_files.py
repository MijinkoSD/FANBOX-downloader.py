from traceback import format_exc
from time import sleep

import requests

from .common import WAIT_TIME_FILE
from .util import urlparse_filename
from .rest import Session
from .define.file import PROFILE_SUB_DIR_NAMES, POST_SUB_DIR_NAMES
from .define.stats import FileDownloadStats
from .file.extract_url import extract_url_from_profile, extract_url_from_post
from .file.extract_post_id import extract_post_id
from .file.exist import is_exist_profile_file, is_exist_post_file
from .file.save import save_file_by_profile, save_file_by_post


class DownloadFiles(Session):
    def download(self) -> None:
        "添付ファイルのダウンロードから保存までを全部自動でやってくれるありがたい関数。"

        # 投稿データ・プロフィールデータを読み込む
        # 各種ファイルのURLを抽出
        # URLからファイルを保存し、各種フォルダに振り分ける
        # ダウンロード結果（失敗数など）を返却する

        stats = self.download_profile_only()
        self._log(f'対象: {stats["try_count"]}, '
                  f'成功: {stats["success"]}, '
                  f'失敗: {stats["failure"]}, '
                  f'スキップ: {stats["skip"]}')
        stats = self.download_post_only()
        self._log(f'対象: {stats["try_count"]}, '
                  f'成功: {stats["success"]}, '
                  f'失敗: {stats["failure"]}, '
                  f'スキップ: {stats["skip"]}')

    def download_profile_only(self) -> FileDownloadStats:
        """プロフィールに関するファイルをダウンロードする。

        Returns:
            FileDownloadStats: ダウンロードの統計。
        """
        stats: FileDownloadStats = {
            "try_count": 0,
            "success": 0,
            "failure": 0,
            "skip": 0
        }

        self._log("%sのプロフィールデータを読み込み中" % self.creator_id)
        try:
            profile_urls = extract_url_from_profile(creator_id=self.creator_id)
        except Exception:
            self._log("プロフィールデータの読み込みに失敗しました。\n"
                      f"  クリエイターID: {self.creator_id}\n"
                      "  エラー:\n"
                      "    " + format_exc().replace("\n", "\n    "))
            return stats

        for i, item in enumerate(profile_urls):
            stats["try_count"] += 1
            file_type = item["type"]
            url = item["url"]
            file_name = urlparse_filename(url)
            is_exist = is_exist_profile_file(
                self.creator_id, file_type, file_name)

            # ログ出力
            if not self.args["force_update"] and is_exist:
                self._log("(%d/%d)プロフィールの%sのダウンロードをスキップ"
                          % (i,
                              len(profile_urls),
                              PROFILE_SUB_DIR_NAMES[file_type]))
            else:
                self._log("(%d/%d)プロフィールの%sをダウンロード中..."
                          % (i,
                              len(profile_urls),
                              PROFILE_SUB_DIR_NAMES[file_type]))

            # ファイルのダウンロード
            try:
                r = self.session.get(url, timeout=(6.0, 12.0))
            except requests.exceptions.Timeout:
                self._log("接続がタイムアウトしました。\n"
                          "  URL: " + url)
                stats["failure"] += 1
                sleep(WAIT_TIME_FILE)
                continue
            except ConnectionError:
                self._log("通信が切断されました。\n"
                          "  URL: " + url + "\n"
                          "  エラー内容:\n"
                          "    " + format_exc().replace("\n", "\n    "))
                stats["failure"] += 1
                sleep(WAIT_TIME_FILE)
                continue

            # ステータスコードチェック
            try:
                r.raise_for_status()
            except requests.RequestException:
                self._log("ファイルの取得に失敗しました。\n"
                          "  ステータスコード: " + str(r.status_code))
                stats["failure"] += 1
                sleep(WAIT_TIME_FILE)
                continue

            # ファイル保存
            try:
                save_file_by_profile(r.content, self.creator_id,
                                     file_type, file_name)
            except Exception:
                self._log("ファイルの保存に失敗しました。\n"
                          "  エラー内容:\n"
                          "    " + format_exc().replace("\n", "\n    "))
                stats["failure"] += 1
                sleep(WAIT_TIME_FILE)
                continue

            stats["success"] += 1
            sleep(WAIT_TIME_FILE)
        return stats

    def download_post_only(self) -> FileDownloadStats:
        """投稿に関するファイルをダウンロードする。

        Returns:
            FileDownloadStats: ダウンロードの統計。
        """
        stats: FileDownloadStats = {
            "try_count": 0,
            "success": 0,
            "failure": 0,
            "skip": 0
        }

        post_ids: list[str] = extract_post_id(self.creator_id)
        for i, post_id in enumerate(post_ids):
            self._log("(%d/%d)投稿データ(%s)を読み込み中" % (
                i, len(post_ids), post_id))

            try:
                post_urls = extract_url_from_post(
                    creator_id=self.creator_id, post_id=post_id)
            except Exception:
                self._log("投稿データの読み込みに失敗しました。\n"
                          f"  クリエイターID: {self.creator_id}\n"
                          f"  投稿ID: {post_id}"
                          "  エラー:\n"
                          "    " + format_exc().replace("\n", "\n    "))
                continue

            for i, item in enumerate(post_urls):
                file_type = item["type"]
                url = item["url"]
                file_name = urlparse_filename(url)
                is_exist = is_exist_post_file(
                    self.creator_id, post_id, file_type, file_name)
                stats["try_count"] += 1

                # ログ出力
                if not self.args["force_update"] and is_exist:
                    self._log("  (%d/%d)投稿の%sのダウンロードをスキップ"
                              % (i,
                                 len(post_urls),
                                 POST_SUB_DIR_NAMES[file_type]))
                    stats["skip"] += 1
                    continue
                else:
                    self._log("  (%d/%d)投稿の%sをダウンロード中..."
                              % (i,
                                 len(post_urls),
                                 POST_SUB_DIR_NAMES[file_type]))

                # ファイルのダウンロード
                try:
                    r = self.session.get(url, timeout=(6.0, 12.0))
                except requests.exceptions.Timeout:
                    self._log("  接続がタイムアウトしました。\n"
                              "    URL: " + url)
                    stats["failure"] += 1
                    sleep(WAIT_TIME_FILE)
                    continue
                except ConnectionError:
                    self._log(
                        "  通信が切断されました。\n"
                        "    URL: " + url + "\n"
                        "    エラー内容:\n"
                        "      " + format_exc().replace("\n", "\n      "))
                    stats["failure"] += 1
                    sleep(WAIT_TIME_FILE)
                    continue

                # ステータスコードチェック
                try:
                    r.raise_for_status()
                except requests.RequestException:
                    self._log("ファイルの取得に失敗しました。\n"
                              "  ステータスコード: " + str(r.status_code))
                    stats["failure"] += 1
                    sleep(WAIT_TIME_FILE)
                    continue

                # ファイル保存
                try:
                    save_file_by_post(r.content,
                                      self.creator_id,
                                      post_id,
                                      file_type,
                                      file_name)
                except Exception:
                    self._log("ファイルの保存に失敗しました。\n"
                              "  エラー内容:\n"
                              "    " + format_exc().replace("\n", "\n    "))
                    stats["failure"] += 1
                    sleep(WAIT_TIME_FILE)
                    continue

                stats["success"] += 1
                sleep(WAIT_TIME_FILE)

        return stats

    # TODO: file_.pyを再構築する。ファイル・画像の類をダウンロードできるようにする。
