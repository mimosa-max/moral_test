import streamlit as st
import google.generativeai as genai
import time

# --- 1. 제미나이 API 설정 ---
# 기존의 "AIza..." 코드는 삭제하고 아래 한 줄만 남깁니다.
API_KEY = st.secrets["GOOGLE_API_KEY"]

genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-1.5-pro')

# --- 2. 웹페이지 기본 화면 설정 ---
st.set_page_config(page_title="도덕적 인격 분석기", page_icon="📖", layout="wide")

# 상단 제목 영역
st.markdown("### 📖 AI 도덕적 인격 분석 피드백 생성기")
st.caption("도덕적 사고, 감정, 실천 의지를 분석하고 따뜻한 피드백을 제공합니다. ✨ Powered by Gemini")
st.divider()

# --- 3. 화면을 왼쪽(입력)과 오른쪽(출력) 두 칸으로 나누기 ---
col1, col2 = st.columns([1, 1.2])

# === 왼쪽 창: 학생 입력 영역 ===
with col1:
    st.markdown("#### 📄 분석 내용 입력")
    
    # 학생 이름 칸을 없애고 인물 이름만 넓게 입력받도록 수정
    person_name = st.text_input("선택한 인물", placeholder="예: 안중근 의사")
    
    # 도덕성의 3요소 입력창
    thought = st.text_area("1. 도덕적 사고 (판단)", placeholder="어떤 상황에서 무엇이 옳은 일이라고 생각하고 판단했나요?")
    emotion = st.text_area("2. 도덕적 감정 (공감)", placeholder="그 상황에서 어떤 감정(슬픔, 분노, 책임감 등)을 느꼈을까요?")
    action = st.text_area("3. 도덕적 실천 의지 (행동)", placeholder="생각과 감정을 바탕으로 어떤 행동을 실천했나요?")
    
    # 피드백 생성 버튼
    submit_button = st.button("✨ 피드백 생성하기", type="primary", use_container_width=True)

# === 오른쪽 창: 제미나이 피드백 출력 영역 ===
with col2:
    if not submit_button:
        st.info("🎓\n\n**피드백이 이곳에 생성됩니다.**\n\n좌측에 분석 내용을 모두 입력하고 '생성하기' 버튼을 누르면, 선생님을 대신해 AI가 따뜻하고 구체적인 맞춤형 피드백을 작성해 드립니다.")
    
    else:
        # 이름 확인 부분을 빼고 나머지 빈칸만 확인
        if not person_name or not thought or not emotion or not action:
            st.warning("왼쪽의 모든 입력 칸을 채워주세요!")
        else:
            with st.spinner("아이의 마음에 공감하며 따뜻한 피드백을 작성하고 있습니다..."):
                # 이름이 빠진 새로운 프롬프트
                prompt = f"""
                너는 중학교 도덕 선생님이야. 비판보다는 따뜻한 공감과 지지를 바탕으로 피드백을 줘.
                
                [학생 작성 내용]
                - 분석한 인물: {person_name}
                - 도덕적 사고: {thought}
                - 도덕적 감정: {emotion}
                - 도덕적 실천 의지: {action}
                
                [피드백 작성 지침]
                1. 먼저 학생이 인물의 마음과 상황에 깊이 공감하려고 노력한 점을 구체적으로 다정하게 칭찬해 줘. (특정 이름 대신 '학생'이나 '우리 친구'라고 부를 것)
                2. 도덕적 사고, 감정, 실천 의지가 알맞게 분석되었는지 확인하고, 내용이 잘 연결되었는지 짚어줘.
                3. 이 인물의 도덕적 인격을 학생 자신의 일상생활(친구 관계, 학교생활 등)에 어떻게 적용해 볼 수 있을지 생각해보게 하는 부드러운 성찰 질문을 1개 던져 줘.
                """
                
                try:
                    response = model.generate_content(prompt)
                    
                    st.success("**피드백이 완성되었습니다!**")
                    st.write(response.text)
                except Exception as e:
                    st.error("피드백을 생성하는 중 오류가 발생했습니다. API 키를 확인해 주세요.")
