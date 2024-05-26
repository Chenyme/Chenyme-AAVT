import os
import math
import time
import subprocess
from openai import OpenAI
from faster_whisper import WhisperModel
import pandas as pd


def cache(cache):  # 缓存检测
    total_size = 0
    for root, dirs, files in os.walk(cache):  # 遍历文件夹中的所有文件和子文件夹
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


def get_folders_info(root_folder):
    ind = 1
    folders_info = []
    for folder_name in os.listdir(root_folder):
        folder_path = os.path.join(root_folder, folder_name)
        if os.path.isdir(folder_path):
            folder_size = cache(folder_path)
            folders_info.append({
                '序号': str(ind),
                '文件名': folder_name,
                '大小': convert_size(folder_size)
            })
            ind += 1
    return pd.DataFrame(folders_info)


def file_to_mp3(file_name, path):
    try:
        if file_name.split('.')[-1] != "mp3":
            command = f"ffmpeg -loglevel error -i {file_name} -vn -acodec libmp3lame -ab 320k -f mp3 output.mp3"
            subprocess.run(command, shell=True, cwd=path)
    except:
        raise EOFError("错误！可能是 FFmpeg 未被正确配置 或 上传文件格式不受支持！")


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


def openai_whisper_result(key, base, path, prompt, temperature):
    print("\n*** OpenAI API 调用模式 ***\n")
    if base != "https://api.openai.com/v1":
        print(f"- 代理已开启，URL：{base}")

    client = OpenAI(api_key=key, base_url=base)
    audio_file = open(path + "/output.mp3", "rb")
    transcript = client.audio.transcriptions.create(
        model="whisper-1",
        file=audio_file,
        response_format="verbose_json",
        timestamp_granularities=["segment"],
        prompt=prompt,
        temperature=temperature)
    result = {'text': transcript.text, 'segments': transcript.segments}
    print(f"- whisper识别内容：\n{result['text']}\n")
    return result


def faster_whisper_result(file_path, device, model_name, prompt, temp, vad, lang, beam_size, min_vad):
    if model_name not in ['tiny', 'tiny.en', 'base', 'base.en', 'small', 'small.en', 'medium', 'medium.en', 'large-v1',
                          'large-v2', 'large-v3', 'large', 'distil-small.en', 'distil-medium.en', 'distil-large-v2',
                          'distil-large-v3']:
        print("\n*** Faster Whisper 本地模型加载模式 ***\n")
    else:
        print("\n*** Faster Whisper 调用模式 ***\n")
    print(f"- 运行模型：{model_name}")
    print(f"- 运行方式：{device}")
    print(f"- VAD辅助：{vad}")

    file_path = file_path + "/output.mp3"
    model = WhisperModel(model_name, device)
    if lang == "自动识别" and vad is False:
        segments, _ = model.transcribe(file_path,
                                       initial_prompt=prompt,
                                       beam_size=beam_size,
                                       temperature=temp
                                       )
    elif lang == "自动识别" and vad is True:
        segments, _ = model.transcribe(file_path,
                                       initial_prompt=prompt,
                                       beam_size=beam_size,
                                       vad_filter=vad,
                                       vad_parameters=dict(min_silence_duration_ms=min_vad),
                                       temperature=temp
                                       )
    elif vad is False:
        segments, _ = model.transcribe(file_path,
                                       initial_prompt=prompt,
                                       language=lang,
                                       beam_size=beam_size,
                                       temperature=temp
                                       )
    elif vad is True:
        segments, _ = model.transcribe(file_path,
                                       initial_prompt=prompt,
                                       language=lang,
                                       beam_size=beam_size,
                                       vad_filter=vad,
                                       vad_parameters=dict(min_silence_duration_ms=min_vad),
                                       temperature=temp
                                       )

    result = faster_whisper_result_dict(segments)
    print(f"- whisper识别内容：\n{result['text']}\n")
    return result


