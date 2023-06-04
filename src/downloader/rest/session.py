from typing import Any
from urllib.parse import parse_qs, urlparse

import requests

from .common import Headers
from .args import Args
from ..util import print_with_timestamp


class Session:
    def __init__(self,
                 args: Args,
                 creator_id: str,
                 FANBOXSESSID: str = "", log_to_stdout: bool = False):
        """APIと通信するための基本的な枠組みを提供する基底クラスです。"""
        self.creator_id = creator_id
        self.args = args
        self.session = requests.Session()
        if FANBOXSESSID:
            self.sessid = FANBOXSESSID
        else:
            self.sessid = ""
        self.session.headers = Headers
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

    def _download_json(self, url: str, **kwargs: Any) -> Any:
        """指定されたURLからJSONをダウンロードする。"""
        r = self.session.get(url, **kwargs)
        try:
            r.raise_for_status()
        except requests.RequestException:
            print("Error: HTTP Status Code: " + str(r.status_code))
            return {}
        return r.json()

    @staticmethod
    def _parse_url_query(url: str) -> dict[str, str]:
        """URLについているパラメータを返す"""
        query = parse_qs(urlparse(url).query)
        result: dict[str, str] = {}
        for k in query:
            result[k] = query[k][0]
        return result
