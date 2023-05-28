from typing import TypeAlias

from ...response.creator import Creator


ListRecommended: TypeAlias = list[Creator]
"""ログイン中のアカウントにおすすめしているクリエイターの一覧。"""
