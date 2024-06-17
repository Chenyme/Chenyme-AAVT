import os
import re
import cv2
import toml
import torch
import base64
import datetime
import subprocess
import streamlit as st
import streamlit_antd_components as sac
from openai import OpenAI
from faster_whisper import WhisperModel


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


def extract_frames(video_path, output_dir):
    video = cv2.VideoCapture(video_path)
    timestamp = 0
    while True:
        ret, frame = video.read()
        if not ret:
            break
        current_timestamp = video.get(cv2.CAP_PROP_POS_MSEC) / 1000  # 转换为秒
        if int(current_timestamp) > timestamp:
            timestamp = int(current_timestamp)
            cv2.imwrite(f'{output_dir}/frame_{timestamp}.png', frame)
    video.release()


def mp4_to_mp3(path):
    try:
        command = f"ffmpeg -loglevel error -i uploaded.mp4 -vn -acodec libmp3lame -ab 320k -f mp3 output_audio.mp3"
        subprocess.run(command, shell=True, cwd=path)
    except:
        raise EOFError("错误！可能是 FFmpeg 未被正确配置 或 上传文件格式不受支持！")
    return path + '/output_audio.mp3'


def openai_whisper(key, base, prompt, tem, path):
    client = OpenAI(api_key=key, base_url=base)
    audio_file = open(path, "rb")
    transcript = client.audio.transcriptions.create(
        model="whisper-1",
        file=audio_file,
        response_format="verbose_json",
        timestamp_granularities=["segment"],
        prompt=prompt,
        temperature=tem)
    result = {'text': transcript.text, 'segments': transcript.segments}
    return result


def faster_whisper(file_path, device, model_name, prompt, temp, vad, lang):
    model = WhisperModel(model_name, device)
    if lang == "自动识别" and vad is False:
        segments, _ = model.transcribe(file_path,
                                       initial_prompt=prompt,
                                       temperature=temp
                                       )
    elif lang == "自动识别" and vad is True:
        segments, _ = model.transcribe(file_path,
                                       initial_prompt=prompt,
                                       vad_filter=vad,
                                       temperature=temp
                                       )
    elif vad is False:
        segments, _ = model.transcribe(file_path,
                                       initial_prompt=prompt,
                                       language=lang,
                                       temperature=temp
                                       )
    elif vad is True:
        segments, _ = model.transcribe(file_path,
                                       initial_prompt=prompt,
                                       language=lang,
                                       vad_filter=vad,
                                       temperature=temp
                                       )

    segments = list(segments)
    result = {
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
    return result


def openai_api(key, base, model, text, tem, system_message):
    client = OpenAI(api_key=key, base_url=base)
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": text}
        ],
        temperature=tem)
    answer = response.choices[0].message.content
    return answer


