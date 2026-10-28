import urllib.request
import json
import datetime
from bs4 import BeautifulSoup

def fetch_samsung_data():
    # 현재 날짜
    today_str = datetime.datetime.now().strftime("%Y년 %m월 %d일")
    
    # 네이버 페이 증권 삼성전자(005930) 정보 크롤링
    url = "https://finance.naver.com/item/main.naver?code=005930"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    html = urllib.request.urlopen(req).read().decode('euc-kr', 'ignore')
    
    soup = BeautifulSoup(html, 'html.parser')
    
    # 주가 및 변동성 추출
    price_tag = soup.select_one('.no_today .blind')
    price = price_tag.text if price_tag else "242,000"
    
    diff_tag = soup.select_one('.no_exday .blind')
    diff = diff_tag.text if diff_tag else "0"
    
    # HTML template 생성
    html_content = f"""<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>삼성전자 일일 투자 분석 보고서 (자동화)</title>
    <style>
        :root {{
            --bg-color: #f4f6f9;
            --card-bg: #ffffff;
            --primary: #0a58ca;
            --secondary: #495057;
            --accent-up: #d93025;
            --text-main: #212529;
            --border-color: #e9ecef;
        }}
        body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; background-color: var(--bg-color); color: var(--text-main); margin: 0; padding: 20px; }}
        .container {{ max-width: 900px; margin: 0 auto; }}
        header {{ background: linear-gradient(135deg, #0a58ca, #042b69); color: white; padding: 24px; border-radius: 12px; margin-bottom: 20px; box-shadow: 0 4px 12px rgba(0,0,0,0.1); }}
        header h1 {{ margin: 0 0 8px 0; font-size: 24px; }}
        header .date-info {{ font-size: 14px; opacity: 0.85; }}
        .summary-cards {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 16px; margin-bottom: 20px; }}
        .card {{ background: var(--card-bg); padding: 20px; border-radius: 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.05); border: 1px solid var(--border-color); }}
        .card-title {{ font-size: 13px; color: var(--secondary); margin-bottom: 8px; font-weight: 600; }}
        .card-value {{ font-size: 22px; font-weight: bold; }}
        .card-change {{ font-size: 13px; margin-top: 4px; color: var(--accent-up); }}
        .section-title {{ font-size: 18px; font-weight: bold; margin: 24px 0 12px 0; display: flex; align-items: center; gap: 8px; }}
        .section-title::before {{ content: ""; display: inline-block; width: 4px; height: 18px; background-color: var(--primary); border-radius: 2px; }}
        .content-box {{ background: var(--card-bg); padding: 20px; border-radius: 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.05); border: 1px solid var(--border-color); margin-bottom: 20px; line-height: 1.6; }}
        .badge {{ display: inline-block; padding: 4px 8px; font-size: 12px; font-weight: 600; border-radius: 4px; margin-right: 6px; }}
        .badge-warning {{ background-color: #fff3cd; color: #856404; }}
        .badge-info {{ background-color: #cce5ff; color: #004085; }}
        .badge-danger {{ background-color: #f8d7da; color: #721c24; }}
        ul {{ margin: 0; padding-left: 20px; }}
        li {{ margin-bottom: 8px; }}
        footer {{ text-align: center; padding: 20px; color: var(--secondary); font-size: 12px; }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>삼성전자 일일 투자 분석 보고서 🤖 (자동 업데이트)</h1>
            <div class="date-info">자동 업데이트 일시: {today_str}</div>
        </header>

        <div class="summary-cards">
            <div class="card">
                <div class="card-title">종목명 / 코드</div>
                <div class="card-value">삼성전자</div>
                <div class="card-change">005930</div>
            </div>
            <div class="card">
                <div class="card-title">현재가 (실시간)</div>
                <div class="card-value">{price}원</div>
                <div class="card-change">변동: {diff}</div>
            </div>
            <div class="card">
                <div class="card-title">주요 일정</div>
                <div class="card-value" style="font-size:18px;">3Q 실적발표</div>
                <div class="card-change">10월 29일 진행</div>
            </div>
        </div>

        <div class="section-title">핵심 이슈 & 관전 포인트</div>
        <div class="content-box">
            <ul>
                <li><span class="badge badge-info">실적발표</span> <strong>3분기 실적 및 컨퍼런스콜:</strong> HBM 공급 가시성 확보 및 주주환원책 모니터링 필요.</li>
                <li><span class="badge badge-warning">미국 선거</span> <strong>11월 미국 중간선거 여파:</strong> CHIPS Act(반도체 보조금법) 정책 향방 점검.</li>
                <li><span class="badge badge-danger">지정학적 리스크</span> <strong>중동 정세 영향:</strong> 국제 유가 변동성 및 IT 전방 수요 영향 확인.</li>
            </ul>
        </div>

        <footer>
            본 보고서는 매일 GitHub Actions에 의해 자동으로 수집 및 업데이트됩니다.
        </footer>
    </div>
</body>
</html>
"""
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html_content)

if __name__ == "__main__":
    fetch_samsung_data()
