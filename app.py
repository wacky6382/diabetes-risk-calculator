import streamlit as st
import numpy as np

# 1. 網頁基礎設定
st.set_page_config(
    page_title="糖尿病風險評估-蔡瑋峻醫師", 
    page_icon="🩺", 
    layout="centered"
)

# 2. 手機端視覺優化 (客製化 CSS)
st.markdown("""
    <style>
    /* 設定主背景色與字體 */
    .stApp { background-color: #F8FAFC; }
    
    /* 讓手機端的標題與文字更清楚 */
    h1 { color: #007380; font-family: 'PingFang TC', 'Heiti TC', sans-serif; font-size: 2rem !important; }
    p, label { font-size: 1.15rem !important; font-weight: 600 !important; color: #1E293B !important; }

    /* 強化輸入框顯示，方便手指點擊 */
    .stNumberInput div div input {
        font-size: 1.3rem !important;
        padding: 12px !important;
        background-color: #FFFFFF !important;
        border: 2px solid #E2E8F0 !important;
        border-radius: 10px !important;
    }

    /* 數值卡片設計 */
    div[data-testid="stMetric"] {
        background-color: #ffffff;
        border-radius: 15px;
        padding: 18px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
        border-top: 5px solid #007380;
    }
    </style>
    """, unsafe_allow_html=True)

# 標題與研究來源說明
st.title("🩺 糖尿病風險衛教計算器")
st.markdown("### 台南奇美醫院 蔡瑋峻醫師 關心您")
st.info("💡 **實證醫學基礎**：本工具採用 2023 年《BMJ Open》針對 64,875 名台灣人之研究模型 [cite: 6, 12, 141]。")

# --- 第一區塊：生理指標輸入 (設定間距 0.1) ---
st.header("1. 請輸入生理數值")
st.write("點擊「+」或「-」可微調 0.1 單位")

col1, col2 = st.columns(2)
with col1:
    h = st.number_input("身高 (cm)", value=170.0, step=0.1, format="%.1f")
    w = st.number_input("體重 (kg)", value=70.0, step=0.1, format="%.1f")
with col2:
    waist = st.number_input("腰圍 (cm)", value=85.0, step=0.1, format="%.1f")
    hip = st.number_input("臀圍 (cm)", value=95.0, step=0.1, format="%.1f")

# --- 第二區塊：其他關鍵風險因子 ---
st.header("2. 其他基本資料")
c_age = st.number_input("年齡", 30, 70, 38)
c_gender = st.selectbox("性別", ["男", "女"], index=0)

with st.expander("📝 點擊輸入學歷與生活史"):
    c_edu = st.selectbox("教育程度", 
        options=[1, 2, 3, 4, 5, 6, 7], 
        format_func=lambda x: {1:"不識字", 2:"自修", 3:"小學", 4:"國中", 5:"高中", 6:"大學", 7:"研究所"}[x],
        index=6)
    c_family = st.radio("糖尿病家族史 (父母/兄弟姊妹)", ["沒有", "有"], index=0)
    c_betel = st.radio("是否有吃檳榔習慣", ["從未或極少", "有"], index=0)

# --- 運算邏輯 (引用論文 Table 2 Model 1 係數) ---
bmi = w / ((h / 100) ** 2)
whr = waist / hip

# 論文係數 [cite: 231, 232]
intercept = -12.935 
b_age = 0.046 
b_sex = -0.215 if c_gender == "男" else 0.0
b_bmi = 0.132 
b_whr = 4.950 
b_edu = -0.071 
b_family = 0.593 if c_family == "有" else 0.0
b_betel = 0.184 if c_betel == "有" else 0.0

logit_p = intercept + (b_age * c_age) + b_sex + (b_bmi * bmi) + (b_whr * whr) + (b_edu * c_edu) + b_family + b_betel
probability = 1 / (1 + np.exp(-logit_p))

# --- 第三區塊：結果呈現 ---
st.divider()
st.subheader("📊 您目前的生理指數")
m1, m2 = st.columns(2)
m1.metric("計算所得 BMI", f"{bmi:.2f}")
m2.metric("計算所得 腰臀比 (WHR)", f"{whr:.2f}")

st.subheader("🏆 風險預測結果")
# 論文建議之糖尿病預測切截點為 0.0065 [cite: 247]
if probability >= 0.0065:
    st.error(f"### 風險值：{probability:.4f}")
    st.markdown("⚠️ **評估結果：高於切截點 (0.0065)**")
    st.write("根據 2023 台灣 Biobank 模型預估，您具備較高的未診斷糖尿病風險 [cite: 32, 353]。")
else:
    st.success(f"### 風險值：{probability:.4f}")
    st.markdown("✅ **評估結果：低於切截點 (0.0065)**")
    st.write("目前風險較低，請繼續保持理想的腰圍與體重指標。")

# 警語
st.warning("⚠️ 本預測結果僅供參考。若有相關症狀，請持本結果向醫師諮詢並進行抽血確認 [cite: 349, 350]。")
