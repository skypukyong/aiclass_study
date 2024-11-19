import streamlit as st

@st.cache_data
def ask_gpt(prompt):
    client = st.session_state['openai_client']
    response = client.chat.completions.create(
        model = "gpt-4o-mini",
        messages = [
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content


client = st.session_state.get('openai_client', None)
if client is None:
    if st.button("API Key를 입력하세요."):
        st.switch_page("pages/1_Setting.py")
    st.stop()

st.header("Ask GPT")



prompt = st.chat_input("질문을 입력하세요.")
st.session_state.prompt = prompt
with st.chat_message("user"):
    st.write(prompt)

answer = ''
if prompt:
    answer = ask_gpt(prompt)

    with st.chat_message("ai"):
        st.write(answer)

