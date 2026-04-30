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

BASE_STYLE = """
<style>
:root{
    --navy:#07111f;
    --blue:#12355b;
    --deep:#0f172a;
    --gold:#c49a3a;
    --soft:#f3f6fa;
    --text:#222;
    --muted:#64748b;
}
body{
    margin:0;
    font-family:Arial, Helvetica, sans-serif;
    background:var(--soft);
    color:var(--text);
    line-height:1.75;
}
.topbar{
    background:#050b14;
    color:#cbd5e1;
    padding:9px 30px;
    font-size:13px;
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
}
.nav a:hover{
    color:#facc15;
}
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
.article{
    padding:30px;
    margin-bottom:24px;
}
.side-card{
    padding:22px;
    margin-bottom:20px;
}
.article h2,.side-card h3{
    color:#12355b;
    margin-top:0;
}
.article h2{
    font-size:28px;
}
.article h3{
    color:#1e3a5f;
}
.article img{
    width:100%;
    border-radius:14px;
    margin:16px 0;
}
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
.table th{
    background:#12355b;
    color:white;
}
.table th,.table td{
    border:1px solid #d8dee9;
    padding:10px;
    text-align:left;
}
.news-list li{
    margin-bottom:10px;
}
.footer{
    text-align:center;
    color:#777;
    padding:38px;
    font-size:13px;
}
.tiny-access{
    color:#777;
    text-decoration:none;
    font-size:11px;
}
.tiny-access:hover{
    color:#333;
}
@media(max-width:850px){
    .grid{grid-template-columns:1fr;}
    .header h1{font-size:30px;}
    .nav a{display:inline-block;margin:6px 8px;}
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
    content = """
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
    return page("Türkiye Data Board", content)

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
