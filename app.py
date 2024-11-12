import streamlit as st
from openai import OpenAI
st.write("Hello World!")
prompt = st.text_input("질문을 입력하세요")

client = OpenAI(api_key="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")
response = client.images.generate(
  model="dall-e-3",
  prompt=prompt)
image_url = response.data[0].url
st.image(image_url)
