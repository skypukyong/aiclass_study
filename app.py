import streamlit as st
from openai import OpenAI
st.write("Hello World!")
question = st.text_input("질문을 입력하세요")

client = OpenAI(api_key="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")
response = client.chat.completions.create(
  model="gpt-4o-mini",
  messages=[
    {"role": "user", "content": question}
  ]
)
st.write(response.choices[0].message.content)
