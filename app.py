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
    background: #f4f6f8;
    color: #222;
}
.header {
    background: linear-gradient(135deg, #102030, #1d3557);
    color: white;
    padding: 35px;
    text-align: center;
}
.nav {
    background: #14213d;
    padding: 12px;
    text-align: center;
}
.nav a {
    color: white;
    margin: 0 15px;
    text-decoration: none;
    font-weight: bold;
}
.container {
    max-width: 950px;
    margin: 30px auto;
    padding: 0 20px;
}
.article {
    background: white;
    padding: 22px;
    margin-bottom: 18px;
    border-radius: 12px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.08);
}
.article h2 {
    color: #1d3557;
}
.article img {
    width: 100%;
    border-radius: 12px;
    margin-top: 12px;
}
.footer {
    text-align: center;
    color: #777;
    padding: 25px;
}
.tiny-access {
    color: #777;
    text-decoration: none;
    font-size: 12px;
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

<div class="header">
    <h1>Global Economy Monitor</h1>
    <p>Markets, finance, trade, and international economic analysis</p>
</div>

<div class="nav">
    <a href="/">Home</a>
    <a href="/markets">Markets</a>
    <a href="/finance">Finance</a>
    <a href="/trade">Trade</a>
    <a href="/policy">Policy</a>
</div>

<div class="container">
{content}
</div>

<div class="footer">
    © 2026 Global Economy Monitor · <a class="tiny-access" href="/archive-briefing">archive</a>
</div>

</body>
</html>
"""

@app.route("/")
def home():
    content = """
    <div class="article">
        <h2>Global Markets Watch: Inflation and Interest Rate Expectations</h2>
        <p>
        Global investors continue to monitor inflation expectations, central bank policy decisions,
        and bond market movements. Interest rate expectations remain one of the strongest drivers
        of financial market pricing.
        </p>
        <img src="https://images.unsplash.com/photo-1611974789855-9c2a0a7236a3?auto=format&fit=crop&w=1200&q=80">
    </div>

    <div class="article">
        <h2>Energy Prices and Emerging Market Pressure</h2>
        <p>
        Energy-importing countries may face pressure on current account balances when oil and gas
        prices increase. Exchange rate stability and diversified energy sources remain important.
        </p>
        <img src="https://images.unsplash.com/photo-1473341304170-971dccb5ac1e?auto=format&fit=crop&w=1200&q=80">
    </div>

    <div class="article">
        <h2>Portfolio Strategy: Why Diversification Still Matters</h2>
        <p>
        Diversification can reduce unsystematic risk by spreading capital across different assets.
        However, market-wide risk cannot be fully eliminated.
        </p>
    </div>
    """
    return page("Global Economy Monitor", content)

@app.route("/markets")
def markets():
    content = """
    <div class="article">
        <h2>Markets</h2>
        <p>
        Equity markets are affected by earnings expectations, interest rates, liquidity conditions,
        and global risk appetite. When interest rates rise, investors often reassess stock valuations.
        </p>
        <img src="https://images.unsplash.com/photo-1642790106117-e829e14a795f?auto=format&fit=crop&w=1200&q=80">
    </div>
    """
    return page("Markets", content)

@app.route("/finance")
def finance():
    content = """
    <div class="article">
        <h2>Finance</h2>
        <p>
        Financial analysis focuses on profitability, liquidity, leverage, efficiency, and market
        valuation. Investors compare expected return with risk before making portfolio decisions.
        </p>
        <img src="https://images.unsplash.com/photo-1554224155-6726b3ff858f?auto=format&fit=crop&w=1200&q=80">
    </div>
    """
    return page("Finance", content)

@app.route("/trade")
def trade():
    content = """
    <div class="article">
        <h2>International Trade</h2>
        <p>
        International trade is shaped by exchange rates, tariffs, logistics costs, geopolitical risks,
        and supply chain strategies. Firms increasingly focus on supplier diversification.
        </p>
        <img src="https://images.unsplash.com/photo-1494412519320-aa613dfb7738?auto=format&fit=crop&w=1200&q=80">
    </div>
    """
    return page("Trade", content)

@app.route("/policy")
def policy():
    content = """
    <div class="article">
        <h2>Economic Policy</h2>
        <p>
        Fiscal and monetary policy influence inflation, employment, exchange rates, and investment
        expectations. Central bank credibility remains important for price stability.
        </p>
        <img src="https://images.unsplash.com/photo-1529107386315-e1a2ed48a620?auto=format&fit=crop&w=1200&q=80">
    </div>
    """
    return page("Policy", content)

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
    max-width: 750px;
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
    height: 170px;
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
        "SELECT * FROM messages ORDER BY id DESC LIMIT 200"
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