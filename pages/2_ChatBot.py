import streamlit as st

@st.cache_data
def ask_gpt(messages):
    client = st.session_state['openai_client']
    response = client.chat.completions.create(
        model="gpt-4o-mini",  # 적절한 모델 이름으로 변경하세요
        messages=messages
    )
    return response.choices[0].message.content


client = st.session_state.get('openai_client', None)
if client is None:
    if st.button("API Key를 입력하세요."):
        st.switch_page("pages/1_Setting.py")
    st.stop()

st.header("Ask GPT")

# 대화 내역을 session_state에 저장
if 'messages' not in st.session_state:
    st.session_state['messages'] = []

prompt = st.chat_input("질문을 입력하세요.")
st.session_state.prompt = prompt

answer = ''
if prompt:
    # 사용자 메시지를 대화 내역에 추가
    st.session_state['messages'].append({"role": "user", "content": prompt})
    
    # 이전 대화와 함께 GPT 모델에 요청
    answer = ask_gpt(st.session_state['messages'])

    # AI의 응답을 대화 내역에 추가
    st.session_state['messages'].append({"role": "assistant", "content": answer})

    # 대화 표시
    with st.chat_message("user"):
        st.write(prompt)
    
    with st.chat_message("assistant"):
        st.write(answer)

# 대화 내역을 계속 이어가려면 이 코드를 사용합니다.
