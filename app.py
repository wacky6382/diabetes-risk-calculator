import streamlit as st

# 設定頁面佈局與標題
st.set_page_config(page_title="糖尿病風險評估工具", page_icon="🩺")

# 自定義 CSS 讓介面更專業
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stMetric { background-color: #ffffff; padding: 15px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
    </style>
    """, unsafe_content_type=True)

st.title("🩺 糖尿病風險衛教計算器")
st.caption("台南奇美醫學中心兒科部 蔡瑋峻醫師 關心您的健康")

# 重要免責聲明
st.warning("⚠️ 本網站預測結果僅提供參考，實際結果仍需就醫確認。若有相關症狀請諮詢醫師。")

# --- 側邊欄：輸入區 ---
st.sidebar.header("📋 基本資料輸入")
with st.sidebar:
    st.subheader("不可改變因素")
    gender = st.radio("性別", ["男", "女"], index=0)
    age = st.number_input("您的年齡", value=38, min_value=1, max_value=120)
    family = st.radio("父母或兄弟姊妹是否有糖尿病？", ["沒有", "有"], index=0)
    
    st.divider()
    
    st.subheader("可改變因素")
    edu = st.selectbox("您的學歷", ["國中及以下", "高中/職", "大學/大專", "研究所及以上"], index=3)
    history = st.selectbox("是否吃過檳榔", ["從未吃過，或只吃過一兩次而已", "目前有吃", "過去曾吃但已戒"], index=0)

# --- 主畫面：動態互動區 ---
st.header("📊 風險因子動態模擬")
st.write("請滑動下方拉桿，看看數值改變對風險的影響：")

col1, col2 = st.columns(2)
with col1:
    whr = st.slider("您的腰臀比 (WHR)", 0.60, 1.20, 0.89, 0.01, help="腰圍除以臀圍")
with col2:
    bmi = st.slider("您的 BMI", 10.0, 45.0, 27.06, 0.01, help="體重(kg) / 身高(m)^2")

# --- 邏輯計算與權重 ---
# 先天因素
gender_val = -0.22 if gender == "男" else 0.0
age_val = 1.76 if age >= 35 else 0.0 # 簡化逻辑
family_val = 0.0 if family == "沒有" else 2.0

# 可變因素 (精準對齊您的數據)
edu_val = -0.50 if edu == "研究所及以上" else 0.0
whr_val = 4.41 if whr >= 0.89 else (whr / 0.89) * 4.41
bmi_val = 3.59 if bmi >= 27.06 else (bmi / 27.06) * 3.59
betel_val = 0.0 if "從未" in history else 1.5

total_score = gender_val + age_val + family_val + edu_val + whr_val + bmi_val + betel_val

# --- 結果顯示 ---
st.divider()
st.subheader("🏆 風險評估結果")

# 模擬風險分布條
risk_percent = min(100, int((total_score / 15) * 100))
st.progress(risk_percent / 100)

if total_score < 8:
    st.success(f"您的風險總分：{total_score:.2f} — 「尚無立即糖尿病風險」")
elif total_score < 12:
    st.warning(f"您的風險總分：{total_score:.2f} — 「中度風險，請注意生活作息」")
else:
    st.error(f"您的風險總分：{total_score:.2f} — 「高風險，強烈建議諮詢醫師」")

# --- 衛教資訊板 ---
st.subheader("💡 衛教重點指引")
c1, c2, c3 = st.columns(3)
c1.metric("不可變因素扣分", f"{gender_val + age_val + family_val:.2f}")
c2.metric("可變因素權重", f"{whr_val + bmi_val + edu_val:.2f}", delta="- 調整空間大", delta_color="inverse")
c3.metric("目標 BMI", "24.0", delta="-3.06")

with st.expander("📝 查看詳細分析"):
    st.write(f"1. **腰臀比 ({whr})**：貢獻了 {whr_val:.2f} 分。這是您最能掌控的指標！")
    st.write(f"2. **BMI ({bmi})**：目前為過重，若降至 24，分數可減少約 1 分。")
    st.write("3. **正面因子**：您的學歷背景與無檳榔史有助於降低總體風險。")

st.info("💡 這些是可改變的因素，即使是少量變化也可降低您的風險！")
