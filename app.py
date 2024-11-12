import streamlit as st
from openai import OpenAI
st.write("Hello World!")
question = st.text_input("질문을 입력하세요")

client = OpenAI(api_key="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")
response = client.chat.completions.create(
  model="gpt-4o-mini",
  messages=[
    {"role": "user", "content": "question"}
  ]
)
st.write(response.choices[0].message.content)
