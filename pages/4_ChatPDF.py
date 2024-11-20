import streamlit as st
import pdfplumber
import openai
import faiss
import tempfile
import os

# OpenAI API 호출 함수
@st.cache_data
def ask_gpt(messages):
    client = st.session_state['openai_client']
    response = client.chat.completions.create(
        model="gpt-4",  # 적절한 모델 사용
        messages=messages
    )
    return response.choices[0].message.content

# OpenAI 클라이언트 초기화
client = st.session_state.get('openai_client', None)
if client is None:
    if st.button("API Key를 입력하세요."):
        st.switch_page("pages/1_Setting.py")
    st.stop()

st.header("Ask GPT with PDF Search")

# 대화 내역을 세션 상태에 저장
if 'messages' not in st.session_state:
    st.session_state['messages'] = []

# 대화 내역 초기화 버튼
if st.button('Clear'):
    st.session_state['messages'] = []
    st.experimental_rerun()

# 대화창 나가기 버튼
if st.button('대화창 나가기'):
    st.session_state['messages'] = []  # 대화 내역 초기화
    st.session_state['openai_client'] = None  # OpenAI 클라이언트 정보 삭제
    st.experimental_rerun()  # 페이지 새로고침

# PDF 파일 업로드 (하나의 파일만 받기)
uploaded_file = st.file_uploader("PDF 파일을 업로드하세요.", type=["pdf"])

# 파일 업로드 후 텍스트 추출 및 벡터 스토어 초기화
if uploaded_file:
    with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
        tmp_file.write(uploaded_file.read())
        tmp_file_path = tmp_file.name

    # pdfplumber를 사용하여 PDF 파일에서 텍스트 추출
    text = ""
    with pdfplumber.open(tmp_file_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text()

    # 임시 파일 경로 삭제
    os.remove(tmp_file_path)

    # 벡터 스토어 초기화 (faiss를 이용해 텍스트 벡터화)
    # FAISS는 단순히 텍스트를 벡터로 변환하는 라이브러리입니다.
    # 여기에서는 간단한 임시 벡터화를 위한 예시입니다.
    def embed_text(text):
        # OpenAI API를 사용하여 텍스트를 벡터로 변환 (여기서는 임시로 단순히 텍스트를 벡터화한다고 가정)
        response = client.embeddings.create(
            model="text-embedding-ada-002",  # 텍스트 임베딩 모델
            input=text
        )
        return response['data'][0]['embedding']
    
    # 텍스트를 벡터로 변환
    embedding = embed_text(text)
    
    # FAISS 벡터 스토어 생성 (1차원 벡터 스토어 예시)
    dim = len(embedding)  # 벡터의 차원 크기
    index = faiss.IndexFlatL2(dim)  # L2 거리 기반 인덱스 생성
    faiss_index = faiss.IndexIDMap2(index)  # FAISS 인덱스 생성
    faiss_index.add_with_ids([embedding], [0])  # 벡터와 ID 추가

    # 검색 쿼리 받기
    query = st.text_input("질문을 입력하세요 (PDF에서 검색할 내용):")

    if query:
        # 쿼리 벡터화
        query_embedding = embed_text(query)
        
        # FAISS에서 쿼리와 유사한 벡터 검색
        D, I = faiss_index.search([query_embedding], k=1)  # 가장 유사한 1개 결과 검색
        st.write(f"유사도 점수: {D[0][0]}")  # 유사도 점수 출력
        st.write(f"가장 유사한 텍스트: {text}")  # 유사한 텍스트 출력

# 대화 내역 출력
if 'messages' in st.session_state:
    for message in st.session_state['messages']:
        with st.chat_message(message['role']):
            st.write(message['content'])

# 사용자 입력 받기 (채팅 입력)
prompt = st.chat_input("질문을 입력하세요.")
st.session_state.prompt = prompt

if prompt:
    # 사용자의 메시지를 대화 내역에 추가
    st.session_state['messages'].append({"role": "user", "content": prompt})

    # AI의 응답을 받아오기
    answer = ask_gpt(st.session_state['messages'])

    # AI의 응답을 대화 내역에 추가
    st.session_state['messages'].append({"role": "assistant", "content": answer})
