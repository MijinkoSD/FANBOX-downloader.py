from typing import TypeAlias, TypedDict, Literal

ProfileSubDir: TypeAlias = Literal["icon", "cover", "thumbnails", "images"]
"""profile内のサブディレクトリ名"""
PostSubDir: TypeAlias = Literal["cover", "thumbnails", "images", "files"]
"""post内のサブディレクトリ名"""

PROFILE_SUB_DIR_NAMES: dict[ProfileSubDir, str] = {
    "icon": "ユーザーアイコン画像",
    "cover": "カバー画像",
    "thumbnails": "ポートフォリオのサムネイル画像",
    "images": "ポートフォリオの元画像",
}
"""profile内のサブディレクトリの日本語名"""

POST_SUB_DIR_NAMES: dict[PostSubDir, str] = {
    "cover": "カバー画像",
    "thumbnails": "サムネイル画像",
    "images": "元画像",
    "files": "ファイル",
}
"""post内のサブディレクトリの日本語名"""


class _ProfileName(TypedDict):
    type: ProfileSubDir
    name: str


class _PostName(TypedDict):
    type: PostSubDir
    name: str
