import os
import json
from typing import Any


def save_json(data: Any, dir: str) -> None:
    """データをjsonとして保存します。

    Args:
        data (Any): 保存するデータ。
        dir (str): 保存先のファイルパス。
    """
    os.makedirs(os.path.dirname(dir), exist_ok=True)
    with open(dir, mode="wt", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
