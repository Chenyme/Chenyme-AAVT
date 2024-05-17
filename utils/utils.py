import os
import math
import time
import tempfile
import subprocess
import pandas as pd
import streamlit as st
from openai import OpenAI
from faster_whisper import WhisperModel


@st.cache_resource
def audio_chatbot(system, prompt, key, base):  # 音频助手
    client = OpenAI(api_key=key, base_url=base)
    if base == '':
        client = OpenAI(api_key=key)

    response = client.chat.completions.create(model="gpt-3.5-turbo",
                                              messages=[{"role": "system", "content": system},
                                                        {"role": "user", "content": prompt}])
    msg = response.choices[0].message.content
    st.session_state.messages.append({"role": "user", "content": prompt})  # 缓存回答
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
        'segments': [{
                'id': segment.id,
                'seek': segment.seek,
                'start': segment.start,
                'end': segment.end,
                'text': segment.text,
                'tokens': segment.tokens,
                'temperature': segment.temperature,
                'avg_logprob': segment.avg_logprob,
                'compression_ratio': segment.compression_ratio,
                'no_speech_prob': segment.no_speech_prob}
            for segment in segments
        ]
    }
    return segments_dict


def openai_whisper(key, base, proxy_on, prompt, temperature, temp_dir):
    files_in_folder = os.listdir(temp_dir)
    if "output.mp3" not in files_in_folder:
        command = "ffmpeg -i uploaded.mp4 -vn -acodec libmp3lame -ab 320k -f mp3 output.mp3"
        subprocess.run(command, shell=True, cwd=temp_dir)
    client = OpenAI(api_key=key)
    if proxy_on:
        client = OpenAI(api_key=key, base_url=base)
        print("\n\n代理开启，代理地址："+base)
    audio_file = open(temp_dir + "/output.mp3", "rb")
    transcript = client.audio.transcriptions.create(
        model="whisper-1",
        file=audio_file,
        response_format="verbose_json",
        timestamp_granularities=["segment"],
        prompt=prompt,
        temperature=temperature
    )
    result = {'text': transcript.text, 'segments': transcript.segments}
    return result


def get_whisper_result(uploaded_file, temp_dir, device, option, vad, lang, beam_size, min_vad):  # whisper识别配置
    path_video = tmp_filepath(uploaded_file, temp_dir)
    model = WhisperModel(option, device)
    if lang == "自动识别":
        segments, _ = model.transcribe(path_video,
                                       initial_prompt="Don’t make each line too long.",
                                       vad_filter=vad,
                                       beam_size=beam_size,
                                       vad_parameters=dict(min_silence_duration_ms=min_vad)
                                       )
    else:
        segments, _ = model.transcribe(path_video,
                                       initial_prompt="Don’t make each line too long.",
                                       vad_filter=vad,
                                       language=lang,
                                       beam_size=beam_size,
                                       vad_parameters=dict(min_silence_duration_ms=min_vad)
                                       )
    whisper_result = faster_whisper_result_dict(segments)
    os.unlink(path_video)
    return whisper_result


def openai_translate1(key, base, proxy_on, result, language1, language2, waittime):
    client = OpenAI(api_key=key)
    if proxy_on:
        client = OpenAI(api_key=key, base_url=base)
        print("\n\n代理开启，代理地址："+base)
    segments = result['segments']
    print("---\n翻译内容：")
    segment_id = 0
    for segment in segments:
        text = segment['text']
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user",
                       "content": "直接回复" + language2 + "翻译结果。注意：只需给出结果，禁止出现除结果以外的其他任何内容！" + str(text)}])
        answer = response.choices[0].message.content
        result['segments'][segment_id]['text'] = answer
        segment_id += 1
        print(answer)
        time.sleep(waittime)
    return result


def chunk_for_gpt4(result, n):  # GPT4分块
    texts = [''] * n
    index, count = 0, 0
    for segment in result['segments']:
        words = segment['text'].split()
        if len(words) >= 2:  # 英文检测
            count += len(words)
        else:  # 中文
            count += len(segment['text'])

        if count > 800:
            count = len(words)
            index += 1
        texts[index] += segment['text'] + "<br>\n"
    return texts


def openai_translate2(key, base, proxy_on, result, language1, language2, n, waittime):  # 调用GPT4翻译
    segment_id = 0
    texts = chunk_for_gpt4(result, n)
    client = OpenAI(api_key=key)
    if proxy_on:
        client = OpenAI(api_key=key, base_url=base)
        print("\n\n代理开启，代理地址："+base)
    for text in texts:
        if text:
            prompt = "You are a senior translator proficient in " + language1 + " and " + language2 + ". Please translate the content in markdown format below line by line. Make sure that there are as many lines as there are after translation. The result is output in markdown format, and now you can directly give the translation result.!" + text
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}])
            answer = response.choices[0].message
            contents = answer.content.split('\n')
            time.sleep(waittime)

            for content in contents:
                if content and '```' not in content:
                    if '<br>' in content:
                        content = content.replace("<br>", "")
                    else:
                        content = content
                    result['segments'][segment_id]['text'] = content
                    segment_id += 1
    return result


def chunk_for_kimi(result, n):
    texts = [''] * n
    index, count = 0, 0
    for segment in result['segments']:
        words = segment['text'].split()
        if len(words) >= 2:  # 英文检测
            count += len(words)
        else:  # 中文
            count += len(segment['text'])

        if count > 500:
            count = len(words)
            index += 1
        texts[index] += segment['text'] + "<br>\n"
    return texts


