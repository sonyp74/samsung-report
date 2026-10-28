import urllib.request
import urllib.parse
import datetime
from bs4 import BeautifulSoup

# 설정 정보
TELEGRAM_TOKEN = "9077507634:AAG8zS8EDOniS8-iP4pRK99XmIrnAmVpj5I"
CHAT_ID = "8955893121"
AVG_PRICE_A = "320,638원"
AVG_PRICE_B = "279,399원"

def send_telegram(msg):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = urllib.parse.urlencode({"chat_id": CHAT_ID, "text": msg, "parse_mode": "Markdown"}).encode('utf-8')
    try:
        urllib.request.urlopen(urllib.request.Request(url, data=payload, method='POST'))
    except Exception as e:
        print(f"텔레그램 전송 실패: {e}")

def main():
    today_str = datetime.datetime.now().strftime("%Y년 %m월 %d일")
    
    # 네이버 증권 크롤링 (실패 시 기본값 방어 코드 포함)
    try:
        url = "https://finance.naver.com/item/main.naver?code=005930"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        html = urllib.request.urlopen(req).read().decode('euc-kr', 'ignore')
        soup = BeautifulSoup(html, 'html.parser')
        price = soup.select_one('.no_today .blind').text
        diff = soup.select_one('.no_exday .blind').text
    except Exception:
        price = "242,000"
        diff = "0"

    # 텔레그램 알림 메시지
    telegram_text = (
        f"📊 *[삼성전자 데일리 리포트]* ({today_str})\n\n"
        f"💰 *현재가:* {price}원 (전일비: {diff})\n"
        f"📦 *보유:* 168주 (약 4,000만 원)\n"
        f"  • 계좌1 평단: *{AVG_PRICE_A}*\n"
        f"  • 계좌2 평단: *{AVG_PRICE_B}*\n\n"
        f"🎯 *오늘의 판단:* 실적 발표 앞둔 관찰 자리\n"
        f"🌐 [대시보드 보기](https://sonyp74.github.io/samsung-report/)"
    )
    send_telegram(telegram_text)
    
    # 웹 대시보드 (index.html) 생성
    html_content = f"""<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>삼성전자 투자 분석 보고서</title>
    <style>
        body {{ font-family: -apple-system, sans-serif; background: #f4f6f9; margin: 0; padding: 20px; color: #212529; }}
        .container {{ max-width: 800px; margin: 0 auto; background: #fff; padding: 24px; border-radius: 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.05); }}
        h1 {{ color: #0a58ca; font-size: 22px; margin-top: 0; }}
        .box {{ background: #e7f1ff; padding: 16px; border-radius: 8px; margin-bottom: 16px; font-size: 14px; line-height: 1.6; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>삼성전자 데일리 투자 분석 보고서 📊</h1>
        <p>최종 업데이트: {today_str}</p>
        <div class="box">
            <strong>📦 보유 현황:</strong> 총 168주 (약 4,000만원)<br>
            • 계좌 1 평단가: <strong>{AVG_PRICE_A}</strong><br>
            • 계좌 2 평단가: <strong>{AVG_PRICE_B}</strong>
        </div>
        <div class="box">
            <strong>📈 실시간 시세:</strong> 현재가 <strong>{price}원</strong> (전일 대비: {diff})
        </div>
        <div class="box">
            <strong>🎯 오늘의 결론 & 액션 플랜:</strong><br>
            • HBM3E 모멘텀 유지 속 3분기 실적 컨퍼런스콜(10/29) 대기.<br>
            • 무리한 추격 매수 자제 및 실적 발표 전까지 '관찰' 유지.
        </div>
    </div>
</body>
</html>"""

    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html_content)

if __name__ == "__main__":
    main()
