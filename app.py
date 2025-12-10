import streamlit as st
from openai import OpenAI
import os

# 从环境变量安全读取（强烈推荐，Key 不写死在代码里）
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),           # Vercel 环境变量填这里
    base_url="https://openrouter.ai/api/v1"        # 用 OpenRouter 代理最稳（可选直连 https://api.openai.com/v1 也行）
)

assistant_id = os.getenv("ASSISTANT_ID", "asst_0xmUolnfgXKtSVx5bvEXwBKc")  # 可从环境变量读，默认你的ID

st.set_page_config(page_title="阿Ken ST2U 专业 AI", page_icon="💹")
st.title("阿Ken ST2U 专业 AI 分身")
st.caption("投资 | 销售 | AI工具 | 教育内容，非投资建议")

# 初始化对话线程
if "thread_id" not in st.session_state:
    thread = client.beta.threads.create()
    st.session_state.thread_id = thread.id

# 用户输入
if prompt := st.chat_input("问 ST2U、股票、销售技巧？"):
    with st.chat_message("user"):
        st.markdown(prompt)

    # 发送给你的 Assistant
    client.beta.threads.messages.create(
        thread_id=st.session_state.thread_id,
        role="user",
        content=prompt
    )
    run = client.beta.threads.runs.create(
        thread_id=st.session_state.thread_id,
        assistant_id=assistant_id
    )

    # 等待回复
    with st.chat_message("assistant").write("思考中...")
    with st.chat_message("assistant"):
        with st.spinner(""):
            while run.status not in ["completed", "failed", "cancelled"]:
                run = client.beta.threads.runs.retrieve(
                    thread_id=st.session_state.thread_id,
                    run_id=run.id
                )
            if run.status == "completed":
                messages = client.beta.threads.messages.list(thread_id=st.session_state.thread_id)
                response = messages.data[0].content[0].text.value
                st.markdown(response)
            else:
                st.error("AI 思考失败，请重试")

# Vercel 必须的启动方式（重点！）
if __name__ == "__main__":
    import streamlit.web.bootstrap as bootstrap
    bootstrap.run("app.py", is_hello=False, args=[], flag_options={})
