"""Refresh the Samsung Electronics quote shown in index.html."""

from __future__ import annotations

import re
from datetime import datetime
from pathlib import Path
from urllib.request import Request, urlopen
from zoneinfo import ZoneInfo

from bs4 import BeautifulSoup


ROOT = Path(__file__).resolve().parent
REPORT = ROOT / "index.html"
QUOTE_URL = "https://finance.naver.com/item/main.naver?code=005930"


def fetch_quote() -> tuple[int, int]:
    request = Request(QUOTE_URL, headers={"User-Agent": "Mozilla/5.0"})
    with urlopen(request, timeout=20) as response:
        html = response.read().decode("euc-kr", errors="replace")

    soup = BeautifulSoup(html, "html.parser")
    current = soup.select_one(".today .blind") or soup.select_one(".no_today .blind")
    change = soup.select_one(".no_exday .blind")
    if current is None or change is None:
        raise RuntimeError("Could not find Samsung quote values on Naver Finance")

    price = int(re.sub(r"\D", "", current.get_text()))
    change_text = change.get_text(strip=True).replace(",", "")
    match = re.search(r"-?\d+", change_text)
    if not match:
        raise RuntimeError(f"Could not parse daily price change: {change_text!r}")
    return price, int(match.group())


def main() -> None:
    price, change = fetch_quote()
    html = REPORT.read_text(encoding="utf-8")
    html, price_count = re.subn(
        r'(<div class="card-title">오늘 종가</div>\s*<div class="card-value">)[^<]*(</div>)',
        lambda m: f"{m.group(1)}{price:,}원{m.group(2)}",
        html,
        count=1,
    )
    html, change_count = re.subn(
        r"(전일 대비:\s*)-?[\d,]+",
        lambda m: f"{m.group(1)}{change:+,}",
        html,
        count=1,
    )
    if price_count != 1 or change_count != 1:
        raise RuntimeError("Report quote fields were not found exactly once")

    today = datetime.now(ZoneInfo("Asia/Seoul"))
    html, date_count = re.subn(
        r"업데이트:\s*\d{4}년\s*\d{1,2}월\s*\d{1,2}일\s*기준",
        f"업데이트: {today.year}년 {today.month}월 {today.day}일 기준",
        html,
        count=1,
    )
    if date_count != 1:
        raise RuntimeError("Report update date was not found exactly once")

    REPORT.write_text(html, encoding="utf-8")
    print(f"Updated Samsung quote: {price:,} KRW (change {change:+,})")


if __name__ == "__main__":
    main()
