import time
import json
import subprocess
import requests
from pathlib import Path
from openai import OpenAI
from openai import OpenAIError
from concurrent.futures import ThreadPoolExecutor
from faster_whisper import WhisperModel
import anthropic
import pandas as pd
import google.generativeai as genai
import re
import cv2
import os
import toml
import torch
import base64
import streamlit as st


def get_global_info():
    path = os.getcwd().replace("utils", "") + "/"
    llms_path = path + "config/llms.toml"
    with open(llms_path, 'r', encoding="utf-8") as config_file:
        llms = toml.load(config_file)
    global_key = llms["Global"]["key"]
    global_url = llms["Global"]["url"]
    all_in_one = llms["Global"]["all"]
    return global_key, global_url, all_in_one


def FileToMp3(log_level: str, input_dir: str, output_dir: str, output_name: str = "output.mp3"):
    input_path = Path(input_dir)
    output_path = Path(output_dir) / output_name

    if not input_path.is_file():
        raise FileNotFoundError(f"输入文件不存在: {input_path}")

    if input_path.suffix.lower() == ".mp3":
        print("\033[1;34m🎧 文件已经是 MP3 格式，无需转换。\033[0m")
        return output_path

    try:
        command = [
            "ffmpeg", "-loglevel", log_level, "-i", str(input_path),
            "-vn", "-acodec", "libmp3lame", "-ab", "320k",
            "-f", "mp3", str(output_path)
        ]
        subprocess.run(command, check=True)
        print("\033[1;34m🎧 文件已成功转换为 MP3 格式！\033[0m")
        return output_path

    except subprocess.CalledProcessError as e:
        raise EOFError(f"FFmpeg 执行失败: {e}")
    except Exception as e:
        raise EOFError(f"发生错误！可能是 FFmpeg 未被正确配置或上传文件格式不受支持。详细信息: {e}")


def OpenaiWhisperResult(key: str, url: str, path: str, model: str, prompt: str, temperature: float):
    print("\n\033[1;35m*** OpenAI Whisper API 调用模式 ***\033[0m\n")
    print(f"\033[1;34m🈴 识别模型: {model}\033[0m")
    global_key, global_url, all_in_one = get_global_info()

    if all_in_one:
        client = OpenAI(api_key=global_key, base_url=global_url)
        print(f"\033[1;34m🌐 代理地址: {global_url}\033[0m")
    else:
        client = OpenAI(api_key=key, base_url=url)
        if url != "https://api.openai.com/v1":
            print(f"\033[1;34m🌐 代理地址: {url}\033[0m")

    audio_path = Path(path)
    try:
        if audio_path.is_file():
            audio_file_path = audio_path
        else:
            audio_file_path = audio_path / "output.mp3"
        if not audio_file_path.is_file():
            raise FileNotFoundError(f"文件未找到：{audio_file_path}")
    except FileNotFoundError as e:
        return {"error": f"文件错误：{str(e)}"}

    try:
        with audio_file_path.open("rb") as audio_file:
            transcript = client.audio.transcriptions.create(
                model=model,
                file=audio_file,
                response_format="verbose_json",
                timestamp_granularities=["segment"],
                prompt=prompt,
                temperature=temperature
            )
    except OpenAIError as e:
        return {"error": f"OpenAI Whisper API 请求失败：{str(e)}"}

    finally:
        audio_file.close()

    result = {'text': transcript.text, 'segments': transcript.segments}
    print(f"\033[1;34m📝 Whisper识别结果:\033[0m\n{result['text']}\n")
    return result


