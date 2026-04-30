from flask import Flask, request, redirect, render_template_string, session
from datetime import datetime
import sqlite3
import os

app = Flask(__name__)

app.secret_key = os.environ.get("SECRET_KEY", "change-this-secret-key")
PASSWORD = os.environ.get("CHAT_PASSWORD", "İzelLale")

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

BASE_STYLE = """
<style>
body {
    margin: 0;
    font-family: Arial, sans-serif;
    background: #eef1f5;
    color: #222;
    line-height: 1.7;
}
.topbar {
    background: #07111f;
    color: #cfd8e3;
    padding: 8px 30px;
    font-size: 13px;
}
.header {
    background: linear-gradient(135deg, #0b1f36, #1d3557, #0f172a);
    color: white;
    padding: 45px 30px;
    text-align: center;
}
.header h1 {
    margin: 0;
    font-size: 38px;
}
.header p {
    margin-top: 10px;
    font-size: 16px;
    color: #dbeafe;
}
.nav {
    background: #14213d;
    padding: 14px;
    text-align: center;
    position: sticky;
    top: 0;
    z-index: 10;
}
.nav a {
    color: white;
    margin: 0 16px;
    text-decoration: none;
    font-weight: bold;
}
.nav a:hover {
    text-decoration: underline;
}
.container {
    max-width: 1080px;
    margin: 30px auto;
    padding: 0 22px;
}
.grid {
    display: grid;
    grid-template-columns: 2fr 1fr;
    gap: 22px;
}
.article {
    background: white;
    padding: 26px;
    margin-bottom: 22px;
    border-radius: 14px;
    box-shadow: 0 3px 12px rgba(0,0,0,0.08);
}
.article h2 {
    color: #1d3557;
    margin-top: 0;
}
.article h3 {
    color: #243b53;
}
.article img {
    width: 100%;
    border-radius: 12px;
    margin: 14px 0;
}
.badge {
    display: inline-block;
    background: #e0ecff;
    color: #1d3557;
    padding: 5px 10px;
    border-radius: 20px;
    font-size: 12px;
    font-weight: bold;
    margin-bottom: 8px;
}
.data-box {
    background: #f8fafc;
    border-left: 5px solid #1d3557;
    padding: 16px;
    margin: 16px 0;
    border-radius: 8px;
}
.side-card {
    background: white;
    padding: 20px;
    margin-bottom: 18px;
    border-radius: 14px;
    box-shadow: 0 3px 12px rgba(0,0,0,0.08);
}
.side-card h3 {
    margin-top: 0;
    color: #1d3557;
}
.news-list li {
    margin-bottom: 10px;
}
.footer {
    text-align: center;
    color: #777;
    padding: 35px;
    font-size: 13px;
}
.tiny-access {
    color: #777;
    text-decoration: none;
    font-size: 11px;
}
.tiny-access:hover {
    color: #444;
}
@media (max-width: 800px) {
    .grid {
        grid-template-columns: 1fr;
    }
    .nav a {
        display: inline-block;
        margin: 6px 8px;
    }
    .header h1 {
        font-size: 28px;
    }
}
</style>
"""

def page(title, content):
    return f"""
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>{title}</title>
<meta name="viewport" content="width=device-width, initial-scale=1.0">
{BASE_STYLE}
</head>
<body>

<div class="topbar">
    Türkiye Economy Desk · Macro Briefing · Markets · Trade · Policy
</div>

<div class="header">
    <h1>Türkiye Economic Monitor</h1>
    <p>Macroeconomic analysis, markets, trade, finance, and geopolitical economy</p>
</div>

<div class="nav">
    <a href="/">Home</a>
    <a href="/markets">Markets</a>
    <a href="/finance">Finance</a>
    <a href="/trade">Trade</a>
    <a href="/policy">Policy</a>
    <a href="/geopolitics">Geopolitics</a>
</div>

<div class="container">
{content}
</div>

<div class="footer">
    © 2026 Türkiye Economic Monitor · Data commentary based on public macroeconomic indicators ·
    <a class="tiny-access" href="/archive-briefing">archive</a>
</div>

</body>
</html>
"""

