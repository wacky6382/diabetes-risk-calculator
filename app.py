import streamlit as st
import numpy as np

st.set_page_config(page_title="台灣版糖尿病風險計算器", page_icon="🇹🇼")

st.title("🩺 糖尿病風險衛教計算器 (實證醫學版)")
st.caption("參考來源：BMJ Open Diabetes Research & Care 2023;11:e003423 (Taiwan Biobank Study)")

# --- 側邊欄輸入 ---
with st.sidebar:
    st.header("個人參數")
    age = st.number_input("年齡 (Age)", 30, 70, 38)
    gender = st.selectbox("性別 (Sex)", ["男", "女"], index=0)
    edu_level = st.slider("教育程度 (1:不識字 ~ 7:研究所)", 1, 7, 7)
    family_hx = st.radio("糖尿病家族史 (父母/兄弟姊妹)", ["無", "有"], index=0)
    betel = st.radio("檳榔習慣", ["從未或極少", "經常"], index=0)

# --- 主畫面滑桿 ---
st.header("可改變生理指標")
whr = st.slider("腰臀比 (WHR)", 0.60, 1.20, 0.89, 0.01)
bmi = st.slider("BMI", 15.0, 40.0, 27.06, 0.1)

# --- 論文 Model 1 係數計算 (Beta Coefficients) ---
intercept = -12.935
b_age = 0.046
b_sex = -0.215 if gender == "男" else 0
b_bmi = 0.132
b_whr = 4.950
b_edu = -0.071
b_family = 0.593 if family_hx == "有" else 0
b_betel = 0.184 if betel == "經常" else 0

# 計算 Logit 與 機率
logit_p = intercept + (b_age * age) + (b_sex) + (b_bmi * bmi) + (b_whr * whr) + (b_edu * edu_level) + b_family + b_betel
probability = 1 / (1 + np.exp(-logit_p))

# --- 結果呈現 ---
st.divider()
st.subheader("📊 實證評估結果")

# 論文切截點參考：0.0065 (糖尿病預測)
if probability >= 0.0065:
    st.error(f"預估風險值：{probability:.4f} (高於切截點 0.0065)")
    st.write("🔴 **建議：** 根據研究模型，您的風險偏高，建議尋求醫療諮詢並進行空腹血糖檢測。")
else:
    st.success(f"預估風險值：{probability:.4f} (低於切截點 0.0065)")
    st.write("🟢 **評估：** 尚無立即未診斷糖尿病風險，請繼續保持良好生活習慣。")

with st.expander("📚 論文實證重點 (What this study adds)"):
    st.write("""
    - 本模型針對台灣人口開發，AUC 表現達 80.39% [cite: 29]。
    - **腰臀比**被證實是台灣人最重要的風險指標 [cite: 325]。
    - **教育程度**與糖尿病風險成負相關，高識能有助於預防 [cite: 330]。
    - 檳榔咀嚼史是台灣特有的顯著風險因子 [cite: 195]。
    """)