def FasterWhisperResultDict(segments):
    segments = list(segments)
    return {
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


def FasterWhisperResult(file_path: str, device: str, model_name: str, prompt: str, temp: float, vad: bool, lang: str, beam_size: int, min_vad: int):
    valid_models = ['tiny', 'tiny.en', 'base', 'base.en', 'small', 'small.en', 'medium', 'medium.en', 'large-v1', 'large-v2', 'large-v3', 'large', 'distil-small.en', 'distil-medium.en', 'distil-large-v2', 'distil-large-v3']
    if device:
        device = "cuda"
    else:
        device = "cpu"

    if model_name in valid_models:
        print("\n\033[1;35m*** Faster Whisper 自动下载模式 ***\033[0m\n")
    else:
        print("\n\033[1;35m*** Faster Whisper 本地模型模式 ***\033[0m\n")

    print(f"\033[1;34m🖥️ 运行模型: {model_name} \033[0m")
    print(f"\033[1;34m⚙️️ 运行方式: {device} \033[0m")
    print(f"\033[1;34m🎙️ VAD辅助: {vad} \033[0m")

    file_path = Path(file_path)
    try:
        if file_path.is_file():
            audio_file = file_path.open("rb")
        else:
            audio_file = (file_path / "output.mp3").open("rb")
    except FileNotFoundError as e:
        return {"error": f"文件错误：{str(e)}"}

    try:
        with audio_file:
            model = WhisperModel(model_name, device)
            transcribe_args = {
                "initial_prompt": prompt,
                "beam_size": beam_size,
                "temperature": temp
            }
            if vad:
                transcribe_args.update({
                    "vad_filter": vad,
                    "vad_parameters": dict(min_silence_duration_ms=min_vad)
                })
            if lang != "自动识别":
                transcribe_args["language"] = lang

            segments, _ = model.transcribe(audio_file, **transcribe_args)

        result = FasterWhisperResultDict(segments)
        print(f"\033[1;34m📝 Whisper识别结果:\033[0m\n{result['text']}")
        return result

    except Exception as e:
        return {"error": f"转录过程发生错误：{str(e)}"}


def runWhisperSeperateProc(*args):
    try:
        with ThreadPoolExecutor() as executor:
            future = executor.submit(FasterWhisperResult, *args)
            return future.result()

    except Exception as e:
        st.error(f"An error occurred during transcription: {e}")
        st.stop()


def translate(system_prompt, user_prompt, api_key, base_url, model, result, wait_time, srt):
    print("\n\033[1;35m*** API 调用翻译模式 ***\033[0m\n")
    print(f"\033[1;34m🈴 翻译模型: {model}\033[0m")
    global_key, global_url, all_in_one = get_global_info()

    if all_in_one:
        client = OpenAI(api_key=global_key, base_url=global_url)
        print(f"\033[1;34m🌐 代理地址: {global_url}\033[0m")
        print(f"\033[1;34m📝 翻译内容: \033[0m")

        segment_id = 0
        segments = result['segments']

        context_size = 2
        previous_texts = []
        original_user_prompt = user_prompt

        for segment in segments:
            text = segment['text']

            if len(previous_texts) > 0:
                combined_text = "\n".join(previous_texts[-context_size:]) + "\n"
            else:
                combined_text = text
            current_user_prompt = original_user_prompt.replace("{combined_text}", combined_text)

            response = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": current_user_prompt + str(text)}
                ])
            answer = response.choices[0].message.content

            if srt == "原始语言为首":
                result['segments'][segment_id]['text'] = str(text) + "\n" + str(answer)
            elif srt == "目标语言为首":
                result['segments'][segment_id]['text'] = str(answer) + "\n" + str(text)
            else:
                result['segments'][segment_id]['text'] = answer
            segment_id += 1
            print(answer)

            previous_texts.append(text)
            if len(previous_texts) > context_size:
                previous_texts.pop(0)
            time.sleep(wait_time)

    else:
        if "gpt" in model:
            if base_url != "https://api.openai.com/v1":
                print(f"\033[1;34m🌐 代理地址: {base_url}\033[0m")
            print(f"\033[1;34m📝 翻译内容: \033[0m")
            client = OpenAI(api_key=api_key, base_url=base_url)
            segment_id = 0
            segments = result['segments']
            original_user_prompt = user_prompt
            context_size = 2
            previous_texts = []
            for segment in segments:
                text = segment['text']

                if len(previous_texts) > 0:
                    combined_text = "\n".join(previous_texts[-context_size:]) + "\n"
                else:
                    combined_text = text
                current_user_prompt = original_user_prompt.replace("{combined_text}", combined_text)
                response = client.chat.completions.create(
                    model=model,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": current_user_prompt + str(text)}
                    ])
                answer = response.choices[0].message.content

                if srt == "原始语言为首":
                    result['segments'][segment_id]['text'] = str(text) + "\n" + str(answer)
                elif srt == "目标语言为首":
                    result['segments'][segment_id]['text'] = str(answer) + "\n" + str(text)
                else:
                    result['segments'][segment_id]['text'] = answer

                segment_id += 1
                print(answer)

                previous_texts.append(text)
                if len(previous_texts) > context_size:
                    previous_texts.pop(0)

                time.sleep(wait_time)

        elif "claude" in model:
            if base_url != "https://api.anthropic.com/v1/messages":
                print(f"\033[1;34m🌐 代理地址: {base_url}\033[0m")
            print(f"\033[1;34m📝 翻译内容: \033[0m")
            segment_id = 0
            segments = result['segments']
            client = anthropic.Anthropic(api_key=api_key, base_url=base_url)

            context_size = 2
            previous_texts = []
            original_user_prompt = user_prompt

            for segment in segments:
                text = segment['text']

                if len(previous_texts) > 0:
                    combined_text = "\n".join(previous_texts[-context_size:]) + "\n"
                else:
                    combined_text = text
                current_user_prompt = original_user_prompt.replace("{combined_text}", combined_text)

                message = client.messages.create(
                    model=model,
                    max_tokens=1024,
                    system=system_prompt,
                    messages=[
                        {"role": "user", "content": current_user_prompt + str(text)}
                    ])

                answer = message.content[0]['text']
                if srt == "原始语言为首":
                    result['segments'][segment_id]['text'] = str(text) + "\n" + str(answer)
                elif srt == "目标语言为首":
                    result['segments'][segment_id]['text'] = str(answer) + "\n" + str(text)
                else:
                    result['segments'][segment_id]['text'] = answer
                segment_id += 1
                print(answer)

                previous_texts.append(text)
                if len(previous_texts) > context_size:
                    previous_texts.pop(0)

                time.sleep(wait_time)

        elif "gemini" in model:
            if base_url is None:
                print("- Python SDK 调用：如果需要使用代理，请填写 BASE_URL，系统将自动启用代理模式！")
                segment_id = 0
                segments = result['segments']

                context_size = 2
                previous_texts = []
                original_user_prompt = user_prompt

                print(f"\033[1;34m📝 翻译内容: \033[0m")
                for segment in segments:
                    text = segment['text']

                    if len(previous_texts) > 0:
                        combined_text = "\n".join(previous_texts[-context_size:]) + "\n"
                    else:
                        combined_text = text
                    current_user_prompt = original_user_prompt.replace("{combined_text}", combined_text)

                    genai.configure(api_key=api_key)
                    model = genai.GenerativeModel(model)
                    answer = model.generate_content(system_prompt + current_user_prompt + str(text))
                    if srt == "原始语言为首":
                        result['segments'][segment_id]['text'] = str(text) + "\n" + str(answer)
                    elif srt == "目标语言为首":
                        result['segments'][segment_id]['text'] = str(answer) + "\n" + str(text)
                    else:
                        result['segments'][segment_id]['text'] = answer
                    segment_id += 1
                    print(answer.text)

                    previous_texts.append(text)
                    if len(previous_texts) > context_size:
                        previous_texts.pop(0)

                    time.sleep(wait_time)
            else:
                print("- Request 请求调用（适用于代理模式，若不想使用Request模式，请把BASE_URL留空！)")
                print(f"\033[1;34m🌐 代理地址: {base_url}\033[0m")
                print(f"\033[1;34m📝 翻译内容: \033[0m")
                segment_id = 0
                segments = result['segments']

                context_size = 2
                previous_texts = []
                original_user_prompt = user_prompt

                for segment in segments:
                    text = segment['text']

                    if len(previous_texts) > 0:
                        combined_text = "\n".join(previous_texts[-context_size:]) + "\n"
                    else:
                        combined_text = text
                    current_user_prompt = original_user_prompt.replace("{combined_text}", combined_text)

                    payload = json.dumps({
                        "model": model,
                        "messages": [
                            {
                                "role": "system",
                                "content": system_prompt
                            },
                            {
                                "role": "user",
                                "content": current_user_prompt + str(text)
                            }
                        ],
                        "temperature": 0.8
                    })
                    headers = {
                        'Content-Type': 'application/json',
                        'Authorization': api_key
                    }
                    response = requests.request("POST", base_url, headers=headers, data=payload)
                    answer = response.json()
                    try:
                        answer = answer["choices"][0]["message"]["content"]
                        if srt == "原始语言为首":
                            result['segments'][segment_id]['text'] = str(text) + "\n" + str(answer)
                        elif srt == "目标语言为首":
                            result['segments'][segment_id]['text'] = str(answer) + "\n" + str(text)
                        else:
                            result['segments'][segment_id]['text'] = answer
                        segment_id += 1
                        print(answer.text)

                        previous_texts.append(text)
                        if len(previous_texts) > context_size:
                            previous_texts.pop(0)

                        time.sleep(wait_time)
                    except Exception as e:
                        print("\n\033[1;31m------- 请阅读下方报错内容 -------\033[0m\n")
                        print(f"\033[1;31m❌ 发生错误: {type(e).__name__}\033[0m")
                        print(f"\033[1;33m💬 错误详情: \033[0m\n{answer}\n")
                        print("\033[1;31m------- 请根据报错内容检查你的 API Key 或代理配置 -------\033[0m\n")
                        raise e

        else:
            print(f"\033[1;34m📝 翻译内容: \033[0m")
            client = OpenAI(api_key=api_key, base_url=base_url)
            segment_id = 0
            segments = result['segments']

            context_size = 2
            previous_texts = []
            original_user_prompt = user_prompt

            for segment in segments:
                text = segment['text']

                if len(previous_texts) > 0:
                    combined_text = "\n".join(previous_texts[-context_size:]) + "\n"
                else:
                    combined_text = text
                current_user_prompt = original_user_prompt.replace("{combined_text}", combined_text)

                response = client.chat.completions.create(
                    model=model,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": current_user_prompt + str(text)}
                    ])
                answer = response.choices[0].message.content

                if srt == "原始语言为首":
                    result['segments'][segment_id]['text'] = str(text) + "\n" + str(answer)
                elif srt == "目标语言为首":
                    result['segments'][segment_id]['text'] = str(answer) + "\n" + str(text)
                else:
                    result['segments'][segment_id]['text'] = answer
                segment_id += 1
                print(answer)

                previous_texts.append(text)
                if len(previous_texts) > context_size:
                    previous_texts.pop(0)

                time.sleep(wait_time)
    return result


