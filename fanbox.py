#!/usr/bin/env python3
from time import sleep
from typing import Any, AnyStr
import os
import json
import argparse
import datetime
import re
import urllib.parse

import requests


BASE_URL = "https://api.fanbox.cc/"
BASE_LOCAL_DIR = "./posts/"


def save_json(data:Any, dir:str):
    """変数の中身をjsonファイルに保存します。"""
    os.makedirs(os.path.dirname(dir), exist_ok=True)
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

WAIT_TIME = 0.2

class Post:
    def __init__(self, creator_id:str, args:argparse.Namespace={}, FANBOXSESSID:str="", log_to_stdout:bool=False):
        """FANBOXの投稿の内、ファイル以外の要素（文章やページを構成するデータ）を取得するクラスです。"""
        self.creator_id = creator_id
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

    def download(self, page_limit:int|None = None) -> None:
        "投稿データのダウンロードから保存までを全部自動でやってくれるありがたい関数。"
        data = self.get_creator_get()
        self.save_post(data, filename="%s_profile_%d.json")
        if page_limit is int:
            if page_limit == 0: return
        data = self.download_postlist(self.get_paginateCreator(),limit=page_limit)
        self.save_post(data)

    def get_paginateCreator(self) -> dict:
        """post.paginateCreatorを叩いて全ページのURLを取得する。"""
        self.__log("投稿データを確認中...")
        url = BASE_URL+"post.paginateCreator"
        payload = {"creatorId":self.creator_id}
        return self.__download_json(url, params=payload)
    
    def get_listCreator(self, **kwargs) -> dict:
        """post.listCreatorを叩いてページの詳細情報を取得する。"""
        url = BASE_URL+"post.listCreator"
        payload = kwargs
        return self.__download_json(url, params=payload)
    
    def get_creator_get(self) -> dict:
        """creator.getを叩いてクリエイターのFANBOX上のプロフィールなどを取得する。"""
        self.__log("プロフィール情報をダウンロード中...")
        url = BASE_URL+"creator.get"
        payload = {"creatorId": self.creator_id}
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

    def download_postlist(self, paginate:dict, limit=None) -> list:
        """投稿データ一覧を全てダウンロードして返します。"""
        posts = []
        if limit is None: limit = len(paginate["body"])
        for i in range(limit):
            self.__log( "投稿データをダウンロード中...(%d/%d件)" % (i+1, limit) )
            param = self.__query_parse(paginate["body"][i])
            posts += self.get_listCreator(**param)["body"]["items"]
            sleep(WAIT_TIME)
        return posts

    def save_post(self, data:list, filename="%s_%d.json") -> None:
        """
        ダウンロードした投稿データをローカルに保存します。
        
        Params
        -------
        data:
            保存するデータ。
        filename:
            保存するときのファイル名。
        """
        filedir = os.path.join(BASE_LOCAL_DIR, filename % (self.creator_id, time_now()))
        save_json(data, filedir)

