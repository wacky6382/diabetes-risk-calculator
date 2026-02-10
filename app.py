import streamlit as st
import numpy as np

# 1. 頁面配置：設定為自動適應寬度
st.set_page_config(page_title="糖尿病風險評估", page_icon="🩺", layout="centered")

# 2. 手機端視覺優化 (CSS)
st.markdown("""
    <style>
    /* 全域背景與字體優化 */
    .stApp {
        background-color: #F8FAFC;
    }
    h1, h2, h3 {
        color: #0F172A;
        font-family: "Microsoft JhengHei", sans-serif;
    }
    p, label {
        font-size: 1.1rem !important;
        font-weight: 500 !important;
        color: #334155 !important;
    }
    
    /* 強化輸入框與按鈕在手機上的點擊感 */
    .stNumberInput div div input {
        font-size: 1.2rem !important;
        padding: 10px !important;
        border-radius: 8px !important;
    }
    
    /* 卡片式設計：顯示計算結果 */
    div[data-testid="stMetric"] {
        background-color: #ffffff;
        border-radius: 12px;
        padding: 15px;
        box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1);
        border-left: 6px solid #007380;
    }
    
    /* 警告與成功訊息框字體加大 */
    .stAlert p {
        font-size: 1rem !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 標題與來源
st.title("🩺 糖尿病風險衛教計算器")
st.markdown("**台南奇美醫院 蔡瑋峻醫師 關心您的健康**")
st.caption("實證醫學來源：BMJ Open Diabetes Research & Care 2023 [cite: 13]")

# 重要免責聲明
st.warning("⚠️ 本預測結果僅供衛教參考。若有『多吃、多喝、多尿』或體重減輕，請務必諮詢醫師 [cite: 34, 46]。")

# --- 主畫面：生理指標輸入 ---
st.header("📏 請輸入生理指標")
st.write("點擊「+」或「-」可精確調整至 0.1")

# 使用 columns 在大螢幕併排，手機會自動垂直排列
col1, col2 = st.columns(2)

with col1:
    height = st.number_input("身高 (cm)", value=170.0, step=0.1, format="%.1f")
    weight = st.number_input("體重 (kg)", value=78.2, step=0.1, format="%.1f")

with col2:
    waist = st.number_input("腰圍 (cm)", value=89.0, step=0.1, format="%.1f")
    hip = st.number_input("臀圍 (cm)", value=100.0, step=0.1, format="%.1f")

# --- 側邊欄：風險因子 (手機版側邊欄可收納) ---
with st.sidebar:
    st.header("📋 其他風險因子")
    age = st.number_input("您的年齡", 30, 70, 38)
    gender = st.selectbox("性別", ["男", "女"], index=0)
    family_hx = st.radio("糖尿病家族史 (父母/兄弟姊妹)", ["沒有", "有"], index=0)
    
    st.divider()
    edu_level = st.selectbox("教育程度", 
        options=[1, 2, 3, 4, 5, 6, 7], 
        format_func=lambda x: {1:"不識字", 2:"自修", 3:"小學", 4:"國中", 5:"高中", 6:"大學", 7:"研究所"}[x],
        index=6)
    betel = st.radio("是否有吃檳榔習慣", ["從未或極少", "目前/過去有"], index=0)

# --- 邏輯運算 ---
bmi = weight / ((height / 100) ** 2)
whr = waist / hip

# 論文 Model 1 係數 [cite: 231, 232]
intercept = -12.935
b_age = 0.046
b_sex = -0.215 if gender == "男" else 0.0
b_bmi = 0.132
b_whr = 4.950
b_edu = -0.071
b_family = 0.593 if family_hx == "有" else 0.0
b_betel = 0.184 if "目前" in betel else 0.0

logit_p = intercept + (b_age * age) + b_sex + (b_bmi * bmi) + (b_whr * whr) + (b_edu * edu_level) + b_family + b_betel
probability = 1 / (1 + np.exp(-logit_p))

# --- 結果顯示 ---
st.divider()
st.subheader("📊 評估數值")
m_col1, m_col2 = st.columns(2)
m_col1.metric("您的 BMI", f"{bmi:.2f}")
m_col2.metric("您的 腰臀比 (WHR)", f"{whr:.2f}")

st.subheader("🏆 糖尿病風險預測")

# 論文 Model 1 切截點：0.0065 [cite: 247]
if probability >= 0.0065:
    st.error(f"### 預估風險值：{probability:.4f}")
    st.markdown("#### **評估結果：高於切截點 (0.0065)**")
    st.markdown("您具有較高的未診斷糖尿病風險。")
    st.info("💡 **建議：** 建議至奇美醫院或其他醫療院所進行抽血（空腹血糖/糖化血色素）檢測 [cite: 353]。")
else:
    st.success(f"### 預估風險值：{probability:.4f}")
    st.markdown("#### **評估結果：低於切截點 (0.0065)**")
    st.write("目前風險較低，請維持理想的腰圍與體重。")

with st.expander("📚 為什麼這份報告具備參考價值？"):
    st.write("這份計算器是基於 **64,875 名台灣人** 的大數據研究成果 [cite: 141]：")
    st.write("* **腰臀比 (WHR)**：是台灣人最重要的風險指標，影響力（Beta 4.950）遠高於其他因素 [cite: 325, 232]。")
    st.write("* **教育程度**：研究發現高教育程度（研究所）具備統計學上的保護效力 [cite: 330, 232]。")
    st.write("* **精準度**：本模型預測未診斷糖尿病的 AUC 準確度達 **80.39%** [cite: 251]。")
