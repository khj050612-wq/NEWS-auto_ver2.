import streamlit as st
import google.generativeai as genai

# 1. API 키 설정
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("Secrets에서 API 키를 먼저 등록해주세요!")

st.set_page_config(page_title="보건의료 수집기", layout="wide")

# 세션 관리
if 'stage' not in st.session_state:
    st.session_state.stage = 0

# 키워드
keywords = ["진단검사의학과 인공지능", "디지털 병리", "보행 파킨슨", "의료기사법", "서울아산병원 AI"]

st.title("🏥 보건·의료 역량 창고")
selected_kw = st.selectbox("키워드 선택", keywords)

if st.button(f"'{selected_kw}' 기사 가져오기"):
    st.session_state.stage = 1

if st.session_state.stage >= 1:
    st.info(f"검색된 기사: {selected_kw} 관련 최신 성과 보고")
    if st.button("✨ AI 심화 분석 시작"):
        with st.spinner("분석 중..."):
            try:
                # 가장 확실한 최신 모델명 하나만 타겟팅
                model = genai.GenerativeModel('gemini-1.5-flash')
                prompt = f"보건의료 전문가 입장에서 '{selected_kw}'의 수치와 인사이트를 분석해줘."
                
                response = model.generate_content(prompt)
                
                st.subheader("📋 분석 결과")
                # 빨강/파랑 시각화
                res = response.text.replace("**", "<span style='color:red; font-weight:bold;'>").replace("*", "<span style='color:blue; font-weight:bold;'>")
                st.markdown(res, unsafe_allow_html=True)
                st.session_state.stage = 2
            except Exception as e:
                st.error(f"오류 내용: {e}")

if st.sidebar.button("초기화"):
    st.session_state.stage = 0
    st.rerun()
    