class File:
    def __init__(self, creator_id:str, args:argparse.Namespace={}, FANBOXSESSID:str="", log_to_stdout:bool=False):
        """FANBOXの投稿の内、ファイルや画像を取得するクラスです。"""
        self.creator_id = creator_id
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

    def download(self):
        "添付ファイルのダウンロードから保存までを全部自動でやってくれるありがたい関数。"
        data = self.getprofiledata()
        self.download_files_on_profile(profiledata=data)
        data = self.getpostdata()
        self.download_files(postdata=data)

    def __search_post_filename(self, creator_id:str, date:int=None) -> str:
        """
        指定した投稿者のダウンロード済みの投稿データの中からファイル名を1つ返します。

        dateを省略した場合は一番新しい日付時刻のファイル名を返します。
        

        Params
        --------
        creator_id:
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
            patten = re.compile("^" + re.escape(creator_id) + "_\d{14}\.json$")
            files = [f for f in files if isfile(BASE_LOCAL_DIR, f) and bool(patten.match(f))]
            if files:
                return sorted(files, reverse=True)[0]
            else:
                raise FileNotFoundError("保存済みの%sの投稿データが見つかりませんでした。" % creator_id)
        else:
            file = creator_id+"_"+str(date)+".json"
            if isfile(BASE_LOCAL_DIR, file):
                return file
            else:
                raise FileNotFoundError("%sというファイルが見つかりませんでした。" % file)

    def __search_profile_filename(self, creator_id:str, date:int=None) -> str:
        """
        指定した投稿者のダウンロード済みの投稿データの中からファイル名を1つ返します。

        dateを省略した場合は一番新しい日付時刻のファイル名を返します。


        Params
        --------
        creator_id:
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
            patten = re.compile("^" + re.escape(creator_id) + "_profile_\d{14}\.json$")
            files = [f for f in files if isfile(BASE_LOCAL_DIR, f) and bool(patten.match(f))]
            if files:
                return sorted(files, reverse=True)[0]
            else:
                raise FileNotFoundError("保存済みの%sのプロフィールデータが見つかりませんでした。" % creator_id)
        else:
            file = creator_id+"_profile_"+str(date)+".json"
            if isfile(BASE_LOCAL_DIR, file):
                return file
            else:
                raise FileNotFoundError("%sというファイルが見つかりませんでした。" % file)
    
    def getpostdata(self) -> list:
        """最新の投稿データを読み込み、そのデータを返します。"""
        filedir = os.path.join(BASE_LOCAL_DIR,
                               self.__search_post_filename(creator_id=self.creator_id))
        with open(filedir, mode="rt", encoding="utf-8") as f:
            return json.load(f)
    
    def getprofiledata(self) -> list:
        """最新のプロフィールデータを読み込み、そのデータを返します。"""
        filedir = os.path.join(BASE_LOCAL_DIR,
                               self.__search_profile_filename(creator_id=self.creator_id))
        with open(filedir, mode="rt", encoding="utf-8") as f:
            return json.load(f)
    
    def __extract_file_url(self, data:list) -> dict[str, dict[str, list[str]]]:
        """
        投稿データからダウンロード可能なURL（主に画像やファイルのもの）を返します。
        
        なお、ブログタイプの投稿に含まれるファイル・埋め込み、
        テキストタイプ、動画・音楽タイプの投稿に含まれるファイルは未確認のため対応していません。

        Return
        -------
        ```json
        {
            <post_id>: {
                "image":[<URL>],
                "cover":[<URL>],
                "thumb":[<URL>],
                "file" :[<URL>]
            }
        }
        ```
        """
        urldata = {}
        for d in data:
            id = d["id"]
            urldata[id] = {"image":[], "cover":[], "thumb":[], "file":[]} # 空であろうと必ずリスト型を保つ。
            if d["coverImageUrl"] is not None:
                urldata[id]["cover"] += [d["coverImageUrl"]]
            if d["body"] is None: continue # d["body"]の中身が空の場合は何もしない。
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
    
    def __extract_profile_url(self, data:list) -> dict[str, list[str]]:
        """
        プロフィールデータからダウンロード可能なURL（主に画像やファイルのもの）を返します。
        
        Return
        --------
        ```json
        {
            "image":[<URL>],
            "cover":[<URL>],
            "thumb":[<URL>],
            "icon" :[<URL>]
        }
        ```
        """
        urldata = {"image":[], "cover":[], "thumb":[], "icon":[]} # 空であろうと必ずリスト型を保つ。
        if data["body"]["user"]["iconUrl"] is not None:
            urldata["icon"] += [data["body"]["user"]["iconUrl"]]
        if data["body"]["coverImageUrl"] is not None:
            urldata["cover"] += [data["body"]["coverImageUrl"]]
        urldata["image"] = [u["imageUrl"] for u in data["body"]["profileItems"] if "imageUrl" in u]
        urldata["thumb"] = [u["thumbnailUrl"] for u in data["body"]["profileItems"] if "thumbnailUrl" in u]
        return urldata

    def __get_urls_len(self, urls:dict[str, dict[str, list[str]]]) -> int:
        """URLをまとめた変数の中にある要素の数を数えます。"""
        count = 0
        if type(urls) is dict:
            for v in urls.values():
                count += self.__get_urls_len(v)
        elif type(urls) is list:
            for v in urls:
                count += self.__get_urls_len(v)
        elif type(urls) is str:
            count += 1
        return count

    def download_files(self, postdata:dict) -> None:
        """投稿データから添付ファイルや画像等をダウンロードします。"""
        def save(urls:list[str], postid:str, filetype:str, count:int) -> int:
            """画像をダウンロードして保存する"""
            if not urls: return count
            dir = os.path.join(BASE_LOCAL_DIR, self.creator_id, postid, filetype)
            os.makedirs(dir, exist_ok=True)
            for url in urls:
                count += 1
                if (os.path.isfile(os.path.join(dir, os.path.basename(url)))
                        and not self.args.force_update):
                    self.__log("ファイルのダウンロードをスキップ(%d/%d件)" % (count, max_count))
                    continue
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
        urls = self.__extract_file_url(data=postdata)
        max_count = self.__get_urls_len(urls)
        for postid, t in urls.items():
            if self.__get_urls_len(t) == 0: continue
            os.makedirs(os.path.join(BASE_LOCAL_DIR, self.creator_id, postid), exist_ok=True)
            count = save(t["image"], postid=postid, filetype="images", count=count)
            count = save(t["cover"], postid=postid, filetype="cover", count=count)
            count = save(t["thumb"], postid=postid, filetype="thumbnails", count=count)
            count = save(t["file"], postid=postid, filetype="files", count=count)

    def download_files_on_profile(self, profiledata:dict) -> None:
        """プロフィールに含まれるファイルをダウンロードします。"""
        def save(urls:list[str], filetype:str, count:int) -> int:
            """画像をダウンロードして保存する"""
            if not urls: return count
            dir = os.path.join(BASE_LOCAL_DIR, "profile", self.creator_id, filetype)
            os.makedirs(dir, exist_ok=True)
            for url in urls:
                count += 1
                if (os.path.isfile(os.path.join(dir, os.path.basename(url)))
                        and not self.args.force_update):
                    self.__log("プロフィール画像のダウンロードをスキップ(%d/%d件)" % (count, max_count))
                    continue
                self.__log("プロフィール画像をダウンロード中...(%d/%d件)" % (count, max_count))
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
        urls = self.__extract_profile_url(data=profiledata)
        max_count = self.__get_urls_len(urls)
        os.makedirs(os.path.join(BASE_LOCAL_DIR, "profile", self.creator_id), exist_ok=True)
        count = save(urls["image"], filetype="images", count=count)
        count = save(urls["cover"], filetype="cover", count=count)
        count = save(urls["thumb"], filetype="thumbnails", count=count)
        count = save(urls["icon"], filetype="icon", count=count)