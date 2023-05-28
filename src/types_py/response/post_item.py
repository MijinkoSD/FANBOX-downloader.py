from typing import TypedDict

from .user import User
from .cover import Cover


class PostItem(TypedDict):
    id: str
    """投稿のID。"""
    title: str
    """投稿のタイトル。"""
    feeRequired: int
    """
    閲覧に必要なプランの支援額。
    支援額がこの値未満なら閲覧できない。
    全体公開の投稿では0が格納される。
    """
    publishedDatetime: str
    """
    投稿日時。
    ISO 8601（"yyyy-MM-ddThh:mm:ssZ"）の形式で表記される。
    日本時間(GMT+9)の2023年4月1日0時5分30秒の例) "2023-04-01T00:05:30+09:00"
    """
    updatedDatetime: str
    """
    （おそらく）更新日時。
    ISO 8601（"yyyy-MM-ddThh:mm:ssZ"）の形式で表記される。
    """
    tags: list[str]
    """投稿に設定されたハッシュタグ。"""
    isLiked: bool
    """不明。"""
    likeCount: int
    """いいねの数。"""
    commentCount: int
    """コメント数。"""
    isRestricted: bool
    """支援していないなどで閲覧条件を満たしていなければtrue。"""
    user: User
    """投稿者の情報"""
    creatorId: str
    """投稿者のクリエイターID"""
    hasAdultContent: bool
    """R-18の投稿であればtrue。"""
    cover: Cover
    """カバー画像の情報。"""
    excerpt: str
    """
    投稿本文の最初の部分。
    投稿の閲覧条件を満たしていない場合は空文字列が格納される。
    """
