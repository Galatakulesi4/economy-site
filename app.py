from flask import Flask, request, redirect, render_template_string, session
from datetime import datetime
import sqlite3
import os

app = Flask(__name__)

app.secret_key = os.environ.get("SECRET_KEY", "change-this-secret-key")
PASSWORD = os.environ.get("CHAT_PASSWORD", "SertSena")

def get_db():
    conn = sqlite3.connect("chat.db")
    conn.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sender TEXT,
            text TEXT,
            time TEXT
        )
    """)
    return conn

# ─────────────────────────────────────────────
#  SAMPLE / DEMO DATA  (clearly labelled)
# ─────────────────────────────────────────────
SAMPLE_DATA = {
    "note": "⚠️ SAMPLE / DEMO DATA — illustrative values for UI demonstration only",
    "countries": {
        "Turkey":        {"gdp": 1320, "gdp_growth": 3.4,  "inflation": 30.87, "unemployment": 8.5,  "interest_rate": 46.0, "usd_exchange": 32.5,  "current_account": -24.1},
        "Iran":          {"gdp": 367,  "gdp_growth": 4.2,  "inflation": 44.5,  "unemployment": 10.2, "interest_rate": 23.0, "usd_exchange": 42000, "current_account": 5.2},
        "Germany":       {"gdp": 4456, "gdp_growth": -0.2, "inflation": 2.3,   "unemployment": 5.8,  "interest_rate": 4.5,  "usd_exchange": 0.93,  "current_account": 176.0},
        "United States": {"gdp": 27360,"gdp_growth": 2.8,  "inflation": 3.5,   "unemployment": 3.9,  "interest_rate": 5.25, "usd_exchange": 1.0,   "current_account": -821.0},
        "China":         {"gdp": 17795,"gdp_growth": 5.2,  "inflation": 0.1,   "unemployment": 5.1,  "interest_rate": 3.45, "usd_exchange": 7.24,  "current_account": 253.0},
    }
}

INDICATOR_META = {
    "gdp": {
        "label": "GDP (USD Billion)",
        "icon": "📊",
        "meaning": "Gross Domestic Product — the total monetary value of all goods and services produced within a country in a year.",
        "why_matters": "GDP measures economic size. Larger GDP means more resources, stronger negotiating power, and greater capacity for public investment.",
        "interpret": "High GDP = large, productive economy. Low GDP ≠ poor governance — smaller nations have smaller GDPs by nature. Growth rate matters as much as absolute size.",
        "unit": "B USD",
    },
    "gdp_growth": {
        "label": "GDP Growth (%)",
        "icon": "📈",
        "meaning": "The percentage change in GDP compared to the previous year, adjusted for inflation (real growth).",
        "why_matters": "Growth drives employment creation, corporate earnings and fiscal revenue. Sustained growth signals economic health.",
        "interpret": "Above 3% = solid expansion. 0–2% = sluggish. Negative = recession. High-income nations often grow slower than emerging markets.",
        "unit": "%",
    },
    "inflation": {
        "label": "Inflation (CPI, %)",
        "icon": "🔥",
        "meaning": "Consumer Price Index inflation — the annual percentage rise in the average price level of goods and services households buy.",
        "why_matters": "High inflation erodes real purchasing power, distorts investment decisions, and reduces the real return on savings.",
        "interpret": "2% = widely considered healthy. Above 10% = high, harmful to savings. Above 30% = severe structural problem requiring policy action.",
        "unit": "%",
    },
    "unemployment": {
        "label": "Unemployment (%)",
        "icon": "👥",
        "meaning": "The share of the labor force that is jobless and actively seeking employment.",
        "why_matters": "Unemployment represents wasted human capital and is linked to social stress, reduced consumption and fiscal pressure.",
        "interpret": "Below 4% = near full employment (may cause wage inflation). 5–8% = moderate slack. Above 10% = significant problem.",
        "unit": "%",
    },
    "interest_rate": {
        "label": "Policy Interest Rate (%)",
        "icon": "🏦",
        "meaning": "The benchmark rate set by the central bank, used to guide borrowing costs across the economy.",
        "why_matters": "The policy rate is the primary lever for controlling inflation and credit growth. It signals the central bank's stance.",
        "interpret": "High rates = tight policy, expensive credit, reduces inflation. Low rates = loose policy, cheap credit, stimulates growth but may raise inflation.",
        "unit": "%",
    },
    "usd_exchange": {
        "label": "USD Exchange Rate",
        "icon": "💱",
        "meaning": "The number of domestic currency units needed to buy one US Dollar.",
        "why_matters": "Exchange rates affect import costs, inflation, external debt burden and export competitiveness.",
        "interpret": "Rising value (more local currency per USD) = depreciation, often inflationary. Falling value = appreciation, can reduce import costs.",
        "unit": "local/USD",
    },
    "current_account": {
        "label": "Current Account (USD Billion)",
        "icon": "⚖️",
        "meaning": "The net flow of goods, services, income and transfers between a country and the rest of the world.",
        "why_matters": "A deficit means a country spends more on imports than it earns from exports — requiring external financing. A surplus is the opposite.",
        "interpret": "Large surplus = strong external position (e.g. Germany, China). Large deficit = dependency on foreign capital inflows (vulnerability).",
        "unit": "B USD",
    },
}

BASE_STYLE = """
<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;600&family=Sora:wght@300;400;600;700&display=swap');

