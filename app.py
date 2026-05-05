import streamlit as st
import google.generativeai as genai
import datetime

# 1. 설정: Gemini API 키 및 구글 시트 연결 설정 (현재는 화면 표시 위주)
# 실제 구글 시트 저장을 위해서는 gspread 라이브러리 설정이 필요합니다.
genai.configure(api_key="YOUR_GEMINI_API_KEY") # 희진님의 API 키 입력

st.set_page_config(page_title="보건의료 자소서 소스 수집기", layout="wide")

# 2. 희진님의 전문 키워드 그룹화
keywords = {
    "진단/기술": ["진단검사의학과 인공지능", "디지털 병리", "심초음파 AI", "심전도 분석", "뇌파 검사"],
    "신경/임상": ["보행 파킨슨 분석", "인지 치매 검사", "안구운동검사 안진", "암 진단 기술"],
    "시스템/정책": ["검사 자동화 시스템 TLA", "디지털 헬스케어 웨어러블", "원격의료 재택의료 POCT", "의료기사법 돌봄의료"],
    "상급종합병원": ["서울아산병원 AI 의료", "삼성서울병원 디지털 헬스", "서울대학교병원 빅데이터", "세브란스병원"]
}

# 사이드바: 키워드 선택
st.sidebar.title("🔍 검색 설정")
category = st.sidebar.selectbox("카테고리 선택", list(keywords.keys()))
selected_keyword = st.sidebar.selectbox("핵심 키워드", keywords[category])

# 앱 메인 화면
st.title("🏥 보건·의료 전공 역량 창고")
st.caption(f"현재 선택된 타겟: {selected_keyword}")

# 모듈 1: 기사 수집 (여기서는 예시 리스트를 보여주고, 실제로는 뉴스 API 연동 가능)
st.subheader("🌐 모듈 1: 관련 최신 뉴스 수집")
if st.button(f"'{selected_keyword}' 최신 기사 가져오기"):
    # 실제 뉴스 API 호출 코드가 들어갈 자리입니다.
    st.success(f"'{selected_keyword}' 관련 최신 기사 3개를 찾았습니다.")
    
    # 예시 기사 선택 UI
    article_options = [
        f"[{selected_keyword}] 관련 상급종합병원 도입 가속화... 현장의 목소리는?",
        f"신기술 도입에 따른 {selected_keyword} 분석 효율성 30% 향상 사례",
        f"의료진이 말하는 {selected_keyword} 기술의 한계와 미래"
    ]
    selected_article = st.radio("분석할 기사를 선택하세요:", article_options)
    
    if st.button("선택한 기사 심화 분석 시작 (모듈 2)"):
        st.session_state['start_analysis'] = True

# 모듈 2: 심화 분석 (그 블로그 방식 그대로!)
if st.session_state.get('start_analysis'):
    st.divider()
    st.subheader("📑 모듈 2: 보건·의료 전문 분석 (By Gemini AI)")
    
    with st.spinner("보건·의료 관점에서 수치와 인사이트를 추출 중입니다..."):
        # AI에게 블로그 방식의 분석 프롬프트 전달
        prompt = f"""
        너는 보건의료 전문 커리어 컨설턴트야. 
        '{selected_keyword}'와 관련된 기사를 분석해서 자소서 소스를 만들어줘.
        
        [출력 형식]
        1. 제목: 기사 제목
        2. 단체: 관련 주요 기관(상급종합병원 등)
        3. 핵심키워드: #태그 형식 3개
        4. 수치데이터: 기사 속 중요한 숫자/통계 (빨간색 강조를 위해 **수치** 형식으로 표현)
        5. 핵심인사이트: 산업의 흐름 및 시사점 (파란색 강조를 위해 *인사이트* 형식으로 표현)
        6. 실무자역질문: 면접에서 활용할 날카로운 질문 1개
        7. 날짜: 오늘 날짜
        8. 기사링크: 원본 링크 주소
        
        보건의료 전공자(임상병리, 간호, 보건행정 등)의 관점에서 아주 전문적으로 작성해줘.
        """
        
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content(prompt)
        analysis_result = response.text

    # 화면 표시 (블로그 느낌으로 가독성 있게)
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.info("🎨 시각적 분석 (수치-Red / 인사이트-Blue)")
        # 실제 구현시 HTML/CSS를 사용하여 텍스트에 색상을 입힙니다.
        st.markdown(analysis_result.replace("**", "<span style='color:red'>").replace("*", "<span style='color:blue'>"), unsafe_allow_html=True)

    with col2:
        st.warning("💾 구글 시트 저장 데이터 확인")
        # 저장 전 최종 확인 칸 생성
        st.text_input("제목", value="[분석완료] " + selected_keyword)
        st.text_area("핵심 인사이트 요약")
        
        if st.button("구글 시트에 행 추가하기"):
            # 여기에 구글 시트 저장 로직 (gspread) 연동
            st.balloons()
            st.success("구글 시트 '보건의료_역량_창고'에 저장이 완료되었습니다!")

st.sidebar.divider()
st.sidebar.info("💡 저장된 데이터는 나중에 [자소서 생성 모듈]에서 자동으로 불러오게 됩니다.")
