import streamlit as st
from openai import OpenAI
st.write("Hello World!")
api_key = st.text_input("apikey입력")
 
prompt = st.text_input("질문을 입력하세요")
client = OpenAI(api_key=api_key)
response = client.chat.completions.create(
  model="gpt-4o-mini",
  messages=[
    {"role": "user", "content": prompt}
  ]
)

st.write(response.choices[0].message.content)