@app.route("/")
def home():
    content = """
    <div class="grid">
        <div>
            <div class="article">
                <span class="badge">Main Briefing</span>
                <h2>Türkiye Economic Outlook: Growth, Inflation, Policy Credibility and External Balance</h2>
                <p>
                Türkiye remains one of the most important emerging market economies because of its large population,
                diversified industrial base, strategic location between Europe, the Middle East and Central Asia,
                and its role in trade, logistics, tourism and manufacturing. The economy has shown resilience,
                but the macroeconomic environment continues to be shaped by high inflation, exchange-rate sensitivity,
                monetary tightening, external financing needs and geopolitical risk.
                </p>
                <p>
                According to World Bank country data, Türkiye's current-dollar GDP was about 1.32 trillion USD in 2024,
                with a population of roughly 85.5 million. This places Türkiye among the largest economies in the world,
                but its per-capita income and macro-financial stability indicators remain highly sensitive to inflation,
                exchange-rate movements and global capital flows.
                </p>
                <img src="https://images.unsplash.com/photo-1524231757912-21f4fe3a7200?auto=format&fit=crop&w=1200&q=80">
                <div class="data-box">
                    <b>Key Macro Snapshot:</b><br>
                    GDP size: about 1.32 trillion USD in 2024<br>
                    Population: about 85.5 million in 2024<br>
                    2025 growth: around 3.6% according to official/outlook summaries<br>
                    Inflation: still elevated, but moving through a disinflation process<br>
                    Main policy issue: balancing price stability, growth and external confidence
                </div>
            </div>

            <div class="article">
                <span class="badge">GDP and Real Economy</span>
                <h2>GDP Growth: Resilience Despite Tight Financial Conditions</h2>
                <p>
                Türkiye's growth model has historically relied on domestic demand, credit expansion, construction,
                services, exports and tourism. In recent years, the policy mix has shifted toward tighter monetary
                conditions to reduce inflation. This creates a difficult balance: higher interest rates can help reduce
                inflation expectations, but they may also slow private investment, consumption and credit-sensitive sectors.
                </p>
                <p>
                The 2025 growth performance was moderate rather than weak. Annual growth around 3.6% indicates that the
                economy continued to expand despite restrictive monetary policy. However, the composition of growth matters.
                If growth depends heavily on consumption and inventories rather than productivity, exports and investment,
                long-term sustainability becomes weaker.
                </p>
                <p>
                For 2026 and 2027, international forecasts generally expect moderate growth. A key question is whether
                the Turkish economy can move from inflation-driven nominal expansion toward productivity-based real growth.
                This requires stronger institutional credibility, lower risk premia, technology investment, higher value-added
                exports and more predictable policy implementation.
                </p>
            </div>

            <div class="article">
                <span class="badge">Inflation</span>
                <h2>Inflation: The Central Problem of the Adjustment Process</h2>
                <p>
                Inflation remains the most important macroeconomic challenge for Türkiye. High inflation reduces purchasing
                power, weakens long-term planning, increases uncertainty for firms and households, and makes financial
                valuation more difficult. Even when nominal wages rise, real purchasing power may remain under pressure
                if price increases continue faster than income growth.
                </p>
                <p>
                Türkiye's inflation dynamics are connected to several channels: exchange-rate pass-through, energy import
                costs, food prices, rents, wage adjustments, expectations and fiscal conditions. Because Türkiye imports
                significant amounts of energy, global oil and natural gas prices can quickly influence domestic inflation
                and the current account balance.
                </p>
                <p>
                The disinflation process depends not only on high policy rates but also on credibility. If households and
                firms believe inflation will remain high, they adjust prices, wages and contracts accordingly. This creates
                inflation inertia. Therefore, the Central Bank's communication, policy consistency and coordination with
                fiscal policy are essential.
                </p>
                <img src="https://images.unsplash.com/photo-1642790106117-e829e14a795f?auto=format&fit=crop&w=1200&q=80">
            </div>

            <div class="article">
                <span class="badge">Monetary Policy</span>
                <h2>Interest Rates, Turkish Lira and Investor Confidence</h2>
                <p>
                Monetary policy in Türkiye is closely watched because interest-rate decisions affect the Turkish lira,
                bank deposits, credit growth, bond yields, stock-market valuations and foreign investor behavior.
                A tight monetary stance may attract lira deposits and portfolio flows, but it also increases financing
                costs for firms and households.
                </p>
                <p>
                The key policy challenge is sequencing. If interest rates are reduced too early, inflation expectations
                may become unanchored again. If rates remain too high for too long, financial conditions can become
                restrictive for production and investment. The credibility of the policy path is therefore as important
                as the level of the policy rate itself.
                </p>
                <p>
                For investors, the Turkish lira is not only a currency variable but also a confidence indicator. Stable
                reserve accumulation, lower dollarization and predictable monetary policy can reduce external vulnerability.
                However, political risk, global risk appetite and energy prices continue to influence capital flows.
                </p>
            </div>

            <div class="article">
                <span class="badge">External Balance</span>
                <h2>Current Account, Energy Imports and Export Strategy</h2>
                <p>
                Türkiye's current account balance is structurally sensitive to energy prices. When oil and natural gas
                prices rise, the import bill increases and external financing needs become more visible. Tourism revenues,
                manufacturing exports and service income help offset this pressure, but the energy channel remains a
                major macroeconomic risk.
                </p>
                <p>
                A sustainable improvement in the current account requires higher value-added exports, domestic energy
                diversification, renewable energy investment and stronger logistics competitiveness. Türkiye has advantages
                in automotive, machinery, textiles, defense industry, white goods, tourism and regional trade networks.
                However, global competition requires technological upgrading and productivity growth.
                </p>
                <img src="https://images.unsplash.com/photo-1494412519320-aa613dfb7738?auto=format&fit=crop&w=1200&q=80">
            </div>

            <div class="article">
                <span class="badge">Politics and Economy</span>
                <h2>Political Economy: Institutions, Risk Premium and Policy Predictability</h2>
                <p>
                Türkiye's economic outlook cannot be separated from political economy. Investors evaluate not only GDP
                growth and inflation but also institutional quality, legal predictability, regulatory stability and
                foreign-policy risk. A country can have strong growth potential, but if policy uncertainty is high, the
                required risk premium also rises.
                </p>
                <p>
                The relationship with the European Union remains economically important because the EU is one of Türkiye's
                largest trade partners. Customs Union modernization, investment flows, visa policy, migration management,
                defense cooperation and regional diplomacy all influence the economic environment.
                </p>
                <p>
                Relations with the United States, Russia, the Middle East and Central Asia also matter. Energy routes,
                defense policy, sanctions risk, regional conflict and trade corridors can affect foreign direct investment,
                currency expectations and sovereign risk perception.
                </p>
            </div>

            <div class="article">
                <span class="badge">Markets</span>
                <h2>Borsa Istanbul, Bonds and Portfolio Allocation</h2>
                <p>
                In a high-inflation environment, investors often search for assets that can protect real purchasing power.
                Equities, gold, foreign currency, inflation-linked instruments and real assets become important alternatives.
                However, each asset has different risks. Stocks may benefit from nominal revenue growth, but valuations can
                fall when interest rates rise. Bonds may become attractive when disinflation becomes credible and yields
                begin to decline.
                </p>
                <p>
                Portfolio strategy in Türkiye requires close attention to inflation, policy rates, exchange rates and
                company-level fundamentals. Export-oriented firms may benefit from foreign-currency revenues, while highly
                indebted firms can suffer from expensive financing. Banks are sensitive to regulation, deposit costs,
                loan growth and asset quality.
                </p>
            </div>

            <div class="article">
                <span class="badge">Structural Reform</span>
                <h2>Long-Term Challenges: Productivity, Education, Technology and Rule of Law</h2>
                <p>
                Türkiye's long-term potential depends on productivity growth. Sustainable development requires more than
                short-term credit expansion. It requires education quality, labor-market efficiency, digital transformation,
                research and development, institutional trust and efficient capital allocation.
                </p>
                <p>
                Productivity-oriented reforms would help Türkiye move from middle-income pressure toward higher value-added
                production. This means stronger universities, better vocational training, deeper capital markets, transparent
                public procurement, predictable tax policy and stronger innovation ecosystems.
                </p>
            </div>
        </div>

        <div>
            <div class="side-card">
                <h3>Indicator Board</h3>
                <ul class="news-list">
                    <li><b>GDP:</b> About 1.32 trillion USD in 2024.</li>
                    <li><b>Population:</b> About 85.5 million.</li>
                    <li><b>Inflation:</b> Still elevated; disinflation remains the main policy target.</li>
                    <li><b>Growth:</b> Moderate expansion expected for 2026.</li>
                    <li><b>Main risk:</b> Inflation persistence and external financing sensitivity.</li>
                </ul>
            </div>

            <div class="side-card">
                <h3>Market Watch</h3>
                <p>
                Investors are watching CBRT policy decisions, foreign reserves, exchange-rate stability,
                inflation expectations, bank profitability, bond yields and Borsa Istanbul valuations.
                </p>
            </div>

            <div class="side-card">
                <h3>Geopolitical Watch</h3>
                <p>
                Türkiye's location gives it strategic value in energy, logistics, migration, defense,
                Black Sea security, Middle East diplomacy and Europe-Asia trade corridors.
                </p>
            </div>

            <div class="side-card">
                <h3>Policy Questions</h3>
                <ul class="news-list">
                    <li>Can disinflation continue without a sharp growth slowdown?</li>
                    <li>Will reserve accumulation strengthen external confidence?</li>
                    <li>Can exports shift toward higher value-added sectors?</li>
                    <li>Will policy credibility reduce the risk premium?</li>
                </ul>
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
        <h2>Financial Markets in Türkiye: Equities, Bonds, FX and Risk Appetite</h2>
        <p>
        Turkish financial markets are strongly influenced by inflation expectations, interest-rate policy,
        exchange-rate dynamics and global emerging-market sentiment. In periods of high inflation, investors
        try to protect real returns, while firms focus on working-capital management and financing costs.
        </p>
        <img src="https://images.unsplash.com/photo-1559526324-593bc073d938?auto=format&fit=crop&w=1200&q=80">
        <p>
        Borsa Istanbul can attract domestic investors when inflation is high and alternative real returns are uncertain.
        However, equity valuations are not risk-free. Higher discount rates reduce the present value of future cash flows.
        Therefore, even profitable companies can face valuation pressure when interest rates remain high.
        </p>
        <p>
        Bond markets are particularly sensitive to the disinflation path. If investors believe inflation will fall,
        longer-term bonds may become more attractive. But if inflation expectations remain sticky, investors demand
        higher yields as compensation.
        </p>
    </div>

    <div class="article">
        <h2>Sector Sensitivity</h2>
        <p>
        Banks are affected by deposit costs, credit regulation, net interest margins and asset quality. Exporters are
        influenced by exchange rates and external demand. Construction and real estate are sensitive to credit costs.
        Tourism benefits from foreign-currency revenues but remains exposed to geopolitical and seasonal risks.
        </p>
    </div>
    """
    return page("Markets", content)

