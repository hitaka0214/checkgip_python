import ipaddress
import os

import requests
from lxml import html


UGTOP_URL = "https://www.ugtop.com/spill.shtml"


def fetch_global_ip(session: requests.Session, url: str = UGTOP_URL) -> str:
    resp = session.get(
        url,
        timeout=20,
        headers={
            # 一部サイトはデフォルトUAのHTTPクライアントを弾くことがあるため明示
            "User-Agent": "Mozilla/5.0 (compatible; checkgip/0.1; +https://example.invalid)",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        },
    )
    resp.raise_for_status()

    # Ruby版: doc.xpath('//tr[2]/td').text
    # 現在のページ構造では td の直下が text ノードでないため、子孫も含めて取得する
    doc = html.fromstring(resp.content)
    text = doc.xpath("//tr[2]//td//text()")
    return "".join(text).strip()


def validate_ip(gip: str) -> None:
    try:
        ipaddress.ip_address(gip)
    except ValueError:
        print(f"ERROR this is not ipaddress = {gip}")
        raise SystemExit(1)


def main() -> None:
    with requests.Session() as session:
        # プロキシ環境変数(HTTPS_PROXY等)の影響を受けないようにする
        session.trust_env = False
        gip = fetch_global_ip(session)
        validate_ip(gip)
        print(gip)


if __name__ == "__main__":
    main()
