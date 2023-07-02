from typing import TypeAlias, TypedDict, Literal

ProfileSubDir: TypeAlias = Literal["icon", "cover", "thumbnails", "images"]
"""profile内のサブディレクトリ名"""
PostSubDir: TypeAlias = Literal["cover", "thumbnails", "images", "files"]
"""post内のサブディレクトリ名"""

PROFILE_SUB_DIR_NAMES: list["_ProfileName"] = [{
    "type": "icon",
    "name": "ユーザーアイコン画像",
}, {
    "type": "cover",
    "name": "カバー画像",
}, {
    "type": "thumbnails",
    "name": "ポートフォリオのサムネイル画像",
}, {
    "type": "images",
    "name": "ポートフォリオの元画像",
}]
"""profile内のサブディレクトリの日本語名"""

POST_SUB_DIR_NAMES: list["_PostName"] = [{
    "type": "cover",
    "name": "カバー画像",
}, {
    "type": "thumbnails",
    "name": "サムネイル画像",
}, {
    "type": "images",
    "name": "元画像",
}, {
    "type": "files",
    "name": "ファイル",
}]
"""post内のサブディレクトリの日本語名"""


class _ProfileName(TypedDict):
    type: ProfileSubDir
    name: str


class _PostName(TypedDict):
    type: PostSubDir
    name: str
