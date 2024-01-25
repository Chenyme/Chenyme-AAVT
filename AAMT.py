# 作者：chenyme
# 版本：v0.3
# 博客站：待更新

import os
import json
import streamlit as st
import torch
from openai import OpenAI
from utils.utils import (
    generate_srt_from_result,
    openai_translate1,
    openai_translate2,
    kimi_translate,
    srt_mv,
    cache,
    convert_size,
    whisper_choose,
    parse_srt_file,
    save_srt_file,
)

st.set_page_config(
    page_title="AAMT v0.3",
    page_icon="🎞️",
    layout="wide",  # 设置布局样式为宽展示
    initial_sidebar_state="expanded"  # 设置初始边栏状态为展开
)

st.title("AI全自动视频翻译🎞️")


dir_1 = os.path.dirname(os.path.abspath(__file__))
dir_2 = dir_1.replace("\\", "/")
log_dir = dir_2 + "/public/log.md"
read_dir = dir_2 + "/public/README.md"  # Readme文档
config_dir = dir_2 + "/config/"  # 配置文件
cache_dir = dir_2 + "/cache/"  # 本地缓存
temp_dir = dir_2 + "/cache/"  # 运行缓存
print("当前项目的配置文件位置：", config_dir)
print("当前项目的本地缓存位置：", cache_dir)
SRT = False

with st.sidebar:
    st.title("POWERD BY @CHENYME")
    st.caption("🖥Chenyme-AAMT Version：0.3")
    st.write("------")
    st.write(
        "恭喜你完成了AAMT项目的部署！请先前往设置页面配置环境，同时确保按照步骤安装好所有依赖环境和库，以保证项目稳定运行！")
    with open(read_dir, 'r', encoding='utf-8') as file:
        markdown_content = file.read()
    t = st.container(border=True, height=500)
    if "messages" not in st.session_state:
        st.session_state["messages"] = [{"role": "assistant", "content": markdown_content}]
    t.caption("🚀 A chatbot build with OpenAI LLM")
    for msg in st.session_state.messages:
        t.chat_message(msg["role"]).write("欢迎来到AAMT v0.3，我是AI助手，您可以随时向我发起提问！")

    if prompt := st.text_input("输入您的问题", help="这是基于GPT3.5的AI助手，你可以问任何问题，按Enter以发送"):
        client = OpenAI(api_key=st.session_state.openai_key, base_url=st.session_state.openai_base)
        st.session_state.messages.append({"role": "user", "content": prompt})
        t.chat_message("user").write(prompt)
        response = client.chat.completions.create(model="gpt-3.5-turbo", messages=st.session_state.messages)
        msg = response.choices[0].message.content
        st.session_state.messages.append({"role": "assistant", "content": msg})
        t.chat_message("assistant").write(msg)

with open(config_dir + "config.json", 'r') as file:  # 读取配置
    config = json.load(file)

tab1, tab2, tab3 = st.tabs(["主页", "设置", "关于"])

with tab1:
    col1, col2 = st.columns(2, gap="medium")
    with col1:
        # 文件上传
        uploaded_file = st.file_uploader("请在这里上传视频：", type=['mp4', 'mov'])
        if uploaded_file is not None:
            with open(cache_dir + "uploaded.mp4", "wb") as file:
                file.write(uploaded_file.getbuffer())
            st.success("上传成功")

        # 选择翻译模型
        option = st.selectbox('选择你要使用的翻译模型', ('kimi', 'gpt-3.5-turbo', 'gpt-4', '无需翻译'), index=0)

        # 翻译语种设置
        if option != '无需翻译':
            language1 = st.selectbox('原始语言', ('中文', 'English', '日本語', '한국인', 'Italiano', 'Deutsch'), index=1)
            language2 = st.selectbox('目标语言', ('中文', 'English', '日本語', '한국인', 'Italiano', 'Deutsch'), index=0)

        # GPU加速
        wdc = not torch.cuda.is_available()
        on = st.toggle('启用GPU加速*', disabled=wdc, help='请确保您正确安装了cuda、pytorch，否则该选项开启无效！')
        device = 'cuda' if on else 'cpu'

        if option != '无需翻译':
            with col2:
                c = st.container(border=True, height=500)
                c.write('预览（Preview）')
            if st.button('运行程序'):
                with col2:
                    if uploaded_file is not None:
                        with st.spinner('正在识别视频内容...'):
                            # whisper识别
                            result, path_video = whisper_choose(uploaded_file, temp_dir,
                                                                st.session_state.w_model_option,
                                                                device,
                                                                st.session_state.w_name)
                            os.unlink(path_video)  # 删除缓存文件
                            print("whisper识别：" + result['text'])  # whisper源语言识别内容

                        with st.spinner('正在翻译文本...'):
                            if option == 'kimi':
                                result = kimi_translate(st.session_state.kimi_key, result, language1,
                                                        language2)  # 使用kimi翻译成目标语言
                            elif option == 'gpt-3.5-turbo':
                                result = openai_translate1(st.session_state.openai_key, st.session_state.openai_base,
                                                           result,
                                                           language1, language2)  # 使用gpt3.5翻译成目标语言
                            elif option == 'gpt-4':
                                result = openai_translate2(st.session_state.openai_key, st.session_state.openai_base,
                                                           result,
                                                           language1, language2)  # 使用gpt4翻译成目标语言

                        with st.spinner('正在生成SRT字幕文件...'):
                            srt_content = generate_srt_from_result(result)  # 生成SRT字幕内容
                            with open(cache_dir + "output.srt", 'w', encoding='utf-8') as srt_file:  # 将SRT内容写入SRT文件
                                srt_file.write(srt_content)
                            SRT = True

                        with st.spinner('正在合并视频，请耐心等待视频生成...'):
                            srt_mv(cache_dir)
                        c.success("翻译已完成！")

                        video_file = open(cache_dir + "output.mp4", 'rb')
                        video_bytes = video_file.read()
                        c.video(video_bytes)

                    else:
                        with col1:
                            st.error("请先上传视频！")

        elif option == '无需翻译':
            with col2:
                c = st.container(border=True, height=500)
                c.write('预览（Preview）')

            if st.button('运行程序'):
                with col2:
                    if uploaded_file is not None:
                        with st.spinner('正在识别视频内容...'):
                            # whisper识别
                            result, path_video = whisper_choose(uploaded_file, temp_dir,
                                                                st.session_state.w_model_option,
                                                                device,
                                                                st.session_state.w_name)
                            os.unlink(path_video)  # 删除缓存文件

                        with st.spinner('正在生成SRT字幕文件...'):
                            srt_content = generate_srt_from_result(result)  # 生成SRT字幕内容
                            with open(cache_dir + "output.srt", 'w', encoding='utf-8') as srt_file:  # 将SRT内容写入SRT文件
                                srt_file.write(srt_content)
                            SRT = True

                        with st.spinner('正在合并视频，请耐心等待视频生成...'):
                            srt_mv(cache_dir)
                        c.success("翻译已完成！")

                        video_file = open(cache_dir + "output.mp4", 'rb')
                        video_bytes = video_file.read()
                        c.video(video_bytes)

                    else:
                        with col1:
                            st.error("请先上传视频！")

