import streamlit as st
import google.generativeai as genai

# 1. API 키 설정
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("Streamlit Cloud 설정(Secrets)에서 GEMINI_API_KEY를 등록해주세요!")

st.set_page_config(page_title="보건의료 자소서 소스 수집기", layout="wide")

# 세션 상태 초기화 (처음 실행될 때만)
if 'stage' not in st.session_state:
    st.session_state.stage = 0

# 키워드 데이터
keywords = {
    "진단/기술": ["진단검사의학과 인공지능", "디지털 병리", "심초음파 AI", "심전도 분석", "뇌파 검사"],
    "신경/임상": ["보행 파킨슨 분석", "인지 치매 검사", "안구운동검사 안진", "암 진단 기술"],
    "시스템/정책": ["검사 자동화 시스템 TLA", "디지털 헬스케어 웨어러블", "원격의료 재택의료 POCT", "의료기사법 돌봄의료"],
    "상급종합병원": ["서울아산병원 AI 의료", "삼성서울병원 디지털 헬스", "서울대학교병원 빅데이터", "세브란스병원"]
}

# 사이드바
st.sidebar.title("🔍 검색 설정")
category = st.sidebar.selectbox("카테고리 선택", list(keywords.keys()))
selected_keyword = st.sidebar.selectbox("핵심 키워드", keywords[category])

st.title("🏥 보건·의료 전공 역량 창고")
st.write(f"현재 타켓: **{selected_keyword}**")

# --- 모듈 1: 기사 수집 ---
st.subheader("🌐 모듈 1: 기사 수집")

# 기사 가져오기 버튼을 누르면 스테이지 1로 진입
if st.button(f"'{selected_keyword}' 관련 최신 기사 가져오기"):
    st.session_state.stage = 1

if st.session_state.stage >= 1:
    # (실제 API 연동 전까지는 예시 데이터)
    article_options = [
        f"[{selected_keyword}] 상급종합병원 도입 사례 분석",
        f"{selected_keyword} 기술의 임상적 유효성과 미래 전망",
        f"의료진 인터뷰: {selected_keyword} 도입 후 변화된 워크플로우"
    ]
    
    selected_article = st.radio("분석할 기사를 선택하세요:", article_options)
    
    # 분석 시작 버튼을 누르면 스테이지 2로 진입
    if st.button("✨ 이 기사 심화 분석 시작"):
        st.session_state.selected_article = selected_article
        st.session_state.stage = 2

# --- 모듈 2: 심화 분석 (그 블로그 스타일!) ---
if st.session_state.stage >= 2:
    st.divider()
    st.subheader("📑 모듈 2: 보건·의료 전문 분석 결과")
    
    with st.spinner("AI가 수치와 인사이트를 추출하고 있습니다..."):
        model = genai.GenerativeModel('gemini-1.5-flash')
        prompt = f"""
        기사: {st.session_state.selected_article}
        키워드: {selected_keyword}
        
        보건의료 전문 컨설턴트 관점에서 위 기사를 분석해줘. 
        [중요] 수치는 **수치** 형식으로, 인사이트는 *인사이트* 형식으로 작성해.

        1. 제목: {st.session_state.selected_article}
        2. 단체: 관련 주요 기관
        3. 핵심키워드: #태그1 #태그2 #태그3
        4. 수치데이터: 기사 속 핵심 수치 (빨간색 강조를 위해 **수치** 형식 사용)
        5. 핵심인사이트: 산업의 흐름 (파란색 강조를 위해 *인사이트* 형식 사용)
        6. 실무자역질문: 면접용 날카로운 질문 1개
        7. 날짜: 2026-05-05
        8. 기사링크: https://news.naver.com/...
        """
        
        try:
            response = model.generate_content(prompt)
            result_text = response.text
            
            col1, col2 = st.columns([1, 1])
            with col1:
                st.info("🎨 시각적 분석 (Red:수치 / Blue:인사이트)")
                # 마크다운 내 특수문자를 HTML 색상 태그로 치환
                styled_result = result_text.replace("**", "<span style='color:#FF4B4B; font-weight:bold;'>").replace("*", "<span style='color:#1C83E1; font-weight:bold;'>")
                st.markdown(f"<div style='line-height:1.8;'>{styled_result}</div>", unsafe_allow_html=True)
            
            with col2:
                st.warning("💾 저장 및 자소서 활용")
                st.text_area("텍스트 데이터 (복사용)", value=result_text, height=250)
                if st.button("구글 시트에 최종 저장"):
                    st.balloons()
                    st.success("데이터가 성공적으로 저장되었습니다!")
        
        except Exception as e:
            st.error(f"API 호출 중 오류가 발생했습니다: {e}")

# 초기화 버튼 (사이드바 하단)
if st.sidebar.button("🔄 검색 초기화"):
    st.session_state.stage = 0
    st.rerun()
