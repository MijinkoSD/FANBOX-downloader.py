import argparse
from typing import Any

import requests

from .util import print_with_timestamp


class Session:
    """
    廃止予定
    移行先：.rest.session
    """

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
