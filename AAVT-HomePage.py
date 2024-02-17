import os
import toml
import shutil
import streamlit as st
from openai import OpenAI
from utils.utils import (convert_size, cache)


st.set_page_config(
    page_title="AAVT v0.5",
    page_icon="🎞️",
    layout="wide",  # 设置布局样式为宽展示
    initial_sidebar_state="expanded"  # 设置初始边栏状态为展开
)


project_dir = os.path.dirname(os.path.abspath(__file__)).replace("\\", "/")
log_dir = project_dir + "/public/log.md"  # 更新日志
read_dir = project_dir + "/public/README.md"  # 项目文档
config_dir = project_dir + "/config/"  # 配置文件
cache_dir = project_dir + "/pages/cache/"  # 本地缓存

with open(read_dir, 'r', encoding='utf-8') as file:
    markdown_content = file.read()

config = toml.load(config_dir + "config.toml")  # 加载配置
st.session_state.openai_key = config["GPT"]["openai_key"]
st.session_state.openai_base = config["GPT"]["openai_base"]

st.title("🖥Chenyme-AAVT Version:0.5")
st.caption("POWERED BY @CHENYME")

tab1, tab2, tab3 = st.tabs(["主页", "设置", "关于"])
with tab1:  # 主界面功能
    messages = st.container(height=500)
    if "messages" not in st.session_state:
        st.session_state["messages"] = [{"role": "assistant", "content": "我是本项目的AI小助手，有什么可以帮你的么?"}]

    for msg in st.session_state.messages:
        messages.chat_message(msg["role"]).write(msg["content"])

    if prompt := st.chat_input():
        client = OpenAI(api_key=st.session_state.openai_key)
        st.session_state.messages.append({"role": "user", "content": prompt})
        messages.chat_message("user").write(prompt)
        response = client.chat.completions.create(model="gpt-3.5-turbo", messages=[{"role": "system", "content": "你是一个基于下面内容的AI小助手，请基于下面的内容和自己的知识回答用户问题。" + markdown_content},
                                                                                   {"role": "user", "content": prompt}])
        msg = response.choices[0].message.content
        st.session_state.messages.append({"role": "assistant", "content": msg})
        messages.chat_message("assistant").write(msg)

with tab2:
    openai_api_key = config["GPT"]["openai_key"]
    openai_api_base = config["GPT"]["openai_base"]
    kimi_api_key = config["KIMI"]["kimi_key"]
    whisper_version = config["WHISPER"]["whisper_version_default"]
    whisper_model = config["WHISPER"]["whisper_model_default"]

    # Whisper模型
    st.write("#### Whisper识别设置")
    st.write("长视频推荐使用Faster-whisper和large模型获得最佳断句、识别体验。")
    w_version_d = {'openai-whisper': 0, 'faster-whisper': 1}
    w_model_d = {'tiny': 0, 'base': 1, 'small': 2, 'medium': 3, 'large': 4}
    w_version = st.selectbox('选择whisper版本', ('openai-whisper', 'faster-whisper'),
                             index=w_version_d[whisper_version])
    w_model_option = st.selectbox('选择识别模型', ('tiny', 'base', 'small', 'medium', 'large'),
                                  index=w_model_d[whisper_model])

    if w_version != whisper_version:
        config["WHISPER"]["whisper_version_default"] = w_version
        with open(config_dir + '/config.toml', 'w', encoding='utf-8') as file:
            toml.dump(config, file)

        st.success("默认版本已切换为：" + w_version)
    if w_model_option != whisper_model:
        config["WHISPER"]["whisper_model_default"] = w_model_option
        with open(config_dir + '/config.toml', 'w', encoding='utf-8') as file:
            toml.dump(config, file)
        st.success("默认模型已切换为：" + w_model_option)
    st.write('------')

    # OPENAI账户
    st.write("#### 翻译设置")
    st.write("##### KIMI账户设置")
    new_kimi_key = st.text_input("KIMI-API-KEY：")
    st.write("##### OPENAI账户设置")
    proxy_on = st.toggle('启用代理', help='如果你能直接访问openai.com，则无需启用。')
    new_openai_key = st.text_input("OPENAI-API-KEY：")
    new_openai_base = st.text_input("OPENAI-API-BASE：")

    if st.button("保存"):
        if new_kimi_key != kimi_api_key and new_kimi_key != "":
            config["KIMI"]["kimi_key"] = new_kimi_key
            kimi_api_key = new_kimi_key
        if new_openai_base != openai_api_base and new_openai_base != "":
            config["GPT"]["openai_base"] = new_openai_base
            openai_api_base = new_openai_base
        if new_openai_key != openai_api_key and new_openai_key != "":
            config["GPT"]["openai_key"] = new_openai_key
            openai_api_key = new_openai_key
        with open(config_dir + "config.toml", 'w', encoding='utf-8') as file:
            toml.dump(config, file)
        st.success("已保存")
    st.write('------')

    # 本地缓存
    st.write("#### 本地缓存")
    st.write(f"本地缓存已占用：{convert_size(cache(cache_dir))}")
    if st.button("清除本地缓存"):
        # 获取文件夹内所有文件的列表
        file_list = os.listdir(cache_dir)
        if not file_list:
            st.error("无本地缓存文件。")
        else:
            # 遍历列表中的文件，并删除每个文件
            for file_name in file_list:
                file_path = os.path.join(cache_dir, file_name)
                print('已删除文件夹:\n' + file_path)
                shutil.rmtree(file_path)
            st.success("所有缓存文件已成功删除。")

    st.session_state.openai_base = openai_api_base
    st.session_state.openai_key = openai_api_key
    st.session_state.kimi_key = kimi_api_key
    st.session_state.proxy_on = proxy_on
    st.session_state.w_model_option = w_model_option
    st.session_state.w_name = w_version

with tab3:
    with open(log_dir, 'r', encoding='utf-8') as file:
        markdown_log = file.read()
    st.write(markdown_log)
    st.caption('由本地log.md读取加载')
    st.write('')
    st.write('')
    st.write('')
    st.write('')
    st.write('')
    st.write('')
    st.write(markdown_content)
    st.caption('由本地README.md读取加载')