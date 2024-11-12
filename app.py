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
