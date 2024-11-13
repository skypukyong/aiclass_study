import streamlit as st
from openai import OpenAI
st.write("Hello World!")
if 'key' not in st.session_state:
 st.session_state['key'] = api_key
else :
 api_key = st.text_input("apikey입력")
 st.session_state['key'] = api_key
st.write(st.session_state['key'])
prompt = st.text_input("질문을 입력하세요")
client = OpenAI(api_key=st.session_state['key'])
response = client.chat.completions.create(
  model="gpt-4o-mini",
  messages=[
    {"role": "user", "content": prompt}
  ]
)

st.write(response.choices[0].message.content)