def translate(api_key, base_url, model, result, language1, language2, wait_time):

    if "gpt" in model:
        if base_url != "https://api.openai.com/v1":
            print(f"- 代理地址：{base_url}")
        print("- 翻译内容：\n")
        client = OpenAI(api_key=api_key, base_url=base_url)
        segment_id = 0
        segments = result['segments']
        for segment in segments:
            text = segment['text']
            response = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": f"You are a professional translator in {language1} and {language2}" },
                    {"role": "user", "content": f"Reply directly to {language2} translation results. Note: Just give the translation results, prohibited to return anything other! Content to be translated: \n" + str(text)}
                ])
            answer = response.choices[0].message.content
            result['segments'][segment_id]['text'] = answer
            segment_id += 1
            print(answer)
            time.sleep(wait_time)

    else:
        print("- 翻译内容：\n")
        if "moonshot" in model:
            client = OpenAI(api_key=api_key, base_url=base_url)
        elif "glm" in model:
            client = OpenAI(api_key=api_key, base_url=base_url)
        elif "deepseek" in model:
            client = OpenAI(api_key=api_key, base_url=base_url)

        segment_id = 0
        segments = result['segments']
        for segment in segments:
            text = segment['text']
            response = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": f"你是对{language1}和{language2}十分专业的翻译专家"},
                    {"role": "user", "content": f"将下面的文本的翻译成{language2}。你只允许给出最后的翻译结果，除结果外不允许回复任何无关的话语。文本：" + str(text)}
                ])
            answer = response.choices[0].message.content
            result['segments'][segment_id]['text'] = answer
            segment_id += 1
            print(answer)
            time.sleep(wait_time)
    return result


def local_translate(api_key, base_url, model, result, language1, language2):
    print("- 本地大模型翻译")
    print("- 翻译内容：\n")
    client = OpenAI(api_key=api_key, base_url=base_url)
    segments = result['segments']
    segment_id = 0
    for segment in segments:
        text = segment['text']
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": f"你是对{language1}和{language2}十分专业的翻译专家"},
                {"role": "user", "content": f"将下面的文本的翻译成{language2}。你只允许给出最后的翻译结果，除结果外不允许回复任何无关的话语。文本：" + str(text)}])
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


def check_cuda_support():
    try:
        result = subprocess.run(["ffmpeg", "-hwaccels"], capture_output=True, text=True)
        return "cuda" in result.stdout
    except Exception as e:
        print(f" 未检测到 CUDA 状态，本地合并为 CPU 模式，若要使用 GPU 请检查 CUDA 是否配置成功")
        return False


def srt_mv(name, crf, quality, setting, path, font, font_size, font_color, subtitle_model):  # 视频合成字幕
    font_color = font_color.replace("#", "H")
    cuda_supported = check_cuda_support()

    if subtitle_model == "硬字幕":
        if cuda_supported:
            command = f"""ffmpeg -loglevel error -hwaccel cuda -i {name} -lavfi "subtitles=output.srt:force_style='FontName={font},FontSize={font_size},PrimaryColour=&{font_color}&,Outline=1,Shadow=0,BackColour=&H9C9C9C&,Bold=-1,Alignment=2'" -preset {quality} -c:v {setting} -crf {crf} -y -c:a copy output.mp4"""
        else:
            command = f"""ffmpeg -loglevel error -i {name} -lavfi "subtitles=output.srt:force_style='FontName={font},FontSize={font_size},PrimaryColour=&{font_color}&,Outline=1,Shadow=0,BackColour=&H9C9C9C&,Bold=-1,Alignment=2'" -preset {quality} -c:v libx264 -crf {crf} -y -c:a copy output.mp4"""
    else:
        if cuda_supported:
            command = f"""ffmpeg -loglevel error -hwaccel cuda -i {name} -i output_with_style.srt -c:v {setting} -crf {crf} -y -c:a copy -c:s mov_text -preset {quality} output.mp4"""
        else:
            command = f"""ffmpeg -loglevel error -i {name} -i output_with_style.srt -c:v libx264 -crf {crf} -y -c:a copy -c:s mov_text -preset {quality} output.mp4"""

    subprocess.run(command, shell=True, cwd=path)


def parse_srt_file(srt_content):  # SRT转换pandas.DataFrame对象
    lines = srt_content.strip().split('\n')
    subtitles = []
    current_subtitle = None

    for line in lines:
        line = line.strip()

        if line.isdigit():
            if current_subtitle is not None:
                subtitles.append(current_subtitle)
            current_subtitle = {'index': str(line)}
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


def show_video(path, name):
    video_file = open(path + "/" + name, 'rb')
    video_bytes = video_file.read()
    return video_bytes


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


def check_ffmpeg():
    try:
        result = subprocess.run(['ffmpeg', '-version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if result.returncode == 0:
            return True
        else:
            return False
    except FileNotFoundError:
        return False
