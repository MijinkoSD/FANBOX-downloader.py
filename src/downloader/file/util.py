import re
import json
from os import makedirs, path, scandir
from typing import Any


def read_json(file_path: str) -> Any:
    """jsonからデータを取得します。

    Args:
        file_path (str): 読み込み先のファイルパス。

    Returns:
        Any: 読み込んだデータ。
    """
    with open(file_path, mode="rt", encoding="utf-8") as f:
        return json.load(f)


def save_json(data: Any, file_path: str) -> None:
    """データをjsonとして保存します。

    Args:
        data (Any): 保存するデータ。
        file_path (str): 保存先のファイルパス。
    """
    makedirs(path.dirname(file_path), exist_ok=True)
    with open(file_path, mode="wt", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def get_latest_filename(
        dir: str, pattern: str = r".*"
) -> str:
    r"""指定したディレクトリ内のファイルをファイル名の降順で並べたとき、一番先頭に来るファイルのファイル名を返します。
    一番最新の日付が入ったファイル名を取得するのにも使えます（やり方は後述）。

    Args:
        dir (str): 探索するディレクトリ。
        pattern (str, optional): ファイル名を絞り込む正規表現。省略した場合は".*"になる。

    Returns:
        str: 条件に合致したファイル名。

    Examples:
        最新の日付が入ったファイル名を取得する場合。
        patternには数字8桁(YYYYMMDD)がファイル名のjsonファイルを絞り込むように設定する。
        >>> get_latest_filename(dir=".", pattern=r"\d{14}.json")
    """
    _pattern = re.compile(pattern)
    files: list[str] = []

    # 引数の条件に合致するファイル名を取得する。
    with scandir(path=dir) as entries:
        for entry in entries:
            if entry.is_file() and _pattern.match(entry.name):
                files.append(entry.name)

    # 結果を返す。
    if files:
        return sorted(files, reverse=True)[0]
    else:
        raise FileNotFoundError(
            "ファイルが見つかりませんでした。\n"
            "  検索場所：%s\n"
            "  検索パターン：%s"
            % (path, pattern)
        )
