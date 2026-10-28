import urllib.request
import urllib.parse
import json
import datetime
from bs4 import BeautifulSoup

# ==========================================
# 1. 텔레그램 봇 연동 설정
# ==========================================
TELEGRAM_TOKEN = "9077507634:AAG8zS8EDOniS8-iP4pRK99XmIrnAmVpj5I"
CHAT_ID = "8955893121"

def send_telegram_message(message):
    """텔레그램 봇으로 긴급 알림 메시지 전송"""
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
            print("✅ 텔레그램 알림 전송 성공!")
    except Exception as e:
        print(f"❌ 텔레그램 전송 실패: {e}")

# ==========================================
# 2. 크롤링 및 메인 로직
# ==========================================
def fetch_samsung_data():
    now = datetime.datetime.now()
    today_str = now.strftime("%Y년 %m월 %d일")
    date_badge = now.strftime("%Y.%m.%d")
    
    # 네이버 증권 삼성전자(005930) 정보 크롤링
    url = "https://finance.naver.com/item/main.naver?code=005930"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    
    try:
        html = urllib.request.urlopen(req).read().decode('euc-kr', 'ignore')
        soup = BeautifulSoup(html, 'html.parser')
        
        # 현재가 & 전일대비
        price_tag = soup.select_one('.no_today .blind')
        price = price_tag.text if price_tag else "242,000"
        
        diff_tag = soup.select_one('.no_exday .blind')
        diff = diff_tag.text if diff_tag else "0"
        
        # 거래량
        volume_tag = soup.select('.table_watch td')[2] if len(soup.select('.table_watch td')) > 2 else None
        volume = volume_tag.text.strip() if volume_tag else "1,676만"
    except Exception as e:
        print(f"크롤링 중 예외 발생, 기본값 적용: {e}")
        price = "242,000"
        diff = "▲ 20,000 (+9.01%)"
        volume = "1,676만 주"

    # ------------------------------------------
    # A. 텔레그램 메일/스마트폰 전송 메시지
    # ------------------------------------------
    telegram_text = f"""📊 *[삼성전자 데일리 투자 리포트]* ({today_str})

💰 *현재가:* {price}원 (전일 대비: {diff})
📦 *보유현황:* 168주 / 평단 238,000원 (약 4,000만 원)

🎯 *오늘의 결론*
• 가설 유지: AI 메모리 수요·이익 기대감 유효
• 수급 개선: 외국인·기관 동반 순매수 유입
• 추격 주의: 내일 실적 컨퍼런스콜이 단기 분기점

📌 *오늘의 판단*
"오늘은 추격 매수 자리보다 '관찰'의 자리입니다."

🌐 [웹 대시보드 전체보기](https://sonyp74.github.io/samsung-report/)
"""
    send_telegram_message(telegram_text)

    # ------------------------------------------
    # B. 대시보드 웹페이지 (index.html) 생성
    # ------------------------------------------
    html_content = f"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>삼성전자 일일 투자 분석 | {date_badge}</title>