def local_translate(system_prompt, user_prompt, api_key, base_url, model, result, srt):
    print("\n\033[1;35m*** 本地大模型翻译模式 ***\033[0m\n")
    print(f"\033[1;34m🈴 翻译模型: {model}\033[0m")
    print(f"\033[1;34m📝 翻译内容: \033[0m")
    client = OpenAI(api_key=api_key, base_url=base_url)
    segments = result['segments']
    segment_id = 0

    context_size = 2
    previous_texts = []
    original_user_prompt = user_prompt

    for segment in segments:
        text = segment['text']

        if len(previous_texts) > 0:
            combined_text = "\n".join(previous_texts[-context_size:]) + "\n"
        else:
            combined_text = text
        current_user_prompt = original_user_prompt.replace("{combined_text}", combined_text)

        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": current_user_prompt + str(text)}
            ])

        answer = response.choices[0].message.content
        if srt == "原始语言为首":
            result['segments'][segment_id]['text'] = str(text) + "\n" + str(answer)
        elif srt == "目标语言为首":
            result['segments'][segment_id]['text'] = str(answer) + "\n" + str(text)
        else:
            result['segments'][segment_id]['text'] = answer
        segment_id += 1
        print(answer)

        previous_texts.append(text)
        if len(previous_texts) > context_size:
            previous_texts.pop(0)

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


