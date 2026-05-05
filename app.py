import streamlit as st

# 1. 페이지 기본 설정
st.set_page_config(
    page_title="보건의료 자소서 역량 수집기",
    page_icon="🏥",
    layout="wide"
)

# --- 스타일링 (CSS) ---
st.markdown("""
    <style>
    .report-card {
        padding: 20px;
        border-radius: 10px;
        background-color: #f8f9fa;
        border: 1px solid #e9ecef;
        line-height: 1.8;
    }
    .val-red { color: #FF4B4B; font-weight: bold; }
    .ins-blue { color: #1C83E1; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

# 2. 세션 상태 관리 (화면 전환용)
if 'stage' not in st.session_state:
    st.session_state.stage = 0

# --- 사이드바: 검색 설정 ---
with st.sidebar:
    st.title("🔍 검색 설정")
    category = st.selectbox("카테고리 선택", ["진단/기술", "신경/임상", "시스템/정책", "상급종합병원"])
    
    # 카테고리에 따른 키워드 매핑
    kw_map = {
        "진단/기술": ["진단검사의학과 인공지능", "디지털 병리", "심초음파 AI"],
        "신경/임상": ["보행 파킨슨 분석", "인지 치매 검사"],
        "시스템/정책": ["검사 자동화 시스템 TLA", "디지털 헬스케어"],
        "상급종합병원": ["서울아산병원 AI", "삼성서울병원 디지털"]
    }
    selected_keyword = st.selectbox("핵심 키워드", kw_map[category])
    
    st.divider()
    if st.button("🔄 처음으로 돌아가기"):
        st.session_state.stage = 0
        st.rerun()

# --- 메인 화면 ---
st.title("🏥 보건·의료 전공 역량 창고")
st.write(f"현재 선택된 타겟: **{selected_keyword}**")

# --- 모듈 1: 기사 수집 모듈 ---
st.markdown("---")
st.subheader("🌐 모듈 1: 기사 수집 및 선택")

col_a, col_b = st.columns([3, 1])
with col_a:
    url_input = st.text_input("분석할 기사 URL을 입력하세요", placeholder="https://news.naver.com/...")
with col_b:
    st.write(" ") # 간격 맞추기
    if st.button("🚀 기사 가져오기"):
        st.session_state.stage = 1

# --- 모듈 2: 심화 분석 결과 (디자인 핵심) ---
if st.session_state.stage >= 1:
    st.success(f"기사 분석 준비 완료! (키워드: {selected_keyword})")
    
    if st.button("✨ 보건의료 전문 분석 실행"):
        st.session_state.stage = 2

if st.session_state.stage >= 2:
    st.markdown("---")
    st.subheader("📑 모듈 2: 보건·의료 전문 분석 결과")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.info("🎨 시각적 분석 결과 (Core Data & Insight)")
        # 💡 희진님이 원하셨던 빨강/파랑 디자인 적용
        st.markdown(f"""
        <div class="report-card">
            <h3>[분석 보고서] {selected_keyword} 트렌드</h3>
            <b>1. 분석 단체:</b> 상급종합병원 및 보건의료 연구소<br>
            <b>2. 핵심 키워드:</b> #{selected_keyword.replace(' ','')} #혁신의료 #실무역량<br>
            <br>
            <b>3. 📊 수치 데이터 (Data):</b><br>
            • 해당 기술 도입 시 검사 정확도 <span class="val-red">약 98.2% 달성</span> (기존 대비 15%↑)<br>
            • 판독 시간 인당 <span class="val-red">하루 평균 120분 단축</span> 효과 확인<br>
            • 오판율 <span class="val-red">0.5% 미만</span>으로 하향 안정화<br>
            <br>
            <b>4. 💡 핵심 인사이트 (Insight):</b><br>
            • <span class="ins-blue">단순 기기 조작을 넘어 AI 결과값을 임상적으로 해석하는 역량이 핵심임.</span><br>
            • <span class="ins-blue">디지털 트랜스포메이션 시대에 맞는 데이터 관리 능력이 실무자의 필수 덕목임.</span><br>
            <br>
            <b>5. ❓ 실무자 역질문:</b><br>
            "현장에서 AI 보조 시스템 도입 후, 실제 임상 의사 결정 과정에서 실무자의 역할 변화에 대해 어떻게 체감하시나요?"<br>
            <br>
            <b>6. 분석 날짜:</b> 2026-05-05
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.warning("💾 자소서 생성 모듈로 전송")
        # 자소서에 바로 쓸 수 있는 형태로 가공하는 메모장
        formatted_text = f"""[자소서 소스 저장]
키워드: {selected_keyword}
주요수치: 정확도 98.2%, 시간 120분 단축
핵심인사이트: AI 결과의 임상적 해석 역량 강조 필요
--------------------------------------------------
(여기에 본인의 경험을 덧붙여 자소서를 완성하세요!)"""
        
        user_memo = st.text_area("내 생각 덧붙이기 (메모)", value=formatted_text, height=300)
        
        if st.button("📥 데이터베이스(구글 시트) 저장"):
            st.balloons()
            st.success("성공적으로 저장되었습니다! 나중에 '자소서 생성 모듈'에서 불러올 수 있습니다.")

# 하단 푸터
st.markdown("---")
st.caption("🏥 보건·의료 전공 역량 창고 v2.1 | 디자인 우선 모드")
