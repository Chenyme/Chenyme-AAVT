# 作者：chenyme
# 版本：v0.4
# 博客站：待更新

import os
import toml
import torch
import shutil
import datetime
import streamlit as st
from utils.utils import (aavt_chatbot, get_whisper_result, kimi_translate, openai_translate1, openai_translate2,
                         generate_srt_from_result, srt_mv, srt_to_vtt, srt_to_ass, srt_to_stl, show_video,
                         parse_srt_file, convert_size, cache)

project_dir = os.path.dirname(os.path.abspath(__file__)).replace("\\", "/")
log_dir = project_dir + "/public/log.md"  # 更新日志
read_dir = project_dir + "/public/README.md"  # 项目文档
config_dir = project_dir + "/config/"  # 配置文件
cache_dir = project_dir + "/cache/"  # 本地缓存

with open('public/README.md', 'r', encoding='utf-8') as file:
    markdown_content = file.read()
config = toml.load("config/config.toml")  # 加载配置
st.session_state.openai_key = config["GPT"]["openai_key"]
st.session_state.openai_base = config["GPT"]["openai_base"]

st.set_page_config(
    page_title="AAVT v0.4",
    page_icon="🎞️",
    layout="wide",  # 设置布局样式为宽展示
    initial_sidebar_state="expanded"  # 设置初始边栏状态为展开
)
st.title("AI全自动视频翻译🎞️")

tab1, tab2, tab3 = st.tabs(["主页", "设置", "关于"])

with st.sidebar:  # 侧边栏功能
    st.title("POWERED BY @CHENYME")
    st.caption("🖥Chenyme-AAVT Version：0.4")
    st.write(
        "恭喜你成功启动了AAVT项目！请先前往设置页面配置环境，同时确保按照步骤安装好所有依赖环境和库，以保证项目稳定运行！")

    sidebar_chat = st.container(border=True, height=500)
    sidebar_chat.caption("🚀 A ChatBot Based on OpenAI LLM")
    sidebar_chat_prompt = st.text_input("输入您的问题",
                                        help="这是基于 `gpt-3.5-turbo` 的AI助手，你可以问任何问题，按 `Enter` 以发送，为了节省Token，相同的问题会被缓存，您可以在右上角设置中点击 `Clear Cahce` 清楚缓存并重新提问。")

    if "messages" not in st.session_state:
        st.session_state["messages"] = [
            {"role": "assistant", "content": "欢迎来到AAVT v0.4，我是AI助手，您可以随时向我发起提问！"}]
    for msg in st.session_state.messages:
        sidebar_chat.chat_message(msg["role"]).write(msg["content"])

    if sidebar_chat_prompt != '':
        msg = aavt_chatbot(markdown_content, sidebar_chat_prompt, st.session_state.openai_key,
                           st.session_state.openai_base)
        sidebar_chat.chat_message("user").write(sidebar_chat_prompt)
        sidebar_chat.chat_message("assistant").write(msg)

