#!/usr/bin/env python3
import sys
import argparse

import fanbox

module_description='''
吾輩はFANBOXダウンローダー。
説明はまだ無い。
'''

#やけにオプション引数が多い（TODO代わり）
parser = argparse.ArgumentParser(description=module_description, formatter_class=argparse.RawDescriptionHelpFormatter)
parser.add_argument("-s", "--session-id", type=str, help="FANBOXSESSID（FANBOXのセッションID）を設定します。有料プランの投稿をダウンロードするには必須です。")
# parser.add_argument("-f", "--force-update", action="store_true", help="以前ダウンロードしたコンテンツも上書きして再ダウンロードします。")
# parser.add_argument("-b", "--before-id", type=int, help="指定した投稿ID以前（その投稿も含む）の投稿をダウンロードします。")
# parser.add_argument("-l", "--limit", type=int, help="1投稿者あたりの取得数。省略した場合は可能な限り取得します。")
# parser.add_argument("--ignore-free-posts", action="store_true", help="無料の投稿に含まれる画像はダウンロードしません。")
# parser.add_argument("--ignore-adult-contents", action="store_true", help="成人向けの投稿に含まれる画像はダウンロードしません。")
# parser.add_argument("--include-higher-plan", action="store_true", help="未加入のプラン投稿も可能な限りダウンロードします。基本的にはサムネイルとタイトルのみが取得できるはずです。")
parser.add_argument("creator_id", nargs="+", type=str, help="投稿者のID")

if len(sys.argv) <= 1:
    parser.print_help()
    exit()
args = parser.parse_args()

if args.session_id is None:
    sessid = ""
else:
    sessid = args.session_id

for cid in args.creator_id:
    fb = fanbox.Post(creator_id=cid, args=args, FANBOXSESSID=sessid, log_to_stdout=True)
    fb.download()
    sessid = fb.sessid
    fb = fanbox.File(creator_id=cid, args=args, FANBOXSESSID=sessid, log_to_stdout=True)
    fb.download()
    sessid = fb.sessid