@app.route("/finance")
def finance():
    content = """
    <div class="article">
        <span class="badge">Finance</span>
        <h2>Corporate Finance in a High-Inflation Economy</h2>
        <p>
        In Türkiye, corporate finance decisions are shaped by inflation, exchange-rate volatility and high nominal
        interest rates. Companies must manage liquidity, debt maturity, foreign-currency exposure and operating margins.
        Financial analysis therefore requires both accounting ratios and macroeconomic interpretation.
        </p>
        <img src="https://images.unsplash.com/photo-1554224155-6726b3ff858f?auto=format&fit=crop&w=1200&q=80">
        <p>
        Liquidity ratios show whether a firm can meet short-term obligations. Leverage ratios show debt burden.
        Profitability ratios indicate whether the firm can turn sales and assets into profit. But in a high-inflation
        environment, nominal growth can mislead analysts. Real growth and inflation-adjusted performance matter more.
        </p>
    </div>

    <div class="article">
        <h2>Investment Strategy and Real Return</h2>
        <p>
        Investors should compare nominal returns with inflation. A 35% nominal return may look high, but if inflation
        is also high, the real return can be much lower. This is why real return, risk premium, currency movement and
        opportunity cost are central concepts in Turkish financial analysis.
        </p>
    </div>
    """
    return page("Finance", content)

