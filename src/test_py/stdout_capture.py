import sys
from io import StringIO
from typing import Any


class StdOutCapture:
    def __enter__(self) -> StringIO:
        io = StringIO()
        sys.stdout = io
        return io

    def __exit__(self, *args: Any) -> None:
        sys.stdout = sys.__stdout__