st.write('''------
##### 实验功能🧪''')
st.caption("运行程序后自动显示，实际可能会有BUG，后续版本会逐步完善并实装！")
file_path = cache_dir + 'output.srt'
if SRT:
    srt_data = parse_srt_file(file_path)
    edited_data = st.data_editor(srt_data, height=300, hide_index=True)

    if edited_data is not None:
        st.write('编辑后的数据：')
        st.write(edited_data)

    with open(cache_dir + 'output.srt', "rb") as file:
        contents = file.read()

    if st.button('保存修改后的SRT'):
        save_srt_file(edited_data, file_path)
        st.write('数据已保存至', file_path)


# 全局设置
with tab2:
    openai_api_key = config["openai_key"]
    openai_api_base = config["openai_base"]
    kimi_api_key = config["kimi_key"]
    whisper_version = config["whisper_version_default"]
    whisper_model = config["whisper_model_default"]

    # Whisper模型
    st.write("#### Whisper识别设置")
    w_version_d = {'openai-whisper': 0, 'faster-whisper': 1}
    w_model_d = {'tiny': 0, 'base': 1, 'small': 2, 'medium': 3, 'large': 4}

    w_version = st.selectbox('选择whisper版本', ('openai-whisper', 'faster-whisper'),
                             index=w_version_d[whisper_version])
    w_model_option = st.selectbox('选择识别模型', ('tiny', 'base', 'small', 'medium', 'large'),
                                  index=w_model_d[whisper_model])

    if w_model_option != whisper_model:
        config["whisper_model_default"] = w_model_option
        with open(config_dir + "config.json", 'w') as file:
            json.dump(config, file, indent=4)
        st.success("默认模型已切换为：" + w_model_option)

    if w_version != whisper_version:
        config["whisper_version_default"] = w_version
        with open(config_dir + "config.json", 'w') as file:
            json.dump(config, file, indent=4)
        st.success("默认版本已切换为：" + w_version)

    st.write('------')
    # OPENAI账户
    st.write("#### 翻译设置")
    st.write("###### KIMI账户设置")
    new_kimi_key = st.text_input("KIMI-API-KEY：")
    st.write("###### OPENAI账户设置")
    new_openai_base = st.text_input("OPENAI-API-BASE：")
    new_openai_key = st.text_input("OPENAI-API-KEY：")

    if st.button("保存"):
        if new_kimi_key != kimi_api_key and new_kimi_key != "":
            config["kimi_key"] = new_kimi_key
            kimi_api_key = new_kimi_key
        if new_openai_base != openai_api_base and new_openai_base != "":
            config["openai_key"] = new_openai_key
            openai_api_key = new_openai_key
        if new_openai_key != openai_api_key and new_openai_key != "":
            config["openai_base"] = new_openai_base
            openai_api_base = new_openai_base
        with open(config_dir + "config.json", 'w') as file:
            json.dump(config, file, indent=4)
        st.success("已保存")

    st.write('------')
    # 本地缓存
    st.write("#### 本地缓存")
    st.write(f"本地缓存已占用：{convert_size(cache(cache_dir))}")
    if st.button("清除本地缓存"):
        # 获取文件夹内所有文件的列表
        file_list = os.listdir(cache_dir)
        # 遍历列表中的文件，并删除每个文件
        for file_name in file_list:
            file_path = os.path.join(cache_dir, file_name)
            if os.path.isfile(file_path):
                os.remove(file_path)
        st.success("所有缓存文件已成功删除。")

    st.session_state.openai_base = openai_api_base
    st.session_state.openai_key = openai_api_key
    st.session_state.kimi_key = kimi_api_key
    st.session_state.w_model_option = w_model_option
    st.session_state.w_name = w_version

with tab3:
    with open(log_dir, 'r', encoding='utf-8') as file:
        markdown_log = file.read()
    st.write(markdown_log)
    st.caption('由本地log.md读取加载')
    st.write(markdown_content)
    st.caption('由本地README.md读取加载')
