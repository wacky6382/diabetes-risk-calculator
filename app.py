import streamlit as st
import numpy as np

# 頁面配置
st.set_page_config(page_title="台灣版糖尿病風險計算器", page_icon="🩺")

# 專業樣式設定
st.markdown("""
    <style>
    .stApp { background-color: #F0F4F8; }
    div[data-testid="stMetric"] {
        background-color: #ffffff;
        border-left: 5px solid #007380;
        border-radius: 5px;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🩺 糖尿病風險衛教計算器")
st.caption("實證醫學來源：BMJ Open Diabetes Research & Care 2023 (Taiwan Biobank Study)")

# 免責聲明
st.warning("⚠️ 本預測結果僅供衛教參考。若有『多吃、多喝、多尿』或體重減輕，請務必諮詢醫師。")

# --- 側邊欄：基本與行為資料 ---
with st.sidebar:
    st.header("📋 基礎資料")
    age = st.number_input("年齡", 30, 70, 38)
    gender = st.selectbox("性別", ["男", "女"], index=0)
    family_hx = st.radio("糖尿病家族史 (父母/兄弟姊妹)", ["沒有", "有"], index=0)
    
    st.divider()
    st.header("🥗 生活與教育")
    # 論文中的教育程度編碼：7 代表研究所
    edu_level = st.selectbox("教育程度", 
        options=[1, 2, 3, 4, 5, 6, 7], 
        format_func=lambda x: {1:"不識字", 2:"自修", 3:"小學", 4:"國中", 5:"高中", 6:"大學", 7:"研究所"}[x],
        index=6)
    betel = st.radio("是否有吃檳榔習慣", ["從未或極少", "目前/過去有"], index=0)

# --- 主畫面：生理指標輸入 ---
st.header("📏 生理指標輸入")
col1, col2 = st.columns(2)

with col1:
    height = st.number_input("身高 (cm)", 100.0, 250.0, 170.0)
    weight = st.number_input("體重 (kg)", 30.0, 200.0, 78.2)

with col2:
    waist = st.number_input("腰圍 (cm)", 50.0, 150.0, 89.0)
    hip = st.number_input("臀圍 (cm)", 50.0, 150.0, 100.0)

# --- 自動計算指標 ---
bmi = weight / ((height / 100) ** 2)
whr = waist / hip

# 顯示計算結果
c1, c2 = st.columns(2)
c1.metric("計算所得 BMI", f"{bmi:.2f}")
c2.metric("計算所得 腰臀比 (WHR)", f"{whr:.2f}")

# --- 論文 Model 1 邏輯運算 ---
# 係數 (Beta)
intercept = -12.935
b_age = 0.046
b_sex = -0.215 if gender == "男" else 0.0
b_bmi = 0.132
b_whr = 4.950
b_edu = -0.071
b_family = 0.593 if family_hx == "有" else 0.0
b_betel = 0.184 if "目前" in betel else 0.0

# 計算 Logit 與 機率
logit_p = intercept + (b_age * age) + b_sex + (b_bmi * bmi) + (b_whr * whr) + (b_edu * edu_level) + b_family + b_betel
probability = 1 / (1 + np.exp(-logit_p))

# --- 結果評估 ---
st.divider()
st.subheader("🏆 風險評估結果")

# 論文 Model 1 切截點：0.0065
if probability >= 0.0065:
    st.error(f"預估風險值：{probability:.4f}")
    st.write("🔴 **結果：高於切截點 (0.0065)。** 您具有較高的未診斷糖尿病風險，建議至醫院進行抽血檢測。")
else:
    st.success(f"預估風險值：{probability:.4f}")
    st.write("🟢 **結果：低於切截點 (0.0065)。** 目前風險較低，請維持理想的腰圍與體重。")

with st.expander("📝 為什麼要測量這些？ (實證筆記)"):
    st.write(f"""
    * **腰臀比 (WHR)**：本研究發現其 Beta 值高達 **4.950**，是預測台灣人代謝健康最重要的單一指標。
    * **BMI**：反映整體肥胖程度，結合腰臀比能提供更精準的預測。
    * **教育程度**：較高的健康識能與較低的糖尿病風險呈顯著相關。
    """)
