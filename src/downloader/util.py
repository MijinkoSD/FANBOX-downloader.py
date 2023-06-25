#!/usr/bin/env python3
import datetime


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
