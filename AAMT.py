# 作者：chenyme
# 版本：v0.2.1
# 博客站：http://47.113.202.149:8080/

import os
import streamlit as st
import whisper
from utils.utils import generate_srt_from_result, tmp_filepath, openai_translate, srt_mv, cache, convert_size
from config.config import openai_key, openai_url

st.set_page_config(
    page_title="AAMT v0.2.1",
    page_icon="📊",
    layout="wide",  # 设置布局样式为宽展示
    initial_sidebar_state="expanded"  # 设置初始边栏状态为展开
)

st.title("Chenyme-AAMT")
st.write("##### AI全自动视频翻译")

with st.sidebar:
    st.title("欢迎！")
    st.write('''
    ### 尊敬的用户，恭喜你完成了该项目的安装！
    欢迎您使用AAMT V0.2.1！本项目的目标是为您提供一个简单易用的全自动视频翻译工具，以便您能够快速地将翻译后的字幕与原视频合并，从而更轻松地享受翻译后的内容。
    请注意以下事项：
    1. 请确保您的系统已正确安装Python，并且版本号为3.8或更高。
    2. 请确保已经安装了所有依赖库，并设置了ffmpeg为环境变量。
    3. 如果在安装或运行过程中遇到任何问题，请查阅项目文档或联系开发人员以获取帮助。
    ''')

dir_now = os.path.dirname(os.path.abspath(__file__))
cache_dir = dir_now + "/cache/"
cache_dir = cache_dir.replace("\\", "/")
print("当前项目的缓存位置：", cache_dir)

tab1, tab2, tab3 = st.tabs(["主页", "设置", "关于"])

with tab1:
    # 文件上传逻辑
    uploaded_file = st.file_uploader("请在这里上传视频：", type=['mp4', 'mov'])
    if uploaded_file is not None:
        with open(cache_dir + "uploaded.mp4", "wb") as file:
            file.write(uploaded_file.getbuffer())
        st.success("上传成功")

    if st.button('运行程序'):
        if uploaded_file is not None:
            with st.spinner('Wait for it...'):
                # whisper识别
                model = whisper.load_model(st.session_state.option)
                pathvideo = tmp_filepath(uploaded_file)
                result = model.transcribe(pathvideo)
                print("whisper识别：" + result['text'])  # whisper源语言识别内容
                result = openai_translate(st.session_state.key, st.session_state.base, result)  # 翻译成目标语言
                srt_content = generate_srt_from_result(result)  # 生成SRT字幕内容
                with open(cache_dir + "output.srt", 'w', encoding='utf-8') as srt_file:  # 将SRT内容写入SRT文件
                    srt_file.write(srt_content)
                srt_mv(cache_dir)

            if st.download_button(
                    label="Click to Download SRT",
                    data=srt_content.encode('utf-8'),
                    key='srt_download',
                    file_name=cache_dir + 'output.srt',
                    mime='text/srt',
            ):
                st.success("下载成功")

            video_file = open(cache_dir + "output.mp4", 'rb')
            video_bytes = video_file.read()
            st.video(video_bytes)
        else:
            st.error("请先上传视频！")

# 全局设置
with tab2:
    st.write("### Whisper识别设置")
    option = st.selectbox('选择你要使用的识别模型（默认：base）', ('tiny', 'base', 'small', 'medium', 'large'), index=1)
    st.write("### OPENAI设置")
    base = st.text_input("OPENAI-API-BASE：")
    key = st.text_input("OPENAI-API-KEY：")
    openai_api_key = openai_key
    openai_api_base = openai_url

    if st.button("保存"):
        # 设置
        if base != openai_api_base and base != "":
            openai_api_base = base
        else:
            openai_api_base = openai_api_base

        if key != openai_api_key and key != "":
            openai_api_key = key
        else:
            openai_api_key = openai_api_key
        st.success("已保存")

    st.write("### 本地缓存")
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

    st.session_state.base = openai_api_base
    st.session_state.key = openai_api_key
    st.session_state.option = option

with tab3:
    st.write('''
    ### 版本 0.2.1 更新日志
    ---
    #### 修复的问题
    
    - install.bat中增加了openai的依赖库。
    - 修复了缓存位置错乱的 bug，现在您的项目缓存将被正确管理。
    - 现在支持识别项目本地缓存的大小，帮助您更好地了解和管理您的数据。
    - 引入了一键清除本地缓存功能，让您可以轻松地释放磁盘空间。
    - 修复了设置界面中 OPENAI 设置和 Whisper 设置错位的 bug，确保设置选项的可用性和正确性。
    
    #### 感谢您的反馈
    
    我们要特别感谢您的反馈和支持，这些改进和修复都是基于您的建议和需求而来的。我们一直致力于不断提升 Chenyme-AAMT 的质量和功能，以满足您的期望。
    
    如果您有任何问题、建议或反馈，请随时联系我们。我们期待听到您的声音，以便不断改进我们的应用程序。
    
    祝您愉快地使用 Chenyme-AAMT！
    
    谢谢您的支持
    
    ''')
