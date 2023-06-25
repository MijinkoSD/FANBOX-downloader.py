from urllib.parse import urljoin

from src.types_py.rest.creator import Get
from .common import BASE_URL
from .session import Session
from .args import Args


class Creator(Session):
    def __init__(self, args: Args, creator_id: str) -> None:
        super().__init__(args=args, creator_id=creator_id)

    def get_creator(self) -> Get:
        """クリエイターのプロフィールなどを取得する。"""
        self._log("プロフィール情報をダウンロード中...")
        url = urljoin(BASE_URL, "creator.get")
        payload = {"creatorId": self.creator_id}
        json: Get = self._download_json(url, params=payload)
        return json
