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
    telegram_text = (
        f"📊 *[삼성전자 데일리 투자 리포트]* ({today_str})\n\n"
        f"💰 *현재가:* {price}원 (전일 대비: {diff})\n"
        f"📦 *보유현황:* 총 168주 (약 4,000만 원)\n"
        f"  • 계좌 1 평단: *{AVG_PRICE_A}*\n"
        f"  • 계좌 2 평단: *{AVG_PRICE_B}*\n\n"
        f"🎯 *1. 오늘의 결론*\n"
        f"• 투자 가설 유지: HBM3E 공급 가시성 및 업황 회복 기대감 지속\n"
        f"• 계좌 관리: 평단가 상향 대응 및 실적 컨퍼런스콜 관망 유지\n\n"
        f"📰 *3. 주요 촉매*\n"
        f"• 3분기 실적 컨퍼런스콜: HBM3E 퀄테스트 및 가이던스 집중\n\n"
        f"📌 *오늘의 판단*\n"
        f'"지금은 추격 매수가 아닌, 실적 발표를 앞둔 \'관찰\'의 자리입니다."\n\n'
        f"🌐 [웹 대시보드에서 전체 보기](https://sonyp74.github.io/samsung-report/)"
    )
    
    # 텔레그램 알림 전송 실행
    send_telegram_message(telegram_text)
    
    # HTML 템플릿 (문법 오류 원천 차단형)
    html_template = """<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>삼성전자 일일 투자 분석 보고서</title>
    <style>
        :root {
            --bg-color: #f4f6f9;
            --card-bg: #ffffff;
            --primary: #0a58ca;
            --secondary: #495057;
            --accent-up: #d93025;
            --text-main: #212529;
            --border-color: #e9ecef;
        }
        body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; background-color: var(--bg-color); color: var(--text-main); margin: 0; padding: 20px; }
        .container { max-width: 900px; margin: 0 auto; }
        header { background: linear-gradient(135deg, #0a58ca, #042b69); color: white; padding: 24px; border-radius: 12px; margin-bottom: 20px; box-shadow: 0 4px 12px rgba(0,0,0,0.1); }
        header h1 { margin: 0 0 8px 0; font-size: 24px; }
        header .date-info { font-size: 14px; opacity: 0.85; }
        
        .portfolio-summary {
            background: #e7f1ff;
            border: 1px solid #b6d4fe;
            border-radius: 12px;
            padding: 16px 20px;
            margin-bottom: 20px;
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
            gap: 12px;
        }
        .portfolio-item { font-size: 14px; color: #084298; }
        .portfolio-item strong { font-size: 16px; font-weight: bold; color: #052c65; display: block; margin-top: 2px; }

        .summary-cards { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 16px; margin-bottom: 20px; }
        .card { background: var(--card-bg); padding: 20px; border-radius: 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.05); border: 1px solid var(--border-color); }
        .card-title { font-size: 13px; color: var(--secondary); margin-bottom: 8px; font-weight: 600; }
        .card-value { font-size: 22px; font-weight: bold; }
        .card-change { font-size: 13px; margin-top: 4px; color: var(--accent-up); }

        .section-title { font-size: 18px; font-weight: bold; margin: 28px 0 12px 0; display: flex; align-items: center; gap: 8px; color: #111; }
        .section-title::before { content: ""; display: inline-block; width: 4px; height: 18px; background-color: var(--primary); border-radius: 2px; }
        
        .content-box { background: var(--card-bg); padding: 20px; border-radius: 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.05); border: 1px solid var(--border-color); margin-bottom: 16px; line-height: 1.6; }
        .content-box ul { margin: 0; padding-left: 20px; }
        .content-box li { margin-bottom: 8px; }

        .conclusion-box { border-left: 5px solid var(--primary); font-size: 15px; font-weight: 500; }
        .action-banner { background: linear-gradient(135deg, #212529, #343a40); color: #fff; padding: 20px; border-radius: 12px; text-align: center; font-size: 18px; font-weight: bold; margin-top: 24px; box-shadow: 0 4px 12px rgba(0,0,0,0.15); }
        .action-banner span { color: #ffda6a; }
        .badge { display: inline-block; padding: 4px 8px; font-size: 12px; font-weight: 600; border-radius: 4px; margin-right: 6px; }
        .badge-warning { background-color: #fff3cd; color: #856404; }
        .badge-info { background-color: #cce5ff; color: #004085; }
        .badge-danger { background-color: #f8d7da; color: #721c24; }
        footer { text-align: center; padding: 24px 0; color: var(--secondary); font-size: 12px; }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>삼성전자 데일리 투자 분석 보고서 📊</h1>
            <div class="date-info">업데이트: {TODAY_STR} 기준</div>
        </header>

        <div class="portfolio-summary">
            <div class="portfolio-item">보유 수량: <strong>168주 (약 4,000만원)</strong></div>
            <div class="portfolio-item">계좌 1 평단가: <strong>{AVG_PRICE_A}</strong></div>
            <div class="portfolio-item">계좌 2 평단가: <strong>{AVG_PRICE_B}</strong></div>
            <div class="portfolio-item">현재 상태: <strong style="color:var(--primary);">계좌별 분할 관리 중</strong></div>
        </div>

        <div class="summary-cards">
            <div class="card">
                <div class="card-title">종목명 / 코드</div>
                <div class="card-value">삼성전자</div>
                <div class="card-change">005930</div>
            </div>
            <div class="card">
                <div class="card-title">오늘 종가</div>
                <div class="card-value">{PRICE}원</div>
                <div class="card-change">전일 대비: {DIFF}</div>
            </div>
            <div class="card">
                <div class="card-title">핵심 촉매</div>
                <div class="card-value" style="font-size:18px;">3Q 실적발표</div>
                <div class="card-change">컨퍼런스콜 진행 예정</div>
            </div>
        </div>

        <div class="section-title">1. 오늘의 결론</div>
        <div class="content-box conclusion-box">
            <ul>
                <li><strong>투자 가설 유지:</strong> HBM3E 공급 가시성 및 메모리 업황 회복 기대감으로 중장기 모멘텀 유효.</li>
                <li><strong>계좌별 전략 관리:</strong> 계좌 1({AVG_PRICE_A}) 및 계좌 2({AVG_PRICE_B})의 평단 차이를 고려한 구간별 대응.</li>
                <li><strong>실적 이벤트 대기:</strong> 컨퍼런스콜 발표 전까지 무리한 추격 매수보다는 보유 관망 전략이 유효.</li>
            </ul>
        </div>

        <div class="section-title">2. 오늘 뭐가 바뀌었나</div>
        <div class="content-box">
            <ul>
                <li><strong>투자 가설:</strong> HBM 턴어라운드 모멘텀 유효, 단기 변동성에도 중장기 재평가 라인 유지.</li>
                <li><strong>수급 동향:</strong> 외국인 순매수세 및 기관 저가 매수 유입 지속, 개인 매물 출회.</li>
                <li><strong>메모리 가격:</strong> DRAM/NAND 고정거래가격 안정세 유지, 서버용 HBM 수요 호조.</li>
                <li><strong>기술적 위치:</strong> 주요 마디대 안착 시도 중, 상방 저항대 관망.</li>
                <li><strong>내 감정 상태:</strong> 계좌별 평단가를 고려한 냉정한 리스크 관리 및 심리적 안정 유지.</li>
            </ul>
        </div>

        <div class="section-title">3. 뉴스 & 촉매 (주가 직접 영향)</div>
        <div class="content-box">
            <ul>
                <li><span class="badge badge-info">실적/IR</span> <strong>3분기 실적 컨퍼런스콜:</strong> HBM3E 퀄테스트 진행 상황 및 4분기/내년 가이던스 발표가 핵심 촉매.</li>
                <li><span class="badge badge-warning">미국 정책</span> <strong>미국 반도체 정책 변수:</strong> 보조금 지급 일정 및 대중 규제 여파 모니터링.</li>
                <li><span class="badge badge-danger">지정학적</span> <strong>대외 불확실성:</strong> 매크로 환경 및 유가 변동성에 따른 전방 IT 수요 점검.</li>
            </ul>
        </div>

        <div class="section-title">4. If-Then 액션 플랜</div>
        <div class="content-box">
            <ul>
                <li><strong>IF 주요 저항선 강하게 돌파 시:</strong> 상승 추세 강화로 판단, 홀딩 유지하며 계좌별 목표가 상향.</li>
                <li><strong>IF 지지선 하향 이탈 시:</strong> 리스크 관리 라인 작동, 계좌별 비중 조절 검토.</li>
                <li><strong>IF 실적 서프라이즈 (HBM 공급 확정 등):</strong> 보유 물량 유지 후 차기 저항선까지 추종.</li>
                <li><strong>IF 실적 미스 / 가이던스 악화:</strong> 단기 변동성 확대 시 분할 매도 대응.</li>
            </ul>
        </div>

        <div class="section-title">5. 매매일지</div>
        <div class="content-box">
            <ul>
                <li><strong>오늘 한 거래:</strong> 없음 (Holding 유지)</li>
                <li><strong>안 한 이유:</strong> 대형 실적 이벤트 대기 중이므로 사전 뇌동매매 자제.</li>
                <li><strong>사후 점검:</strong> 두 계좌의 평단가를 명확히 파악하고 이벤트 결과 확인 후 대응하는 것이 최선.</li>
            </ul>
        </div>

        <div class="action-banner">
            🎯 오늘의 매매 판단: <span>"지금은 추격 매수가 아닌, 실적 발표를 앞둔 '관찰'의 자리입니다."</span>
        </div>

        <footer>
            본 보고서는 매일 GitHub Actions을 통해 자동으로 데이터가 업데이트됩니다.
        </footer>
    </div>
</body>
</html>
"""
    
    # 데이터를 템플릿에 안전하게 대입
    html_content = html_template.replace("{TODAY_STR}", today_str) \
                                .replace("{PRICE}", price) \
                                .replace("{DIFF}", diff) \
                                .replace("{AVG_PRICE_A}", AVG_PRICE_A) \
                                .replace("{AVG_PRICE_B}", AVG_PRICE_B)

    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html_content)

if __name__ == "__main__":
    fetch_samsung_data()