@app.route("/trade")
def trade():
    content = """
    <div class="article">
        <span class="badge">Trade</span>
        <h2>Türkiye's Trade Position: Europe, Energy and Regional Corridors</h2>
        <p>
        Türkiye's trade structure reflects its geographic position and industrial capacity. The country is closely
        connected to European markets through manufacturing supply chains, while also maintaining commercial links
        with the Middle East, North Africa, Central Asia and Russia.
        </p>
        <img src="https://images.unsplash.com/photo-1508385082359-f38ae991e8f2?auto=format&fit=crop&w=1200&q=80">
        <p>
        The Customs Union with the European Union remains a central element of Türkiye's trade architecture.
        Modernization of this framework could influence investment, standards, digital trade and services.
        However, political relations and regulatory alignment continue to shape the pace of progress.
        </p>
    </div>

    <div class="article">
        <h2>Energy Import Dependence</h2>
        <p>
        Energy import dependence is one of the main reasons Türkiye's current account balance is sensitive to global
        commodity prices. Renewable energy, domestic production, energy efficiency and diversified supply contracts
        can reduce this vulnerability over time.
        </p>
    </div>
    """
    return page("Trade", content)

@app.route("/policy")
def policy():
    content = """
    <div class="article">
        <span class="badge">Policy</span>
        <h2>Economic Policy: Disinflation, Credibility and Fiscal Coordination</h2>
        <p>
        Türkiye's policy framework is currently centered on reducing inflation while preserving financial stability.
        Monetary policy alone is not enough. Fiscal discipline, income policy, public-sector pricing decisions and
        structural reforms all influence the inflation path.
        </p>
        <img src="https://images.unsplash.com/photo-1529107386315-e1a2ed48a620?auto=format&fit=crop&w=1200&q=80">
        <p>
        Policy credibility is built through consistency. When economic actors believe that the authorities will maintain
        a clear anti-inflation stance, expectations can improve. If expectations improve, the cost of disinflation may
        become lower over time.
        </p>
    </div>

    <div class="article">
        <h2>Fiscal Policy</h2>
        <p>
        Fiscal policy affects inflation through public spending, taxes, administered prices and budget deficits.
        A credible medium-term fiscal framework can support monetary policy by reducing demand pressure and improving
        investor confidence.
        </p>
    </div>
    """
    return page("Policy", content)