with tab1:  # 主界面功能

    col1, col2 = st.columns(2, gap="medium")
    with col1:
        # 文件上传
        uploaded_file = st.file_uploader("请在这里上传视频：", type=['mp4', 'mov'])
        if uploaded_file is not None:
            st.success("上传成功")

        # GPU加速
        wdc = not torch.cuda.is_available()
        GPU_on = st.toggle('启用GPU加速*', disabled=wdc, help='请确保您正确安装了cuda、pytorch，否则该选项开启无效！')
        device = 'cuda' if GPU_on else 'cpu'

        # 翻译模型
        translate_option = st.selectbox('请在这里选择翻译模型：', ('kimi', 'gpt-3.5-turbo', 'gpt-4', '无需翻译'),
                                        index=0)
        if translate_option != '无需翻译':
            col3, col4 = st.columns(2)
            with col3:
                language1 = st.selectbox('原始语言', ('中文', 'English', '日本語', '한국인', 'Italiano', 'Deutsch'),
                                         index=1)
            with col4:
                language2 = st.selectbox('目标语言', ('中文', 'English', '日本語', '한국인', 'Italiano', 'Deutsch'),
                                         index=0)
            if st.button('运行程序'):
                if uploaded_file is not None:
                    with st.spinner('正在加载视频缓存...'):
                        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H-%M-%S")
                        output_file = cache_dir + current_time
                        os.makedirs(output_file)
                        with open(output_file + "/uploaded.mp4", "wb") as file:
                            file.write(uploaded_file.getbuffer())

                    with st.spinner('正在识别视频内容...'):
                        # whisper识别
                        result = get_whisper_result(uploaded_file, output_file, device, st.session_state.w_model_option,
                                                    st.session_state.w_name)
                        print("whisper识别：" + result['text'])

                    with st.spinner('正在翻译文本...'):
                        if translate_option == 'kimi':
                            result = kimi_translate(st.session_state.kimi_key, result, language1,
                                                    language2)  # 使用kimi翻译成目标语言
                        elif translate_option == 'gpt-3.5-turbo':
                            result = openai_translate1(st.session_state.openai_key, st.session_state.openai_base, st.session_state.proxy_on,
                                                       result, language1, language2)  # 使用gpt3.5翻译成目标语言
                        elif translate_option == 'gpt-4':
                            result = openai_translate2(st.session_state.openai_key, st.session_state.openai_base, st.session_state.proxy_on,
                                                       result, language1, language2, )  # 使用gpt4翻译成目标语言

                    with st.spinner('正在生成SRT字幕文件...'):
                        srt_content = generate_srt_from_result(result)  # 生成SRT字幕内容
                        with open(output_file + "/output.srt", 'w', encoding='utf-8') as srt_file:  # 将SRT内容写入SRT文件
                            srt_file.write(srt_content)

                    with st.spinner('正在合并视频，请耐心等待视频生成...'):
                        srt_mv(output_file)

                    st.session_state.srt_content = srt_content
                    st.session_state.output = output_file
                else:
                    st.warning("请先上传视频")

        elif translate_option == '无需翻译':
            if st.button('运行程序'):
                if uploaded_file is not None:
                    with st.spinner('正在加载视频缓存...'):
                        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H-%M-%S")
                        output_file = cache_dir + current_time
                        os.makedirs(output_file)
                        with open(output_file + "/uploaded.mp4", "wb") as file:
                            file.write(uploaded_file.getbuffer())

                    with st.spinner('正在识别视频内容...'):
                        # whisper识别
                        result = get_whisper_result(uploaded_file, cache_dir, device, st.session_state.w_model_option,
                                                    st.session_state.w_name)

                        print("whisper识别：" + result['text'])

                    with st.spinner('正在生成SRT字幕文件...'):
                        srt_content = generate_srt_from_result(result)  # 生成SRT字幕内容
                        with open(output_file + "/output.srt", 'w', encoding='utf-8') as srt_file:  # 将SRT内容写入SRT文件
                            srt_file.write(srt_content)

                    with st.spinner('正在合并视频，请耐心等待视频生成...'):
                        srt_mv(output_file)

                    st.session_state.srt_content = srt_content
                    st.session_state.output = output_file
                else:
                    st.warning("请先上传视频")

    with col2:
        c = st.container(border=True, height=500)
        c.write('预览和下载（Preview & Download）')
        captions_option = c.radio('下载的字幕格式：', ('srt', 'vtt', 'ass', 'stl'), index=0, horizontal=True)
        try:
            if captions_option == 'srt':
                c.download_button(
                    label="点击下载SRT字幕文件",
                    data=st.session_state.srt_content.encode('utf-8'),
                    key='srt_download',
                    file_name='output.srt',
                    mime='text/srt',
                )
            elif captions_option == 'vtt':
                vtt_content = srt_to_vtt(st.session_state.srt_content)
                c.download_button(
                    label="点击下载VTT字幕文件",
                    data=vtt_content.encode('utf-8'),
                    key='vtt_download',
                    file_name='output.vvt',
                    mime='text/vtt',
                )
            elif captions_option == 'ass':
                ass_content = srt_to_ass(st.session_state.srt_content)
                c.download_button(
                    label="点击下载ASS字幕文件",
                    data=ass_content.encode('utf-8'),
                    key='ass_download',
                    file_name='output.ass',
                    mime='text/ass',
                )
            elif captions_option == 'stl':
                stl_content = srt_to_stl(st.session_state.srt_content)
                c.download_button(
                    label="点击下载STL字幕文件",
                    data=stl_content.encode('utf-8'),
                    key='stl_download',
                    file_name='output.stl',
                    mime='text/stl',
                )

        except:
            c.warning('这里是预览窗口，运行后自动显示预览结果。')

        try:
            video_bytes = show_video(st.session_state.output)
            c.video(video_bytes)
        except:
            c.write('')

    st.write('''
    ------
    ##### 实验功能🧪
    ''')
    st.caption("运行程序后自动显示，实际可能会有BUG，后续版本会逐步完善并实装！")
    try:
        srt_data = parse_srt_file(st.session_state.srt_content)
        edited_data = st.data_editor(srt_data, height=300, hide_index=True)

        if edited_data is not None:
            st.write('编辑后的数据：')
            st.dataframe(edited_data, height=300, hide_index=True)
    except:
        st.write('')

with tab2:
    openai_api_key = config["GPT"]["openai_key"]
    openai_api_base = config["GPT"]["openai_base"]
    kimi_api_key = config["KIMI"]["kimi_key"]
    whisper_version = config["WHISPER"]["whisper_version_default"]
    whisper_model = config["WHISPER"]["whisper_model_default"]

    # Whisper模型
    st.write("#### Whisper识别设置")
    w_version_d = {'openai-whisper': 0, 'faster-whisper': 1}
    w_model_d = {'tiny': 0, 'base': 1, 'small': 2, 'medium': 3, 'large': 4}
    w_version = st.selectbox('选择whisper版本', ('openai-whisper', 'faster-whisper'),
                             index=w_version_d[whisper_version])
    w_model_option = st.selectbox('选择识别模型', ('tiny', 'base', 'small', 'medium', 'large'),
                                  index=w_model_d[whisper_model])

    if w_version != whisper_version:
        config["WHISPER"]["whisper_version_default"] = w_version
        with open(config_dir + '/config.toml', 'w') as file:
            toml.dump(config, file)
        st.success("默认版本已切换为：" + w_version)
    if w_model_option != whisper_model:
        config["WHISPER"]["whisper_model_default"] = w_model_option
        with open(config_dir + '/config.toml', 'w') as file:
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
        with open(config_dir + "config.toml", 'w') as file:
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
