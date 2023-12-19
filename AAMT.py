# 作者：chenyme
# 版本：v0.2.2
# 博客站：待更新

import os
import json
import streamlit as st
import whisper
from utils.utils import generate_srt_from_result, tmp_filepath, openai_translate, srt_mv, cache, convert_size

st.set_page_config(
    page_title="AAMT v0.2.2",
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
    欢迎您使用AAMT V0.2.2！本项目的目标是为您提供一个简单易用的全自动视频翻译工具，以便您能够快速地将翻译后的字幕与原视频合并，从而更轻松地享受翻译后的内容。
    请注意以下事项：
    1. 请确保您的系统已正确安装Python，并且版本号为3.8或更高。
    2. 请确保已经安装了所有依赖库，并设置了ffmpeg为环境变量。
    3. 如果在安装或运行过程中遇到任何问题，请查阅项目文档或联系开发人员以获取帮助。
    ''')

dir_1 = os.path.dirname(os.path.abspath(__file__))
dir_2 = dir_1.replace("\\", "/")
config_dir = dir_2 + "/config/"
cache_dir = dir_2 + "/cache/"
print("当前项目的配置文件：", config_dir)
print("当前项目的缓存位置：", cache_dir)

with open(config_dir + "config.json", 'r') as file:  # 读取配置
    config = json.load(file)

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
    openai_api_key = config["openai_key"]
    openai_api_base = config["openai_base"]
    whisper_model = config["whisper_model_default"]
    st.write("#### Whisper识别设置")
    model = {'tiny': 0, 'base': 1, 'small': 2, 'medium': 3, 'large': 4}
    option = st.selectbox('选择你要使用的识别模型', ('tiny', 'base', 'small', 'medium', 'large'), index=model[whisper_model])
    if option != whisper_model:
        config["whisper_model_default"] = option
        with open(config_dir + "config.json", 'w') as file:
            json.dump(config, file, indent=4)
        st.success("默认模型已切换为：" + option)

    st.write("#### OPENAI设置")
    new_key = st.text_input("OPENAI-API-KEY：")
    new_base = st.text_input("OPENAI-API-BASE：")

    if st.button("保存"):
        if new_base != openai_api_base and new_base != "":
            config["openai_key"] = new_key
            openai_api_key = new_key
        if new_key != openai_api_key and new_key != "":
            config["openai_base"] = new_base
            openai_api_base = new_base
        with open(config_dir + "config.json", 'w') as file:
            json.dump(config, file, indent=4)
        st.success("已保存")

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

    st.session_state.base = openai_api_base
    st.session_state.key = openai_api_key
    st.session_state.option = option

with tab3:
    st.write('''
    #### 版本 0.2.2 更新日志
    #####
    ##### 增加最大上传文件大小限制
    - 在此版本中，我们增加了最大上传文件大小的限制。之前的版本仅支持最大200MB的文件上传，而现在，为您提供了更大的容量，最高可支持50GB的文件上传。这一改动旨在满足更广泛的使用场景和用户需求。
    
    ##### 自动保存设置参数
    - 根据反馈，我们注意到无法自动保存设置参数的问题，导致下次使用时需要重新设置。现在，您可以放心地进行设置，系统会自动保存您的参数，确保下次使用时便捷无忧。
    
    ##### 感谢您的反馈
    感谢您给予的反馈。如果您有任何问题、建议或反馈，请随时与我们联系。
    ######
    ###### 祝您愉快地使用 Chenyme-AAMT！
    ######
    ###### 再次感谢您的持续支持。
    ''')
