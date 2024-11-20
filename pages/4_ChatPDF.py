import streamlit as st
from langchain.document_loaders import PyPDFLoader
from langchain.vectorstores import FAISS
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.chains import RetrievalQA
import os
import faiss
import tempfile

# OpenAI API 호출을 위한 캐시 함수
@st.cache_data
def ask_gpt(messages):
    client = st.session_state['openai_client']  # 세션에서 OpenAI 클라이언트 가져오기
    response = client.chat.completions.create(
        model="gpt-4",  # 적절한 모델을 사용 (예: gpt-4)
        messages=messages  # 대화 메시지를 모델에 전달
    )
    return response.choices[0].message.content  # 모델의 응답 내용을 반환

# OpenAI 클라이언트 초기화
client = st.session_state.get('openai_client', None)  # 세션에서 OpenAI 클라이언트를 가져옴
if client is None:
    if st.button("API Key를 입력하세요."):  # API 키를 입력하라는 버튼
        st.switch_page("pages/1_Setting.py")  # API 키 입력 페이지로 이동
    st.stop()  # 클라이언트가 없으면 실행을 멈춤

st.header("Ask GPT with PDF Search")  # 페이지 제목

# 대화 내역을 세션 상태에 저장
if 'messages' not in st.session_state:  # 대화 내역이 없으면 초기화
    st.session_state['messages'] = []

# 대화 내역 초기화 버튼
if st.button('Clear'):
    st.session_state['messages'] = []  # 대화 내역 초기화
    st.experimental_rerun()  # 페이지를 새로고침하여 초기 상태로 되돌림

# 대화창 나가기 버튼
if st.button('대화창 나가기'):
    st.session_state['messages'] = []  # 대화 내역 초기화
    st.session_state['openai_client'] = None  # OpenAI 클라이언트 정보 삭제
    st.experimental_rerun()  # 페이지 새로고침

# PDF 파일 업로드 (하나의 파일만 받기)
uploaded_file = st.file_uploader("PDF 파일을 업로드하세요.", type=["pdf"])

# 파일 업로드 후 벡터 스토어 초기화 또는 로드
if uploaded_file:
    with tempfile.NamedTemporaryFile(delete=False) as tmp_file:  # 임시 파일 생성
        tmp_file.write(uploaded_file.read())  # 업로드된 파일 내용을 임시 파일에 저장
        tmp_file_path = tmp_file.name  # 임시 파일 경로 저장

    # PDF 파일을 PyPDFLoader로 로드하여 내용 추출
    loader = PyPDFLoader(tmp_file_path)
    documents = loader.load()  # PDF에서 문서 내용 불러오기

    # OpenAI 임베딩을 사용하여 벡터 스토어 생성
    embeddings = OpenAIEmbeddings()
    vector_store = FAISS.from_documents(documents, embeddings)  # 문서로부터 벡터 스토어 생성

    # 벡터 스토어 삭제 버튼
    if st.button('Clear Vector Store'):
        if os.path.exists(tmp_file_path):  # 임시 파일이 존재하면 삭제
            os.remove(tmp_file_path)
        vector_store = None  # 벡터 스토어 초기화
        st.session_state['vector_store'] = None  # 세션 상태에서 벡터 스토어 정보 삭제
        st.write("Vector Store has been cleared.")  # 벡터 스토어 삭제 메시지 출력
    
    # PDF 내용에 대해 질문 입력 받기
    query = st.text_input("질문을 입력하세요 (PDF에서 검색할 내용):")

    if query:
        if vector_store:
            # 벡터 스토어에서 검색 쿼리를 처리
            qa_chain = RetrievalQA.from_chain_type(
                llm=client,  # OpenAI 모델 클라이언트를 사용하여 질문 처리
                chain_type="stuff",  # 문서 검색 방법 설정
                retriever=vector_store.as_retriever(search_type="similarity", search_kwargs={"k": 1})  # 유사도 기반 검색 (k=1은 가장 유사한 1개 문서 반환)
            )
            answer = qa_chain.run(query)  # 질문에 대한 답변 실행
            st.write(answer)  # 답변 출력
        else:
            st.write("PDF 파일을 먼저 업로드하고 검색을 시도하세요.")  # 파일이 업로드되지 않으면 안내 메시지 출력

# 이전 대화 내역 출력
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
