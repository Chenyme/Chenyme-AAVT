# 作者：chenyme
# 版本：v0.2
# 博客站：http://47.113.202.149:8090/

import streamlit as st
import whisper
from utils.utils import generate_srt_from_result, tmp_filepath, openai_translate
from config.config import openai_key, openai_url
from cache.use import srt_mv

st.set_page_config(
    page_title="AAMT v0.2",
    page_icon="📊",
    layout="wide",  # 设置布局样式为宽展示
    initial_sidebar_state="expanded"  # 设置初始边栏状态为展开
)

st.title("AAMT")
st.write("##### AI全自动视频翻译")

with st.sidebar:
    st.title("欢迎！")
    st.write('''
    ### 尊敬的用户，恭喜你完成了该项目的安装！
    欢迎您使用AAMT V0.2！本项目的目标是为您提供一个简单易用的全自动视频翻译工具，以便您能够快速地识别视频声音并生成字幕文件，将翻译后的字幕与原视频合并，从而更轻松地享受翻译后的内容。
    请注意以下事项：
    1. 请确保您的系统已正确安装Python，并且版本号为3.8或更高。
    2. 请确保已经安装了所有依赖库，并设置了ffmpeg为环境变量。
    3. 如果在安装或运行过程中遇到任何问题，请查阅项目文档或联系开发人员以获取帮助。
    ''')

tab1, tab2, tab3 = st.tabs(["主页", "设置", "关于"])

with tab1:
    # 文件上传逻辑
    uploaded_file = st.file_uploader("请在这里上传视频：", type=['mp4', 'mov'])
    if uploaded_file is not None:
        with open("uploaded.mp4", "wb") as file:
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
                with open("output.srt", 'w', encoding='utf-8') as srt_file:  # 将SRT内容写入SRT文件
                    srt_file.write(srt_content)
                srt_mv()

            if st.download_button(
                    label="Click to Download SRT",
                    data=srt_content.encode('utf-8'),
                    key='srt_download',
                    file_name='output.srt',
                    mime='text/srt',
            ):
                st.success("下载成功")

            video_file = open("output.mp4", 'rb')
            video_bytes = video_file.read()
            st.video(video_bytes)
        else:
            st.error("请先上传视频！")

# 全局设置
with tab2:
    st.write("### OPENAI设置")
    base = st.text_input("OPENAI-API-BASE：")
    key = st.text_input("OPENAI-API-KEY：")
    option = st.selectbox('选择你要使用的识别模型（默认：base）', ('tiny', 'base', 'small', 'medium', 'large'), index=1)
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

    st.session_state.base = openai_api_base
    st.session_state.key = openai_api_key
    st.session_state.option = option

with tab3:
    st.write('''
    ## 版本0.2 更新日志
    
    ### 界面优化
    
    - 优化了用户界面，提供更清晰的使用界面。
    - 改进了布局和标题栏以提高导航体验。
    
    ### 视频存储逻辑更新
    
    - 重新编写了视频存储逻辑，便于项目缓存的存放。
    - 改进了代码中的函数库存储与调用。
    
    ### 代码优化
    
    - 对核心代码进行了优化，提高了性能和稳定性。
    - 修复了已知的问题，改进了应用程序的整体可靠性。
    
    ### 新增全局设置界面
    
    - 引入了全局设置界面，使用户可以更新OPENAI配置和Whisper模型参数。

    ### 新增关于界面
    
    - 新增关于界面，展示应用程序的版本信息。
    
    我们感谢您的持续支持和反馈，这个版本的发布是我们不断改进和发展的一部分。如果您有任何问题、建议或反馈，请随时联系。
    谢谢您的支持
    ''')