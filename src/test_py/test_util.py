import re
from os import linesep
from unittest import TestCase

from src.downloader.util import print_with_timestamp, \
    urlparse_filename
from src.test_py.stdout_capture import StdOutCapture


class TestUtil(TestCase):
    def test_print_with_timestamp(self) -> None:
        pattern = re.compile(r"^\[\d+/\d{2}/\d{2} \d{2}:\d{2}:\d{2}\] .*")
        text = "テキスト"
        with StdOutCapture() as io:
            print_with_timestamp(text)
            stdout = io.getvalue().rstrip(linesep)
        assert (pattern.match(stdout) is not None
                and stdout.endswith(text))

    def test_print_with_timestamp_with_multiline_text(self) -> None:
        pattern = [
            re.compile(r"^\[\d+/\d{2}/\d{2} \d{2}:\d{2}:\d{2}\] .*"),
            re.compile(' '*22 + r".*")]
        text = ["テキスト", "2行目"]
        with StdOutCapture() as io:
            print_with_timestamp("\n".join(text))
            stdout = io.getvalue().rstrip(linesep)

        for ptn, txt, stdo in zip(pattern, text, stdout.splitlines()):
            assert (ptn.match(stdo) is not None
                    and stdo.endswith(txt))

    def test_urlparse_filename(self) -> None:
        filename = "ファイル名.file"

        def verify(url: str) -> bool:
            return urlparse_filename(url) == filename

        assert verify(f"https://example.com/{filename}")
        assert verify(f"https://example.com/foo/{filename}")
        assert verify(f"https://example.com/foo/{filename}?param=bar")
        assert verify(f"https://example.com/foo/{filename}#fragment")
        assert verify(f"http://example.com/{filename}")
        assert verify(f"https://127.0.0.1:1234/{filename}")
        assert verify(f"http://127.0.0.1:1234/{filename}")