:root{
    --navy:#07111f;
    --blue:#12355b;
    --deep:#0f172a;
    --gold:#c49a3a;
    --soft:#f3f6fa;
    --text:#222;
    --muted:#64748b;
    /* dark UI additions */
    --dk-bg:#0b1120;
    --dk-card:#111827;
    --dk-border:#1e2d45;
    --dk-accent:#3b82f6;
    --dk-gold:#f59e0b;
    --dk-green:#10b981;
    --dk-red:#ef4444;
    --dk-text:#e2e8f0;
    --dk-muted:#64748b;
}
body{
    margin:0;
    font-family:'Sora', Arial, sans-serif;
    background:var(--soft);
    color:var(--text);
    line-height:1.75;
}
.topbar{
    background:#050b14;
    color:#cbd5e1;
    padding:9px 30px;
    font-size:13px;
    font-family:'IBM Plex Mono', monospace;
}
.header{
    background:linear-gradient(135deg,#06111f,#12355b,#1d3557,#0f172a);
    color:white;
    padding:55px 30px;
    text-align:center;
}
.header h1{
    font-size:44px;
    margin:0;
    letter-spacing:.5px;
    font-family:'Sora', sans-serif;
    font-weight:700;
}
.header p{
    margin-top:10px;
    color:#dbeafe;
}
.nav{
    background:#0b1f36;
    padding:14px;
    text-align:center;
    position:sticky;
    top:0;
    z-index:10;
    box-shadow:0 3px 8px rgba(0,0,0,.16);
}
.nav a{
    color:white;
    margin:0 15px;
    text-decoration:none;
    font-weight:bold;
    font-size:14px;
}
.nav a:hover{color:#facc15;}
.container{
    max-width:1180px;
    margin:32px auto;
    padding:0 22px;
}
.grid{
    display:grid;
    grid-template-columns:2fr 1fr;
    gap:24px;
}
.article,.side-card{
    background:white;
    border-radius:16px;
    box-shadow:0 4px 14px rgba(0,0,0,.08);
}
.article{padding:30px;margin-bottom:24px;}
.side-card{padding:22px;margin-bottom:20px;}
.article h2,.side-card h3{color:#12355b;margin-top:0;}
.article h2{font-size:28px;}
.article h3{color:#1e3a5f;}
.article img{width:100%;border-radius:14px;margin:16px 0;}
.badge{
    display:inline-block;
    background:#e8f1ff;
    color:#12355b;
    padding:5px 12px;
    border-radius:22px;
    font-size:12px;
    font-weight:bold;
    margin-bottom:10px;
}
.badge-demo{
    display:inline-block;
    background:#fef3c7;
    color:#92400e;
    padding:5px 14px;
    border-radius:22px;
    font-size:12px;
    font-weight:bold;
    border:1px dashed #f59e0b;
}
.data-box{
    background:#f8fafc;
    border-left:5px solid #12355b;
    padding:16px;
    border-radius:10px;
    margin:18px 0;
}
.quote{
    background:#fff7ed;
    border-left:5px solid var(--gold);
    padding:16px;
    border-radius:10px;
    margin:18px 0;
}
.table{
    width:100%;
    border-collapse:collapse;
    margin:18px 0;
    background:#fff;
}
.table th{background:#12355b;color:white;}
.table th,.table td{border:1px solid #d8dee9;padding:10px;text-align:left;}
.news-list li{margin-bottom:10px;}
.footer{text-align:center;color:#777;padding:38px;font-size:13px;}
.tiny-access{color:#777;text-decoration:none;font-size:11px;}
.tiny-access:hover{color:#333;}

/* ── DARK DATA SECTIONS ── */
.dark-section{
    background:var(--dk-bg);
    padding:40px 0;
    margin:0 -22px;
}
.dark-section .container{margin:0 auto;}

.indicator-grid{
    display:grid;
    grid-template-columns:repeat(auto-fill,minmax(300px,1fr));
    gap:20px;
    margin:24px 0;
}
.indicator-card{
    background:var(--dk-card);
    border:1px solid var(--dk-border);
    border-radius:14px;
    padding:22px;
    color:var(--dk-text);
    transition:transform .2s, box-shadow .2s;
}
.indicator-card:hover{
    transform:translateY(-3px);
    box-shadow:0 8px 24px rgba(0,0,0,.4);
}
.indicator-card .ic-icon{font-size:28px;margin-bottom:8px;}
.indicator-card .ic-label{
    font-size:11px;
    text-transform:uppercase;
    letter-spacing:1.5px;
    color:var(--dk-muted);
    font-family:'IBM Plex Mono',monospace;
}
.indicator-card .ic-value{
    font-size:36px;
    font-weight:700;
    color:var(--dk-accent);
    font-family:'IBM Plex Mono',monospace;
    margin:4px 0;
}
.indicator-card .ic-unit{font-size:12px;color:var(--dk-muted);}
.indicator-card .ic-divider{
    border:none;
    border-top:1px solid var(--dk-border);
    margin:14px 0;
}
.ic-pill{
    font-size:11px;
    padding:3px 9px;
    border-radius:20px;
    font-weight:600;
    margin-bottom:6px;
    display:inline-block;
}
.ic-meaning{font-size:13px;color:#94a3b8;margin:6px 0 4px;}
.ic-interpret{font-size:12px;color:#64748b;font-style:italic;}

/* explanation card */
.explain-card{
    background:var(--dk-card);
    border:1px solid var(--dk-border);
    border-radius:12px;
    padding:18px 22px;
    color:var(--dk-text);
    margin-bottom:16px;
}
.explain-card h4{
    color:var(--dk-accent);
    margin:0 0 8px;
    font-size:15px;
    display:flex;
    align-items:center;
    gap:8px;
}
.explain-row{
    display:grid;
    grid-template-columns:1fr 1fr 1fr;
    gap:12px;
    margin-top:10px;
}
.explain-item{
    background:#0f172a;
    border-radius:8px;
    padding:12px;
    font-size:12px;
    color:#cbd5e1;
}
.explain-item strong{
    display:block;
    color:var(--dk-gold);
    margin-bottom:4px;
    font-size:11px;
    text-transform:uppercase;
    letter-spacing:.8px;
}

/* comparison table dark */
.dk-table{
    width:100%;
    border-collapse:collapse;
    font-family:'IBM Plex Mono',monospace;
    font-size:13px;
    color:var(--dk-text);
}
.dk-table th{
    background:#1e2d45;
    color:#94a3b8;
    padding:12px 14px;
    text-align:left;
    font-size:11px;
    text-transform:uppercase;
    letter-spacing:1px;
}
.dk-table td{
    padding:11px 14px;
    border-bottom:1px solid #1a2840;
}
.dk-table tr:hover td{background:#131f33;}
.dk-table .country-name{
    font-weight:600;
    color:#e2e8f0;
    font-family:'Sora',sans-serif;
}
.num-pos{color:var(--dk-green);}
.num-neg{color:var(--dk-red);}
.num-neu{color:#94a3b8;}
.num-warn{color:var(--dk-gold);}

/* chart wrapper */
.chart-wrap{
    background:var(--dk-card);
    border:1px solid var(--dk-border);
    border-radius:14px;
    padding:24px;
    margin:24px 0;
}
.chart-wrap h3{
    color:var(--dk-text);
    margin:0 0 16px;
    font-size:16px;
    font-family:'Sora',sans-serif;
}
.chart-wrap canvas{max-height:280px;}

.demo-banner{
    background:linear-gradient(90deg,#1c1400,#2d1f00);
    border:1px dashed #f59e0b;
    border-radius:10px;
    padding:12px 18px;
    color:#fbbf24;
    font-size:13px;
    margin-bottom:24px;
    font-family:'IBM Plex Mono',monospace;
}
.section-title{
    color:var(--dk-text);
    font-size:22px;
    font-family:'Sora',sans-serif;
    font-weight:700;
    margin:0 0 6px;
}
.section-sub{
    color:var(--dk-muted);
    font-size:14px;
    margin-bottom:24px;
}

@media(max-width:850px){
    .grid{grid-template-columns:1fr;}
    .header h1{font-size:30px;}
    .nav a{display:inline-block;margin:6px 8px;}
    .indicator-grid{grid-template-columns:1fr;}
    .explain-row{grid-template-columns:1fr;}
}
</style>
"""

CHARTJS = '<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>'

def page(title, content, use_charts=False):
    extra = CHARTJS if use_charts else ""
    return f"""
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>{title}</title>
<meta name="viewport" content="width=device-width, initial-scale=1.0">
{BASE_STYLE}
{extra}
</head>
<body>

<div class="topbar">
    Türkiye Macro Desk · GDP · Inflation · Markets · Trade · Geopolitical Economy
</div>

<div class="header">
    <h1>Türkiye Economic Monitor</h1>
    <p>Independent-style macroeconomic briefing on Türkiye, markets, trade, policy and global risk</p>
</div>

<div class="nav">
    <a href="/">Home</a>
    <a href="/markets">Markets</a>
    <a href="/finance">Finance</a>
    <a href="/trade">Trade</a>
    <a href="/policy">Policy</a>
    <a href="/geopolitics">Geopolitics</a>
    <a href="/data">Data Board</a>
</div>

<div class="container">
{content}
</div>

<div class="footer">
    © 2026 Türkiye Economic Monitor · Public macroeconomic commentary ·
    <a class="tiny-access" href="/archive-briefing">archive</a>
</div>

</body>
</html>
"""

# ─────────────────────────────────────────────
#  HELPER: build indicator cards for one country
# ─────────────────────────────────────────────
def build_indicator_cards(country):
    d = SAMPLE_DATA["countries"][country]
    cards = []
    for key, meta in INDICATOR_META.items():
        val = d[key]
        # format value nicely
        if key == "usd_exchange":
            disp = f"{val:,.2f}" if val < 1000 else f"{val:,.0f}"
        elif key in ("gdp", "current_account"):
            disp = f"{val:+,.1f}" if key == "current_account" else f"{val:,.0f}"
        else:
            disp = f"{val:.1f}"

        # colour hint
        if key == "inflation":
            col = "num-pos" if val < 5 else ("num-warn" if val < 15 else "num-neg")
        elif key == "gdp_growth":
            col = "num-pos" if val > 2 else ("num-warn" if val >= 0 else "num-neg")
        elif key == "unemployment":
            col = "num-pos" if val < 5 else ("num-warn" if val < 8 else "num-neg")
        elif key == "current_account":
            col = "num-pos" if val > 0 else "num-neg"
        else:
            col = "num-neu"

        cards.append(f"""
        <div class="indicator-card">
            <div class="ic-icon">{meta['icon']}</div>
            <div class="ic-label">{meta['label']}</div>
            <div class="ic-value {col}">{disp}</div>
            <div class="ic-unit">{meta['unit']}</div>
            <hr class="ic-divider">
            <div class="ic-meaning">{meta['meaning']}</div>
            <div class="ic-interpret">{meta['interpret']}</div>
        </div>""")
    return "\n".join(cards)

# ─────────────────────────────────────────────
#  HELPER: explanation cards
# ─────────────────────────────────────────────
def build_explanation_cards():
    html = []
    for key, meta in INDICATOR_META.items():
        html.append(f"""
        <div class="explain-card">
            <h4>{meta['icon']} {meta['label']}</h4>
            <div class="explain-row">
                <div class="explain-item">
                    <strong>What it means</strong>
                    {meta['meaning']}
                </div>
                <div class="explain-item">
                    <strong>Why it matters</strong>
                    {meta['why_matters']}
                </div>
                <div class="explain-item">
                    <strong>How to interpret</strong>
                    {meta['interpret']}
                </div>
            </div>
        </div>""")
    return "\n".join(html)

# ─────────────────────────────────────────────
#  HELPER: dark comparison table
# ─────────────────────────────────────────────
def build_comparison_table():
    countries = list(SAMPLE_DATA["countries"].keys())
    rows = []
    for c in countries:
        d = SAMPLE_DATA["countries"][c]
        def cls(key, v):
            if key == "inflation":   return "num-pos" if v < 5 else ("num-warn" if v < 15 else "num-neg")
            if key == "gdp_growth":  return "num-pos" if v > 2 else ("num-warn" if v >= 0 else "num-neg")
            if key == "unemployment":return "num-pos" if v < 5 else ("num-warn" if v < 8 else "num-neg")
            if key == "current_account": return "num-pos" if v > 0 else "num-neg"
            return "num-neu"

        usd = d['usd_exchange']
        usd_str = f"{usd:,.2f}" if usd < 1000 else f"{usd:,.0f}"
        rows.append(f"""
        <tr>
            <td class="country-name">{c}</td>
            <td class="num-neu">${d['gdp']:,.0f}B</td>
            <td class="{cls('gdp_growth', d['gdp_growth'])}">{d['gdp_growth']:+.1f}%</td>
            <td class="{cls('inflation', d['inflation'])}">{d['inflation']:.1f}%</td>
            <td class="{cls('unemployment', d['unemployment'])}">{d['unemployment']:.1f}%</td>
            <td class="num-neu">{d['interest_rate']:.2f}%</td>
            <td class="num-neu">{usd_str}</td>
            <td class="{cls('current_account', d['current_account'])}">${d['current_account']:+,.1f}B</td>
        </tr>""")
    return "\n".join(rows)

@app.route("/")
def home():
    content = """
    <div class="grid">
        <div>
            <div class="article">
                <span class="badge">Main Analysis</span>
                <h2>Türkiye Economic Outlook: Growth, Inflation, External Balance and Policy Credibility</h2>
                <p>
                Türkiye is one of the most strategically important emerging-market economies. It connects Europe,
                the Middle East, the Black Sea, the Caucasus and Central Asia. Its economy is large, diversified and
                institutionally complex: manufacturing, tourism, construction, financial services, logistics, defense
                industry, agriculture and technology all play important roles.
                </p>
                <p>
                According to World Bank country data, Türkiye's GDP was around 1.32 trillion USD in 2024, with a
                population of about 85.5 million. This makes Türkiye a major G20 and OECD economy. However, size alone
                does not remove vulnerability. The country still faces inflation persistence, exchange-rate sensitivity,
                current-account pressure and high dependence on imported energy.
                </p>
                <img src="https://images.unsplash.com/photo-1524231757912-21f4fe3a7200?auto=format&fit=crop&w=1400&q=80">
                <div class="data-box">
                    <b>Macro Snapshot</b><br>
                    GDP: about 1.32 trillion USD in 2024<br>
                    Population: about 85.5 million in 2024<br>
                    TÜİK headline indicators show annual CPI at 30.87% for March 2026 and unemployment at 8.5% for February 2026.<br>
                    OECD projects Türkiye growth at 3.6% in 2025, 3.4% in 2026 and 4.0% in 2027.<br>
                    IMF/Reuters reported a 2026 growth forecast of 3.4%, with inflation expected to remain elevated.
                </div>
            </div>

            <div class="article">
                <span class="badge">GDP</span>
                <h2>GDP and Real Economy: Strong Capacity, Moderate Growth</h2>
                <p>
                Türkiye's GDP structure is supported by a broad domestic market and a diversified production base.
                The country is not dependent on a single sector. Manufacturing exports, tourism income, construction,
                services, retail, transportation and defense-related production all contribute to national output.
                </p>
                <p>
                The important issue is not only whether GDP grows, but how it grows. If growth is driven mainly by
                credit expansion, consumption and nominal price increases, it may create inflationary pressure.
                If growth comes from productivity, technology, exports and investment, it becomes more sustainable.
                </p>
                <p>
                The current macroeconomic transition is an attempt to reduce inflation without producing a deep
                slowdown. This is difficult because tight monetary policy reduces credit growth and demand, while firms
                still face high input costs, wage pressure and exchange-rate uncertainty.
                </p>
                <table class="table">
                    <tr><th>Area</th><th>Economic Meaning</th><th>Risk</th></tr>
                    <tr><td>Domestic Demand</td><td>Supports growth and tax revenues</td><td>Can keep inflation high</td></tr>
                    <tr><td>Exports</td><td>Improves foreign-currency inflow</td><td>Weak EU demand can hurt sales</td></tr>
                    <tr><td>Tourism</td><td>Supports services balance</td><td>Geopolitical shocks can reduce arrivals</td></tr>
                    <tr><td>Construction</td><td>Creates employment and local demand</td><td>Highly sensitive to interest rates</td></tr>
                </table>
            </div>

            <div class="article">
                <span class="badge">Inflation</span>
                <h2>Inflation: Türkiye's Central Macroeconomic Challenge</h2>
                <p>
                Inflation is the main problem affecting households, companies and investors. High inflation reduces
                purchasing power, weakens savings behavior, complicates pricing, distorts financial statements and
                raises uncertainty. Even when nominal wages increase, households may feel poorer if prices rise faster
                than income.
                </p>
                <p>
                Türkiye's inflation problem is multi-channel. Exchange-rate pass-through, energy import costs, rents,
                food prices, wage adjustments, expectations and fiscal conditions all interact. Because Türkiye imports
                a large share of its energy needs, global oil and gas prices can quickly become domestic inflation pressure.
                </p>
                <p>
                Disinflation requires more than one policy rate decision. It requires credibility, coordination,
                fiscal discipline and stable expectations. If firms and consumers believe prices will keep rising fast,
                they change behavior today: firms increase prices early, workers demand higher wages, and consumers may
                bring purchases forward. This creates inflation inertia.
                </p>
                <img src="https://images.unsplash.com/photo-1642790106117-e829e14a795f?auto=format&fit=crop&w=1400&q=80">
                <div class="quote">
                    <b>Interpretation:</b> The key question is whether inflation falls because demand weakens temporarily,
                    or because expectations, credibility and policy coordination improve permanently.
                </div>
            </div>

            <div class="article">
                <span class="badge">Central Bank</span>
                <h2>Monetary Policy: Interest Rates, Lira Stability and Credibility</h2>
                <p>
                The Central Bank of the Republic of Türkiye plays a central role in the adjustment process. A tight
                monetary stance can reduce inflation expectations, increase the attractiveness of lira assets and slow
                excessive credit expansion. However, high interest rates also increase borrowing costs for firms and
                households.
                </p>
                <p>
                For investors, the policy rate is not only a number. It is a signal. If the signal is credible,
                market participants may expect inflation to fall. If the signal is not credible, high rates alone may
                fail to stabilize expectations.
                </p>
                <p>
                The Turkish lira is also a confidence indicator. Currency stability depends on inflation expectations,
                foreign reserves, global risk appetite, current-account dynamics and political risk. A stable currency
                can reduce pass-through to prices, but forced stability without credibility may create future pressure.
                </p>
            </div>

            <div class="article">
                <span class="badge">External Balance</span>
                <h2>Current Account and Energy Dependence</h2>
                <p>
                Türkiye's current account is structurally sensitive to energy imports. When oil and natural gas prices
                rise, Türkiye's import bill increases. This can widen the current-account deficit and increase external
                financing needs. Tourism revenues and manufacturing exports help reduce this pressure, but energy remains
                a strategic vulnerability.
                </p>
                <p>
                A stronger current-account position requires higher value-added exports, domestic renewable energy
                investment, improved energy efficiency and a broader export base. Türkiye has advantages in automotive,
                textiles, white goods, machinery, defense industry, logistics and tourism. The challenge is moving from
                cost competitiveness toward technology and brand competitiveness.
                </p>
                <img src="https://images.unsplash.com/photo-1508385082359-f38ae991e8f2?auto=format&fit=crop&w=1400&q=80">
            </div>

            <div class="article">
                <span class="badge">Political Economy</span>
                <h2>Political Economy: Institutions, Rule Predictability and Risk Premium</h2>
                <p>
                Macroeconomic indicators do not exist in isolation. Investors evaluate Türkiye through a political-economy
                lens: institutional credibility, legal predictability, regulatory stability, central-bank independence,
                foreign-policy risk and the quality of economic governance.
                </p>
                <p>
                If policy is predictable, investors require a lower risk premium. If policy changes suddenly, investors
                demand a higher return to compensate for uncertainty. This directly affects bond yields, equity valuation,
                foreign direct investment and currency expectations.
                </p>
                <p>
                Türkiye's relationship with the European Union is especially important because the EU is a major trade
                partner. Customs Union modernization, regulatory alignment, migration policy, visa issues, defense
                cooperation and investment relations all have economic consequences.
                </p>
            </div>

            <div class="article">
                <span class="badge">Structural Reform</span>
                <h2>Long-Term Development: Productivity, Education, Technology and Capital Markets</h2>
                <p>
                Türkiye's long-term economic performance depends on productivity. Sustainable growth requires better
                education outcomes, stronger vocational training, innovation capacity, digital infrastructure, deeper
                capital markets and efficient allocation of capital.
                </p>
                <p>
                Productivity reform is not a single policy. It is a system: universities, research centers, private firms,
                public institutions, industrial policy, financial markets and export strategy must support each other.
                Without productivity growth, nominal GDP may rise but real welfare may remain under pressure.
                </p>
                <img src="https://images.unsplash.com/photo-1497366811353-6870744d04b2?auto=format&fit=crop&w=1400&q=80">
            </div>
        </div>

        <div>
            <div class="side-card">
                <h3>Indicator Board</h3>
                <ul class="news-list">
                    <li><b>GDP:</b> around 1.32 trillion USD in 2024.</li>
                    <li><b>Population:</b> around 85.5 million.</li>
                    <li><b>Inflation:</b> elevated but under disinflation target.</li>
                    <li><b>Growth:</b> moderate expansion expected.</li>
                    <li><b>Main vulnerability:</b> inflation, energy imports and external financing.</li>
                </ul>
            </div>

            <div class="side-card">
                <h3>Market Watch</h3>
                <p>
                Key variables: CBRT policy rate, lira stability, reserves, Borsa Istanbul earnings,
                bond yields, bank margins, foreign portfolio flows and global energy prices.
                </p>
            </div>

            <div class="side-card">
                <h3>Geopolitical Watch</h3>
                <p>
                Türkiye's location gives it importance in NATO, Black Sea security, Middle East diplomacy,
                energy corridors, migration policy and Europe-Asia logistics routes.
                </p>
            </div>

            <div class="side-card">
                <h3>Key Questions</h3>
                <ul class="news-list">
                    <li>Can inflation fall without a sharp slowdown?</li>
                    <li>Can policy credibility lower the risk premium?</li>
                    <li>Can exports move toward higher value-added production?</li>
                    <li>Can foreign investors regain long-term confidence?</li>
                    <li>Can energy dependence be reduced through renewables?</li>
                </ul>
            </div>

            <div class="side-card">
                <h3>Quick Glossary</h3>
                <p><b>GDP:</b> total value of goods and services produced.</p>
                <p><b>Current Account:</b> trade, services, income and transfers balance.</p>
                <p><b>Risk Premium:</b> extra return investors demand for uncertainty.</p>
                <p><b>Disinflation:</b> inflation falls but prices still rise.</p>
            </div>

            <div class="side-card" style="background:#0b1120;border:1px solid #1e2d45;">
                <h3 style="color:#3b82f6;">→ Data Board</h3>
                <p style="color:#94a3b8;font-size:14px;">
                    Visit the <a href="/data" style="color:#f59e0b;">Data Board</a> for full macroeconomic indicators,
                    country comparison charts, and indicator explanation cards.
                </p>
            </div>
        </div>
    </div>
    """
    return page("Türkiye Economic Monitor", content)


@app.route("/markets")
def markets():
    content = """
    <div class="article">
        <span class="badge">Markets</span>
        <h2>Borsa Istanbul, Bonds, FX and Investor Behavior</h2>
        <p>
        Turkish financial markets are shaped by inflation expectations, monetary policy, exchange-rate dynamics,
        company earnings and global risk appetite. Domestic investors often search for protection against inflation,
        while foreign investors focus on policy credibility and currency risk.
        </p>
        <img src="https://images.unsplash.com/photo-1559526324-593bc073d938?auto=format&fit=crop&w=1400&q=80">
        <p>
        In equity markets, high inflation can increase nominal revenues, but it can also reduce valuation multiples
        because discount rates rise. Banks, exporters, retailers, industrial firms and energy companies each react
        differently to inflation and exchange-rate movements.
        </p>
        <p>
        Bond markets are especially sensitive to the expected path of inflation. If investors believe disinflation
        will continue, longer-duration bonds may become attractive. If inflation expectations remain sticky, investors
        demand higher yields.
        </p>
        <table class="table">
            <tr><th>Asset</th><th>Potential Advantage</th><th>Main Risk</th></tr>
            <tr><td>Equities</td><td>Can benefit from nominal growth</td><td>High rates reduce valuation</td></tr>
            <tr><td>Bonds</td><td>Benefit if yields fall</td><td>Inflation surprise hurts real return</td></tr>
            <tr><td>Gold</td><td>Inflation and currency hedge</td><td>No cash flow, volatile price</td></tr>
            <tr><td>FX</td><td>Currency protection</td><td>Policy and regulation risk</td></tr>
        </table>
    </div>

    <div class="article">
        <h2>Sector Analysis</h2>
        <p>
        Banks are affected by deposit costs, credit regulation, loan quality and net interest margins.
        Exporters depend on foreign demand and exchange-rate competitiveness. Retailers are sensitive to household
        purchasing power. Construction is linked to credit costs, housing demand and public investment.
        </p>
        <p>
        Investors should not treat the Turkish market as one single block. A strong macro story can still produce
        weak results for some firms, while difficult macro conditions can still create opportunities for companies
        with foreign-currency revenues, strong balance sheets and pricing power.
        </p>
    </div>
    """
    return page("Türkiye Markets", content)


@app.route("/finance")
def finance():
    content = """
    <div class="article">
        <span class="badge">Finance</span>
        <h2>Corporate Finance in Türkiye: Inflation, Debt and Real Return</h2>
        <p>
        Corporate finance in Türkiye requires inflation-aware analysis. Nominal sales growth may look strong, but
        analysts must ask whether real sales volume increased. Similarly, nominal profit can rise while real purchasing
        power of profit declines.
        </p>
        <img src="https://images.unsplash.com/photo-1554224155-6726b3ff858f?auto=format&fit=crop&w=1400&q=80">
        <p>
        Firms with strong pricing power can pass cost increases to customers. Firms without pricing power face margin
        compression. Companies with foreign-currency debt face additional risk if the lira depreciates, while companies
        with export revenues may have a natural hedge.
        </p>
    </div>

    <div class="article">
        <h2>Ratio Analysis</h2>
        <p>
        Liquidity ratios show short-term payment capacity. Leverage ratios show debt burden. Profitability ratios show
        how efficiently a firm turns sales and assets into profit. Efficiency ratios reveal inventory, receivables and
        asset turnover. In Türkiye, these ratios must be interpreted with inflation, exchange rate and interest rate context.
        </p>
        <table class="table">
            <tr><th>Ratio Group</th><th>Question Answered</th><th>Türkiye Context</th></tr>
            <tr><td>Liquidity</td><td>Can the firm pay short-term debts?</td><td>Working capital costs are high</td></tr>
            <tr><td>Leverage</td><td>How debt-dependent is the firm?</td><td>High rates increase interest burden</td></tr>
            <tr><td>Profitability</td><td>Can the firm generate profit?</td><td>Inflation can distort nominal margins</td></tr>
            <tr><td>Efficiency</td><td>How well are assets used?</td><td>Inventory strategy matters in inflation</td></tr>
        </table>
    </div>
    """
    return page("Türkiye Finance", content)


@app.route("/trade")
def trade():
    content = """
    <div class="article">
        <span class="badge">Trade</span>
        <h2>Türkiye's Trade Position: EU, Energy, Logistics and Regional Corridors</h2>
        <p>
        Türkiye's trade position is shaped by geography. The country is close to Europe, the Middle East, North Africa,
        the Black Sea and Central Asia. This creates logistics advantages, but also exposes Türkiye to regional instability.
        </p>
        <img src="https://images.unsplash.com/photo-1494412519320-aa613dfb7738?auto=format&fit=crop&w=1400&q=80">
        <p>
        The EU remains central for Turkish exports, especially in automotive, machinery, textiles, white goods and
        intermediate goods. Türkiye's Customs Union relationship with the EU gives industrial exporters an important
        framework, but modernization of this relationship remains a long-term issue.
        </p>
    </div>

    <div class="article">
        <h2>Energy and Current Account</h2>
        <p>
        Energy imports are one of the biggest structural weaknesses in Türkiye's external balance. When oil and natural
        gas prices rise, the import bill increases and the current-account balance deteriorates. Renewable energy,
        domestic exploration, efficiency and diversified contracts can reduce vulnerability.
        </p>
        <img src="https://images.unsplash.com/photo-1473341304170-971dccb5ac1e?auto=format&fit=crop&w=1400&q=80">
    </div>

    <div class="article">
        <h2>Export Upgrading</h2>
        <p>
        Türkiye needs higher value-added exports to improve long-term external stability. This means moving from
        low-margin production toward technology, design, branding, software, defense systems, advanced machinery,
        medical technology and green industry.
        </p>
    </div>
    """
    return page("Türkiye Trade", content)


@app.route("/policy")
def policy():
    content = """
    <div class="article">
        <span class="badge">Policy</span>
        <h2>Economic Policy: Disinflation, Fiscal Discipline and Credibility</h2>
        <p>
        Türkiye's policy challenge is to reduce inflation while maintaining financial stability and avoiding a severe
        growth shock. Monetary policy can slow demand and support the lira, but fiscal policy must also help.
        Public spending, administered prices, tax policy and wage decisions all affect inflation.
        </p>
        <img src="https://images.unsplash.com/photo-1529107386315-e1a2ed48a620?auto=format&fit=crop&w=1400&q=80">
        <p>
        Credibility is the most valuable policy asset. If markets believe the government and central bank will maintain
        a consistent anti-inflation program, risk premium can fall. If credibility weakens, even high interest rates
        may not be enough to stabilize expectations.
        </p>
    </div>

    <div class="article">
        <h2>Policy Mix</h2>
        <p>
        A successful policy mix includes monetary tightening, fiscal coordination, transparent communication, reserve
        accumulation, predictable regulation and structural reforms. These elements work together. If one part fails,
        the whole adjustment process becomes more expensive.
        </p>
        <table class="table">
            <tr><th>Policy Area</th><th>Purpose</th><th>Risk if Weak</th></tr>
            <tr><td>Monetary Policy</td><td>Anchor inflation expectations</td><td>Currency pressure</td></tr>
            <tr><td>Fiscal Policy</td><td>Control demand and deficit</td><td>Inflation persistence</td></tr>
            <tr><td>Reserve Policy</td><td>Strengthen external confidence</td><td>FX vulnerability</td></tr>
            <tr><td>Structural Reform</td><td>Raise productivity</td><td>Low-quality growth</td></tr>
        </table>
    </div>
    """
    return page("Türkiye Policy", content)


@app.route("/geopolitics")
def geopolitics():
    content = """
    <div class="article">
        <span class="badge">Geopolitics</span>
        <h2>Türkiye's Geopolitical Economy</h2>
        <p>
        Türkiye's economy is deeply connected to geopolitics. The country is a NATO member, an EU candidate country,
        a Black Sea actor, a Middle East neighbor, an energy corridor and a logistics bridge between Europe and Asia.
        This gives Türkiye strategic value, but also exposes it to regional risks.
        </p>
        <img src="https://images.unsplash.com/photo-1521295121783-8a321d551ad2?auto=format&fit=crop&w=1400&q=80">
        <p>
        Relations with the EU affect trade, investment, standards and customs rules. Relations with the US influence
        defense, finance and sanctions risk. Relations with Russia matter for energy, tourism, agriculture and regional
        diplomacy. Middle East developments affect oil prices, migration and security expectations.
        </p>
    </div>

    <div class="article">
        <h2>Energy Corridors and Security</h2>
        <p>
        Türkiye's position in energy routes gives it strategic importance. Pipelines, LNG infrastructure, Black Sea
        energy developments and renewable investment all influence the country's energy-security profile.
        Energy security is not only a foreign-policy issue; it directly affects inflation, trade balance and growth.
        </p>
    </div>

    <div class="article">
        <h2>Risk Premium and Diplomacy</h2>
        <p>
        Diplomatic stability can reduce risk premium. Regional escalation can increase it. For emerging markets,
        risk premium affects borrowing costs, exchange-rate expectations and investment decisions. Therefore,
        foreign policy and economic policy cannot be analyzed separately.
        </p>
    </div>
    """
    return page("Türkiye Geopolitics", content)


@app.route("/data")
def data():
    indicator_cards = build_indicator_cards("Turkey")
    explanation_cards = build_explanation_cards()
    comparison_rows = build_comparison_table()

    countries = list(SAMPLE_DATA["countries"].keys())
    inflations   = [SAMPLE_DATA["countries"][c]["inflation"]    for c in countries]
    growths      = [SAMPLE_DATA["countries"][c]["gdp_growth"]   for c in countries]
    unemployments= [SAMPLE_DATA["countries"][c]["unemployment"] for c in countries]
    interest_rates=[SAMPLE_DATA["countries"][c]["interest_rate"] for c in countries]
    curr_accs    = [SAMPLE_DATA["countries"][c]["current_account"] for c in countries]
    gdps         = [SAMPLE_DATA["countries"][c]["gdp"]          for c in countries]

    content = f"""
    <!-- ── classic light article ── -->
    <div class="article">
        <span class="badge">Data Board</span>
        <h2>Türkiye Macro Data Board</h2>
        <p>
        This page summarizes important indicators used in Türkiye macroeconomic analysis. The values are written as
        a public-style economic dashboard and should be updated periodically if the site is maintained regularly.
        </p>
        <table class="table">
            <tr><th>Indicator</th><th>Recent Reference</th><th>Economic Interpretation</th></tr>
            <tr><td>GDP</td><td>About 1.32 trillion USD in 2024</td><td>Large emerging-market economy</td></tr>
            <tr><td>Population</td><td>About 85.5 million in 2024</td><td>Large domestic market</td></tr>
            <tr><td>GDP Growth</td><td>3.4% y/y in 2025 Q4 according to TÜİK dashboard</td><td>Moderate expansion</td></tr>
            <tr><td>Inflation</td><td>30.87% annual CPI in March 2026 according to TÜİK dashboard</td><td>Still elevated</td></tr>
            <tr><td>Unemployment</td><td>8.5% in February 2026 according to TÜİK dashboard</td><td>Labor market pressure moderate</td></tr>
            <tr><td>OECD Growth Forecast</td><td>3.4% for 2026, 4.0% for 2027</td><td>Recovery with moderate growth</td></tr>
        </table>
        <img src="https://images.unsplash.com/photo-1460925895917-afdab827c52f?auto=format&fit=crop&w=1400&q=80">
    </div>

    <div class="article">
        <h2>How to Read These Indicators</h2>
        <p>
        GDP shows the size of the economy, but it does not show distribution, inflation or welfare by itself.
        Inflation shows the pace of price increases. Unemployment shows labor-market slack. Current account data
        shows external balance. Interest rates show monetary stance. Exchange rates show both domestic and external
        confidence conditions.
        </p>
        <p>
        In Türkiye, these indicators must be read together. For example, strong GDP growth with high inflation may
        not mean welfare improvement. A narrowing current account deficit may be positive, but if it happens because
        imports collapse due to weak demand, the interpretation is different.
        </p>
    </div>
    """

    # ── DARK SECTION starts here ──
    dark = f"""
    </div><!-- close .container -->

    <div style="background:#0b1120; padding:48px 0; margin-top:16px;">
    <div class="container">

        <!-- DEMO BANNER -->
        <div class="demo-banner">
            ⚠ SAMPLE / DEMO DATA &nbsp;—&nbsp; All values below are illustrative examples for UI demonstration only.
            They are based on broadly realistic orders of magnitude but are <u>not</u> verified live data.
        </div>

        <!-- ── SECTION 1: Turkey indicator cards ── -->
        <div class="section-title">🇹🇷 Türkiye — Macroeconomic Indicators</div>
        <div class="section-sub">Six key indicators with definitions and interpretation guidance</div>
        <span class="badge-demo">DEMO DATA</span>
        <div class="indicator-grid">
            {indicator_cards}
        </div>

        <!-- ── SECTION 2: Charts ── -->
        <div style="display:grid;grid-template-columns:1fr 1fr;gap:20px;margin:32px 0;">

            <div class="chart-wrap">
                <h3>📈 GDP Growth Rate Comparison (%)</h3>
                <canvas id="chartGrowth"></canvas>
            </div>

            <div class="chart-wrap">
                <h3>🔥 Inflation Rate Comparison (%)</h3>
                <canvas id="chartInflation"></canvas>
            </div>

            <div class="chart-wrap">
                <h3>👥 Unemployment Rate (%)</h3>
                <canvas id="chartUnemployment"></canvas>
            </div>

            <div class="chart-wrap">
                <h3>🏦 Policy Interest Rate (%)</h3>
                <canvas id="chartInterest"></canvas>
            </div>

        </div>

        <div class="chart-wrap">
            <h3>⚖️ Current Account Balance (USD Billion) — Surplus vs Deficit</h3>
            <canvas id="chartCA" style="max-height:220px;"></canvas>
        </div>

        <!-- ── SECTION 3: Country Comparison Table ── -->
        <div class="section-title" style="margin-top:40px;">🌍 Country Comparison</div>
        <div class="section-sub">Turkey · Iran · Germany · United States · China — side-by-side macro snapshot</div>
        <span class="badge-demo">DEMO DATA</span>

        <div style="overflow-x:auto;margin-top:16px;border-radius:12px;border:1px solid #1e2d45;">
        <table class="dk-table">
            <thead>
                <tr>
                    <th>Country</th>
                    <th>GDP (B USD)</th>
                    <th>GDP Growth</th>
                    <th>Inflation</th>
                    <th>Unemployment</th>
                    <th>Policy Rate</th>
                    <th>FX (per USD)</th>
                    <th>Current Acc.</th>
                </tr>
            </thead>
            <tbody>
                {comparison_rows}
            </tbody>
        </table>
        </div>
        <div style="font-size:11px;color:#475569;margin-top:8px;font-family:'IBM Plex Mono',monospace;">
            🟢 Favorable &nbsp;|&nbsp; 🟡 Moderate &nbsp;|&nbsp; 🔴 Elevated concern &nbsp;|&nbsp; — Neutral
            &nbsp;&nbsp;· Color coding is relative and simplified for readability.
        </div>

        <!-- ── SECTION 4: GDP bar chart ── -->
        <div class="chart-wrap" style="margin-top:32px;">
            <h3>📊 GDP Size Comparison (USD Billion)</h3>
            <canvas id="chartGDP" style="max-height:240px;"></canvas>
        </div>

        <!-- ── SECTION 5: Explanation Cards ── -->
        <div class="section-title" style="margin-top:48px;">📖 Indicator Guide</div>
        <div class="section-sub">What each indicator means, why it matters, and how to interpret high or low values</div>
        {explanation_cards}

    </div>
    </div>

    <div class="container">
    <!-- dummy open tag to let page() close it cleanly -->
    <div style="display:none;">
    """

    # Build chart JS
    labels_js = str(countries)
    chart_js = f"""
    <script>
    const LABELS = {labels_js};
    const COLORS = ['#3b82f6','#ef4444','#10b981','#f59e0b','#a855f7'];

    function barChart(id, data, label, color, horizontal) {{
        const ctx = document.getElementById(id);
        if(!ctx) return;
        new Chart(ctx, {{
            type: horizontal ? 'bar' : 'bar',
            data: {{
                labels: LABELS,
                datasets: [{{
                    label: label,
                    data: data,
                    backgroundColor: COLORS,
                    borderColor: COLORS,
                    borderWidth: 1,
                    borderRadius: 6,
                }}]
            }},
            options: {{
                indexAxis: horizontal ? 'y' : 'x',
                responsive: true,
                plugins: {{
                    legend: {{ display: false }},
                    tooltip: {{ callbacks: {{ label: ctx => ' ' + ctx.parsed[horizontal ? 'x' : 'y'] }} }}
                }},
                scales: {{
                    x: {{ ticks: {{ color:'#94a3b8' }}, grid: {{ color:'#1e2d45' }} }},
                    y: {{ ticks: {{ color:'#94a3b8' }}, grid: {{ color:'#1e2d45' }} }}
                }}
            }}
        }});
    }}

    barChart('chartGrowth',     {growths},       'GDP Growth %',     '#3b82f6', false);
    barChart('chartInflation',  {inflations},    'Inflation %',      '#ef4444', false);
    barChart('chartUnemployment',{unemployments},'Unemployment %',   '#f59e0b', false);
    barChart('chartInterest',   {interest_rates},'Policy Rate %',    '#a855f7', false);
    barChart('chartGDP',        {gdps},          'GDP B USD',        '#10b981', true);

    // Current account — special color per sign
    (function(){{
        const ctx = document.getElementById('chartCA');
        if(!ctx) return;
        const vals = {curr_accs};
        const cols = vals.map(v => v >= 0 ? '#10b981' : '#ef4444');
        new Chart(ctx, {{
            type: 'bar',
            data: {{
                labels: LABELS,
                datasets: [{{ label: 'Current Account B USD', data: vals,
                    backgroundColor: cols, borderColor: cols, borderWidth:1, borderRadius:6 }}]
            }},
            options: {{
                responsive: true,
                plugins: {{ legend: {{ display: false }} }},
                scales: {{
                    x: {{ ticks: {{ color:'#94a3b8' }}, grid: {{ color:'#1e2d45' }} }},
                    y: {{ ticks: {{ color:'#94a3b8' }}, grid: {{ color:'#1e2d45' }},
                          title: {{ display:true, text:'B USD', color:'#64748b' }} }}
                }}
            }}
        }});
    }})();
    </script>
    """

    full_content = content + dark + chart_js
    return page("Türkiye Data Board", full_content, use_charts=True)


# ─────────────────────────────────────────────
#  ARCHIVE / CHAT (unchanged)
# ─────────────────────────────────────────────
CHAT_PAGE = """
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>Archive Briefing</title>
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<style>
body{
    background:#0f1117;
    color:white;
    font-family:Arial, sans-serif;
    padding:20px;
}
.box{
    max-width:780px;
    margin:auto;
}
h2{text-align:center;}
.msg{
    background:#1f2430;
    padding:12px;
    margin:8px 0;
    border-radius:10px;
    white-space:pre-wrap;
}
small{color:#aaa;}
input,textarea,button{
    width:100%;
    padding:12px;
    margin-top:8px;
    border-radius:8px;
    border:none;
    box-sizing:border-box;
}
textarea{
    height:240px;
    resize:vertical;
}
button{
    background:#4f7cff;
    color:white;
    font-weight:bold;
    cursor:pointer;
}
.exit{background:#444;}
.clear{background:#b33a3a;}
.refresh{background:#2d6a4f;}
.back{background:#555;}
</style>
</head>
<body>
<div class="box">

{% if not session.get("ok") %}
<h2>Archive Briefing Access</h2>
<form method="post" action="/login">
    <input name="name" placeholder="Your name" required>
    <input name="password" type="password" placeholder="Access code" required>
    <button type="submit">Enter</button>
</form>

<form method="get" action="/">
    <button class="back" type="submit">Back to Monitor</button>
</form>

{% else %}
<h2>Archive Briefing</h2>

<form method="get" action="/archive-briefing">
    <button class="refresh" type="submit">Refresh Messages</button>
</form>

{% for m in messages %}
<div class="msg">
    <b>{{ m[1] }}</b> <small>{{ m[3] }}</small><br>
    {{ m[2] }}
</div>
{% endfor %}

<form method="post" action="/send">
    <textarea name="text" placeholder="Write a long message..." required></textarea>
    <button type="submit">Send</button>
</form>

<form method="post" action="/clear">
    <button class="clear" type="submit">Clear All Messages</button>
</form>

<form method="post" action="/logout">
    <button class="exit" type="submit">Exit</button>
</form>

{% endif %}
</div>
</body>
</html>
"""

@app.route("/archive-briefing")
def archive_briefing():
    conn = get_db()
    messages = conn.execute(
        "SELECT * FROM messages ORDER BY id DESC LIMIT 500"
    ).fetchall()
    conn.close()
    messages = list(reversed(messages))
    return render_template_string(CHAT_PAGE, messages=messages)

@app.route("/login", methods=["POST"])
def login():
    password = request.form.get("password")
    name = request.form.get("name")
    if password == PASSWORD:
        session["ok"] = True
        session["name"] = name
    return redirect("/archive-briefing")

@app.route("/send", methods=["POST"])
def send():
    if session.get("ok"):
        text = request.form.get("text", "").strip()
        if text:
            conn = get_db()
            conn.execute(
                "INSERT INTO messages(sender, text, time) VALUES (?, ?, ?)",
                (session.get("name", "Anonymous"), text, datetime.now().strftime("%Y-%m-%d %H:%M"))
            )
            conn.commit()
            conn.close()
    return redirect("/archive-briefing")

@app.route("/clear", methods=["POST"])
def clear():
    if session.get("ok"):
        conn = get_db()
        conn.execute("DELETE FROM messages")
        conn.commit()
        conn.close()
    return redirect("/archive-briefing")

@app.route("/logout", methods=["POST"])
def logout():
    session.clear()
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