<style>
:root {{
    --bg: #f8fafc;
    --panel: #ffffff;
    --ink: #0f172a;
    --muted: #64748b;
    --line: #e2e8f0;
    --navy: #1e293b;
    --blue: #2563eb;
    --blue-soft: #eff6ff;
    --green: #059669;
    --green-soft: #ecfdf5;
    --red: #dc2626;
    --red-soft: #fef2f2;
    --amber: #d97706;
    --amber-soft: #fffbeb;
    --shadow: 0 4px 16px -2px rgba(15, 23, 42, 0.05);
}}
* {{ box-sizing: border-box; }}
body {{ margin: 0; background: var(--bg); color: var(--ink); font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Pretendard", sans-serif; line-height: 1.6; }}
.wrap {{ max-width: 1040px; margin: auto; padding: 28px 20px 48px; }}

.top {{ display: flex; justify-content: space-between; align-items: flex-start; gap: 16px; margin-bottom: 22px; }}
.eyebrow {{ font-size: 12px; letter-spacing: 0.05em; color: var(--blue); font-weight: 700; text-transform: uppercase; }}
.title {{ font-size: 26px; letter-spacing: -0.03em; margin: 4px 0; color: var(--navy); font-weight: 800; }}
.sub {{ color: var(--muted); font-size: 13px; }}
.stamp {{ border: 1px solid var(--line); background: var(--panel); padding: 8px 14px; border-radius: 8px; font-size: 12px; color: var(--muted); white-space: nowrap; font-weight: 500; }}

.hero {{ display: grid; grid-template-columns: 1.3fr 1fr; gap: 14px; margin-bottom: 16px; }}
.card {{ background: var(--panel); border: 1px solid var(--line); border-radius: 14px; padding: 20px; box-shadow: var(--shadow); }}
.kicker {{ font-size: 12px; color: var(--muted); font-weight: 600; }}
.price {{ font-size: 32px; font-weight: 800; letter-spacing: -0.03em; margin: 6px 0 2px; color: var(--navy); }}
.change {{ display: inline-flex; align-items: center; gap: 6px; background: var(--green-soft); color: var(--green); border-radius: 6px; padding: 4px 10px; font-size: 13px; font-weight: 700; margin-top: 4px; }}

.metrics {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px; margin-top: 18px; }}
.metric {{ padding: 10px 12px; background: #f1f5f9; border-radius: 8px; }}
.metric span {{ display: block; font-size: 11px; color: var(--muted); }}
.metric strong {{ font-size: 14px; display: block; margin-top: 2px; color: var(--navy); }}

.position-head {{ display: flex; justify-content: space-between; align-items: center; gap: 12px; }}
.tag {{ font-size: 11px; padding: 4px 10px; border-radius: 999px; background: var(--amber-soft); color: var(--amber); font-weight: 700; }}
.holding-grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 12px; margin-top: 16px; }}
.holding-grid span {{ display: block; font-size: 12px; color: var(--muted); }}
.holding-grid strong {{ font-size: 18px; color: var(--navy); font-weight: 700; }}
.pnl {{ margin-top: 14px; padding: 12px; border-radius: 8px; background: var(--green-soft); display: flex; justify-content: space-between; color: var(--green); font-weight: 700; font-size: 13px; }}

.section {{ margin-top: 18px; }}
.section-title {{ display: flex; align-items: center; gap: 8px; margin: 0 0 12px; font-size: 16px; letter-spacing: -0.02em; color: var(--navy); font-weight: 700; }}
.num {{ width: 24px; height: 24px; border-radius: 6px; background: var(--blue-soft); color: var(--blue); display: inline-flex; align-items: center; justify-content: center; font-size: 12px; font-weight: 800; }}

.conclusion {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 12px; }}
.conclusion article {{ border: 1px solid var(--line); border-radius: 12px; padding: 16px; background: var(--panel); box-shadow: var(--shadow); }}
.conclusion b {{ display: block; font-size: 14px; margin-bottom: 6px; color: var(--navy); }}
.conclusion p {{ margin: 0; font-size: 13px; color: var(--muted); line-height: 1.5; }}
.status {{ font-size: 10px; font-weight: 800; padding: 3px 8px; border-radius: 4px; display: inline-block; margin-bottom: 8px; }}
.status.good {{ color: var(--green); background: var(--green-soft); }}
.status.watch {{ color: var(--amber); background: var(--amber-soft); }}

.grid2 {{ display: grid; grid-template-columns: 1fr 1fr; gap: 14px; }}
.subhead {{ font-size: 14px; font-weight: 700; margin: 0 0 12px; color: var(--navy); }}
.flow-row {{ display: flex; align-items: center; justify-content: space-between; padding: 9px 0; border-bottom: 1px solid var(--line); font-size: 13px; }}
.flow-val {{ font-weight: 700; }}
.buy {{ color: var(--green); }}
.sell {{ color: var(--red); }}
.thesis {{ display: flex; gap: 10px; align-items: flex-start; padding: 10px 0; border-bottom: 1px solid var(--line); font-size: 13px; }}
.dot {{ width: 6px; height: 6px; border-radius: 50%; background: var(--blue); margin-top: 8px; flex-shrink: 0; }}