def generate_srt_from_result_2(result, font, font_size, font_color):  # 格式化为SRT字幕的形式
    segments = result['segments']
    srt_content = ''
    segment_id = 1
    for segment in segments:
        start_time = int(segment['start'] * 1000)
        end_time = int(segment['end'] * 1000)
        text = segment['text']

        srt_content += f"{segment_id}\n"
        srt_content += f"{milliseconds_to_srt_time_format(start_time)} --> {milliseconds_to_srt_time_format(end_time)}\n"
        srt_content += f"<font color={font_color}><font face={font}><font size={font_size}> {text}\n\n"
        segment_id += 1
    return srt_content


def check_cuda_installed():
    if torch.cuda.is_available():
        return True
    else:
        return False

def check_ffmpeg_hwaccel():
    try:
        result = subprocess.run(["ffmpeg", "-hwaccels"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        hwaccels = result.stdout.splitlines()
        if 'cuda' in hwaccels:
            return True
        else:
            return False
    except Exception as e:
        return False


def srt_mv(log, name, crf, quality, setting, path, font, font_size, font_color, subtitle_model):  # 视频合成字幕
    font_color = font_color.lstrip('#')  # 去掉 '#' 符号
    bb = font_color[4:6]
    gg = font_color[2:4]
    rr = font_color[0:2]
    font_color = f"&H{bb}{gg}{rr}&"
    cuda_installed = check_cuda_installed()
    cuda_supported = check_ffmpeg_hwaccel() if cuda_installed else False

    if subtitle_model == "硬字幕":
        if cuda_supported:
            command = f"""ffmpeg -loglevel {log} -hwaccel cuda -i {name} -lavfi "subtitles=output.srt:force_style='FontName={font},FontSize={font_size},PrimaryColour={font_color},Outline=1,Shadow=0,BackColour=&H9C9C9C&,Bold=-1,Alignment=2'" -preset {quality} -c:v {setting} -crf {crf} -y -c:a copy output.mp4"""
        else:
            command = f"""ffmpeg -loglevel {log} -i {name} -lavfi "subtitles=output.srt:force_style='FontName={font},FontSize={font_size},PrimaryColour={font_color},Outline=1,Shadow=0,BackColour=&H9C9C9C&,Bold=-1,Alignment=2'" -preset {quality} -c:v libx264 -crf {crf} -y -c:a copy output.mp4"""
    else:
        if cuda_supported:
            command = f"""ffmpeg -loglevel {log} -hwaccel cuda -i {name} -i output_with_style.srt -c:v {setting} -crf {crf} -y -c:a copy -c:s mov_text -preset {quality} output.mp4"""
        else:
            command = f"""ffmpeg -loglevel {log} -i {name} -i output_with_style.srt -c:v libx264 -crf {crf} -y -c:a copy -c:s mov_text -preset {quality} output.mp4"""

    subprocess.run(command, shell=True, cwd=path)


def parse_srt_file(srt_content, srt_setting="关闭"):
    lines = srt_content.strip().split('\n')
    subtitles = []

    if srt_setting == "关闭":
        current_subtitle = {'索引': '', '起始': '', '结束': '', '字幕': ''}
    else:
        current_subtitle = {'索引': '', '起始': '', '结束': '', '字幕': '', '翻译字幕': ''}

    for line in lines:
        line = line.strip()

        if line.isdigit():
            if current_subtitle['索引']:
                subtitles.append(current_subtitle)
            if srt_setting == "关闭":
                current_subtitle = {'索引': str(line), '起始': '', '结束': '', '字幕': ''}
            else:
                current_subtitle = {'索引': str(line), '起始': '', '结束': '', '字幕': '', '翻译字幕': ''}
        elif '-->' in line:
            start_time, end_time = line.split('-->')
            current_subtitle['起始'] = start_time.strip()
            current_subtitle['结束'] = end_time.strip()
        elif line != '':
            if srt_setting == "关闭":
                current_subtitle['字幕'] += line + ' '
            elif srt_setting == "原始语言为首":
                if not current_subtitle['字幕']:
                    current_subtitle['字幕'] = line
                else:
                    current_subtitle['翻译字幕'] = line
            elif srt_setting == "目标语言为首":
                if not current_subtitle['翻译字幕']:
                    current_subtitle['翻译字幕'] = line
                else:
                    current_subtitle['字幕'] = line

    if current_subtitle['索引']:
        subtitles.append(current_subtitle)

    df = pd.DataFrame(subtitles)
    return df


def convert_to_srt(edited_data, srt_setting="关闭"):
    subtitles = ''
    for index, row in edited_data.iterrows():
        start_time = row['起始']
        end_time = row['结束']

        if srt_setting == "关闭":
            content = row.get('字幕', '')
            subtitle = f"{index + 1}\n{start_time} --> {end_time}\n{content.strip()}\n\n"
        elif srt_setting == "原始语言为首":
            content1 = row.get('字幕', '')
            content2 = row.get('翻译字幕', '')
            subtitle = f"{index + 1}\n{start_time} --> {end_time}\n{content1}\n{content2}\n\n"
        elif srt_setting == "目标语言为首":
            content1 = row.get('字幕', '')
            content2 = row.get('翻译字幕', '')
            subtitle = f"{index + 1}\n{start_time} --> {end_time}\n{content2}\n{content1}\n\n"

        subtitles += subtitle
    return subtitles


def show_video(path, name):
    video_file = open(path + "/" + name, 'rb')
    video_bytes = video_file.read()
    return video_bytes


def add_font_settings(srt_content, font_color, font_face, font_size, srt_setting="关闭"):
    timestamp_pattern = re.compile(r"(\d{2}:\d{2}:\d{2},\d{3} --> \d{2}:\d{2}:\d{2},\d{3})")
    lines = srt_content.split("\n")
    result = []
    is_translation = False

    for line in lines:
        if line.isdigit():
            result.append(line)
            is_translation = False
        elif timestamp_pattern.match(line):
            result.append(line)
            is_translation = False
        elif line.strip() == "":
            result.append(line)
            is_translation = False
        else:
            if srt_setting == "关闭":
                formatted_line = f'<font color="{font_color}" face="{font_face}" size="{font_size}">{line}</font>'
                result.append(formatted_line)
            elif srt_setting == "原始语言为首":
                if not is_translation:
                    formatted_line = f'<font color="{font_color}" face="{font_face}" size="{font_size}">{line}</font>'
                    is_translation = True
                else:
                    formatted_line = f'<font color="{font_color}" face="{font_face}" size="{font_size}">{line}</font>'
                result.append(formatted_line)
            elif srt_setting == "目标语言为首":
                if not is_translation:
                    formatted_line = f'<font color="{font_color}" face="{font_face}" size="{font_size}">{line}</font>'
                    is_translation = True
                else:
                    formatted_line = f'<font color="{font_color}" face="{font_face}" size="{font_size}">{line}</font>'
                result.append(formatted_line)
    return "\n".join(result)


def srt_to_vtt(srt_content):

    blocks = srt_content.strip().split('\n\n')
    vtt_lines = ['WEBVTT\n']

    for block in blocks:
        lines = block.strip().split('\n')

        if len(lines) >= 2:
            time_range = lines[1].replace(',', '.')
            text = '\n'.join(lines[2:])
            vtt_lines.append(f'{time_range}\n{text}\n')
    vtt_content = '\n'.join(vtt_lines)

    return vtt_content


def srt_to_ass(srt_content, fontname="Arial", size=20, color="&H00FFFFFF"):

    lines = srt_content.strip().split('\n\n')
    ass_header = (
        '[Script Info]\n'
        'Title: Converted from SRT\n'
        'ScriptType: v4.00+\n'
        'Collisions: Normal\n'
        'PlayDepth: 0\n\n'
        '[V4+ Styles]\n'
        'Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding\n'
        f'Style: Default,{fontname},{size},{color},&H000000FF,&H00000000,-1,0,0,1,1.0,0.0,2,10,10,10,1\n\n'
        '[Events]\n'
        'Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n'
    )
    ass_content = ass_header

    for line in lines:
        parts = line.strip().split('\n')
        start, end = parts[1].split(' --> ')
        start = start.replace(',', '.')
        end = end.replace(',', '.')
        text = '\\N'.join(parts[2:])
        ass_content += f'Dialogue: 0,{start},{end},Default,,0,0,0,,{text}\n'

    return ass_content


def srt_to_sbv(srt_content):

    lines = srt_content.strip().split('\n\n')
    sbv_content = ''

    for block in lines:
        parts = block.strip().split('\n')
        start, end = parts[1].split(' --> ')
        start = convert_srt_time_to_sbv(start)
        end = convert_srt_time_to_sbv(end)
        text = '\n'.join(parts[2:])
        sbv_content += f'{start},{end}\n{text}\n\n'

    return sbv_content


def convert_srt_time_to_sbv(time_str):

    hours, minutes, seconds = time_str.split(':')
    seconds, milliseconds = seconds.split(',')
    milliseconds = int(milliseconds) / 10
    sbv_time = f'{hours}:{minutes}:{seconds}.{int(milliseconds):02d}'

    return sbv_time


def local_translate_srt(system_prompt, user_prompt, api_key, base_url, model, srt_content, srt):
    print("\n\033[1;35m*** 本地大模型翻译模式 ***\033[0m\n")
    print(f"\033[1;34m🈴 翻译模型: {model}\033[0m")
    print(f"\033[1;34m📝 翻译内容: \033[0m")
    client = OpenAI(api_key=api_key, base_url=base_url)
    segment_id = 0

    context_size = 2
    previous_texts = []
    original_user_prompt = user_prompt

    for segment in srt_content:
        text = segment['text']

        if len(previous_texts) > 0:
            combined_text = "\n".join(previous_texts[-context_size:]) + "\n"
        else:
            combined_text = text
        current_user_prompt = original_user_prompt.replace("{combined_text}", combined_text)

        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": current_user_prompt + str(text)}
            ])
        answer = response.choices[0].message.content
        if srt == "原始语言为首":
            srt_content[segment_id]['text'] = str(text) + "\n" + str(answer)
        elif srt == "目标语言为首":
            srt_content[segment_id]['text'] = str(answer) + "\n" + str(text)
        else:
            srt_content[segment_id]['text'] = answer
        segment_id += 1
        print(answer)

        previous_texts.append(text)
        if len(previous_texts) > context_size:
            previous_texts.pop(0)

    return srt_content


