# -*- coding: utf-8 -*-
import streamlit as st
import os, time, requests
from datetime import datetime
from pybit.unified_trading import HTTP

st.set_page_config(page_title="TrendPulse", page_icon="⚡", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;600;700&family=IBM+Plex+Sans:wght@300;400;500&display=swap');

* { box-sizing: border-box; margin: 0; padding: 0; }
html, body, [class*="css"], .stApp {
    background: #080b10 !important;
    color: #c9d1d9 !important;
    font-family: 'IBM Plex Sans', sans-serif !important;
}
.stApp { background: #080b10 !important; }

/* Sidebar */
[data-testid="stSidebar"] {
    background: #0d1117 !important;
    border-right: 1px solid #21262d !important;
}
[data-testid="stSidebar"] * { color: #c9d1d9 !important; }

/* Remove default padding */
.block-container { padding: 1.5rem 2rem !important; max-width: 100% !important; }

/* Header */
.tp-header {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 0 0 20px 0;
    border-bottom: 1px solid #21262d;
    margin-bottom: 24px;
}
.tp-logo {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 1.6rem;
    font-weight: 700;
    color: #f0f6fc;
    letter-spacing: -1px;
}
.tp-logo span { color: #58a6ff; }
.tp-mode {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.7rem;
    padding: 3px 10px;
    border-radius: 20px;
    background: #161b22;
    border: 1px solid #30363d;
    color: #8b949e;
    text-transform: uppercase;
    letter-spacing: 2px;
}
.tp-mode.testnet { border-color: #d29922; color: #d29922; background: #1c1912; }
.tp-mode.real    { border-color: #f85149; color: #f85149; background: #1c1012; }

/* Metric cards */
.metric-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 12px;
    margin-bottom: 24px;
}
.metric-box {
    background: #0d1117;
    border: 1px solid #21262d;
    border-radius: 8px;
    padding: 18px 20px;
    position: relative;
    overflow: hidden;
}
.metric-box::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
}
.metric-box.blue::before  { background: #58a6ff; }
.metric-box.green::before { background: #3fb950; }
.metric-box.red::before   { background: #f85149; }
.metric-box.yellow::before { background: #d29922; }

.metric-label {
    font-size: 0.65rem;
    color: #6e7681;
    text-transform: uppercase;
    letter-spacing: 2px;
    margin-bottom: 8px;
    font-family: 'IBM Plex Mono', monospace;
}
.metric-val {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 1.7rem;
    font-weight: 700;
    color: #f0f6fc;
    line-height: 1;
}
.metric-val.blue  { color: #58a6ff; }
.metric-val.green { color: #3fb950; }
.metric-val.red   { color: #f85149; }
.metric-val.yellow { color: #e3b341; }
.metric-sub {
    font-size: 0.72rem;
    color: #6e7681;
    margin-top: 6px;
    font-family: 'IBM Plex Mono', monospace;
}

/* Signal banner */
.signal-buy {
    background: linear-gradient(90deg, #0d2b1d 0%, #0d1117 100%);
    border: 1px solid #238636;
    border-left: 4px solid #3fb950;
    border-radius: 8px;
    padding: 14px 20px;
    margin-bottom: 16px;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.9rem;
    color: #3fb950;
}
.signal-sell {
    background: linear-gradient(90deg, #2d1517 0%, #0d1117 100%);
    border: 1px solid #da3633;
    border-left: 4px solid #f85149;
    border-radius: 8px;
    padding: 14px 20px;
    margin-bottom: 16px;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.9rem;
    color: #f85149;
}
.signal-hold {
    background: linear-gradient(90deg, #1c1912 0%, #0d1117 100%);
    border: 1px solid #9e6a03;
    border-left: 4px solid #d29922;
    border-radius: 8px;
    padding: 14px 20px;
    margin-bottom: 16px;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.9rem;
    color: #d29922;
}

/* Section titles */
.section-title {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.7rem;
    color: #6e7681;
    text-transform: uppercase;
    letter-spacing: 3px;
    padding: 0 0 10px 0;
    border-bottom: 1px solid #21262d;
    margin-bottom: 16px;
    margin-top: 24px;
}

/* Trade buttons */
.stButton > button {
    font-family: 'IBM Plex Mono', monospace !important;
    font-weight: 600 !important;
    font-size: 0.9rem !important;
    letter-spacing: 2px !important;
    border-radius: 6px !important;
    border: none !important;
    height: 52px !important;
    width: 100% !important;
    text-transform: uppercase !important;
    transition: all 0.15s ease !important;
}

/* Order history table */
.order-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 10px 16px;
    border-bottom: 1px solid #161b22;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.8rem;
}
.order-row:hover { background: #0d1117; }
.tag-buy  { color: #3fb950; font-weight: 700; }
.tag-sell { color: #f85149; font-weight: 700; }
.price-val { color: #f0f6fc; }
.time-val  { color: #6e7681; }

/* Input styles */
.stSelectbox > div, .stNumberInput > div { 
    background: #161b22 !important; 
    border: 1px solid #30363d !important;
}

/* Chart background */
.js-plotly-plot .plotly { background: transparent !important; }

/* Streamlit remove top padding */
#MainMenu, footer, header { visibility: hidden; }
.stDeployButton { display: none; }
div[data-testid="stToolbar"] { display: none; }

/* Alert override */
.stAlert { border-radius: 6px !important; }
</style>
""", unsafe_allow_html=True)

# ── Config ────────────────────────────────────────────────────────────────
def get_config():
    api_key = api_secret = ""
    testnet = True
    tele_token = tele_chat = ""
    try:
        import config as c
        api_key, api_secret = c.API_KEY, c.API_SECRET
        testnet = c.TESTNET
        tele_token, tele_chat = c.TELEGRAM_TOKEN, c.TELEGRAM_CHAT_ID
    except ImportError:
        pass
    api_key    = os.environ.get("API_KEY", api_key)
    api_secret = os.environ.get("API_SECRET", api_secret)
    tele_token = os.environ.get("TELEGRAM_TOKEN", tele_token)
    tele_chat  = os.environ.get("TELEGRAM_CHAT_ID", tele_chat)
    return api_key, api_secret, testnet, tele_token, tele_chat

API_KEY, API_SECRET, TESTNET, TELE_TOKEN, TELE_CHAT = get_config()
ATR_PERIOD, ATR_MULTIPLIER, TIMEFRAME = 10, 3.0, "D"

@st.cache_resource
def get_session():
    return HTTP(testnet=TESTNET, api_key=API_KEY, api_secret=API_SECRET)
session = get_session()

# ── Helpers ───────────────────────────────────────────────────────────────
def send_tg(msg):
    if TELE_TOKEN and TELE_CHAT:
        try: requests.post(f"https://api.telegram.org/bot{TELE_TOKEN}/sendMessage",
                           json={"chat_id": TELE_CHAT, "text": msg}, timeout=5)
        except: pass

def get_balance():
    try:
        r = session.get_wallet_balance(accountType="UNIFIED", coin="USDT")
        return float(r["result"]["list"][0]["coin"][0]["walletBalance"])
    except: return None

def get_precio(symbol):
    try:
        r = session.get_tickers(category="spot", symbol=symbol)
        return float(r["result"]["list"][0]["lastPrice"])
    except: return None

def get_candles(symbol):
    try:
        result = session.get_kline(category="spot", symbol=symbol, interval=TIMEFRAME, limit=120)
        c = sorted(result["result"]["list"], key=lambda x: int(x[0]))
        return ([float(x[1]) for x in c],[float(x[2]) for x in c],
                [float(x[3]) for x in c],[float(x[4]) for x in c],[int(x[0]) for x in c])
    except: return None,None,None,None,None

def calc_supertrend(highs, lows, closes):
    trs = [max(highs[i]-lows[i], abs(highs[i]-closes[i-1]), abs(lows[i]-closes[i-1]))
           for i in range(1, len(closes))]
    atr = [sum(trs[:ATR_PERIOD])/ATR_PERIOD]
    for i in range(ATR_PERIOD, len(trs)):
        atr.append((atr[-1]*(ATR_PERIOD-1)+trs[i])/ATR_PERIOD)
    ub, lb, trend = [], [], []
    for i in range(len(atr)):
        idx = i+ATR_PERIOD
        hl2 = (highs[idx]+lows[idx])/2
        bu = hl2+ATR_MULTIPLIER*atr[i]; bl = hl2-ATR_MULTIPLIER*atr[i]
        if i==0:
            ub.append(bu); lb.append(bl)
            trend.append(-1 if closes[idx]<=bu else 1)
        else:
            u = bu if bu<ub[-1] or closes[idx-1]>ub[-1] else ub[-1]
            l = bl if bl>lb[-1] or closes[idx-1]<lb[-1] else lb[-1]
            ub.append(u); lb.append(l)
            if   trend[-1]==-1 and closes[idx]>u:  trend.append(1)
            elif trend[-1]==1  and closes[idx]<l:  trend.append(-1)
            else: trend.append(trend[-1])
    return trend, ub, lb

def place_order(symbol, side, qty, razon="MANUAL"):
    try:
        r = session.place_order(category="linear", symbol=symbol, side=side,
                                orderType="Market", qty=str(qty), timeInForce="GTC")
        oid = r["result"]["orderId"]
        precio = get_precio(symbol) or 0
        send_tg(f"[{side.upper()}] {razon}\nPar: {symbol}\nPrecio: {precio:.2f}\nCantidad: {qty}")
        return True, oid, precio
    except Exception as e:
        return False, str(e), 0

def get_positions(symbol):
    try:
        r = session.get_positions(category="linear", symbol=symbol, settleCoin="USDT")
        return [p for p in r["result"]["list"] if float(p.get("size",0))>0]
    except: return []

# ── Session state ─────────────────────────────────────────────────────────
if "historial" not in st.session_state: st.session_state.historial = []

# ── Sidebar ───────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### ⚙ Configuración")
    symbol = st.selectbox("Par", ["BTCUSDT","ETHUSDT","SOLUSDT","BNBUSDT","XRPUSDT"])
    qty    = st.number_input("Cantidad", min_value=0.0001, value=0.001, step=0.001, format="%.4f")
    st.divider()
    auto = st.checkbox("Auto-refresh (30s)")
    if st.button("↻  Actualizar", use_container_width=True):
        st.cache_data.clear(); st.rerun()
    st.divider()
    st.markdown(f"<div style='font-size:0.7rem;color:#6e7681;font-family:IBM Plex Mono'>{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</div>", unsafe_allow_html=True)

# ── Header ────────────────────────────────────────────────────────────────
modo_class = "testnet" if TESTNET else "real"
modo_txt   = "TESTNET" if TESTNET else "⚠ REAL"
st.markdown(f"""
<div class="tp-header">
  <div class="tp-logo">Trend<span>Pulse</span></div>
  <div class="tp-mode {modo_class}">{modo_txt}</div>
  <div style="flex:1"></div>
  <div style="font-family:'IBM Plex Mono',monospace;font-size:0.75rem;color:#6e7681">{symbol}</div>
</div>
""", unsafe_allow_html=True)

# ── Fetch data ────────────────────────────────────────────────────────────
with st.spinner(""):
    precio  = get_precio(symbol)
    balance = get_balance()
    opens, highs, lows, closes, timestamps = get_candles(symbol)

# ── SuperTrend ────────────────────────────────────────────────────────────
trend_cur = trend_prev = st_line = None
if closes and len(closes) > ATR_PERIOD+5:
    trend, ub, lb = calc_supertrend(highs, lows, closes)
    trend_cur  = trend[-1]
    trend_prev = trend[-2]
    st_line    = lb[-1] if trend_cur==1 else ub[-1]

# ── Metric cards ──────────────────────────────────────────────────────────
p_fmt  = f"${precio:,.2f}"   if precio  else "—"
b_fmt  = f"${balance:,.2f}" if balance else "—"
t_color, t_txt = ("green","▲ ALCISTA") if trend_cur==1 else ("red","▼ BAJISTA") if trend_cur==-1 else ("yellow","—")
st_fmt = f"${st_line:,.2f}" if st_line else "—"

st.markdown(f"""
<div class="metric-grid">
  <div class="metric-box blue">
    <div class="metric-label">Precio {symbol[:3]}/USDT</div>
    <div class="metric-val blue">{p_fmt}</div>
  </div>
  <div class="metric-box">
    <div class="metric-label">Saldo USDT</div>
    <div class="metric-val">{b_fmt}</div>
    <div class="metric-sub">Cuenta unificada</div>
  </div>
  <div class="metric-box {t_color}">
    <div class="metric-label">Tendencia</div>
    <div class="metric-val {t_color}">{t_txt}</div>
  </div>
  <div class="metric-box yellow">
    <div class="metric-label">Nivel SuperTrend</div>
    <div class="metric-val yellow">{st_fmt}</div>
    <div class="metric-sub">ATR({ATR_PERIOD}) × {ATR_MULTIPLIER}</div>
  </div>
</div>
""", unsafe_allow_html=True)

# ── Señal ─────────────────────────────────────────────────────────────────
if trend_cur is not None and trend_prev is not None:
    cambio = trend_cur != trend_prev
    if cambio and trend_cur==1:
        st.markdown('<div class="signal-buy">▲ SEÑAL BOT: COMPRAR — SuperTrend cambió a alcista en el cierre de vela</div>', unsafe_allow_html=True)
    elif cambio and trend_cur==-1:
        st.markdown('<div class="signal-sell">▼ SEÑAL BOT: VENDER — SuperTrend cambió a bajista en el cierre de vela</div>', unsafe_allow_html=True)
    elif trend_cur==1:
        st.markdown('<div class="signal-hold">◆ Tendencia alcista activa — sin cambio en este cierre</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="signal-hold">◆ Tendencia bajista activa — sin cambio en este cierre</div>', unsafe_allow_html=True)

# ── Gráfico ───────────────────────────────────────────────────────────────
st.markdown('<div class="section-title">Gráfico · Diario</div>', unsafe_allow_html=True)

if closes and len(closes) > 20:
    import plotly.graph_objects as go
    n   = min(60, len(closes))
    ts  = [datetime.fromtimestamp(t/1000) for t in timestamps[-n:]]
    fig = go.Figure()
    fig.add_trace(go.Candlestick(
        x=ts, open=opens[-n:], high=highs[-n:], low=lows[-n:], close=closes[-n:],
        name=symbol,
        increasing=dict(line=dict(color="#3fb950", width=1), fillcolor="#1a3a24"),
        decreasing=dict(line=dict(color="#f85149", width=1), fillcolor="#3a1a1a"),
    ))
    # SuperTrend line
    if len(trend) >= n:
        for i in range(n-1):
            idx = len(trend)-n+i
            col = "#3fb950" if trend[idx]==1 else "#f85149"
            val = lb[idx] if trend[idx]==1 else ub[idx]
            val2= lb[idx+1] if trend[idx+1]==1 else ub[idx+1]
            fig.add_trace(go.Scatter(x=[ts[i],ts[i+1]], y=[val,val2],
                mode="lines", line=dict(color=col, width=2),
                showlegend=False, hoverinfo="skip"))
    fig.update_layout(
        paper_bgcolor="#080b10", plot_bgcolor="#0d1117",
        font=dict(color="#8b949e", family="IBM Plex Mono", size=10),
        xaxis=dict(gridcolor="#161b22", linecolor="#21262d", showgrid=True, zeroline=False),
        yaxis=dict(gridcolor="#161b22", linecolor="#21262d", showgrid=True, zeroline=False, side="right"),
        margin=dict(l=0, r=60, t=10, b=0), height=360,
        xaxis_rangeslider_visible=False,
        showlegend=False,
        hovermode="x unified",
    )
    st.plotly_chart(fig, use_container_width=True)

# ── Trading manual ────────────────────────────────────────────────────────
st.markdown('<div class="section-title">Trading Manual</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown("""<style>div[data-testid="column"]:nth-of-type(1) .stButton>button{
        background:#1a3a24 !important; color:#3fb950 !important;
        border:1px solid #238636 !important;}</style>""", unsafe_allow_html=True)
    if st.button(f"▲   COMPRAR  {symbol[:3]}", key="buy", use_container_width=True):
        ok, res, p = place_order(symbol, "Buy", qty)
        if ok:
            st.success(f"✓ Compra ejecutada @ ${p:,.2f}  |  ID: {res}")
            st.session_state.historial.append({"t":"BUY","s":symbol,"q":qty,"p":p,"h":datetime.now().strftime("%H:%M:%S")})
        else:
            st.error(f"✗ Error: {res}")

with col2:
    st.markdown("""<style>div[data-testid="column"]:nth-of-type(2) .stButton>button{
        background:#3a1a1a !important; color:#f85149 !important;
        border:1px solid #da3633 !important;}</style>""", unsafe_allow_html=True)
    if st.button(f"▼   VENDER  {symbol[:3]}", key="sell", use_container_width=True):
        ok, res, p = place_order(symbol, "Sell", qty)
        if ok:
            st.success(f"✓ Venta ejecutada @ ${p:,.2f}  |  ID: {res}")
            st.session_state.historial.append({"t":"SELL","s":symbol,"q":qty,"p":p,"h":datetime.now().strftime("%H:%M:%S")})
        else:
            st.error(f"✗ Error: {res}")

# ── Posiciones ────────────────────────────────────────────────────────────
st.markdown('<div class="section-title">Posiciones Abiertas</div>', unsafe_allow_html=True)

positions = get_positions(symbol)
if positions:
    for pos in positions:
        upnl = float(pos.get("unrealisedPnl", 0))
        col_a, col_b, col_c, col_d = st.columns(4)
        col_a.metric("Lado", pos.get("side",""))
        col_b.metric("Tamaño", pos.get("size",""))
        col_c.metric("Entrada", f"${float(pos.get('avgPrice',0)):,.2f}")
        col_d.metric("P&L", f"{'+'if upnl>=0 else''}${upnl:.2f}", delta=f"{upnl:.2f}")
else:
    st.markdown("<p style='color:#6e7681;font-size:0.8rem;font-family:IBM Plex Mono'>Sin posiciones abiertas</p>", unsafe_allow_html=True)

# ── Historial ─────────────────────────────────────────────────────────────
st.markdown('<div class="section-title">Historial · Esta sesión</div>', unsafe_allow_html=True)

if st.session_state.historial:
    st.markdown('<div style="background:#0d1117;border:1px solid #21262d;border-radius:8px;overflow:hidden">', unsafe_allow_html=True)
    for op in reversed(st.session_state.historial):
        tag_class = "tag-buy" if op["t"]=="BUY" else "tag-sell"
        st.markdown(f"""
        <div class="order-row">
          <span class="{tag_class}">{op['t']}</span>
          <span style="color:#c9d1d9">{op['s']}</span>
          <span style="color:#c9d1d9">{op['q']}</span>
          <span class="price-val">${op['p']:,.2f}</span>
          <span class="time-val">{op['h']}</span>
        </div>""", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
else:
    st.markdown("<p style='color:#6e7681;font-size:0.8rem;font-family:IBM Plex Mono'>Sin operaciones en esta sesión</p>", unsafe_allow_html=True)

if auto:
    time.sleep(30); st.rerun()
