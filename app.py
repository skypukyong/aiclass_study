import streamlit as st
from openai import OpenAI
st.write("Hello World!")
api_key = st.text_input("apikey입력")
prompt = st.text_input("질문을 입력하세요")

client = OpenAI(api_key)
response = client.images.generate(
  model="dall-e-3",
  prompt=prompt)
image_url = response.data[0].url
st.image(image_url)
