from typing import Final

BASE_URL: Final[str] = "https://api.fanbox.cc/"
Headers: Final[dict[str, str]] = {
    "accept": "application/json, text/plain, */*",
    "accept-encoding": "gzip, deflate, br",
    "accept-language": "ja,en-US;q=0.9,en;q=0.8",
    "origin": "https://www.fanbox.cc",
    "referer": "https://www.fanbox.cc/",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 "
    "Safari/537.36"
}