def translate_srt(system_prompt, user_prompt, api_key, base_url, model, srt_content, wait_time, srt):
    print("\n\033[1;35m*** API 调用翻译模式 ***\033[0m\n")
    print(f"\033[1;34m🈴 翻译模型: {model}\033[0m")
    global_key, global_url, all_in_one = get_global_info()
    if all_in_one:
        print(f"\033[1;34m📝 翻译内容: \033[0m")
        print(f"\033[1;34m🌐 代理地址: {base_url}\033[0m")
        client = OpenAI(api_key=global_key, base_url=global_url)

        segment_id = 0
        context_size = 2
        previous_texts = []
        original_user_prompt = user_prompt

        for segment in srt_content:
            text = segment['text']

            if len(previous_texts) > 0:
                combined_text = "\n".join(previous_texts[-context_size:]) + "\n"
            else:
                combined_text = text
            current_user_prompt = original_user_prompt.replace("{combined_text}", combined_text)

            response = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": current_user_prompt + str(text)}
                ])
            answer = response.choices[0].message.content
            if srt == "原始语言为首":
                srt_content[segment_id]['text'] = str(text) + "\n" + str(answer)
            elif srt == "目标语言为首":
                srt_content[segment_id]['text'] = str(answer) + "\n" + str(text)
            else:
                srt_content[segment_id]['text'] = answer
            segment_id += 1
            print(answer)

            previous_texts.append(text)
            if len(previous_texts) > context_size:
                previous_texts.pop(0)

            time.sleep(wait_time)
    else:
        if "gpt" in model:
            if base_url != "https://api.openai.com/v1":
                print(f"\033[1;34m🌐 代理地址: {base_url}\033[0m")
            print(f"\033[1;34m📝 翻译内容: \033[0m")
            client = OpenAI(api_key=api_key, base_url=base_url)
            segment_id = 0

            context_size = 2
            previous_texts = []
            original_user_prompt = user_prompt

            for segment in srt_content:
                text = segment['text']

                if len(previous_texts) > 0:
                    combined_text = "\n".join(previous_texts[-context_size:]) + "\n"
                else:
                    combined_text = text
                current_user_prompt = original_user_prompt.replace("{combined_text}", combined_text)

                response = client.chat.completions.create(
                    model=model,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": current_user_prompt + str(text)}
                    ])
                answer = response.choices[0].message.content

                if srt == "原始语言为首":
                    srt_content[segment_id]['text'] = str(text) + "\n" + str(answer)
                elif srt == "目标语言为首":
                    srt_content[segment_id]['text'] = str(answer) + "\n" + str(text)
                else:
                    srt_content[segment_id]['text'] = answer
                segment_id += 1
                print(answer)

                previous_texts.append(text)
                if len(previous_texts) > context_size:
                    previous_texts.pop(0)

                time.sleep(wait_time)

        elif "claude" in model:
            if base_url != "https://api.anthropic.com/v1/messages":
                print(f"\033[1;34m🌐 代理地址: {base_url}\033[0m")
            print(f"\033[1;34m📝 翻译内容: \033[0m")
            segment_id = 0

            context_size = 2
            previous_texts = []
            original_user_prompt = user_prompt

            for segment in srt_content:
                text = segment['text']

                if len(previous_texts) > 0:
                    combined_text = "\n".join(previous_texts[-context_size:]) + "\n"
                else:
                    combined_text = text
                current_user_prompt = original_user_prompt.replace("{combined_text}", combined_text)

                client = anthropic.Anthropic(api_key=api_key, base_url=base_url)
                message = client.messages.create(
                    model=model,
                    max_tokens=1024,
                    system=system_prompt,
                    messages=[{"role": "user", "content": current_user_prompt + str(text)}])
                answer = message.content[0]['text']
                if srt == "原始语言为首":
                    srt_content[segment_id]['text'] = str(text) + "\n" + str(answer)
                elif srt == "目标语言为首":
                    srt_content[segment_id]['text'] = str(answer) + "\n" + str(text)
                else:
                    srt_content[segment_id]['text'] = answer
                segment_id += 1
                print(answer)

                previous_texts.append(text)
                if len(previous_texts) > context_size:
                    previous_texts.pop(0)

                time.sleep(wait_time)

        elif "gemini" in model:
            print(f"\033[1;34m🌐 代理地址: {base_url}\033[0m")
            if base_url is None:
                print("- Python SDK 调用（若想使用代理，请填入对应的BASE_URL后自动使用代理模式！)")
                print(f"\033[1;34m📝 翻译内容: \033[0m")
                segment_id = 0

                context_size = 2
                previous_texts = []
                original_user_prompt = user_prompt

                for segment in srt_content:
                    text = segment['text']

                    if len(previous_texts) > 0:
                        combined_text = "\n".join(previous_texts[-context_size:]) + "\n"
                    else:
                        combined_text = text
                    current_user_prompt = original_user_prompt.replace("{combined_text}", combined_text)

                    genai.configure(api_key=api_key)
                    model = genai.GenerativeModel(model)
                    answer = model.generate_content(system_prompt + current_user_prompt  + str(text))

                    if srt == "原始语言为首":
                        srt_content[segment_id]['text'] = str(text) + "\n" + str(answer)
                    elif srt == "目标语言为首":
                        srt_content[segment_id]['text'] = str(answer) + "\n" + str(text)
                    else:
                        srt_content[segment_id]['text'] = answer
                    segment_id += 1
                    print(answer.text)

                    previous_texts.append(text)
                    if len(previous_texts) > context_size:
                        previous_texts.pop(0)

                    time.sleep(wait_time)
            else:
                print("- Request 请求调用（适用于代理模式，若不想使用Request模式，请把BASE_URL留空！)")
                print(f"\033[1;34m📝 翻译内容: \033[0m")
                segment_id = 0

                context_size = 2
                previous_texts = []
                original_user_prompt = user_prompt

                for segment in srt_content:
                    text = segment['text']

                    if len(previous_texts) > 0:
                        combined_text = "\n".join(previous_texts[-context_size:]) + "\n"
                    else:
                        combined_text = text
                    current_user_prompt = original_user_prompt.replace("{combined_text}", combined_text)

                    payload = json.dumps({
                        "model": model,
                        "messages": [
                            {
                                "role": "system",
                                "content": system_prompt
                            },
                            {
                                "role": "user",
                                "content": current_user_prompt + str(text)
                            }
                        ],
                        "temperature": 0.8
                    })
                    headers = {
                        'Content-Type': 'application/json',
                        'Authorization': api_key
                    }
                    response = requests.request("POST", base_url, headers=headers, data=payload)
                    answer = response.json()
                    try:
                        answer = answer["choices"][0]["message"]["content"]
                        if srt == "原始语言为首":
                            srt_content[segment_id]['text'] = str(text) + "\n" + str(answer)
                        elif srt == "目标语言为首":
                            srt_content[segment_id]['text'] = str(answer) + "\n" + str(text)
                        else:
                            srt_content[segment_id]['text'] = answer
                        segment_id += 1
                        print(answer.text)

                        previous_texts.append(text)
                        if len(previous_texts) > context_size:
                            previous_texts.pop(0)

                        time.sleep(wait_time)
                    except Exception as e:
                        print("-------请阅读下方报错内容------\n")
                        print(f"An error occurred: {type(e).__name__}, with message: \n {answer}")
                        print("\n-------请根据报错检查你的key或者代理-------\n")
                        raise e

        else:
            print(f"\033[1;34m🌐 代理地址: {base_url}\033[0m")
            print(f"\033[1;34m📝 翻译内容: \033[0m")
            client = OpenAI(api_key=api_key, base_url=base_url)

            segment_id = 0
            context_size = 2
            previous_texts = []
            original_user_prompt = user_prompt

            for segment in srt_content:
                text = segment['text']

                if len(previous_texts) > 0:
                    combined_text = "\n".join(previous_texts[-context_size:]) + "\n"
                else:
                    combined_text = text
                current_user_prompt = original_user_prompt.replace("{combined_text}", combined_text)

                response = client.chat.completions.create(
                    model=model,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": current_user_prompt + str(text)}
                    ])
                answer = response.choices[0].message.content
                if srt == "原始语言为首":
                    srt_content[segment_id]['text'] = str(text) + "\n" + str(answer)
                elif srt == "目标语言为首":
                    srt_content[segment_id]['text'] = str(answer) + "\n" + str(text)
                else:
                    srt_content[segment_id]['text'] = answer
                segment_id += 1
                print(answer)

                previous_texts.append(text)
                if len(previous_texts) > context_size:
                    previous_texts.pop(0)

                time.sleep(wait_time)
    return srt_content