def encode_image(path):
    with open(path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')


def avtb():
    project_dir = os.path.dirname(os.path.abspath(__file__)).replace("\\", "/")
    cache_dir = project_dir + "/output/"
    config_dir = project_dir.replace("AVTB", "") + "config/api.toml"
    config = toml.load(config_dir)
    st.session_state.base_url = config["GPT"]["openai_base"]
    st.session_state.api_key = config["GPT"]["openai_key"]
    model_dir = project_dir.replace("project/AVTB", "model")

    with st.sidebar:
        st.write("#### 视频上传器")
        uploaded_file = st.file_uploader("请在这里上传视频：", type=['mp4', 'mov'], label_visibility="collapsed")
        sac.buttons(items=[sac.ButtonsItem(label='来给我一颗星叭！', icon='github', href='https://github.com/Chenyme/Chenyme_AVTB_Demo')], variant='dashed', index=None, direction='vertical', use_container_width=True, align='center', color='dark')

    st.subheader("视频生成博客")
    st.caption("AI Video To Blog")
    sac.divider(label='POWERED BY @CHENYME', icon="lightning-charge", align='center', color='gray', key="9")
    with st.expander("**识别设置**", expanded=True):
        name = st.text_input("**文章人称视角：**", value="视频作者")
        model = st.selectbox("**Whisper模式**", ("OpenAI-API 接口调用", "Faster-Whisper 本地部署"), index=1,
                             help="`OpenAI-API 接口调用`：使用OpenAI的官方接口进行识别，文件限制25MB（不是上传视频文件，是该项目转换后的音频文件，可以前往Cache查看每次的大小），过大会导致上传失败\n\n`Faster-Whisper 本地部署`：本地识别字幕，无需担心大小限制。请注意，若网络不佳请启用下方的本地模型加载")
        if model == "OpenAI-API 接口调用":
            openai_whisper_api = True
            local_on = False

        else:
            openai_whisper_api = False
            local_on = st.checkbox('**本地加载模型**', value=True, help="使用本地下载好的模型进行转录")

        if not openai_whisper_api:
            col3, col4, col5 = st.columns(3)
            with col3:
                gpu = st.toggle('**GPU加速**', disabled=not torch.cuda.is_available(), help='cuda、pytorch正确后才可使用！')
                vad = st.toggle('**VAD辅助**', help='启用语音活动检测（VAD）以过滤掉没有语音的音频部分')

            with col4:
                language = ['自动识别', 'zh', 'en', 'ja', 'ko', 'fr', 'it', 'de', 'th', 'pt', 'ar']  # language
                lang = st.selectbox('**视频语言**', language,
                                    help="强制指定视频语言会提高识别准确度，但也可能会造成识别出错。\n\n 'zh' - 中文 (Chinese) \n\n'en' - 英语 (English) \n\n 'ja' - 日本語 (Japanese) \n\n 'ko' - 한국어 (Korean) \n\n 'fr' - français (French) \n\n 'it' - Italiano (Italian) \n\n 'de' - Deutsch (German) \n\n 'th' - ภาษาไทย (Thai) \n\n 'pt' - Português (Portuguese) \n\n 'ar' - اللغة العربية (Arabic)")
            with col5:
                if local_on:
                    model_names = os.listdir(model_dir)
                    local_option = st.selectbox('**本地模型**', model_names, index=0,
                                                    help="模型下载：https://huggingface.co/Systran")
                elif not local_on:
                    options = {
                        'faster-whisper': {'models': {'tiny': 0, 'tiny.en': 1, 'base': 2, 'base.en': 3, 'small': 4,
                                                      'small.en': 5, 'medium': 6, 'medium.en': 7, 'large-v1': 8,
                                                      'large-v2': 9, 'large-v3': 10, 'large': 11, 'distil-small.en': 12,
                                                      'distil-medium.en': 13, 'distil-large-v2': 14,
                                                      'distil-large-v3': 15}}}
                    model_option = st.selectbox('**识别模型**', list(options['faster-whisper']['models'].keys()),
                                                help="推荐large模型")
        col3, col4, col5 = st.columns(3)
        with col3:
            base_url = st.text_input("**BASE_URL：**", value=st.session_state.base_url)
        with col4:
            api_key = st.text_input("**API_KEY：**", value=st.session_state.api_key)
        with col5:
            temperature = st.number_input("**模型温度：**", min_value=0.0, max_value=1.0, value=0.8, step=0.1)

        st.write("")
        if st.button("开始生成叭", type="primary", use_container_width=True):
            if uploaded_file is not None:
                current_time = datetime.datetime.now().strftime("%Y-%m-%d %H-%M-%S")
                photos_path = cache_dir + current_time + '/'
                st.session_state.photos_path = photos_path
                os.makedirs(photos_path)

                with open(photos_path + "/uploaded.mp4", "wb") as file:
                    file.write(uploaded_file.getbuffer())

                # 对视频每一秒提取一张视频截图
                print("正在提取视频帧...")
                extract_frames(photos_path + "/uploaded.mp4", photos_path)
                st.toast("视频帧提取完成！")
                print("视频帧提取完成！\n")

                # Whisper生成文本
                print("正在提取文本...")
                audio_path = mp4_to_mp3(photos_path)
                if openai_whisper_api:
                    result = openai_whisper(api_key, base_url, "Nice to meet you!", 0.8, audio_path)
                else:
                    device = 'cuda' if gpu else 'cpu'
                    try:
                        model = model_option
                    except:
                        model = local_option
                    result = faster_whisper(audio_path, device, model, "Nice to meet you!", temperature, vad, lang)

                st.toast("文本提取完成！")
                print("文本提取完成！\n")

                # GPT4o生成文章
                text = result['text']
                content = openai_api(api_key, base_url, "gpt-4o",
                                     "请你将下面的内容，以" + name + "的时间写成一篇文章" + text,
                                     temperature, "你是一位写作高手！")

                # GPT4o选择适合的图片
                print("正在选择图片...")
                num = len(os.listdir(photos_path))
                srt_content = generate_srt_from_result(result)
                choose_photos = openai_api(api_key, base_url, "gpt-4o", "现在有一个视频文件，约：" + str(
                    num) + "秒，现在它被提取出每秒钟的截图并以frame_1的格式依次命名,即" + str(
                    num) + "张图片。现在，请仔细阅读下面的字幕内容，根据下面的srt字幕的内容，返回你认为写一篇关于该字幕的博客的最重要的几个秒数（对应的图片，并仔细检查选择图片名称是否超过，第" + str(
                    num) + "张），请你仔细选择最重要的图片，不要太多，因为我将会把这几个图片作为我的博客的图片内容，请给出你认为最重要的几张图片，你的回答只需给出['frame_1'，'frame_30'，'frame_46']这样的list格式！\n字幕内容：" + srt_content,
                                           temperature, "你是一位完全听从用户的博客助手！")
                list_result = eval(choose_photos)
                list_result = [item + '.png' for item in list_result]

                all_files = os.listdir(photos_path)
                for name in list_result:
                    if name not in all_files:
                        st.warning("选择图片出现错误！")
                        st.stop()

                for file in all_files:
                    if file not in list_result:
                        os.remove(os.path.join(photos_path, file))
                st.toast("图片选择完成！")
                print("图片选择完成！\n")

                # 图片转base64
                print("正在合并最终文章...")
                image_list = [{"type": "text",
                               "text": "请以" + name + "的视角写一篇基于下面内容的博客，选择你认为重要的图片插入到文章合适的地方，你只需要返回markdown格式代码，文章的排版必须高质量，逻辑清晰、引人入胜。图片尽可能不要相邻，图片从前到后的名称依次为" + str(
                                   list_result) + "，文本内容如下：" + content}]
                for i in range(len(list_result)):
                    image_path = photos_path + list_result[i]
                    base64_image = encode_image(image_path)
                    image_list.append({
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}",
                        }})

                # GPT4o生成博客
                client = OpenAI(api_key=api_key, base_url=base_url)
                response = client.chat.completions.create(
                    model="gpt-4o",
                    messages=[{"role": "user", "content": image_list}],
                    temperature=temperature
                )
                answer = response.choices[0].message.content
                st.toast("文章已生成完毕！")
                print("文章已生成完毕！\n" + "文章内容:\n" + answer)

                answer = answer.replace("```markdown\n", "")
                answer = answer.rstrip("`")

                with open(photos_path + 'output.md', 'w', encoding='utf-8') as file:
                    file.write(answer)
                st.session_state.success = False
                st.session_state.answer = answer
            else:
                st.warning("请先上传视频文件！")

    sac.divider(label='结果运行后，将在下方显示', align='center', color='gray')

    try:
        st.write("")
        answer = st.session_state.answer

        st.write("")
        if st.button('打开文章目录', use_container_width=True):
            os.startfile(st.session_state.photos_path)
            st.warning("注意：文件夹已成功打开，可能未置顶显示，请检查任务栏！")

        pattern = r'!\[.*?\]\((.*?)\)'
        matches = re.findall(pattern, answer)
        parts = re.split(pattern, answer)

        for part in parts:
            if part in matches:
                part = part.strip('(').replace(')', '')
                st.image(st.session_state.photos_path + part, width=500)
            else:
                st.markdown(part)

        st.write("")
        sac.divider(label='文章结束', align='center', color='gray')
    except:
        st.title("")
