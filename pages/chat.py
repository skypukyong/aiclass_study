import streamlit as st
import openai  # OpenAI 라이브러리 사용

# API 키 캐시 함수
@st.cache_data
def api_key_input_cache(api_key):
    return api_key

# 세션 상태에 API 키 저장
if 'key' not in st.session_state:
    api_key = st.text_input("API 키를 입력하세요")  # API 키 입력 필드
    if api_key:
        st.session_state.key = api_key_input_cache(api_key)

# 세션 상태에서 API 키 가져오기
api_key = st.session_state.get('key')

# 세션 상태에서 메시지 리스트 초기화
if 'messages' not in st.session_state:
    st.session_state.messages = []  # 메시지 리스트 초기화

if api_key:
    # 질문 입력 받기
    prompt = st.chat_input("질문을 입력하세요")

    if prompt:  # 질문이 입력된 경우에만 API 요청
        # 사용자 질문 출력
        st.chat_message("user").markdown(prompt)
        
        # 메시지 리스트에 사용자 메시지 추가
        st.session_state.messages.append({"role": "user", "content": prompt})

        # OpenAI API 호출
        client = OpenAI(api_key=api_key)

        # GPT 모델에 질문 요청
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}
            ]
        )


        # GPT 응답 처리
        response_message = response['choices'][0]['message']['content']

        # 응답 출력
        with st.chat_message("assistant"):
            st.markdown(response_message)
        
        # 메시지 리스트에 GPT 응답 추가
        st.session_state.messages.append({"role": "assistant", "content": response_message})
