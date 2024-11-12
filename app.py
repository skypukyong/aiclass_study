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
