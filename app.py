import streamlit as st
import numpy as np

# 1. 頁面基礎設定與手機視覺優化
st.set_page_config(page_title="代謝與心血管風險評估", page_icon="🩺", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #F8FAFC; }
    h1, h2, h3, p, label { color: #0F172A !important; font-family: 'PingFang TC', sans-serif; }
    /* 強制輸入框白底黑字，解決手機看不見問題 */
    .stNumberInput div div input {
        background-color: #FFFFFF !important;
        color: #000000 !important;
        font-size: 1.25rem !important;
        padding: 10px !important;
        border: 2px solid #CBD5E1 !important;
        border-radius: 10px !important;
    }
    div[data-testid="stMetric"] {
        background-color: #ffffff;
        border-radius: 12px;
        padding: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        border-top: 6px solid #007380;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🩺 糖尿病與心血管風險評估")
st.markdown("**台南奇美醫院 蔡瑋峻醫師 專業衛教工具**")

# --- 側邊欄：共同基礎資料 ---
with st.sidebar:
    st.header("📋 基礎個人資料")
    age = st.number_input("年齡", 30, 70, 38)
    gender = st.selectbox("性別", ["男", "女"], index=0)
    family_dm = st.radio("糖尿病家族史", ["沒有", "有"], index=0)
    edu = st.selectbox("教育程度", options=[1,2,3,4,5,6,7], 
                       format_func=lambda x: {1:"不識字", 7:"研究所"}.get(x, "一般"), index=6)
    betel = st.radio("是否有吃檳榔習慣", ["無", "有"], index=0)

# --- 第一模組：糖尿病風險 (BMJ Open 2023) ---
st.header("1. 糖尿病篩檢 (2023 實證模型)")
col1, col2 = st.columns(2)
with col1:
    h = st.number_input("身高 (cm)", value=170.0, step=0.1, format="%.1f")
    w = st.number_input("體重 (kg)", value=78.2, step=0.1, format="%.1f")
with col2:
    waist = st.number_input("腰圍 (cm)", value=89.0, step=0.1, format="%.1f")
    hip = st.number_input("臀圍 (cm)", value=100.0, step=0.1, format="%.1f")

# 糖尿病計算邏輯 [cite: 193, 231, 232]
bmi = w / ((h / 100) ** 2)
whr = waist / hip
logit_dm = -12.935 + (0.046 * age) + (-0.215 if gender == "男" else 0) + (0.132 * bmi) + (4.950 * whr) + (-0.071 * edu) + (0.593 if family_dm == "有" else 0) + (0.184 if betel == "有" else 0)
p_dm = 1 / (1 + np.exp(-logit_dm))

m1, m2 = st.columns(2)
m1.metric("計算 BMI", f"{bmi:.2f}")
m2.metric("腰臀比 (WHR)", f"{whr:.2f}")

if p_dm >= 0.0065:
    st.error(f"未診斷糖尿病預測值：{p_dm:.4f} (高風險)")
else:
    st.success(f"未診斷糖尿病預測值：{p_dm:.4f} (低風險)")

st.divider()

# --- 第二模組：心血管風險 (IJERPH 2022) ---
st.header("2. 心血管評估 (2022 實證評分)")
show_cvd = st.checkbox("🔍 我想了解未來 10 年重大心血管事件風險 (中風/心臟病)")

if show_cvd:
    st.info("💡 本模型預測未來 10 年發生中風或冠心病之機率 。")
    c1, c2 = st.columns(2)
    with c1:
        sbp = st.number_input("收縮壓 (SBP, mmHg)", value=120, step=1)
        smoking = st.radio("吸菸習慣", ["從未吸菸", "已戒菸", "目前吸菸"], index=0)
    with c2:
        hdl = st.number_input("高密度脂蛋白 (HDL-C)", value=50, step=1)
        existing_dm = st.radio("是否已確診糖尿病", ["否", "是"], index=0)

    # 2022 論文點數邏輯計算 (精確化)
    cvd_points = 0
    # 年齡點數
    if age >= 60: cvd_points += 4
    elif age >= 50: cvd_points += 2
    # 吸菸
    if smoking == "目前吸菸": cvd_points += 3
    # 血壓
    if sbp >= 160: cvd_points += 5
    elif sbp >= 140: cvd_points += 3
    # 糖尿病史
    if existing_dm == "是": cvd_points += 4
    # HDL
    if hdl < 40: cvd_points += 2
    
    st.subheader("🏆 10 年心血管事件風險點數")
    st.metric("總風險積分", f"{cvd_points} 分")
    
    if cvd_points >= 7:
        st.error("🔴 **高風險群**：建議立即諮詢醫師進行心血管評估。")
    elif cvd_points >= 4:
        st.warning("🟡 **中度風險**：請注意血壓控管與生活作息調整。")
    else:
        st.success("🟢 **低風險群**：請繼續保持健康生活習慣。")

st.warning("⚠️ 本工具僅供診間衛教參考，實際診斷需由醫療人員確認。")
