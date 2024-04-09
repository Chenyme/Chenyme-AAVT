import os
import toml
import shutil
import streamlit as st
from openai import OpenAI
from utils.utils import (convert_size, cache)


st.set_page_config(
    page_title="AAVT v0.6.3",
    page_icon="🎞️",
    layout="wide",  # 设置布局样式为宽展示
    initial_sidebar_state="expanded"  # 设置初始边栏状态为展开
)


project_dir = os.path.dirname(os.path.abspath(__file__)).replace("\\", "/")
log_dir = project_dir + "/public/log.md"  # 更新日志
read_dir = project_dir + "/public/README.md"  # 项目文档
model_dir = project_dir + "/models"  # 模型目录
config_dir = project_dir + "/config/"  # 配置文件
cache_dir = project_dir + "/pages/cache/"  # 本地缓存

with open(read_dir, 'r', encoding='utf-8') as file:
    markdown_content = file.read()
    

st.title("🖥Chenyme-AAVT V0.6.3")
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
    config = toml.load(config_dir + "config.toml")  # 加载配置
    openai_api_key = config["GPT"]["openai_key"]
    st.session_state.openai_key = openai_api_key  # 缓存key
    openai_api_base = config["GPT"]["openai_base"]
    kimi_api_key = config["KIMI"]["kimi_key"]
    whisper_version = config["WHISPER"]["whisper_version_default"]  # whisper配置
    faster_whisper_model = config["WHISPER"]["faster_whisper_model_default"]  # faster_whisper配置
    faster_whisper_model_local = config["WHISPER"]["faster_whisper_model_local"]
    faster_whisper_local_path = config["WHISPER"]["faster_whisper_model_local_path"]
    openai_whisper_model = config["WHISPER"]["openai_whisper_model_default"]  # openai_whisper配置
    
    options = {'openai-whisper': {'version': 0, 'models': {'tiny': 0, 'base': 1, 'small': 2, 'medium': 3, 'large': 4}},
               'faster-whisper': {'version': 1, 'models': {'tiny': 0, 'tiny.en': 1, 'base': 2, 'base.en': 3, 'small': 4,
                                                           'small.en': 5, 'medium': 6, 'medium.en': 7, 'large-v1': 8,
                                                           'large-v2': 9, 'large-v3': 10, 'large': 11, 'distil-small.en': 12,
                                                           'distil-medium.en': 13, 'distil-large-v2': 14}}}

    # Whisper模型
    st.write("#### Whisper识别设置")
    st.write("```推荐使用 Faster-whisper和large（或distil-large-v2）模型获得最佳断句、识别体验！！！```")
    st.write("```请注意distil系列模型不支持GPU加速，但该系列模型本身比其他的模型快约6倍，请勿使用GPU加速！！！```")
    w_local = st.toggle('启用本地加载模型', faster_whisper_model_local)
    config["WHISPER"]["faster_whisper_model_local"] = w_local

    if w_local == 0:
        w_version_option = st.selectbox('选择whisper版本', list(options.keys()), index=options[whisper_version]['version'])
        if w_version_option == "openai-whisper":
            model_index = options[w_version_option]['models'][openai_whisper_model]
            w_model_option = st.selectbox('选择识别模型', list(options[w_version_option]['models'].keys()),
                                          index=model_index)
            config["WHISPER"]["openai_whisper_model_default"] = w_model_option
        else:
            model_index = options[w_version_option]['models'][faster_whisper_model]
            w_model_option = st.selectbox('选择识别模型', list(options[w_version_option]['models'].keys()),
                                          index=model_index)
            config["WHISPER"]["faster_whisper_model_default"] = w_model_option

        config["WHISPER"]["whisper_version_default"] = w_version_option
    else:
        w_version_option = st.selectbox('选择whisper版本', list(options.keys()), index=1, disabled=1)
        model_names = os.listdir(model_dir)
        wlm_option = st.selectbox('选择本地模型', model_names)
        w_local_model_path = model_dir + '/' + wlm_option
        config["WHISPER"]["faster_whisper_model_local_path"] = w_local_model_path

    with open(config_dir + '/config.toml', 'w', encoding='utf-8') as file:
        toml.dump(config, file)

    st.write('------')

    # OPENAI账户
    st.write("#### 翻译设置")
    st.write("##### KIMI账户设置")
    st.write('''```Kimi 是由月之暗面（Moonshot AI）团队的超长记忆 AI 助手。官网：https://www.moonshot.cn/```''')
    new_kimi_key = st.text_input("KIMI-API-KEY：")
    st.write("##### OPENAI账户设置")
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
        with open(config_dir + "/config.toml", 'w', encoding='utf-8') as file:
            toml.dump(config, file)
        st.session_state.openai_key = new_openai_key
        st.success("已保存")
    st.write('------')

    # 本地缓存
    st.write("#### 本地缓存")
    st.write(f"本地缓存已占用：{convert_size(cache(cache_dir))}")
    if st.button("清除本地缓存"):
        if not os.listdir(cache_dir):
            st.error("无本地缓存文件。")
        else:
            for root, dirs, files in os.walk(cache_dir):
                for file in files:
                    os.remove(os.path.join(root, file))
                for adir in dirs:
                    shutil.rmtree(os.path.join(root, adir))
            st.success("所有缓存文件已成功删除。")

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