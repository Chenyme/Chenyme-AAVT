import os
import math
import whisper
import tempfile
import subprocess
import pandas as pd
import streamlit as st
from openai import OpenAI
from faster_whisper import WhisperModel
from langchain.chains import LLMChain
from langchain_openai import ChatOpenAI
from langchain.memory import ConversationBufferWindowMemory
from langchain.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    MessagesPlaceholder,
    SystemMessagePromptTemplate,
)


@st.cache_resource
def audio_chatbot(system, prompt, key, base):
    if base == '':
        client = OpenAI(api_key=key)
    else:
        client = OpenAI(api_key=key, base_url=base)

    response = client.chat.completions.create(model="gpt-3.5-turbo", messages=[{"role": "system", "content": system},
                                                                               {"role": "user", "content": prompt}])
    msg = response.choices[0].message.content

    # 缓存
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.session_state.messages.append({"role": "assistant", "content": msg})
    return msg


def tmp_filepath(uploaded_file, temp_dir):  # 虚拟化文件路径
    with tempfile.NamedTemporaryFile(delete=False, dir=temp_dir) as tmp_file:
        tmp_file.write(uploaded_file.getvalue())
        tmp_file.close()
    return tmp_file.name


def faster_whisper_result_dict(segments):  # faster-whisper中生成器转换dict
    segments = list(segments)
    segments_dict = {
        'text': ' '.join([segment.text for segment in segments]),
        'segments': [
            {
                'id': segment.id,
                'seek': segment.seek,
                'start': segment.start,
                'end': segment.end,
                'text': segment.text,
                'tokens': segment.tokens,
                'temperature': segment.temperature,
                'avg_logprob': segment.avg_logprob,
                'compression_ratio': segment.compression_ratio,
                'no_speech_prob': segment.no_speech_prob
            }
            for segment in segments
        ]
    }
    return segments_dict


def get_whisper_result(uploaded_file, temp_dir, device, option, whisper_name, vad):  # whisper识别配置
    path_video = tmp_filepath(uploaded_file, temp_dir)  # 虚拟化文件路径
    if whisper_name == "openai-whisper":
        model = whisper.load_model(option, device)
        whisper_result = model.transcribe(path_video, initial_prompt='Please break up as many sentences as possible.')
    elif whisper_name == "faster-whisper":
        whisper_result = {}
        model = WhisperModel(option, device)
        segments, _ = model.transcribe(path_video,
                                       initial_prompt='Please break up as many sentences as possible.',
                                       vad_filter=vad,
                                       vad_parameters=dict(min_silence_duration_ms=500)
                                       )
        whisper_result = faster_whisper_result_dict(segments)
    os.unlink(path_video)  # 删除缓存文件
    return whisper_result


def openai_translate1(key, base, proxy_on, result, language1, language2):  # 调用gpt3.5翻译
    if proxy_on:
        llm = ChatOpenAI(openai_api_key=key, openai_api_base=base)
    else:
        llm = ChatOpenAI(openai_api_key=key)
    # 提示词
    prompt = ChatPromptTemplate(
        messages=[
            SystemMessagePromptTemplate.from_template(
                "You are a senior translator proficient in " + language1 + " and " + language2 + ". Your task is to translate whatever the user says. You only need to answer the translation result and do not use punctuation marks other than question marks. Please strictly implement it!"
            ),
            MessagesPlaceholder(variable_name="chat_history"),
            HumanMessagePromptTemplate.from_template("{question}"),
        ]
    )
    # 设置记忆参数
    memory = ConversationBufferWindowMemory(memory_key="chat_history", return_messages=True, k=5)
    conversation = LLMChain(llm=llm, prompt=prompt, verbose=False, memory=memory)
    segments = result['segments']
    segment_id = 0
    for segment in segments:
        text = segment['text']
        response = conversation({"question": text})
        result['segments'][segment_id]['text'] = response['text']
        segment_id += 1
    return result


def openai_translate2(key, base, proxy_on, result, language1, language2):  # 调用GPT4翻译
    text1, text2, text3 = '', '', ''
    segments = result['segments']
    segment_id = 0

    for segment in segments:  # token限制优化
        if len(text1) + len(segment['text']) <= 8000:
            text1 += segment['text'] + "\n"
        elif len(text2) + len(segment['text']) <= 8000:
            text2 += segment['text'] + "\n"
        else:
            text3 += segment['text'] + "\n"

    text_list = [text1, text2, text3]

    for text in text_list:
        if text != '':
            prompt = "You are a senior translator proficient in " + language1 + " and " + language2 + ". Your task is to translate whatever the user says. Keep newline format. You only need to answer the translation result!!!" + text
            if proxy_on:
                llm = ChatOpenAI(model_name="gpt-4", openai_api_key=key, openai_api_base=base)
            else:
                llm = ChatOpenAI(model_name="gpt-4", openai_api_key=key)
            answer = llm.invoke(prompt)
            contents = answer.content.split('\n')
            for content in contents:
                result['segments'][segment_id]['text'] = content
                segment_id += 1
    return result


