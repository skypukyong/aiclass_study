import streamlit as st
from openai import OpenAI
st.write("Hello World!")
if 'key' not in st.session_state:
    api_key = st.text_input("apikey입력")
    if api_key:
        st.session_state.key = api_key
api_key = st.session_state.get('key')
if api_key:
    # 질문 입력 받기
    prompt = st.text_input("질문을 입력하세요")

    # OpenAI API 호출
    if prompt:  # 질문이 입력된 경우에만 API 요청
        openai.api_key = api_key  # API 키 설정

        # GPT 모델에 질문 요청
        response = client.chat.completions.create(
         model="gpt-4o-mini",
         messages=[{"role": "user", "content": prompt}
         ]
        )

        # 응답 출력
        st.write(response.choices[0].message.content)