def read_srt_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        srt = file.read().split('\n\n')
        timestamp_pattern = re.compile(r"(\d{2}:\d{2}:\d{2},\d{3} --> \d{2}:\d{2}:\d{2},\d{3})")
        subtitles = []

        for block in srt:
            lines = block.split('\n')
            if len(lines) >= 3:
                num = lines[0]
                times = lines[1]
                text = "\n".join(lines[2:])

                if timestamp_pattern.match(times):
                    subtitles.append({
                        'number': num,
                        'time': times,
                        'text': text
                    })
    return subtitles


def extract_frames(video_path, output_dir, time_interval=1):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    video = cv2.VideoCapture(video_path)
    if not video.isOpened():
        print(f"\033[1;31m❌ 无法读取视频关键帧，请检查此目录是否存在:\033[0m\033[1;34m {video_path} \033[0m")
        st.toast("无法读取视频关键帧", icon=":material/release_alert:")
        st.stop()

    timestamp = 0
    while True:
        ret, frame = video.read()
        if not ret:
            break

        current_timestamp = video.get(cv2.CAP_PROP_POS_MSEC) / 1000
        if current_timestamp >= timestamp + time_interval:
            timestamp = current_timestamp
            frame_filename = os.path.join(output_dir, f'frame_{int(timestamp)}.png')
            cv2.imwrite(frame_filename, frame)
    video.release()


