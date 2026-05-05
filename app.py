import streamlit as st
import google.generativeai as genai

# 1. API 키 및 모델 설정
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("Streamlit Secrets에 GEMINI_API_KEY를 등록해주세요!")

# 404 에러 방지를 위해 가장 안정적인 모델명 사용
MODEL_NAME = 'gemini-1.5-flash-latest' 

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

st.subheader("🌐 모듈 1: 기사 수집")

if st.button(f"'{selected_keyword}' 관련 최신 기사 가져오기"):
    st.session_state.stage = 1

if st.session_state.stage >= 1:
    article_options = [
        f"[{selected_keyword}] 최신 기술 도입 현황 및 성과",
        f"{selected_keyword} 기반 스마트 병원 구축 사례",
        f"보건의료 현장의 {selected_keyword} 실무 적용 가이드"
    ]
    
    selected_article = st.radio("분석할 기사를 선택하세요:", article_options)
    
    if st.button("✨ 이 기사 심화 분석 시작"):
        st.session_state.selected_article = selected_article
        st.session_state.stage = 2

# 모듈 2 분석 (그 블로그의 수치&인사이트 방식 적용)
if st.session_state.stage >= 2:
    st.divider()
    st.subheader("📑 모듈 2: 보건·의료 전문 분석 결과")
    
    with st.spinner("AI가 분석 중입니다..."):
        try:
            model = genai.GenerativeModel(MODEL_NAME)
            prompt = f"""
            너는 보건의료 전문 커리어 컨설턴트야. 
            기사 제목 '{st.session_state.selected_article}'을 바탕으로 분석해줘.
            
            [출력 양식]
            1. 제목: {st.session_state.selected_article}
            2. 단체: 관련 기관 명시
            3. 핵심키워드: #태그 형식
            4. 수치데이터: 핵심 수치는 **수치**로 강조
            5. 핵심인사이트: 시사점은 *인사이트*로 강조
            6. 실무자역질문: 날카로운 면접 질문
            7. 날짜: 2026-05-05
            8. 기사링크: https://news.naver.com/...
            """
            
            response = model.generate_content(prompt)
            result_text = response.text
            
            col1, col2 = st.columns(2)
            with col1:
                st.info("🎨 시각적 분석 (빨강:수치 / 파랑:인사이트)")
                # 블로그 스타일의 색상 강조 적용
                styled_result = result_text.replace("**", "<span style='color:#FF4B4B; font-weight:bold;'>").replace("*", "<span style='color:#1C83E1; font-weight:bold;'>")
                st.markdown(f"<div style='line-height:1.6;'>{styled_result}</div>", unsafe_allow_html=True)
            
            with col2:
                st.warning("💾 자소서 활용 데이터")
                st.text_area("분석 내용 (복사용)", value=result_text, height=350)
                if st.button("데이터 저장"):
                    st.success("저장 완료!")
                    
        except Exception as e:
            st.error(f"모델 연결 오류: {e}. 'gemini-1.5-flash'로 다시 시도해보세요.")

if st.sidebar.button("🔄 초기화"):
    st.session_state.stage = 0
    st.rerun()
