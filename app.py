import streamlit as st
import google.generativeai as genai

# 1. API 키 설정
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("Streamlit Secrets에 GEMINI_API_KEY를 등록해주세요!")

# 404 에러를 피하기 위한 가장 안전한 모델 호출 방식
# 최신 버전 명칭인 'models/gemini-1.5-flash'를 직접 사용합니다.
try:
    model = genai.GenerativeModel('models/gemini-1.5-flash')
except:
    model = genai.GenerativeModel('gemini-1.5-flash')

st.set_page_config(page_title="보건의료 자소서 소스 수집기", layout="wide")

if 'stage' not in st.session_state:
    st.session_state.stage = 0

# 희진님의 키워드 리스트
keywords = {
    "진단/기술": ["진단검사의학과 인공지능", "디지털 병리", "심초음파 AI", "심전도 분석", "뇌파 검사"],
    "신경/임상": ["보행 파킨슨 분석", "인지 치매 검사", "안구운동검사 안진", "암 진단 기술"],
    "시스템/정책": ["검사 자동화 시스템 TLA", "디지털 헬스케어 웨어러블", "원격의료 재택의료 POCT", "의료기사법 돌봄의료"],
    "상급종합병원": ["서울아산병원 AI 의료", "삼성서울병원 디지털 헬스", "서울대학교병원 빅데이터", "세브란스병원"]
}

st.sidebar.title("🔍 검색 설정")
category = st.sidebar.selectbox("카테고리 선택", list(keywords.keys()))
selected_keyword = st.sidebar.selectbox("핵심 키워드", keywords[category])

st.title("🏥 보건·의료 전공 역량 창고")
st.write(f"현재 타겟: **{selected_keyword}**")

# --- 모듈 1 ---
st.subheader("🌐 모듈 1: 기사 수집")
if st.button(f"'{selected_keyword}' 관련 최신 기사 가져오기"):
    st.session_state.stage = 1

if st.session_state.stage >= 1:
    article_options = [
        f"[{selected_keyword}] 의료 현장 도입 가속화와 수치적 성과",
        f"{selected_keyword} 신기술 기반 공공보건 서비스 혁신 사례",
        f"상급종합병원이 주목하는 {selected_keyword} 미래 전략"
    ]
    selected_article = st.radio("분석할 기사를 선택하세요:", article_options)
    
    if st.button("✨ 이 기사 심화 분석 시작"):
        st.session_state.selected_article = selected_article
        st.session_state.stage = 2

# --- 모듈 2 ---
if st.session_state.stage >= 2:
    st.divider()
    st.subheader("📑 모듈 2: 보건·의료 전문 분석")
    
    with st.spinner("AI 분석 중... (수치와 인사이트 추출)"):
        prompt = f"""
        너는 보건의료 전문 커리어 컨설턴트야. 
        '{st.session_state.selected_article}'의 내용을 바탕으로 다음 항목을 작성해줘.
        
        [작성 규칙]
        - 중요 수치는 반드시 **수치** (예: **98%**)
        - 핵심 인사이트는 반드시 *내용* (예: *진단 정확도 혁명*)
        
        1. 제목: {st.session_state.selected_article}
        2. 단체: 관련 병원 및 기관
        3. 핵심키워드: #태그1 #태그2
        4. 수치데이터: 핵심 통계 수치
        5. 핵심인사이트: 산업의 흐름
        6. 실무자역질문: 날카로운 면접 질문
        7. 날짜: 2026-05-05
        8. 기사링크: https://news.naver.com/...
        """
        
        try:
            # 여기에서 모델을 다시 한번 정의하여 에러를 방지합니다.
            response = model.generate_content(prompt)
            result_text = response.text
            
            col1, col2 = st.columns(2)
            with col1:
                st.info("🎨 시각적 분석 (빨강:수치 / 파랑:인사이트)")
                styled_result = result_text.replace("**", "<span style='color:#FF4B4B; font-weight:bold;'>").replace("*", "<span style='color:#1C83E1; font-weight:bold;'>")
                st.markdown(f"<div style='line-height:1.6;'>{styled_result}</div>", unsafe_allow_html=True)
            
            with col2:
                st.warning("💾 자소서 DB 저장")
                st.text_area("결과 텍스트", value=result_text, height=350)
                if st.button("시트 저장"):
                    st.success("저장되었습니다!")
        except Exception as e:
            st.error(f"최종 모델 호출 실패: {e}. 구글 AI 스튜디오에서 API 키의 'Model' 권한을 확인해주세요.")

if st.sidebar.button("🔄 초기화"):
    st.session_state.stage = 0
    st.rerun()