def write_llms(view, language, key, url, model, text, token, temp):
    print(f"\033[1;34m🈴 写作模型: {model}\033[0m")
    global_key, global_url, all_in_one = get_global_info()
    if all_in_one:

        client = OpenAI(api_key=global_key, base_url=global_url)
        print(f"\033[1;34m🌐 代理地址: {url}\033[0m")
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "你是一个知识渊博且擅长分析的写作助手。你的任务是帮助用户基于文本内容重新创作一篇文章或总结，需遵循以下要求：1. 确保文章结构合理 2. 根据用户的要求调整文章的语气、风格、视角 3.确保文章结构合理，逻辑清晰"},
                {"role": "user", "content": f"请你根据下面的文本内容写一篇{language}的文章或总结，写作时请遵循以下规则：1. 请以{view}的视角写作 2. 总篇幅不得少于{token}字 3.确保逻辑清晰、核心内容完整。文本内容：\n{text}"}
            ])
        answer = response.choices[0].message.content
        print(f"\033[1;34m📝 写作内容: \033[0m")
        print(answer)

    else:
        if "gpt" in model:
            print(f"\033[1;34m🌐 代理地址: {url}\033[0m")
            print(f"\033[1;34m📝 写作内容: \033[0m")
            client = OpenAI(api_key=key, base_url=url)
            response = client.chat.completions.create(
                model=model,
                temperature=temp,
                messages=[
                    {"role": "system", "content": "你是一个知识渊博且擅长分析的写作助手。你的任务是帮助用户基于文本内容重新创作一篇文章或总结，需遵循以下要求：1. 确保文章结构合理 2. 根据用户的要求调整文章的语气、风格、视角 3.确保文章结构合理，逻辑清晰"},
                    {"role": "user", "content": f"请你根据下面的文本内写一篇{language}的文章或总结，写作时请遵循以下规则：1. 请以{view}的视角写作 2. 总篇幅不得少于{token}字 3.确保逻辑清晰、核心内容完整。文本内容：\n{text}"}
                ]
            )
            answer = response.choices[0].message.content
            print(answer)

        elif "claude" in model:
            print(f"\033[1;34m🌐 代理地址: {url}\033[0m")
            print(f"\033[1;34m📝 写作内容: \033[0m")
            client = anthropic.Anthropic(api_key=key, base_url=url)
            message = client.messages.create(
                model=model,
                max_tokens=1024,
                temperature=temp,
                system="你是一个知识渊博且擅长分析的写作助手。你的任务是帮助用户基于文本内容重新创作一篇文章或总结，需遵循以下要求：1. 确保文章结构合理 2. 根据用户的要求调整文章的语气、风格、视角 3.确保文章结构合理，逻辑清晰",
                messages=[{"role": "user", "content": f"请你根据下面的文本内容写一篇{language}的文章或总结，写作时请遵循以下规则：1. 请以{view}的视角写作 2. 总篇幅不得少于{token}字 3.确保逻辑清晰、核心内容完整。文本内容：\n{text}"}]
            )

            answer = message.content[0]['text']

        elif "gemini" in model:
            if url is None:
                print("- Python SDK 调用：如果需要使用代理，请填写 BASE_URL，系统将自动启用代理模式！")
                print(f"\033[1;34m🌐 代理地址: {url}\033[0m")
                genai.configure(client_options={"api_key": key})
                model = genai.GenerativeModel(model)
                answer = model.generate_content("请你根据下面的文本内容写一篇{language}的文章或总结，写作时请遵循以下规则：1. 请以{view}的视角写作 2. 总篇幅不得少于{token}字 3.确保逻辑清晰、核心内容完整。文本内容：\n{text}")
                print(f"\033[1;34m📝 写作内容: \033[0m")
                print(answer)
            else:
                print("- Request 请求调用（适用于代理模式，若不想使用Request模式，请把BASE_URL留空！)")
                print(f"\033[1;34m🌐 代理地址: {url}\033[0m")
                print(f"\033[1;34m📝 写作内容: \033[0m")

                payload = json.dumps({
                    "model": model,
                    "messages": [
                        {"role": "system", "content": "你是一个知识渊博且擅长分析的写作助手。你的任务是帮助用户基于文本内容重新创作一篇文章或总结，需遵循以下要求：1. 确保文章结构合理 2. 根据用户的要求调整文章的语气、风格、视角 3.确保文章结构合理，逻辑清晰"},
                        {"role": "user", "content": f"请你根据下面的文本内容写一篇{language}的文章或总结，写作时请遵循以下规则：1. 请以{view}的视角写作 2. 总篇幅不得少于{token}字 3.确保逻辑清晰、核心内容完整。文本内容：\n{text}"}
                    ],
                    "temperature": 0.8
                })
                headers = {'Content-Type': 'application/json', 'Authorization': key}
                response = requests.request("POST", url, headers=headers, data=payload)
                answer = response.json()

                try:
                    answer = answer["choices"][0]["message"]["content"]
                    print(answer)
                except Exception as e:
                    print("\n\033[1;31m------- 请阅读下方报错内容 -------\033[0m\n")
                    print(f"\033[1;31m❌ 发生错误: {type(e).__name__}\033[0m")
                    print(f"\033[1;33m💬 错误详情: \033[0m\n{answer}\n")
                    print("\033[1;31m------- 请根据报错内容检查你的 API Key 或代理配置 -------\033[0m\n")
                    raise e

        else:
            client = OpenAI(api_key=key, base_url=url)
            response = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": "你是一个知识渊博且擅长分析的写作助手。你的任务是帮助用户基于文本内容重新创作一篇文章或总结，需遵循以下要求：1. 确保文章结构合理 2. 根据用户的要求调整文章的语气、风格、视角 3.确保文章结构合理，逻辑清晰"},
                    {"role": "user", "content": f"请你根据下面的文本内容写一篇{language}的文章或总结，写作时请遵循以下规则：1. 请以{view}的视角写作 2. 总篇幅不得少于{token}字 3.确保逻辑清晰、核心内容完整。文本内容：\n{text}"}
                ])
            answer = response.choices[0].message.content
            print(f"\033[1;34m📝 写作内容: \033[0m")
            print(answer)

    return answer


def encode_image(path):
    with open(path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')
