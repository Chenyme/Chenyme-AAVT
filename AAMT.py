import streamlit as st
import whisper
import tempfile
import subprocess
from langchain.chains import LLMChain
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferWindowMemory
from langchain.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    MessagesPlaceholder,
    SystemMessagePromptTemplate,
)

openai_api_key = ''
openai_api_base = ''


# 格式化为SRT字幕的形式
def generate_srt_from_result(result):
    segments = result['segments']
    srt_content = ''
    segment_id = 1
    for segment in segments:
        start_time = int(segment['start'] * 1000)  # Convert to milliseconds
        end_time = int(segment['end'] * 1000)  # Convert to milliseconds
        text = segment['text']

        srt_content += f"{segment_id}\n"
        srt_content += f"{milliseconds_to_srt_time_format(start_time)} --> {milliseconds_to_srt_time_format(end_time)}\n"
        srt_content += f"{text}\n\n"

        segment_id += 1

    return srt_content


# 将毫秒表示的时间转换为SRT字幕的时间格式
def milliseconds_to_srt_time_format(milliseconds):
    seconds, milliseconds = divmod(milliseconds, 1000)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    return f"{hours:02d}:{minutes:02d}:{seconds:02d},{milliseconds:03d}"


# 虚拟化文件路径
def tmp_filepath(uploaded_file):
    with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
        tmp_file.write(uploaded_file.getvalue())
    return tmp_file.name


st.title("全自动视频翻译")

# openai设置
with st.sidebar:
    st.title("设置")
    base = st.text_input("OPENAI-API-BASE：")
    key = st.text_input("OPENAI-API-KEY：")

    if base != openai_api_base and base != "":
        openai_api_base = base
    else:
        openai_api_base = openai_api_base

    if key != openai_api_key and key != "":
        openai_api_key = key
    else:
        openai_api_key = openai_api_key

# 文件上传逻辑
uploaded_file = st.file_uploader("请在这里上传视频：", type=['mp4', 'mov'])
if uploaded_file is not None:
    with open("uploaded.mp4", "wb") as file:
        file.write(uploaded_file.getbuffer())
    st.success("上传成功")

option = st.selectbox('选择你要使用的识别模型（默认：base）', ('tiny', 'base', 'small', 'medium', 'large'), index=1)
if st.button('运行程序'):
    with st.spinner('Wait for it...'):
        # whisper识别逻辑
        model = whisper.load_model(option)
        pathvideo = tmp_filepath(uploaded_file)
        result = model.transcribe(pathvideo)
        print(result['text'])
        with open('output.srt', 'w', encoding='utf-8') as srt_file:
            srt_file.write(result['text'])
        # LLM
        llm = ChatOpenAI(openai_api_key=openai_api_key, openai_api_base=openai_api_base)
        # Prompt
        prompt = ChatPromptTemplate(
            messages=[
                SystemMessagePromptTemplate.from_template(
                    "You are a senior translator proficient in Chinese and English. Your task is to translate whatever the user says. You only need to answer the translation result and do not use punctuation marks other than question marks. Please strictly implement it!"
                ),
                # The `variable_name` here is what must align with memory
                MessagesPlaceholder(variable_name="chat_history"),
                HumanMessagePromptTemplate.from_template("{question}"),
            ]
        )
        # 设置记忆参数
        memory = ConversationBufferWindowMemory(memory_key="chat_history", return_messages=True, k=5)
        conversation = LLMChain(llm=llm, prompt=prompt, verbose=False, memory=memory)
        # 替换text
        segments = result['segments']
        segment_id = 0
        for segment in segments:
            text = segment['text']
            response = conversation({"question": text})
            result['segments'][segment_id]['text'] = response['text']
            segment_id += 1

        # 生成SRT字幕内容
        srt_content = generate_srt_from_result(result)

        # 将SRT内容写入SRT文件
        with open('output.srt', 'w', encoding='utf-8') as srt_file:
            srt_file.write(srt_content)

        command = ' ffmpeg -i "' + "uploaded.mp4" + '" -lavfi ' + '"subtitles=' + 'output.srt' + ':force_style=' + "'BorderStyle=0,Outline=1,Shadow=0,Fontsize=18'" + '"' + ' -y -crf 1 -c:a copy "' + "output.mp4" + '"'
        print(command)
        subprocess.call(command, shell=True)

    if st.download_button(
            label="Click to Download SRT",
            data=srt_content.encode('utf-8'),
            key='srt_download',
            file_name='output.srt',
            mime='text/srt',
    ):
        st.success("下载成功")

    video_file = open('output.mp4', 'rb')
    video_bytes = video_file.read()
    st.video(video_bytes)