@app.route("/geopolitics")
def geopolitics():
    content = """
    <div class="article">
        <span class="badge">Geopolitics</span>
        <h2>Türkiye's Geopolitical Economy</h2>
        <p>
        Türkiye's economic outlook is connected to its geopolitical position. The country is a NATO member, a candidate
        country for the European Union, a major Black Sea actor, a regional energy corridor and an important diplomatic
        player in the Middle East and Caucasus.
        </p>
        <img src="https://images.unsplash.com/photo-1521295121783-8a321d551ad2?auto=format&fit=crop&w=1200&q=80">
        <p>
        Geopolitical developments can affect tourism, capital flows, defense spending, energy security and trade routes.
        For this reason, investors include political risk and regional stability in their Türkiye analysis.
        </p>
    </div>

    <div class="article">
        <h2>EU, US, Russia and the Middle East</h2>
        <p>
        Relations with the EU affect trade, investment and standards. Relations with the US influence defense, finance
        and sanctions risk. Relations with Russia matter for energy, tourism and regional diplomacy. Developments in the
        Middle East can affect energy prices, migration, logistics and security expectations.
        </p>
    </div>
    """
    return page("Geopolitics", content)

CHAT_PAGE = """
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>Archive Briefing</title>
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<style>
body {
    background: #0f1117;
    color: white;
    font-family: Arial, sans-serif;
    padding: 20px;
}
.box {
    max-width: 760px;
    margin: auto;
}
h2 {
    text-align: center;
}
.msg {
    background: #1f2430;
    padding: 12px;
    margin: 8px 0;
    border-radius: 10px;
    white-space: pre-wrap;
}
small {
    color: #aaa;
}
input, textarea, button {
    width: 100%;
    padding: 12px;
    margin-top: 8px;
    border-radius: 8px;
    border: none;
    box-sizing: border-box;
}
textarea {
    height: 220px;
    resize: vertical;
}
button {
    background: #4f7cff;
    color: white;
    font-weight: bold;
    cursor: pointer;
}
.exit {
    background: #444;
}
.clear {
    background: #b33a3a;
}
.refresh {
    background: #2d6a4f;
}
.back {
    background: #555;
}
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
        "SELECT * FROM messages ORDER BY id DESC LIMIT 300"
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
                (
                    session.get("name", "Anonymous"),
                    text,
                    datetime.now().strftime("%Y-%m-%d %H:%M")
                )
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
