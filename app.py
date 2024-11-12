import streamlit as st
from openai import OpenAI
st.write("Hello World!")
question = st.text_input("질문을 입력하세요")

client = OpenAI(api_key="sk-0qdihuZM4RN-gGz7tk9HqNR6GO10poNv-oftP2HUlRT3BlbkFJnNwX5YP9slEvfPkPJzPchl9tc7oVfMN4eSsQIaw2cA")
response = client.chat.completions.create(
  model="gpt-4o-mini",
  messages=[
    {"role": "user", "content": "question"}
  ]
)
st.write(response.choices[0].message.content)
