import streamlit as st
import google.generativeai as genai
from google.generativeai.types import GenerationConfig

# 1. API 키 설정
if "GEMINI_API_KEY" in st.secrets:
    # 💡 핵심: 버전을 'v1'으로 강제 지정하여 v1beta 에러를 우회합니다.
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("Streamlit Secrets에 API 키를 등록해주세요!")

st.set_page_config(page_title="보건의료 수집기", layout="wide")

# 세션 관리
if 'stage' not in st.session_state:
    st.session_state.stage = 0

st.title("🏥 보건·의료 역량 창고 (최종 최적화)")

# 키워드 및 선택 UI
keywords = ["진단검사의학과 인공지능", "디지털 병리", "보행 파킨슨", "의료기사법", "서울아산병원 AI"]
selected_kw = st.selectbox("키워드 선택", keywords)

if st.button(f"'{selected_kw}' 데이터 가져오기"):
    st.session_state.stage = 1

if st.session_state.stage >= 1:
    st.info(f"분석 대상: {selected_kw} 관련 최신 동향")
    
    if st.button("✨ AI 심화 분석 시작 (강제 연결)"):
        with st.spinner("구글 서버와 통신 중..."):
            try:
                # 💡 모델 선언 시 가장 표준적인 경로인 'gemini-1.5-flash' 사용
                model = genai.GenerativeModel('gemini-1.5-flash')
                
                prompt = f"""
                보건의료 전문가 관점에서 '{selected_kw}'를 분석해.
                수치는 **숫자**, 인사이트는 *내용* 형식으로 작성해줘.
                1. 제목 / 2. 단체 / 3. 키워드 / 4. 수치데이터 / 5. 핵심인사이트 / 6. 역질문
                """
                
                # 강제 호출
                response = model.generate_content(prompt)
                
                if response:
                    st.subheader("📋 분석 완료")
                    # 빨강/파랑 시각화 적용
                    res = response.text.replace("**", "<span style='color:red; font-weight:bold;'>").replace("*", "<span style='color:blue; font-weight:bold;'>")
                    st.markdown(f"<div style='border:1px solid #ddd; padding:20px; border-radius:10px;'>{res}</div>", unsafe_allow_html=True)
                    st.session_state.stage = 2
                    
            except Exception as e:
                # 상세 에러 출력으로 원인 파악
                st.error(f"⚠️ 연결 시도 실패: {str(e)}")
                st.info("💡 해결책: Google AI Studio에서 'New Project'로 키를 새로 발급받아 교체해보세요.")

if st.sidebar.button("초기화"):
    st.session_state.stage = 0
    st.rerun()
