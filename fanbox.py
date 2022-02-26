#!/usr/bin/env python3
from time import sleep
from typing import AnyStr
import os
import json
import argparse
import datetime
import re
from unicodedata import category

import requests
import urllib.parse


BASE_URL = "https://api.fanbox.cc/"
BASE_LOCAL_DIR = "./posts/"


def save_json(data:dict, dir:str):
    with open(dir, mode="wt", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def time_now(utc_add=9) -> int:
    """現在時刻を表す数値を返す"""
    now = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=utc_add)))
    return int(now.strftime('%Y%m%d%H%M%S'))

def print_with_timestamp(value:str, utc_add=9) -> None:
    """頭に時刻表記を追加したうえでprintする。"""
    now = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=utc_add)))
    timestamp = now.strftime('[%Y/%m/%d %H:%M:%S] ')
    print(timestamp+str(value))

WAIT_TIME = 1

class Post:
    def __init__(self, args:argparse.Namespace={}, FANBOXSESSID:str="", log_to_stdout:bool=False):
        self.args = args
        self.session = requests.Session()
        if FANBOXSESSID: self.sessid = FANBOXSESSID
        else: self.sessid = ""
        self.session.headers = {
            "accept"         : "application/json, text/plain, */*",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "ja,en-US;q=0.9,en;q=0.8",
            "origin"         : "https://www.fanbox.cc",
            "referer"        : "https://www.fanbox.cc/",
            "user-agent"     : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36"
        }
        self.is_print_log = log_to_stdout

    @property
    def sessid(self):
        """FANBOXSESSID"""
        return self.session.cookies.get("FANBOXSESSID")
    
    @sessid.setter
    def sessid(self, value):
        """FANBOXSESSID"""
        self.session.cookies.set("FANBOXSESSID", value, domain='.fanbox.cc')

    def __log(self, value:str, utc_add=9):
        """タイムスタンプをつけてログを出力する。"""
        if self.is_print_log:
            print_with_timestamp(value=value, utc_add=utc_add)

    def download(self, creatorId:str, page_limit:int|None = None) -> None:
        "投稿データのダウンロードから保存までを全部自動でやってくれるありがたい関数。"
        data = self.download_posts(self.get_paginateCreator(creatorId=creatorId),limit=page_limit)
        self.save_post(data, creator_id=creatorId)

    def get_paginateCreator(self, creatorId:str) -> dict:
        """post.paginateCreatorを叩いて全ページのURLを取得する。"""
        self.__log("クリエイター情報をダウンロード中...")
        url = BASE_URL+"post.paginateCreator"
        payload = {"creatorId":creatorId}
        return self.__download_json(url, params=payload)
    
    def get_listCreator(self, **kwargs) -> dict:
        """post.listCreatorを叩いてページの詳細情報を取得する。"""
        url = BASE_URL+"post.listCreator"
        payload = kwargs
        return self.__download_json(url, params=payload)

    def __query_parse(self, url:str) -> dict[AnyStr]:
        """URLについているパラメータを返す"""
        query = urllib.parse.parse_qs(urllib.parse.urlparse(url).query)
        for k in query:
            query[k] = query[k][0]
        return query

    def __download_json(self, url, **kwargs) -> dict:
        """指定されたURLからJSONをダウンロードする。"""
        r = self.session.get(url, **kwargs)
        try:
            r.raise_for_status()
        except requests.RequestException as e:
            print("Error: HTTP Status Code: " + str(r.status_code))
            return {}
        return r.json()

    def download_posts(self, paginate:dict, limit=None) -> list:
        """投稿データを全てダウンロードして返します。"""
        posts = []
        if limit is None: limit = len(paginate["body"])
        for i in range(limit):
            self.__log( "投稿データをダウンロード中...(%d/%d件)" % (i+1, limit) )
            param = self.__query_parse(paginate["body"][i])
            posts += self.get_listCreator(**param)["body"]["items"]
            sleep(WAIT_TIME)
        return posts

    def save_post(self, data:list, creator_id:str) -> None:
        """ダウンロードした投稿データをローカルに保存します。"""
        filedir = os.path.join(BASE_LOCAL_DIR, "%s_%d.json" % (creator_id, time_now()))
        save_json(data, filedir)

