import os
import toml
import torch
import datetime
import streamlit as st
from openai import OpenAI
from utils.utils import (get_whisper_result, generate_srt_from_result, parse_srt_file, convert_to_srt)

project_dir = os.path.dirname(os.path.abspath(__file__)).replace("\\", "/")
config_dir = project_dir.replace("/pages", "") + "/config/"  # 配置文件
cache_dir = project_dir + "/cache/"  # 本地缓存
config = toml.load(config_dir + "config.toml")  # 加载配置
st.session_state.openai_key = config["GPT"]["openai_key"]
st.session_state.openai_base = config["GPT"]["openai_base"]

st.set_page_config(
    layout="wide",  # 设置布局样式为宽展示
    initial_sidebar_state="expanded"  # 设置初始边栏状态为展开
)

st.title("AI音频识别🎙️")
col1, col2 = st.columns(2, gap="medium")
with col1:
    # 文件上传
    uploaded_file = st.file_uploader("请在这里上传音频文件：", type=['mp3', 'wav', 'mp4'])
    w_version = st.selectbox('选择whisper版本', ('openai-whisper', 'faster-whisper'), index=1)
    w_model_option = st.selectbox('选择识别模型', ('tiny', 'base', 'small', 'medium', 'large'), index=4)
    # GPU加速
    wdc = not torch.cuda.is_available()
    GPU_on = st.toggle('启用GPU加速*', disabled=wdc, help='请确保您正确安装了cuda、pytorch，否则该选项无法开启！')
    device = 'cuda' if GPU_on else 'cpu'
    # VAD辅助
    VAD_on = st.toggle('启用VAD辅助*', help='请使用faster-whisper模型，否则该选项无法开启！')
    vad = 'True' if GPU_on else 'False'

    if st.button('运行程序'):
        if uploaded_file is not None:
            with st.spinner('正在加载音频缓存...'):
                current_time = datetime.datetime.now().strftime("%Y-%m-%d %H-%M-%S")
                output_file = cache_dir + current_time
                os.makedirs(output_file)
                with open(output_file + "/uploaded.mp3", "wb") as file:
                    file.write(uploaded_file.getbuffer())

            with st.spinner('正在识别音频内容...'):
                result = get_whisper_result(uploaded_file, cache_dir, device, w_model_option, w_version, vad)
                print("whisper识别：" + result['text'])

            with st.spinner('正在生成SRT字幕文件...'):
                srt_content = generate_srt_from_result(result)  # 生成SRT字幕内容
                with open(output_file + "/output.srt", 'w', encoding='utf-8') as srt_file:  # 将SRT内容写入SRT文件
                    srt_file.write(srt_content)

            st.session_state.srt_content1 = srt_content
            st.session_state.output = output_file
            st.session_state.text = result['text']
        else:
            st.error("请先上传音频！")


with col2:
    messages = st.container(height=400)
    if "messages1" not in st.session_state:
        st.session_state["messages1"] = [{"role": "assistant", "content": "您对音频内容有什么疑问?"}]

    for msg1 in st.session_state.messages1:
        messages.chat_message(msg1["role"]).write(msg1["content"])

    try:
        able = False if st.session_state.text else True
    except:
        able = True

    if prompt := st.chat_input(disabled=able, placeholder="基于音频内容的Chat，您可以问任何关于音频的问题"):
        client = OpenAI(api_key=st.session_state.openai_key)
        st.session_state.messages1.append({"role": "user", "content": prompt})
        messages.chat_message("user").write(prompt)
        response = client.chat.completions.create(model="gpt-3.5-turbo", messages=[{"role": "system", "content": "你的任务是基于以下音频内容和自己的知识回答用户问题。音频内容：" + st.session_state.text},
                                                                                   {"role": "user", "content": prompt}])
        msg1 = response.choices[0].message.content
        st.session_state.messages1.append({"role": "assistant", "content": msg1})
        messages.chat_message("assistant").write(msg1)


st.write('------')
st.caption("以下内容会在运行程序后自动显示，请运行后耐心等待！")
try:
    st.write('##### 音轨文件🎶')
    audio_file = open(st.session_state.output + "/uploaded.mp3", 'rb')
    audio_bytes = audio_file.read()
    st.audio(audio_bytes)
except:
    st.write('')

try:
    st.write('------')
    st.write('##### 字幕预览🗒️')
    st.caption("Tips：文本内容可以在左侧表格进行修改微调")
    high = st.slider('文本预览表格的高度', 100, 1000, 500, 50)
    col1, col2 = st.columns(2, gap="medium")
    with col1:
        srt_data = parse_srt_file(st.session_state.srt_content1)
        st.dataframe(srt_data, height=high, hide_index=True, use_container_width=True)
        st.download_button(
            label="下载原始的文件（SRT格式）",
            data=st.session_state.srt_content1.encode('utf-8'),
            file_name='output_old.txt'
        )
    with col2:
        edited_data = st.data_editor(srt_data, height=high, hide_index=True, use_container_width=True)
        srt = convert_to_srt(edited_data)
        st.download_button(
            label="下载修改的文件（SRT格式）",
            data=srt.encode('utf-8'),
            file_name='output_new.txt'
        )
except:
    st.write('')