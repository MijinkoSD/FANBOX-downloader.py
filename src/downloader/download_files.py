
from .rest import Session


class DownloadFiles(Session):
    def download(self) -> None:
        "添付ファイルのダウンロードから保存までを全部自動でやってくれるありがたい関数。"

    # TODO: file_.pyを再構築する。ファイル・画像の類をダウンロードできるようにする。