class File:
    def __init__(self, args:argparse.Namespace={}, FANBOXSESSID:str="", log_to_stdout:bool=False):
        self.args = args
        self.session = requests.Session()
        if FANBOXSESSID: self.sessid = FANBOXSESSID
        else: self.sessid = ""
        self.session.headers = {
            "accept"         : "application/json, text/plain, */*",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "ja,en-US;q=0.9,en;q=0.8",
            "origin"         : "https://www.fanbox.cc",
            "referer"        : "https://www.fanbox.cc/",
            "user-agent"     : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36"
        }
        self.is_print_log = log_to_stdout
    
    @property
    def sessid(self):
        """FANBOXSESSID"""
        return self.session.cookies.get("FANBOXSESSID")
    
    @sessid.setter
    def sessid(self, value):
        """FANBOXSESSID"""
        self.session.cookies.set("FANBOXSESSID", value, domain='.fanbox.cc')
    
    def __log(self, value:str, utc_add=9):
        """タイムスタンプをつけてログを出力する。"""
        if self.is_print_log:
            print_with_timestamp(value=value, utc_add=utc_add)

    def download(self, creatorId:str):
        "添付ファイルのダウンロードから保存までを全部自動でやってくれるありがたい関数。"
        data = self.getpostdata(creatorId=creatorId)
        self.download_files(postdata=data, creatorId=creatorId)

    def __search_post_filename(self, creatorId:str, date:int=None) -> str:
        """
        指定した投稿者のダウンロード済みの投稿データの中からファイル名を1つ返します。

        dateを省略した場合は一番新しい日付時刻のファイル名を返します。
        

        Params
        --------
        creatorId:
            投稿者のID。
        date:
            日付時刻を指定します。
            `YYYYMMDDhhmmss`の形式で渡さなければなりません。
            合致するファイルがない場合はNoneを返します。
            省略した場合は存在するファイルのうち一番最新のものを返します。
        """
        def isfile(basedir, file) -> bool:
            return os.path.isfile(os.path.join(basedir, file))
        
        if date is None:
            files = os.listdir(path=BASE_LOCAL_DIR)
            patten = re.compile("^" + re.escape(creatorId) + "_\d{14}\.json$")
            files = [f for f in files if isfile(BASE_LOCAL_DIR, f) and bool(patten.match(f))]
            if files:
                return sorted(files)[0]
            else:
                raise FileNotFoundError("保存済みの%sの投稿データが見つかりませんでした。" % creatorId)
        else:
            file = creatorId+str(date)+".json"
            if isfile(BASE_LOCAL_DIR, file):
                return file
            else:
                raise FileNotFoundError("%sというファイルが見つかりませんでした。" % file)

    def getpostdata(self, creatorId:str) -> list:
        """最新の投稿データを読み込み、そのデータを返します。"""
        filedir = os.path.join(BASE_LOCAL_DIR,
                               self.__search_post_filename(creatorId=creatorId))
        with open(filedir, mode="rt", encoding="utf-8") as f:
            return json.load(f)
    
    def __extract_file_url(self, postdata:list) -> dict[str, dict[str, list[str]]]:
        """
        投稿データからダウンロード可能なURL（主に画像やファイルのもの）を返します。
        
        なお、ブログタイプの投稿に含まれるファイル・埋め込み、
        テキストタイプ、動画・音楽タイプの投稿に含まれるファイルは未確認のため対応していません。
        """

        urldata = {}
        for d in postdata:
            id = d["id"]
            urldata[id] = {"image":[], "cover":[], "thumb":[], "file":[]} # 空であろうと必ずリスト型を保つ。
            if d["coverImageUrl"] is not None:
                urldata[id]["cover"] = [d["coverImageUrl"]]
            if "files" in d["body"]:
                urldata[id]["file"] += [u["url"] for u in d["body"]["files"] if "url" in u]
            if "images" in d["body"]:
                urldata[id]["image"] += [u["originalUrl"] for u in d["body"]["images"] if "originalUrl" in u]
                urldata[id]["thumb"] += [u["thumbnailUrl"] for u in d["body"]["images"] if "thumbnailUrl" in u]
            if "imageMap" in d["body"]:
                urldata[id]["image"] += [u["originalUrl"] for u in d["body"]["imageMap"].values() if "originalUrl" in u]
                urldata[id]["thumb"] += [u["thumbnailUrl"] for u in d["body"]["imageMap"].values() if "thumbnailUrl" in u]
            # if "fileMap" in d["body"]:
            # if "embedMap" in d["body"]:
            # if "urlEmbedMap" in d["body"]:
        return urldata

    def __get_urls_len(self, urls:dict[str, dict[str, list[str]]]) -> int:
        """URLをまとめた変数の中にあるURLの数を数えます。"""
        count = 0
        for i in urls.values():
            for k in i:
                count += len(i[k])
        return count

    def download_files(self, postdata:dict, creatorId:str) -> None:
        """投稿データから添付ファイルや画像等をダウンロードします。"""
        def save(urls:list[str], postid:str, filetype:str, count:int) -> int:
            """画像をダウンロードして保存する"""
            if not urls: return count
            dir = os.path.join(BASE_LOCAL_DIR, creatorId, postid, filetype)
            os.makedirs(dir, exist_ok=True)
            for url in urls:
                count += 1
                self.__log("ファイルをダウンロード中...(%d/%d件)" % (count, max_count))
                try:
                    r = self.session.get(url, timeout=(6.0, 12.0))
                except requests.exceptions.Timeout:
                    self.__log("接続がタイムアウトしました。")
                    self.__log("　URL: " + url)
                    sleep(WAIT_TIME)
                    continue
                except ConnectionError as e:
                    self.__log("通信が切断されました。")
                    self.__log("　URL: " + url)
                    self.__log("　例外: " + e)
                    sleep(WAIT_TIME)
                    continue
                try:
                    r.raise_for_status()
                except requests.RequestException as e:
                    self.__log("ファイルの取得に失敗しました。")
                    self.__log("　ステータスコード: " + str(r.status_code))
                with open(os.path.join(dir, os.path.basename(url)), mode="wb") as f:
                    f.write(r.content)
                sleep(WAIT_TIME)
            return count

        count = 0
        urls = self.__extract_file_url(postdata=postdata)
        max_count = self.__get_urls_len(urls)
        for postid, t in urls.items():
            os.makedirs(os.path.join(BASE_LOCAL_DIR, creatorId, postid), exist_ok=True)
            count = save(t["image"], postid=postid, filetype="images", count=count)
            count = save(t["cover"], postid=postid, filetype="cover", count=count)
            count = save(t["thumb"], postid=postid, filetype="thumbnail", count=count)
            count = save(t["file"], postid=postid, filetype="files", count=count)