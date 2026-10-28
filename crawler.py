import urllib.request
import urllib.parse
import json
import datetime
from bs4 import BeautifulSoup

# 텔레그램 봇 설정 정보
TELEGRAM_TOKEN = "9077507634:AAG8zS8EDOniS8-iP4pRK99XmIrnAmVpj5I"
CHAT_ID = "8955893121"

# 계좌별 평단가 설정
AVG_PRICE_A = "320,638원"
AVG_PRICE_B = "279,399원"

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    }
    data = urllib.parse.urlencode(payload).encode('utf-8')
    req = urllib.request.Request(url, data=data, method='POST')
    try:
        with urllib.request.urlopen(req) as response:
            print("텔레그램 알림 전송 완료!")
    except Exception as e:
        print(f"텔레그램 전송 실패: {e}")

def fetch_samsung_data():
    today_str = datetime.datetime.now().strftime("%Y년 %m월 %d일")
    
    # 네이버 증권 삼성전자(005930) 정보 크롤링
    url = "https://finance.naver.com/item/main.naver?code=005930"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    html = urllib.request.urlopen(req).read().decode('euc-kr', 'ignore')
    
    soup = BeautifulSoup(html, 'html.parser')
    
    # 주가 및 등락률 추출
    price_tag = soup.select_one('.no_today .blind')
    price = price_tag.text if price_tag else "242,000"
    
    diff_tag = soup.select_one('.no_exday .blind')
    diff = diff_tag.text if diff_tag else "0"
    
    # 텔레그램 메시지 구성
    telegram_text = f"""📊 *[삼성전자 데일리 투자 리포트]* ({today_str})

💰 *현재가:* {price}원 (전일 대비: {diff})
📦 *보유현황:* 총 168주 (약 4,000만 원)
  • 계좌 1 평단: *{AVG_PRICE_A}*
  • 계좌 2 평단: *{AVG_PRICE_B}*

🎯 *1. 오늘의 결론*
• 투자 가설 유지: HBM3E 공급 가시성 및 업황 회복 기대감 지속
• 계좌 관리: 평단가 상향 대응 및 실적 컨퍼런스콜 관망 유지

📰 *3. 주요 촉매*
• 3분기 실적 컨퍼런스콜: HBM3E 퀄테스트 및 가이던스 집중

📌 *오늘의 판단*
"지금은 추
