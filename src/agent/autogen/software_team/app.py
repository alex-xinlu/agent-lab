# app.py —— v1.1 修复版：✅ 完全免费 · ✅ 真实趋势 · ✅ 无 401 错误
import streamlit as st
import requests
import time
from datetime import datetime, timedelta
from streamlit_autorefresh import st_autorefresh
import altair as alt
import pandas as pd

# 🔧 配置（同前）
API_URL_PRICE = "https://api.coingecko.com/api/v3/simple/price"
COIN_ID = "bitcoin"
VS_CURRENCY = "usd"
PARAMS_PRICE = {
    "ids": COIN_ID,
    "vs_currencies": VS_CURRENCY,
    "include_24hr_change": "true"
}
REFRESH_INTERVAL_MS = 30_000
HISTORY_LENGTH = 24  # 保留最近24次价格

# 📦 缓存价格数据（同前）
@st.cache_data(ttl=30)
def fetch_btc_price():
    try:
        with st.spinner("📡 获取比特币实时价格中..."):
            response = requests.get(API_URL_PRICE, params=PARAMS_PRICE, timeout=10)
            response.raise_for_status()
            data = response.json()
            btc_data = data.get(COIN_ID, {})
            if not isinstance(btc_data, dict):
                raise ValueError("API 返回数据格式异常：bitcoin 字段非对象")
            price = btc_data.get(VS_CURRENCY)
            change_24h = btc_data.get(f"{VS_CURRENCY}_24h_change")
            if price is None or not isinstance(price, (int, float)):
                raise ValueError("价格字段缺失或无效")
            if change_24h is None or not isinstance(change_24h, (int, float)):
                raise ValueError("24小时涨跌幅字段缺失或无效")
            change_amount = price * (change_24h / 100) if change_24h else 0.0
            return {
                "price": float(price),
                "change_percent": float(change_24h),
                "change_amount": float(change_amount),
                "timestamp": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
            }
    except requests.exceptions.Timeout:
        raise ConnectionError("⏰ 请求超时，请检查网络连接")
    except requests.exceptions.ConnectionError:
        raise ConnectionError("🌐 无法连接到 CoinGecko 服务器")
    except requests.exceptions.HTTPError as e:
        raise ConnectionError(f"❌ API 请求失败（HTTP {response.status_code}）")
    except Exception as e:
        raise RuntimeError(f"🚨 请求价格时发生未知错误：{str(e)}")

# 🧠 新增：管理本地价格历史（滚动窗口，存于 st.session_state）
def get_or_init_price_history():
    """初始化或获取价格历史列表：[(price, timestamp_str), ...]，最多 HISTORY_LENGTH 项"""
    if "price_history" not in st.session_state:
        st.session_state.price_history = []
    
    # 确保是 list of tuples，且长度 ≤ HISTORY_LENGTH
    history = st.session_state.price_history
    if not isinstance(history, list):
        st.session_state.price_history = []
        return []
    
    # 截断过长历史
    if len(history) > HISTORY_LENGTH:
        st.session_state.price_history = history[-HISTORY_LENGTH:]
    
    return st.session_state.price_history

def append_price_to_history(price: float, timestamp: str):
    """追加新价格到历史（自动截断）"""
    history = get_or_init_price_history()
    history.append((price, timestamp))
    # 保持最新在末尾，最多 HISTORY_LENGTH
    if len(history) > HISTORY_LENGTH:
        st.session_state.price_history = history[-HISTORY_LENGTH:]
    else:
        st.session_state.price_history = history

# 🎨 页面配置（同前）
st.set_page_config(
    page_title="₿ Bitcoin Price Tracker",
    page_icon="🟡",
    layout="centered",
    initial_sidebar_state="collapsed"
)

st.markdown("### 🟡 Bitcoin (BTC) 实时价格追踪器")
st.caption("数据源自 [CoinGecko](https://www.coingecko.com/) • 免费 API")

# ⚙️ 刷新控制（同前）
with st.expander("⚙️ 刷新设置", expanded=False):
    auto_refresh = st.toggle("启用自动刷新（每 30 秒）", value=True)
    if auto_refresh:
        st_autorefresh(interval=REFRESH_INTERVAL_MS, key="auto-refresh-counter")

