import os
import toml
import time
import datetime
import streamlit as st
import streamlit_antd_components as sac
from openai import OpenAI
from .utils.utils2 import (openai_whisper_result, faster_whisper_result, file_to_mp3)


def audio():
    project_dir = os.path.dirname(os.path.abspath(__file__)).replace("\\", "/")
    config_dir = project_dir + "/config/"  # 配置文件
    cache_dir = project_dir + "/cache/"  # 本地缓存

    api_config = toml.load(config_dir + "api.toml")  # 加载API配置
    openai_key = api_config["GPT"]["openai_key"]
    openai_base = api_config["GPT"]["openai_base"]
    kimi_key = api_config["KIMI"]["kimi_key"]
    kimi_base = api_config["KIMI"]["kimi_base"]
    deepseek_key = api_config["DEEPSEEK"]["deepseek_key"]
    deepseek_base = api_config["DEEPSEEK"]["deepseek_base"]
    chatglm_key = api_config["CHATGLM"]["chatglm_key"]
    chatglm_base = api_config["CHATGLM"]["chatglm_base"]
    local_key = api_config["LOCAL"]["api_key"]
    local_base = api_config["LOCAL"]["base_url"]
    local_model = api_config["LOCAL"]["model_name"]

    video_config = toml.load(config_dir + "video.toml")  # 加载video配置
    openai_whisper_api = video_config["WHISPER"]["openai_whisper_api"]  # openai_whisper配置
    faster_whisper_model = video_config["WHISPER"]["faster_whisper_model_default"]  # faster_whisper配置
    faster_whisper_local = video_config["WHISPER"]["faster_whisper_model_local"]  # 本地模型加载
    faster_whisper_local_path = video_config["WHISPER"]["faster_whisper_model_local_path"]  # 本地模型路径
    gpu_setting = video_config["WHISPER"]["gpu"]
    vad_setting = video_config["WHISPER"]["vad"]
    lang_setting = video_config["WHISPER"]["lang"]
    min_vad_setting = video_config["MORE"]["min_vad"]
    beam_size_setting = video_config["MORE"]["beam_size"]
    whisper_prompt_setting = video_config["MORE"]["whisper_prompt"]
    temperature_setting = video_config["MORE"]["temperature"]

    st.title("AI 内容问答助手")
    with st.sidebar:
        uploaded_file = st.file_uploader("请在这里上传视频：", type=["mp3", "mpga", "m4a", "wav", 'mp4', 'mov', 'avi', 'm4v', 'webm', 'flv', 'ico'], label_visibility="collapsed")

    col1, col2 = st.columns([0.3, 0.7])
    with col1:
        sac.divider("模型", align='center', color='gray')
        if st.button("开始识别", type="primary", use_container_width=True):
            if uploaded_file is not None:
                st.session_state.video_name = uploaded_file.name
                time1 = time.time()
                msg = st.toast('开始生成!')
                msg.toast('正在进行视频提取📽️')

                current_time = datetime.datetime.now().strftime("%Y-%m-%d %H-%M-%S")
                output_file = cache_dir + current_time
                os.makedirs(output_file)
                with open(output_file + '/' + uploaded_file.name, "wb") as file:
                    file.write(uploaded_file.getbuffer())
                print(f"- 本次任务目录：{output_file}")
                if uploaded_file.name.split(".")[-1] != "mp3":
                    file_to_mp3(uploaded_file.name, output_file)

                time2 = time.time()
                msg.toast('正在识别视频内容🔍')
                if openai_whisper_api:
                    result = openai_whisper_result(openai_key, openai_base, output_file, whisper_prompt_setting, temperature_setting)
                else:
                    device = 'cuda' if gpu_setting else 'cpu'
                    model = faster_whisper_model
                    if faster_whisper_local:
                        model = faster_whisper_local_path
                    result = faster_whisper_result(output_file, device, "tiny", whisper_prompt_setting, temperature_setting, vad_setting, lang_setting, beam_size_setting, min_vad_setting)
                st.session_state.text = result["text"]
            else:
                st.toast("请先上传文件！")

        with st.expander("模型选择", expanded=True):
            translate_option = sac.menu([
                sac.MenuItem('ChatGPT-OpenAI', icon='1-square-fill', children=[
                    sac.MenuItem('gpt-3.5-turbo', icon='robot'),
                    sac.MenuItem('gpt-4-turbo', icon='robot'),
                    sac.MenuItem('gpt-4o', icon='robot'),
                    sac.MenuItem('gpt-4v', icon='robot'),
                ]),
                sac.MenuItem('Kimi-月之暗面', icon='2-square-fill', children=[
                    sac.MenuItem('moonshot-v1-8k', icon='robot'),
                    sac.MenuItem('moonshot-v1-32k', icon='robot'),
                    sac.MenuItem('moonshot-v1-128k', icon='robot'),
                ]),
                sac.MenuItem('ChatGLM-智谱AI', icon='3-square-fill', children=[
                    sac.MenuItem('glm-3-turbo', icon='robot'),
                    sac.MenuItem('glm-4v', icon='robot'),
                    sac.MenuItem('glm-4', icon='robot'),
                ]),
                sac.MenuItem('DeepSeek-深度求索', icon='4-square-fill', children=[
                    sac.MenuItem('deepseek-chat', icon='robot'),
                ]),
                sac.MenuItem('Local LLMs', icon='5-square-fill', children=[
                    sac.MenuItem('Local', icon='robot'),
                ]),
            ], variant='filled', indent=30, open_all=True, index=1)

    with col2:
        sac.divider("助手", align='center', color='gray')
        with st.popover("**设置**", use_container_width=True):
            height = st.number_input("对话框高度", min_value=300, step=100, value=580)
            pre_prompt = st.text_input("Prompt", value="你是基于以下内容的BOT,请结合自身知识和内容回答用户问题，内容：\n")
            temperature_setting = st.number_input("Temperature", min_value=0.0, max_value=1., step=0.1, value=0.80)
        try:
            able = False if st.session_state.text else True
        except:
            able = True

        messages = st.container(height=height)
        if "messages1" not in st.session_state:
            st.session_state["messages1"] = [{"role": "assistant", "content": "您对上传的内容有什么疑问?"}]

        for msg1 in st.session_state.messages1:
            messages.chat_message(msg1["role"]).write(msg1["content"])

        if prompt := st.chat_input(disabled=able, placeholder="基于上传文件的的Chat，您可以问任何关于上传文件的问题"):
            st.session_state.messages1.append({"role": "user", "content": prompt})
            messages.chat_message("user").write(prompt)

            if "moonshot" in translate_option:
                client = OpenAI(api_key=kimi_key, base_url=kimi_base)
            elif "glm" in translate_option:
                client = OpenAI(api_key=chatglm_key, base_url=chatglm_base)
            elif "deepseek" in translate_option:
                client = OpenAI(api_key=deepseek_key, base_url=deepseek_base)
            elif "local" in translate_option:
                translate_option = local_model
                client = OpenAI(api_key=local_key, base_url=local_base)

            response = client.chat.completions.create(model=translate_option,
                                                      messages=[{"role": "system", "content": pre_prompt + st.session_state.text},
                                                                {"role": "user", "content": prompt}],
                                                      temperature=temperature_setting)
            msg1 = response.choices[0].message.content
            st.session_state.messages1.append({"role": "assistant", "content": msg1})
            messages.chat_message("assistant").write(msg1)