.news-item {{ display: grid; grid-template-columns: 24px 1fr; gap: 10px; padding: 12px; border: 1px solid var(--line); border-radius: 8px; margin-bottom: 10px; background: #fafafa; }}
.news-num {{ font-weight: 800; color: var(--blue); font-size: 13px; }}
.news-item h3 {{ font-size: 13px; margin: 0 0 4px; color: var(--navy); }}
.news-item p {{ font-size: 12px; color: var(--muted); margin: 0; line-height: 1.4; }}
.news-item a {{ font-size: 11px; color: var(--blue); text-decoration: none; display: inline-block; margin-top: 4px; font-weight: 600; }}

.catalyst {{ display: flex; gap: 12px; align-items: flex-start; }}
.datebox {{ background: var(--navy); color: white; border-radius: 8px; padding: 10px; text-align: center; min-width: 68px; }}
.datebox strong {{ display: block; font-size: 20px; font-weight: 800; }}
.datebox span {{ font-size: 10px; opacity: 0.8; }}

.actions {{ display: grid; grid-template-columns: repeat(2, 1fr); gap: 10px; }}
.action {{ border: 1px solid var(--line); border-radius: 10px; padding: 14px; }}
.action h3 {{ font-size: 13px; margin: 0 0 6px; color: var(--navy); }}
.action p {{ font-size: 12px; color: var(--muted); margin: 0; line-height: 1.4; }}
.action.up {{ background: #f0fdf4; border-color: #bbf7d0; }}
.action.down {{ background: #fef2f2; border-color: #fecaca; }}
.action.event {{ background: #eff6ff; border-color: #bfdbfe; }}
.action.neutral {{ background: #fffbeb; border-color: #fef3c7; }}

.journal textarea {{ width: 100%; min-height: 70px; border: 1px solid var(--line); border-radius: 8px; padding: 10px; font: inherit; font-size: 12px; background: #fafafa; margin-bottom: 8px; }}
.journal label {{ display: block; font-size: 11px; font-weight: 700; margin-bottom: 4px; color: var(--navy); }}
.emotion button {{ border: 1px solid var(--line); background: #fff; border-radius: 6px; padding: 6px 10px; font-size: 12px; color: var(--muted); cursor: pointer; margin: 2px; }}
.emotion button.active {{ border-color: var(--blue); background: var(--blue-soft); color: var(--blue); font-weight: 700; }}

.verdict {{ margin-top: 20px; padding: 18px 22px; border-radius: 12px; background: var(--navy); color: #fff; display: flex; justify-content: space-between; align-items: center; gap: 12px; box-shadow: var(--shadow); }}
.verdict span {{ font-size: 12px; opacity: 0.75; }}
.verdict strong {{ font-size: 17px; font-weight: 700; color: #38bdf8; }}

footer {{ font-size: 11px; color: var(--muted); text-align: center; margin-top: 24px; }}

@media(max-width: 768px) {{
    .hero, .grid2, .conclusion, .actions {{ grid-template-columns: 1fr; }}
    .verdict {{ flex-direction: column; align-items: flex-start; }}
}}
</style>
</head>
<body>
<div class="wrap">
<header class="top">
  <div>
    <div class="eyebrow">DAILY INVESTMENT BRIEF · KRX 005930</div>
    <h1 class="title">삼성전자 일일 투자 분석</h1>
    <div class="sub">{today_str} 기준 · 핵심 이벤트: 3분기 실적 컨퍼런스콜</div>
  </div>
  <div class="stamp">데이터 기준: <b>{date_badge}</b></div>
</header>

<div class="hero">
  <section class="card">
    <div class="kicker">삼성전자 · 005930</div>
    <div class="price">{price}원</div>
    <div class="change">전일 대비: {diff}</div>
    <div class="metrics">
      <div class="metric"><span>거래량</span><strong>{volume}</strong></div>
      <div class="metric"><span>장중 범위</span><strong>228,000–243,000</strong></div>
      <div class="metric"><span>시가총액</span><strong>약 1,415조 원</strong></div>
    </div>
  </section>
  <section class="card">
    <div class="position-head">
      <div>
        <div class="kicker">내 보유 현황</div>
        <h2 style="font-size:16px;margin:2px 0 0;color:var(--navy)">168주 · 평단 238,000원</h2>
      </div>
      <span class="tag">실적 발표 대기</span>
    </div>
    <div class="holding-grid">
      <div><span>매수 원금</span><strong>39,984,000원</strong></div>
      <div><span>현재 평가액</span><strong>40,656,000원</strong></div>
    </div>
    <div class="pnl">
      <span>평가손익</span>
      <span>+672,000원 (+1.68%)</span>
    </div>
  </section>
</div>

<section class="section">
<h2 class="section-title"><span class="num">01</span>오늘의 결론 3줄</h2>
<div class="conclusion">
  <article><span class="status good">가설 유지</span><b>AI 메모리 이익 기대 유효</b><p>3분기 잠정 매출 195조, 영업이익 107.4조 수준. 확정 실적과 세부 사업부 질적 성장 확인 필요.</p></article>
  <article><span class="status good">수급 개선</span><b>외국인·기관 동반 순매수</b><p>외국인과 기관의 쌍끌이 매수로 수급 지지선 형성. 단, 장기 매도세 전환 여부는 관찰 필요.</p></article>
  <article><span class="status watch">추격 주의</span><b>실적 컨퍼런스콜 단기 분기점</b><p>급등 후 차익 실현 물량 출회 가능성 보유. 메모리 가격 전망 및 주주환원 발언 검증 단계.</p></article>
</div>
</section>

<section class="section">
<h2 class="section-title"><span class="num">02</span>오늘 뭐가 바뀌었나</h2>
<div class="grid2">
  <div class="card">
    <h3 class="subhead">수급 현황</h3>
    <div class="flow-row"><span>외국인</span><span class="flow-val buy">순매수 +5,990억 원</span></div>
    <div class="flow-row"><span>기관</span><span class="flow-val buy">순매수 +5,202억 원</span></div>
    <div class="flow-row"><span>개인</span><span class="flow-val sell">순매도 -1조 1,134억 원</span></div>
  </div>
  <div class="card">
    <h3 class="subhead">투자 가설 및 기술적 위치</h3>
    <div class="thesis"><span class="dot"></span><div><b>메모리 가격·AI 수요:</b> DRAM/NAND/HBM 수요 강세 유지 여부 확인.</div></div>
    <div class="thesis"><span class="dot"></span><div><b>기술적 위치:</b> 상방 250,000원 돌파 관찰선, 하방 220,000원 리스크 관리선.</div></div>
  </div>
</div>
</section>

<section class="section">
<h2 class="section-title"><span class="num">03</span>뉴스 & 촉매</h2>
<div class="grid2">
  <div class="card">
    <div class="news-item">
      <div class="news-num">01</div>
      <div>
        <h3>3분기 실적 컨퍼런스콜 진행</h3>
        <p>HBM3E 퀄테스트 진전 상황 및 4분기 메모리 가이던스 집중 검증.</p>
        <a href="https://www.samsung.com/global/ir/" target="_blank">삼성 IR 페이지 ↗</a>
      </div>
    </div>
  </div>
  <div class="card">
    <h3 class="subhead">내일 가장 중요한 일정</h3>
    <div class="catalyst">
      <div class="datebox"><strong>29</strong><span>10월</span></div>
      <div>
        <h3 style="margin:0 0 4px;font-size:14px;color:var(--navy)">오전 10:00 · 3분기 실적 발표</h3>
        <p style="font-size:12px;color:var(--muted);margin:0">확정 실적, HBM 공급 가시성, 주주환원 정책 발언 주시.</p>
      </div>
    </div>
  </div>
</div>
</section>

<section class="section">
<h2 class="section-title"><span class="num">04</span>If–Then 액션 플랜</h2>
<div class="actions">
  <div class="action up"><h3>IF 250,000원 강하게 돌파 시</h3><p>추격 매수보다는 종가 안착 여부와 실적 발표 내용 검증 후 홀딩 전략 유지.</p></div>
  <div class="action down"><h3>IF 220,000원 이탈 시</h3><p>반등 가설 훼손 여부 판단 후 일부 비중 축소 및 리스크 관리 라인 가동.</p></div>
</div>
</section>

<section class="section">
<h2 class="section-title"><span class="num">05</span>매매일지</h2>
<div class="grid2">
  <div class="card journal">
    <h3 class="subhead">오늘 거래 기록</h3>
    <label for="trade">오늘 한 거래</label>
    <textarea id="trade" placeholder="예: 거래 없음 / 관망"></textarea>
    <label for="reason">이유 및 사후 점검</label>
    <textarea id="reason" placeholder="예: 실적 발표 전 변동성 관리"></textarea>
  </div>
  <div class="card">
    <h3 class="subhead">감정 상태 체크</h3>
    <div class="emotion" id="emotion">
      <button type="button" data-v="차분함">차분함</button>
      <button type="button" data-v="FOMO·추격">FOMO·추격</button>
      <button type="button" data-v="불안">불안</button>
      <button type="button" data-v="관망">관망</button>
    </div>
    <div style="margin-top:16px;text-align:right">
      <button type="button" id="saveBtn" style="background:var(--navy);color:#fff;border:0;padding:8px 14px;border-radius:6px;font-weight:700;cursor:pointer">일지 저장</button>
    </div>
  </div>
</div>
</section>

<div class="verdict">
  <div>
    <span>오늘의 한 줄 결론</span><br>
    <strong>"오늘은 추격 매수 자리보다 '관찰'의 자리입니다."</strong>
  </div>
  <span>실적 콜 확인 → 가격 안착 확인 → 계획대로 대응</span>
</div>

<footer>
  본 보고서는 매일 GitHub Actions를 통해 자동 업데이트되며 텔레그램으로 전송됩니다.
</footer>
</div>

<script>
(function(){{
 const fields=['trade','reason'];
 const emotion=document.getElementById('emotion');
 emotion.addEventListener('click',e=>{{
   const b=e.target.closest('button[data-v]'); if(!b)return;
   emotion.querySelectorAll('button').forEach(x=>x.classList.toggle('active',x===b));
 }});
 const key='samsung_daily_journal';
 function load(){{try{{
   const d=JSON.parse(localStorage.getItem(key)||'{{}}');
   fields.forEach(id=>{{if(d[id]!==undefined)document.getElementById(id).value=d[id]}});
   if(d.emotion){{const b=[...emotion.querySelectorAll('button')].find(x=>x.dataset.v===d.emotion);if(b)b.classList.add('active')}}
 }}catch(e){{}}}}
 document.getElementById('saveBtn').addEventListener('click',()=>{{
   const d={{}};fields.forEach(id=>d[id]=document.getElementById(id).value);
   const b=emotion.querySelector('button.active');d.emotion=b?b.dataset.v:'';
   try{{localStorage.setItem(key,JSON.stringify(d));alert('일지가 저장되었습니다.')}}catch(e){{}}
 }});
 load();
}})();
</script>
</body>
</html>
"""
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html_content)
    print("✅ index.html 대시보드 생성 완료!")

if __name__ == "__main__":
    fetch_samsung_data()