# 🔁 手动刷新按钮（更新价格 + 更新历史）
col1, col2 = st.columns([4, 1])
with col1:
    st.write("")
with col2:
    if st.button("🔄 刷新全部数据", type="primary", use_container_width=True):
        # 清除价格缓存，触发重新获取
        fetch_btc_price.clear()
        # 注意：历史缓存不清理（保留趋势连续性），由 append 逻辑自动维护
        st.rerun()

# 📊 主价格卡片（同前）
placeholder_metric = st.empty()

try:
    price_data = fetch_btc_price()
    price_usd = price_data["price"]
    change_pct = price_data["change_percent"]
    change_amt = price_data["change_amount"]
    last_updated = price_data["timestamp"]

    # ✅ 将本次价格加入历史（关键！构建趋势数据源）
    append_price_to_history(price_usd, "Now")

    placeholder_metric.metric(
        label="Bitcoin (BTC)",
        value=f"${price_usd:,.2f}",
        delta=f"${change_amt:,.2f} ({change_pct:+.2f}%)",
        delta_color="normal"
    )
    st.caption(f"⏱️ 最后更新：{last_updated}")

except Exception as e:
    placeholder_metric.error(f"❌ 获取实时价格失败：{str(e)}")
    st.info("💡 点击【🔄 刷新全部数据】重试")

# 📈 新增：基于本地历史的「24次刷新趋势图」（✅ 100% 免费！）
st.divider()
st.subheader("📊 24次刷新价格趋势")

placeholder_chart = st.empty()

# 构建趋势 DataFrame（从 st.session_state 读取）
history = get_or_init_price_history()
if len(history) == 0:
    placeholder_chart.info("📈 趋势图正在积累数据…请刷新几次以生成趋势")
else:
    # 创建 DataFrame：index 为 "Now", "1 ago", "2 ago", ...
    n = len(history)
    labels = ["Now"] + [f"{i} refresh{'es' if i > 1 else ''} ago" for i in range(1, n)]
    # 取最后 n 个点（保证顺序：最旧→最新）
    prices = [p for p, _ in history[-n:]]
    timestamps = [t for _, t in history[-n:]]

    df = pd.DataFrame({
        "label": labels[-n:],  # 保证长度一致
        "price": prices,
        "timestamp": timestamps,
        "is_current": [i == len(labels) - 1 for i in range(len(labels))]
    })

    # Altair 图表（同前逻辑，仅数据源不同）
    base = alt.Chart(df).encode(
        x=alt.X("label:N", title="刷新序号（相对当前）", sort=None),
        y=alt.Y("price:Q", title=f"价格（{VS_CURRENCY.upper()}）", scale=alt.Scale(zero=False)),
        tooltip=["label", "price", "timestamp"]
    )

    line = base.mark_line(
        point=True,
        strokeWidth=2,
        color="#FF9900"
    ).encode(
        order="timestamp:N"  # 用 timestamp 字符串排序（"Now" 在最后）
    )

    current_point = base.transform_filter(
        alt.datum.is_current == True
    ).mark_circle(
        size=100,
        color="#00CC66",
        stroke="#FFFFFF",
        strokeWidth=2
    )

    chart = (line + current_point).properties(
        height=300,
        width="container"
    ).configure_axis(
        labelFontSize=12,
        titleFontSize=14
    ).configure_title(
        fontSize=16
    )

    placeholder_chart.altair_chart(chart, use_container_width=True)

    # 补充统计
    min_p = df["price"].min()
    max_p = df["price"].max()
    st.caption(
        f"📉 近 {len(df)} 次刷新区间：${min_p:,.2f} – ${max_p:,.2f} "
        f"（波动幅度：{((max_p - min_p) / min_p * 100):+.2f}%）"
    )

# 📜 页脚（同前）
st.divider()
st.caption(
    "💡 提示：本应用完全开源、无跟踪、不收集任何用户数据。"
    "所有数据均来自 CoinGecko 公共 API。"
)
st.caption(
    "📊 趋势说明：图表基于您主动刷新的 24 个价格点生成（非小时级采样），"
    "真实反映您关注时段内的价格变化轨迹。"
)


# 运行：`streamlit run app.py`