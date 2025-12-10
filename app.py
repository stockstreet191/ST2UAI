import streamlit as st
from openai import OpenAI
import os

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url="https://api.openai.com/v1"
)

assistant_id = os.getenv("ASSISTANT_ID")

st.set_page_config(page_title="阿Ken ST2U 专业 AI", page_icon="💹")
st.title("阿Ken ST2U 专业 AI 分身")
st.caption("投资·销售·AI工具 | 教育内容，非投资建议")

if "thread_id" not in st.session_state:
    thread = client.beta.threads.create()
    st.session_state.thread_id = thread.id

if prompt := st.chat_input("问 ST2U、股票、销售技巧？"):
    with st.chat_message("user"):
        st.markdown(prompt)

    client.beta.threads.messages.create(
        thread_id=st.session_state.thread_id,
        role="user",
        content=prompt
    )
    run = client.beta.threads.runs.create(
        thread_id=st.session_state.thread_id,
        assistant_id=assistant_id
    )

    with st.chat_message("assistant"):
        with st.spinner(""):
            while run.status != "completed":
                run = client.beta.threads.runs.retrieve(thread_id=st.session_state.thread_id, run_id=run.id)
            messages = client.beta.threads.messages.list(thread_id=st.session_state.thread_id)
            response = messages.data[0].content[0].text.value
            st.markdown(response)
