import streamlit as st
from openai import OpenAI
@st.cache_data
def api_key_input_cash(api_key):
    return api_key
if 'key' not in st.session_state:
    api_key = st.text_input("apikey입력")
    if api_key:
        st.session_state.key = api_key_input_cash(api_key)
api_key = st.session_state.get('key')
if api_key:
    # 질문 입력 받기
    
    prompt = st.chat_input("질문을 입력하세요")
    # OpenAI API 호출
    if prompt:   # 질문이 입력된 경우에만 API 요청
        st.chat_message("user").markdown(prompt) 
        st.session_state.messages.append({"role": "user", "content": prompt})
        client = OpenAI(api_key=api_key)

        # GPT 모델에 질문 요청
        response = client.chat.completions.create(
         model="gpt-4o-mini",
         messages=[{"role": "user", "content": prompt}
         ]
        )

        response = f"Echo: {prompt}"
        with st.chat_message("assistant"):
            st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})
