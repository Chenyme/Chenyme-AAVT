import os
import toml
import torch
import datetime
import subprocess
import streamlit as st
import streamlit_antd_components as sac
from openai import OpenAI
from utils.utils import (get_whisper_result, generate_srt_from_result, parse_srt_file, convert_to_srt, openai_whisper)


def audio():
    project_dir = os.path.dirname(os.path.abspath(__file__)).replace("\\", "/")
    cache_dir = project_dir + "/cache/"  # 本地缓存
    config_dir = project_dir.replace("/project", "") + "/config/"  # 配置文件

    # 加载配置
    config = toml.load(config_dir + "config.toml")
    openai_api_key = config["GPT"]["openai_key"]
    openai_api_base = config["GPT"]["openai_base"]
    kimi_api_key = config["KIMI"]["kimi_key"]
    deepseek_api_key = config["DEEPSEEK"]["deepseek_key"]
    faster_whisper_model = config["WHISPER"]["faster_whisper_model_default"]
    faster_whisper_model_local = config["WHISPER"]["faster_whisper_model_local"]
    faster_whisper_model_path = config["WHISPER"]["faster_whisper_model_local_path"]
    openai_whisper_api = config["WHISPER"]["openai_whisper_api"]

    # 页面缓存
    st.session_state.openai_base = openai_api_base
    st.session_state.openai_key = openai_api_key
    st.session_state.kimi_key = kimi_api_key
    st.session_state.deepseek_key = deepseek_api_key
    st.session_state.model_local = faster_whisper_model_local
    st.session_state.model_path = faster_whisper_model_path
    st.session_state.faster_whisper_model = faster_whisper_model
    st.session_state.openai_whisper_api = openai_whisper_api

    st.title("AI音频识别🎙️")
    tab1, tab2, tab3 = st.tabs(["音频问答", "识别设置", "识别内容"])

    # 启用设置
    opt_g = 1
    if "distil" not in faster_whisper_model or torch.cuda.is_available():
        opt_g = 0

    with tab2:
        index = 1
        if openai_whisper_api:
            index = 0
        set_model = st.selectbox("选择whisper识别模式", ("Openai-api 接口调用", "Faster-whisper 本地部署"), index=index)
        st.write('---')
        if set_model == "Faster-whisper 本地部署":
            openai_whisper_api = False
            GPU_on = st.toggle('启用GPU加速', disabled=opt_g, help='自动检测cuda、pytorch可用后开启！')  # GPU
            VAD_on = st.toggle('启用VAD辅助', help='启用语音活动检测（VAD）以过滤掉没有语音的音频部分。')  # VAD
            min_vad = st.number_input('VAD静音检测(ms)', min_value=100, max_value=5000, value=500, step=100,
                                      help="启用VAD辅助后生效！对应`min_silence_duration_ms`参数，最小静音持续时间。")
            beam_size = st.number_input('束搜索大小', min_value=1, max_value=20, value=5, step=1,
                                        help="`beam_size`参数。用于定义束搜索算法中每个时间步保留的候选项数量。束搜索算法通过在每个时间步选择最有可能的候选项来构建搜索树，并根据候选项的得分进行排序和剪枝。较大的beam_size值会保留更多的候选项，扩大搜索空间，可能提高生成结果的准确性，但也会增加计算开销。相反，较小的beam_size值会减少计算开销，但可能导致搜索过早地放弃最佳序列。")
            device = 'cuda' if GPU_on else 'cpu'
            vad = 'True' if VAD_on else 'False'
            language = ('自动识别', 'zh', 'en', 'ja', 'ko', 'it', 'de')  # language
            lang = st.selectbox('选择视频语言', language, index=0,
                                help="强制指定视频语言会提高识别准确度，但也可能会造成识别出错。")
        else:
            openai_whisper_api = True
            proxy_on = st.toggle('启用代理', help='如果你能直接访问openai.com，则无需启用。')
            whisper_prompt = st.text_input('Whisper提示词', value='Don’t make each line too long.')
            temperature = st.number_input('Whisper温度', min_value=0.0, max_value=1.0, value=0.8, step=0.1)

    with (st.sidebar):
        # 文件上传
        st.write("### 文件上传器")
        uploaded_file = st.file_uploader("请在这里上传音频文件：", type=['mp3', 'wav', 'mp4'], label_visibility="collapsed")
        if uploaded_file is not None:  # 判断是否上传成功
            st.write("文件类型:", uploaded_file.type)

        if sac.buttons([sac.ButtonsItem(label='启动识别', icon='calendar-week', color='dark')], index=None, align='center', variant='filled', use_container_width=True):
            if uploaded_file is not None:
                with st.spinner('正在加载音频缓存...'):
                    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H-%M-%S")
                    output_file = cache_dir + current_time
                    os.makedirs(output_file)
                    if uploaded_file.type == "video/mp4":
                        with open(output_file + "/uploaded.mp4", "wb") as file:
                            file.write(uploaded_file.getbuffer())
                        command = "ffmpeg -i uploaded.mp4 -vn -acodec libmp3lame -ab 320k -f mp3 output.mp3"
                        subprocess.run(command, shell=True, cwd=output_file)
                    else:
                        with open(output_file + "/output.mp3", "wb") as file:
                            file.write(uploaded_file.getbuffer())

                with st.spinner('正在识别音频内容...'):
                    if openai_whisper_api:
                        print("---\nAPI调用模式")
                        result = openai_whisper(st.session_state.openai_key, st.session_state.openai_base, proxy_on,
                                                whisper_prompt, temperature, output_file)
                        print("---\nwhisper识别内容：" + result['text'])
                    else:
                        models_option = st.session_state.faster_whisper_model
                        if st.session_state.model_local:
                            models_option = st.session_state.model_path
                        print("---\n本地调用模式\n加载模型：" + models_option)
                        result = get_whisper_result(uploaded_file, output_file, device, models_option, vad, lang, beam_size,
                                                    min_vad)
                        print("---\nwhisper识别内容：" + result['text'])

                with st.spinner('正在生成文本文件...'):
                    srt_content = generate_srt_from_result(result)  # 生成SRT字幕内容
                    with open(output_file + "/output.srt", 'w', encoding='utf-8') as srt_file:  # 将SRT内容写入SRT文件
                        srt_file.write(srt_content)

                st.session_state.srt_content1 = srt_content
                st.session_state.output = output_file
                st.session_state.text = result['text']
            else:
                st.error("请先上传音频！")

    with tab1:
        @st.experimental_dialog("设置")
        def setting():
            index_llm = {'moonshot-v1-8k': 0, 'moonshot-v1-32k': 1, 'moonshot-v1-128k': 2,
                         'deepseek-chat': 3, 'gpt-3.5-turbo': 4, 'gpt-4': 5}
            try:
                st.session_state.index = index_llm[st.session_state.translate_option]
            except:
                st.session_state.index = 4
            proxy_on = st.toggle('启用代理*', help='如果你能直接访问openai.com，则无需启用。')
            translate_option = st.selectbox('问答模型', (
                'kimi-moonshot-v1-8k', 'kimi-moonshot-v1-32k', 'kimi-moonshot-v1-128k', 'deepseek-v2', 'gpt-3.5-turbo',
                'gpt-4'), index=st.session_state.index)
            prompt = st.text_input('默认提示词', value="你的任务是基于以下音频内容和自己的知识回答用户问题。音频内容：")
            temperature = st.number_input('模型温度', min_value=0.0, max_value=1.0, value=0.8, step=0.1)
            if 'gpt' in translate_option:
                client = OpenAI(api_key=st.session_state.openai_key)
                if proxy_on:
                    client = OpenAI(api_key=st.session_state.openai_key, base_url=st.session_state.openai_base)
            elif 'kimi' in translate_option:
                translate_option = translate_option.replace('kimi-', '')
                client = OpenAI(api_key=st.session_state.kimi_key, base_url="https://api.moonshot.cn/v1")
            else:
                translate_option = "deepseek-chat"
                client = OpenAI(api_key=st.session_state.deepseek_key, base_url="https://api.deepseek.com/")
            st.session_state.translate_option = translate_option
            st.session_state.client = client
            st.session_state.prompt = prompt
            st.session_state.temperature = temperature

        messages = st.container(height=425)
        if "messages1" not in st.session_state:
            st.session_state["messages1"] = [{"role": "assistant", "content": "您对音频内容有什么疑问?"}]

        for msg1 in st.session_state.messages1:
            messages.chat_message(msg1["role"]).write(msg1["content"])

        try:
            able = False if st.session_state.text else True
        except:
            able = True

        col3, col4 = st.columns([0.95, 0.05])
        with col4:
            if "setting" not in st.session_state:
                if st.button("⚙️", use_container_width=True, help="请先上传并运行程序哦~"):
                    setting()

        with col3:
            if prompt := st.chat_input(disabled=able, placeholder="基于音频内容的Chat，您可以问任何关于音频的问题"):
                st.session_state.messages1.append({"role": "user", "content": prompt})
                messages.chat_message("user").write(prompt)
                try:
                    test = st.session_state.client
                except:
                    st.session_state.translate_option = 'gpt-3.5-turbo'
                    st.session_state.client = OpenAI(api_key=st.session_state.openai_key)
                    st.session_state.prompt = '你的任务是基于以下音频内容和自己的知识回答用户问题。音频内容：'
                    st.session_state.temperature = 0.8
                response = st.session_state.client.chat.completions.create(model=st.session_state.translate_option,
                                                                           messages=[{"role": "system",
                                                                                      "content": st.session_state.prompt + st.session_state.text},
                                                                                     {"role": "user", "content": prompt}],
                                                                           temperature=st.session_state.temperature)
                msg1 = response.choices[0].message.content
                st.session_state.messages1.append({"role": "assistant", "content": msg1})
                messages.chat_message("assistant").write(msg1)

        with tab3:
            st.caption("以下内容会在运行程序后自动显示，请运行后耐心等待！")
            try:
                st.write('##### 音轨文件🎶')
                audio_file = open(st.session_state.output + "/output.mp3", 'rb')
                audio_bytes = audio_file.read()
                st.audio(audio_bytes)
            except:
                st.write('')

            try:
                st.write('------')
                st.write('##### 字幕预览🗒️')
                st.caption("Tips：文本内容可以在左侧表格进行修改微调")
                high = st.slider('文本预览表格的高度', 100, 1000, 500, 50)
                srt_data = parse_srt_file(st.session_state.srt_content1)
                edited_data = st.data_editor(srt_data, height=high, hide_index=True, use_container_width=True)
                srt = convert_to_srt(edited_data)
                st.download_button(
                    label="下载修改的文件（SRT格式）",
                    data=srt.encode('utf-8'),
                    file_name='output_new.txt'
                )
            except:
                st.write('')