def kimi_translate(kimi_key, result, language1, language2):  # 调用Kimi翻译
    segments = result['segments']
    text = ''
    segment_id = 0
    for segment in segments:
        text += segment['text'] + "\n"

    client = OpenAI(
        api_key=kimi_key,
        base_url="https://api.moonshot.cn/v1",
    )

    completion = client.chat.completions.create(
        model="moonshot-v1-8k",
        messages=[
            {"role": "user", "content": "你是" + language1 + " 和 " + language2 + "的专业翻译人员. 你的任务就是翻译下面的段落，并且保留段落原始的换行格式，请直接回答翻译结果!!!\n段落：\n" + text}
        ],
        temperature=0.5,
    )
    answer = completion.choices[0].message
    contents = answer.content.split('\n')
    print(contents)
    for content in contents:
        result['segments'][segment_id]['text'] = content
        segment_id += 1

    return result


def milliseconds_to_srt_time_format(milliseconds):  # 将毫秒表示的时间转换为SRT字幕的时间格式
    seconds, milliseconds = divmod(milliseconds, 1000)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    return f"{hours:02d}:{minutes:02d}:{seconds:02d},{milliseconds:03d}"


def generate_srt_from_result(result):  # 格式化为SRT字幕的形式
    segments = result['segments']
    srt_content = ''
    segment_id = 1
    for segment in segments:
        start_time = int(segment['start'] * 1000)
        end_time = int(segment['end'] * 1000)
        text = segment['text']
        srt_content += f"{segment_id}\n"
        srt_content += f"{milliseconds_to_srt_time_format(start_time)} --> {milliseconds_to_srt_time_format(end_time)}\n"
        srt_content += f"{text}\n\n"
        segment_id += 1

    return srt_content


def srt_mv(v_dir, font):  # 视频合成字幕
    command = ' ffmpeg -i "' + "uploaded.mp4" + '" -lavfi ' + '"subtitles=' + 'output.srt' + ':force_style=' + "'FontName=" + font + ",FontSize=18,PrimaryColour=&HFFFFFF&,Outline=1,Shadow=1,BackColour=&#9C9C9C&,Bold=-1,Alignment=2'" + '"' + ' -y -crf 1 -c:a copy "' + "output.mp4" + '"'
    subprocess.run(command, shell=True, cwd=v_dir)


def srt_to_vtt(srt_content):
    lines = srt_content.strip().split('\n')
    vtt_lines = ['WEBVTT\n\n']
    for i in range(0, len(lines), 4):
        index = lines[i].strip()
        time_range = lines[i + 1].strip().replace(',', '.')
        text = lines[i + 2].strip()
        vtt_lines.append(f'{index}\n{time_range}\n{text}\n\n')

    vtt_content = '\n'.join(vtt_lines)
    return vtt_content


def srt_to_ass(srt_content):
    lines = srt_content.strip().split('\n\n')
    ass_content = '[Script Info]\nTitle: Converted from SRT\n\n[V4+ Styles]\nFormat: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, TertiaryColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding\nStyle: Default,Arial,20,&H00FFFFFF,&H000000FF,&H00000000,&H00000000,-1,0,0,0,100,100,0,0.00,1,1.00,0.00,2,10,10,10,1\n\n[Events]\nFormat: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n'

    for line in lines:
        parts = line.strip().split('\n')
        start, end = parts[1].split(' --> ')
        text = '\n'.join(parts[2:])
        ass_content += f'Dialogue: 0,{start},{end},Default,,0,0,0,,{text}\n'
    return ass_content


def srt_to_stl(srt_content):
    lines = srt_content.strip().split('\n\n')
    stl_content = ''
    for i, line in enumerate(lines):
        parts = line.strip().split('\n')
        start, end = parts[1].split(' --> ')
        text = '\n'.join(parts[2:])
        text = text.replace('\n', ' ')
        stl_content += f'{i+1}\n{start} {end}\n{text}\n\n'
    return stl_content


@st.cache_resource
def show_video(cache_dir):
    video_file = open(cache_dir + "/output.mp4", 'rb')
    video_bytes = video_file.read()
    return video_bytes


def cache(cache_dir):  # 缓存检测
    total_size = 0
    for root, dirs, files in os.walk(cache_dir):  # 遍历文件夹中的所有文件和子文件夹
        for file_name in files:
            file_path = os.path.join(root, file_name)
            total_size += os.path.getsize(file_path)
    return total_size


def convert_size(size):  # 缓存大小匹配
    if size == 0:
        return "0B"
    size_names = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    i = int(math.floor(math.log(size, 1024)))
    power = math.pow(1024, i)
    size = round(size / power, 2)
    return f"{size} {size_names[i]}"


def parse_srt_file(srt_content):  # SRT转换pandas.DataFrame对象
    lines = srt_content.strip().split('\n')

    subtitles = []
    current_subtitle = None

    for line in lines:
        line = line.strip()

        if line.isdigit():
            if current_subtitle is not None:
                subtitles.append(current_subtitle)

            current_subtitle = {'': int(line)}
        elif '-->' in line:
            start_time, end_time = line.split('-->')
            current_subtitle['start'] = start_time.strip()
            current_subtitle['end'] = end_time.strip()
        elif line != '':
            if 'content' in current_subtitle:
                current_subtitle['content'] += ' ' + line
            else:
                current_subtitle['content'] = line

    if current_subtitle is not None:
        subtitles.append(current_subtitle)

    return pd.DataFrame(subtitles)


def convert_to_srt(edited_data):
    subtitles = ''
    for index, row in edited_data.iterrows():
        start_time = row['start']
        end_time = row['end']
        content = row['content']
        subtitle = f"{index + 1}\n{start_time} --> {end_time}\n{content}\n\n"
        subtitles += subtitle
    return subtitles
