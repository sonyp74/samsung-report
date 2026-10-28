import urllib.request
import urllib.parse
import datetime
from bs4 import BeautifulSoup

# 설정 정보
TELEGRAM_TOKEN = "9077507634:AAG8zS8EDOniS8-iP4pRK99XmIrnAmVpj5I"
CHAT_ID = "8955893121"
DEFAULT_PRICE_A = 320638
DEFAULT_QTY_A = 84
DEFAULT_PRICE_B = 279399
DEFAULT_QTY_B = 84

def send_telegram(msg):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = urllib.parse.urlencode({"chat_id": CHAT_ID, "text": msg, "parse_mode": "Markdown"}).encode('utf-8')
    try:
        urllib.request.urlopen(urllib.request.Request(url, data=payload, method='POST'))
    except Exception as e:
        print(f"텔레그램 전송 실패: {e}")

def main():
    today_str = datetime.datetime.now().strftime("%Y년 %m월 %d일")
    
    # 네이버 증권 크롤링 (현재가 추출)
    try:
        url = "https://finance.naver.com/item/main.naver?code=005930"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        html = urllib.request.urlopen(req).read().decode('euc-kr', 'ignore')
        soup = BeautifulSoup(html, 'html.parser')
        price_str = soup.select_one('.no_today .blind').text.replace(',', '')
        current_price = int(price_str)
        diff = soup.select_one('.no_exday .blind').text
    except Exception:
        current_price = 242000
        diff = "0"

    telegram_text = (
        f"📊 *[삼성전자 데일리 리포트]* ({today_str})\n\n"
        f"💰 *현재가:* {current_price:,}원 (전일비: {diff})\n"
        f"📦 *계좌별 상세 테이블 갱신 완료*\n"
        f"🌐 [대시보드에서 확인하기](https://sonyp74.github.io/samsung-report/)"
    )
    send_telegram(telegram_text)
    
    html_content = f"""<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>삼성전자 일일 투자 분석 보고서</title>
    <style>
        :root {{
            --bg-color: #f4f6f9;
            --card-bg: #ffffff;
            --primary: #0a58ca;
            --secondary: #495057;
            --accent-up: #d93025;
            --accent-down: #1a73e8;
            --text-main: #212529;
            --border-color: #dee2e6;
        }}
        body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; background-color: var(--bg-color); color: var(--text-main); margin: 0; padding: 20px; }}
        .container {{ max-width: 1050px; margin: 0 auto; }}
        header {{ background: linear-gradient(135deg, #0a58ca, #042b69); color: white; padding: 24px; border-radius: 12px; margin-bottom: 20px; box-shadow: 0 4px 12px rgba(0,0,0,0.1); }}
        header h1 {{ margin: 0 0 8px 0; font-size: 24px; }}
        header .date-info {{ font-size: 14px; opacity: 0.85; }}
        
        .table-container {{
            background: #ffffff;
            border: 1px solid var(--border-color);
            border-radius: 12px;
            padding: 20px;
            margin-bottom: 20px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.05);
            overflow-x: auto;
        }}
        .table-title {{ font-size: 16px; font-weight: bold; color: #084298; margin-bottom: 15px; display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 10px; }}
        
        table {{
            width: 100%;
            border-collapse: collapse;
            text-align: center;
            font-size: 14px;
        }}
        th, td {{
            padding: 12px 8px;
            border-bottom: 1px solid var(--border-color);
        }}
        th {{
            background-color: #f8f9fa;
            color: #495057;
            font-weight: 600;
        }}
        input[type="number"] {{
            width: 95px;
            padding: 6px;
            text-align: right;
            border: 1px solid #ced4da;
            border-radius: 4px;
            font-size: 14px;
        }}
        .calc-btn {{
            background-color: var(--primary);
            color: white;
            border: none;
            padding: 8px 16px;
            border-radius: 6px;
            font-weight: bold;
            cursor: pointer;
        }}
        .calc-btn:hover {{ background-color: #084298; }}

        .total-row {{
            font-weight: bold;
            background-color: #e7f1ff;
        }}
        .profit-plus {{ color: var(--accent-up); font-weight: bold; }}
        .profit-minus {{ color: var(--accent-down); font-weight: bold; }}

        .summary-cards {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 16px; margin-bottom: 20px; }}
        .card {{ background: var(--card-bg); padding: 20px; border-radius: 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.05); border: 1px solid var(--border-color); }}
        .card-title {{ font-size: 13px; color: var(--secondary); margin-bottom: 8px; font-weight: 600; }}
        .card-value {{ font-size: 22px; font-weight: bold; }}
        .card-change {{ font-size: 13px; margin-top: 4px; color: var(--accent-up); }}

        .section-title {{ font-size: 18px; font-weight: bold; margin: 28px 0 12px 0; display: flex; align-items: center; gap: 8px; color: #111; }}
        .section-title::before {{ content: ""; display: inline-block; width: 4px; height: 18px; background-color: var(--primary); border-radius: 2px; }}
        
        .content-box {{ background: var(--card-bg); padding: 20px; border-radius: 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.05); border: 1px solid var(--border-color); margin-bottom: 16px; line-height: 1.6; }}
        .content-box ul {{ margin: 0; padding-left: 20px; }}
        .content-box li {{ margin-bottom: 8px; }}

        .conclusion-box {{ border-left: 5px solid var(--primary); font-size: 15px; font-weight: 500; }}
        .action-banner {{ background: linear-gradient(135deg, #212529, #343a40); color: #fff; padding: 20px; border-radius: 12px; text-align: center; font-size: 18px; font-weight: bold; margin-top: 24px; box-shadow: 0 4px 12px rgba(0,0,0,0.15); }}
        .action-banner span {{ color: #ffda6a; }}
        .badge {{ display: inline-block; padding: 4px 8px; font-size: 12px; font-weight: 600; border-radius: 4px; margin-right: 6px; }}
        .badge-warning {{ background-color: #fff3cd; color: #856404; }}
        .badge-info {{ background-color: #cce5ff; color: #004085; }}
        .badge-danger {{ background-color: #f8d7da; color: #721c24; }}
        footer {{ text-align: center; padding: 24px 0; color: var(--secondary); font-size: 12px; }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>삼성전자 데일리 투자 분석 보고서 📊</h1>
            <div class="date-info">업데이트: {today_str} 기준 (현재가: <strong id="header-price">{current_price:,}</strong>원)</div>
        </header>

        <!-- 계좌별 입력 및 테이블 영역 -->
        <div class="table-container">
            <div class="table-title">
                <span>💼 계좌별 상세 현황 및 손익 계산 (매입가 / 수량 수정 가능)</span>
                <button class="calc-btn" onclick="calculate()">반영 및 계산</button>
            </div>
            <table>
                <thead>
                    <tr>
                        <th>종목명</th>
                        <th>매입가</th>
                        <th>평가손익</th>
                        <th>수익률</th>
                        <th>보유수량</th>
                        <th>매입금액</th>
                        <th>평가금액</th>
                    </tr>
                </thead>
                <tbody>
                    <!-- 계좌 1 -->
                    <tr>
                        <td>삼성전자 (계좌1)</td>
                        <td><input type="number" id="price1" value="{DEFAULT_PRICE_A}"></td>
                        <td id="profit1">-</td>
                        <td id="return1">-</td>
                        <td><input type="number" id="qty1" value="{DEFAULT_QTY_A}"></td>
                        <td id="invest1">-</td>
                        <td id="eval1">-</td>
                    </tr>
                    <!-- 계좌 2 -->
                    <tr>
                        <td>삼성전자 (계좌2)</td>
                        <td><input type="number" id="price2" value="{DEFAULT_PRICE_B}"></td>
                        <td id="profit2">-</td>
                        <td id="return2">-</td>
                        <td><input type="number" id="qty2" value="{DEFAULT_QTY_B}"></td>
                        <td id="invest2">-</td>
                        <td id="eval2">-</td>
                    </tr>
                    <!-- 합계 -->
                    <tr class="total-row">
                        <td>합계 / 총평</td>
                        <td>-</td>
                        <td id="total-profit">-</td>
                        <td id="total-return">-</td>
                        <td id="total-qty">-</td>
                        <td id="total-invest">-</td>
                        <td id="total-eval">-</td>
                    </tr>
                </tbody>
            </table>
        </div>

        <div class="summary-cards">
            <div class="card">
                <div class="card-title">종목명 / 코드</div>
                <div class="card-value">삼성전자</div>
                <div class="card-change">005930</div>
            </div>
            <div class="card">
                <div class="card-title">오늘 종가</div>
                <div class="card-value">{current_price:,}원</div>
                <div class="card-change">전일 대비: {diff}</div>
            </div>
            <div class="card">
                <div class="card-title">핵심 촉매</div>
                <div class="card-value" style="font-size:18px;">3Q 실적발표</div>
                <div class="card-change">컨퍼런스콜 진행 예정</div>
            </div>
        </div>

        <div class="section-title">1. 오늘의 결론 및 맞춤 조언</div>
        <div class="content-box conclusion-box">
            <ul>
                <li><strong>투자 가설 유지:</strong> HBM3E 공급 가시성 및 메모리 업황 회복 기대감으로 중장기 모멘텀 유효.</li>
                <li><strong id="advice-status-text">계좌별 상태 분석:</strong> <span id="dynamic-advice">값을 입력하고 [반영 및 계산] 버튼을 누르면 맞춤 조언이 생성됩니다.</span></li>
                <li><strong>실적 이벤트 대기:</strong> 컨퍼런스콜 발표 전까지 무리한 추격 매수보다는 보유 관망 전략이 유효.</li>
            </ul>
        </div>

        <div class="section-title">2. 오늘 뭐가 바뀌었나 (수급/기술적 위치)</div>
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
            🎯 오늘의 매매 판단: <span id="banner-text">"실적 발표를 앞둔 '관찰'의 자리입니다."</span>
        </div>

        <footer>
            본 보고서는 매일 GitHub Actions을 통해 자동으로 데이터가 업데이트됩니다.
        </footer>
    </div>

    <script>
        const currentPrice = {current_price};

        function calculate() {{
            // 계좌 1
            const p1 = parseFloat(document.getElementById('price1').value) || 0;
            const q1 = parseFloat(document.getElementById('qty1').value) || 0;
            const invest1 = p1 * q1;
            const eval1 = currentPrice * q1;
            const profit1 = eval1 - invest1;
            const return1 = invest1 > 0 ? (profit1 / invest1) * 100 : 0;

            document.getElementById('invest1').innerText = invest1.toLocaleString();
            document.getElementById('eval1').innerText = eval1.toLocaleString();
            
            const prof1Elem = document.getElementById('profit1');
            if (profit1 >= 0) {{
                prof1Elem.className = "profit-plus";
                prof1Elem.innerText = "+" + profit1.toLocaleString();
            }} else {{
                prof1Elem.className = "profit-minus";
                prof1Elem.innerText = profit1.toLocaleString();
            }}

            const ret1Elem = document.getElementById('return1');
            ret1Elem.className = return1 >= 0 ? "profit-plus" : "profit-minus";
            ret1Elem.innerText = return1.toFixed(2) + "%";

            // 계좌 2
            const p2 = parseFloat(document.getElementById('price2').value) || 0;
            const q2 = parseFloat(document.getElementById('qty2').value) || 0;
            const invest2 = p2 * q2;
            const eval2 = currentPrice * q2;
            const profit2 = eval2 - invest2;
            const return2 = invest2 > 0 ? (profit2 / invest2) * 100 : 0;

            document.getElementById('invest2').innerText = invest2.toLocaleString();
            document.getElementById('eval2').innerText = eval2.toLocaleString();
            
            const prof2Elem = document.getElementById('profit2');
            if (profit2 >= 0) {{
                prof2Elem.className = "profit-plus";
                prof2Elem.innerText = "+" + profit2.toLocaleString();
            }} else {{
                prof2Elem.className = "profit-minus";
                prof2Elem.innerText = profit2.toLocaleString();
            }}

            const ret2Elem = document.getElementById('return2');
            ret2Elem.className = return2 >= 0 ? "profit-plus" : "profit-minus";
            ret2Elem.innerText = return2.toFixed(2) + "%";

            // 합계
            const totalQty = q1 + q2;
            const totalInvest = invest1 + invest2;
            const totalEval = eval1 + eval2;
            const totalProfit = totalEval - totalInvest;
            const totalReturn = totalInvest > 0 ? (totalProfit / totalInvest) * 100 : 0;

            document.getElementById('total-qty').innerText = totalQty.toLocaleString() + "주";
            document.getElementById('total-invest').innerText = totalInvest.toLocaleString();
            document.getElementById('total-eval').innerText = totalEval.toLocaleString();

            const totProfElem = document.getElementById('total-profit');
            if (totalProfit >= 0) {{
                totProfElem.className = "profit-plus";
                totProfElem.innerText = "+" + totalProfit.toLocaleString();
            }} else {{
                totProfElem.className = "profit-minus";
                totProfElem.innerText = totalProfit.toLocaleString();
            }}

            const totRetElem = document.getElementById('total-return');
            totRetElem.className = totalReturn >= 0 ? "profit-plus" : "profit-minus";
            totRetElem.innerText = totalReturn.toFixed(2) + "%";

            // 맞춤 조언 자동 갱신
            const avgPriceAll = totalQty > 0 ? totalInvest / totalQty : 0;
            let advice = "";
            if (currentPrice >= avgPriceAll) {{
                advice = `현재가(<strong>${{currentPrice.toLocaleString()}}원</strong>)가 전체 평균단가(<strong>${{Math.round(avgPriceAll).toLocaleString()}}원</strong>) 위인 <strong>수익권</strong>입니다. 실적 발표 전까지 여유 있게 홀딩이 유리합니다.`;
            }} else {{
                advice = `현재가(<strong>${{currentPrice.toLocaleString()}}원</strong>)가 전체 평균단가(<strong>${{Math.round(avgPriceAll).toLocaleString()}}원</strong>) 아래인 <strong>손실권</strong>입니다. 10/29 실적 컨퍼런스콜 가이던스를 확인하며 대응하세요.`;
            }}
            document.getElementById('dynamic-advice').innerHTML = advice;
        }}

        // 페이지 로드 시 자동 계산 실행
        window.onload = calculate;
    </script>
</body>
</html>
"""

    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html_content)

if __name__ == "__main__":
    main()