def kimi_translate(kimi_key, translate_option, result, language1, language2, n, waittime):  # 调用Kimi翻译
    model = translate_option.replace('kimi-', '')
    texts = chunk_for_kimi(result, n)
    segment_id = 0
    for text in texts:
        if text:
            print(text)
            client = OpenAI(api_key=kimi_key, base_url="https://api.moonshot.cn/v1")
            completion = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "user", "content": "你是熟知" + language1 + " 和 " + language2 + "的专业翻译，请一行一行的翻译下面的markdown格式的内容，要保证原来有多少行，翻译后就要有多少行。结果输出markdown格式，现在你直接给出翻译结果。"+str(text)}
                ],
                temperature=0.8,
            )
            answer = completion.choices[0].message
            contents = answer.content.split('\n')
            time.sleep(waittime)

            for content in contents:
                if content and '```' not in content:
                    if '<br>' in content:
                        content = content.replace("<br>","")
                    else:
                        content = content
                    result['segments'][segment_id]['text'] = content
                    segment_id += 1
    return result


def deepseek_translate(deepseek_key, result, language2, waittime):
    client = OpenAI(api_key=deepseek_key, base_url="https://api.deepseek.com/")
    segments = result['segments']
    print("---\n翻译内容：")
    segment_id = 0
    for segment in segments:
        text = segment['text']
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[{"role": "user","content": "直接回复" + language2 + "翻译结果。注意：只需给出结果，禁止出现除结果以外的其他任何内容！" + str(text)}],
            temperature=1.1)
        answer = response.choices[0].message.content
        result['segments'][segment_id]['text'] = answer
        segment_id += 1
        print(answer)
        time.sleep(waittime)
    return result


def chatglm_translate(chatglm_key, model, result, language2, waittime):
    client = OpenAI(api_key=chatglm_key, base_url="https://open.bigmodel.cn/api/paas/v4/")
    segments = result['segments']
    print("---\n翻译内容：")
    segment_id = 0
    for segment in segments:
        text = segment['text']
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user","content": "直接回复" + language2 + "翻译结果。注意：只需给出结果，禁止出现除结果以外的其他任何内容！" + str(text)}])
        answer = response.choices[0].message.content
        result['segments'][segment_id]['text'] = answer
        segment_id += 1
        print(answer)
        time.sleep(waittime)
    return result


def local_translate(base_url, api_key, model_name, result, language2):
    client = OpenAI(api_key=api_key, base_url=base_url)
    segments = result['segments']
    print("---\n翻译内容：")
    segment_id = 0
    for segment in segments:
        text = segment['text']
        response = client.chat.completions.create(
            model=model_name,
            messages=[{"role": "user","content": "直接回复" + language2 + "翻译结果。注意：只需给出结果，禁止出现除结果以外的其他任何内容！" + str(text)}])
        answer = response.choices[0].message.content
        result['segments'][segment_id]['text'] = answer
        segment_id += 1
        print(answer)
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

        index = 30
        words = text.split()
        if len(words) <= 2:  # 中文检测
            if len(words) > index:
                text = text[:index] + "\n" + text[index:]
        srt_content += f"{segment_id}\n"
        srt_content += f"{milliseconds_to_srt_time_format(start_time)} --> {milliseconds_to_srt_time_format(end_time)}\n"
        srt_content += f"{text}\n\n"
        segment_id += 1
    return srt_content


def generate_srt_from_result_2(result, font, font_size, font_color):  # 格式化为SRT字幕的形式
    segments = result['segments']
    srt_content = ''
    segment_id = 1
    for segment in segments:
        start_time = int(segment['start'] * 1000)
        end_time = int(segment['end'] * 1000)
        text = segment['text']

        index = 30
        words = text.split()
        if len(words) <= 2:  # 中文检测
            if len(words) > index:
                text = text[:index] + "\n" + text[index:]
        srt_content += f"{segment_id}\n"
        srt_content += f"{milliseconds_to_srt_time_format(start_time)} --> {milliseconds_to_srt_time_format(end_time)}\n"
        srt_content += f"<font color={font_color}><font face={font}><font size={font_size}> {text}\n\n"
        segment_id += 1
    return srt_content


def srt_mv(v_dir, font, font_size, font_color, subtitle_model):  # 视频合成字幕
    modified_color = font_color.replace("#", "H")
    if subtitle_model == "硬字幕":
        command = ' ffmpeg -i "' + "uploaded.mp4" + '" -lavfi ' + '"subtitles=' + 'output.srt' + ':force_style=' + "'FontName=" + font + ",FontSize=" + str(font_size) + ",PrimaryColour=&" + modified_color + "&,Outline=1,Shadow=1,BackColour=&#9C9C9C&,Bold=-1,Alignment=2'" + '"' + ' -y -crf 1 -c:a copy "' + "output.mp4" + '"'
    else:
        command = ' ffmpeg -i "uploaded.mp4" -i output.srt -c copy output.mp4'
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


def srt_to_ass(srt_content, fontname, size, color):
    lines = srt_content.strip().split('\n\n')
    ass_content = ('[Script Info]\nTitle: Converted from SRT\n\n[V4+ Styles]\nFormat: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, TertiaryColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding\nStyle: Default,' + str(fontname) + ',' + str(size) + ',' + str(color) + ',&H000000FF,&H00000000,&H00000000,-1,0,0,0,100,100,0,0.00,1,1.00,0.00,2,10,10,10,1\n\n[Events]\nFormat: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n')
    for line in lines:
        parts = line.strip().split('\n')
        start, end = parts[1].split(' --> ')
        text = '\n'.join(parts[2:])
        ass_content += f'Dialogue: 0,{start},{end},Default,,0,0,0,,"{text}"\n'
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


def show_video(cache_dir):
    video_file = open(cache_dir + "/output.mp4", 'rb')
    video_bytes = video_file.read()
    return video_bytes


def cache(cache_dir):  # 缓存检测
    total_size = 0  # 默认缓存
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