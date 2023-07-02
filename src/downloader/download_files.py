
from .rest import Session


class DownloadFiles(Session):
    def download(self) -> None:
        "添付ファイルのダウンロードから保存までを全部自動でやってくれるありがたい関数。"

        # 投稿データ・プロフィールデータを読み込む
        # 各種ファイルのURLを抽出
        # URLからファイルを保存し、各種フォルダに振り分ける
        # ダウンロード結果（失敗数など）を返却する

    # TODO: file_.pyを再構築する。ファイル・画像の類をダウンロードできるようにする。
