from os.path import join, abspath
from typing import Final

# `src/downloader/file/common.py`を`../../../../`で打ち消す
FILE_ROOT_BASE: Final[str] = abspath(join(__file__, "../../../../"))
"""保存するファイルを格納する大本のディレクトリ"""

POST_FILE_ROOT: Final[str] = abspath(join(FILE_ROOT_BASE, "./posts/"))
PROFILE_FILE_ROOT: Final[str] = abspath(join(FILE_ROOT_BASE, "./profiles/"))
