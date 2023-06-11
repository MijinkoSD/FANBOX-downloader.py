from urllib.parse import urljoin

from src.types_py.rest.post import PagenateCreator, ListCreator, Info
from .common import BASE_URL
from .session import Session
from .args import Args


class Post(Session):
    def __init__(self, args: Args, creator_id: str) -> None:
        super().__init__(args=args, creator_id=creator_id)

    def paginate_creator(self) -> PagenateCreator:
        """post.paginateCreatorを叩いて全ページのURLを取得する。"""
        # self._log("投稿データを確認中...")
        url = urljoin(BASE_URL, "post.paginateCreator")
        payload = {"creatorId": self.creator_id}
        json: PagenateCreator = self._download_json(
            url, params=payload)
        return json

    def list_creator(self, payload: dict[str, str]) -> ListCreator:
        """目次用の簡易投稿データをダウンロードします。

        Args:
            payload (dict[str, str], optional): URLパラメータ。

        Returns:
            ListCreator: 取得したデータ。
        """
        url = urljoin(BASE_URL, "post.listCreator")
        json: ListCreator = self._download_json(
            url, params=payload)
        return json

    def list_creator_by_full_url(self, paginate_url: str) -> ListCreator:
        payload = self._parse_url_query(paginate_url)
        json = self.list_creator(payload=payload)
        return json

    def info(self, post_id: str) -> Info:
        url = urljoin(BASE_URL, "post.info")
        payload = {"postId": post_id}
        json: Info = self._download_json(url, params=payload)
        return json
