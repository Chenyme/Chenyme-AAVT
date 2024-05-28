import os
import toml
import time
import torch
import datetime
import streamlit as st
import streamlit_antd_components as sac
from openai import OpenAI
from .utils.utils2 import (openai_whisper_result, faster_whisper_result, file_to_mp3, check_ffmpeg, check_cuda_support)


def content():
    project_dir = os.path.dirname(os.path.abspath(__file__)).replace("\\", "/")
    config_dir = project_dir + "/config/"  # 配置文件
    cache_dir = project_dir + "/cache/"  # 本地缓存
    model_dir = project_dir.replace("project", "model")

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

    content_config = toml.load(config_dir + "content.toml")  # 加载video配置
    openai_whisper_api = content_config["WHISPER"]["openai_whisper_api"]  # openai_whisper配置
    faster_whisper_model = content_config["WHISPER"]["faster_whisper_model_default"]  # faster_whisper配置
    faster_whisper_local = content_config["WHISPER"]["faster_whisper_model_local"]  # 本地模型加载
    faster_whisper_local_path = content_config["WHISPER"]["faster_whisper_model_local_path"]  # 本地模型路径
    gpu_setting = content_config["WHISPER"]["gpu"]
    beam_size_setting = content_config["MORE"]["beam_size"]
    temperature_setting = content_config["MORE"]["temperature"]
    log_setting = content_config["MORE"]["log"]

    options = {'faster-whisper': {'models': {'tiny': 0, 'tiny.en': 1, 'base': 2, 'base.en': 3, 'small': 4,
                                             'small.en': 5, 'medium': 6, 'medium.en': 7, 'large-v1': 8,
                                             'large-v2': 9, 'large-v3': 10, 'large': 11, 'distil-small.en': 12,
                                             'distil-medium.en': 13, 'distil-large-v2': 14,
                                             'distil-large-v3': 15}}}

    st.subheader("AI 内容问答助手")
    st.caption("AI Content Q&A Assistant")

    with st.sidebar:
        uploaded_file = st.file_uploader("请在这里上传文件：", type=["mp3", "mpga", "m4a", "wav", 'mp4', 'mov', 'avi', 'm4v', 'webm', 'flv', 'ico'], label_visibility="collapsed")

    name = sac.segmented(
        items=[
            sac.SegmentedItem(label="参数设置", icon="gear-wide-connected"),
            sac.SegmentedItem(label="内容问答", icon="file-check"),
            sac.SegmentedItem(label="GitHub", icon="github", href="https://github.com/Chenyme/Chenyme-AAVT"),
        ], align='center', size='sm', radius=20, color='red', divider=False, use_container_width=True
    )

    if name == "参数设置":
        col1, col2 = st.columns([0.65, 0.35], gap="medium")
        with col1:
            with st.expander("**识别设置**", expanded=True):
                model = st.selectbox("Whisper模式", ("OpenAI-API 接口调用", "Faster-Whisper 本地部署"), index=0 if openai_whisper_api else 1, help="`OpenAI-API 接口调用`：使用OpenAI的官方接口进行识别，文件限制25MB（不是上传视频文件，是该项目转换后的音频文件，可以前往Cache查看每次的大小），过大会导致上传失败\n\n`Faster-Whisper 本地部署`：本地识别字幕，无需担心大小限制。请注意，若网络不佳请启用下方的本地模型加载")
                if model == "OpenAI-API 接口调用":
                    openai_whisper_api = True
                    content_config["WHISPER"]["openai_whisper_api"] = openai_whisper_api
                    local_on = False
                    content_config["WHISPER"]["faster_whisper_model_local"] = local_on

                else:
                    col3, col4 = st.columns(2, gap="medium")
                    openai_whisper_api = False
                    content_config["WHISPER"]["openai_whisper_api"] = openai_whisper_api
                    with col3:
                        local_on = st.checkbox('本地模型', faster_whisper_local, help="使用本地下载好的模型进行转录")
                    content_config["WHISPER"]["faster_whisper_model_local"] = local_on

                if not openai_whisper_api:
                    with col4:
                        gpu = st.checkbox('GPU加速', disabled=not torch.cuda.is_available(), help='cuda、pytorch正确后才可使用！', value=gpu_setting)
                        content_config["WHISPER"]["gpu"] = gpu

                    if local_on:
                        model_names = os.listdir(model_dir)
                        path = faster_whisper_local_path

                        try:
                            index_model = model_names.index(path.replace(model_dir + '/', ''))
                            local_option = st.selectbox('本地模型', model_names, index=index_model, help="模型下载：https://huggingface.co/Systran")
                        except:
                            local_option = st.selectbox('本地模型', model_names, index=0, help="模型下载：https://huggingface.co/Systran")
                        local_model_path = model_dir + '/' + local_option
                        content_config["WHISPER"]["faster_whisper_model_local_path"] = local_model_path

                    elif not local_on:
                        model_option = st.selectbox('识别模型', list(options['faster-whisper']['models'].keys()), index=options['faster-whisper']['models'][faster_whisper_model], help="推荐large模型")
                        content_config["WHISPER"]["faster_whisper_model_default"] = model_option

            with st.expander("**高级设置**", expanded=True):
                beam_size = st.number_input("束搜索大小", min_value=1, max_value=20, value=beam_size_setting, step=1, disabled=openai_whisper_api, help="`beam_size`参数。用于定义束搜索算法中每个时间步保留的候选项数量。束搜索算法通过在每个时间步选择最有可能的候选项来构建搜索树，并根据候选项的得分进行排序和剪枝。较大的beam_size值会保留更多的候选项，扩大搜索空间，可能提高生成结果的准确性，但也会增加计算开销。相反，较小的beam_size值会减少计算开销，但可能导致搜索过早地放弃最佳序列。")
                temperature = st.number_input("Whisper温度", min_value=0.0, max_value=1.0, value=temperature_setting, step=0.1, help="Whisper转录时模型温度，越大随机性（创造性）越高。")
                log = st.selectbox("FFmpeg-日志级别", ["quiet", "panic", "fatal", "error", "warning", "info", "verbose", "debug", "trace"], index=["quiet", "panic", "fatal", "error", "warning", "info", "verbose", "debug", "trace"].index(log_setting), help="FFmpeg输出日志。\n- **quiet**：没有输出日志。\n- **panic**：仅在不可恢复的致命错误发生时输出日志。\n- **fatal**：仅在致命错误发生时输出日志。\n- **error**：在错误发生时输出日志。\n- **warning**：在警告级别及以上的事件发生时输出日志。\n- **info**：在信息级别及以上的事件发生时输出日志。\n- **verbose**：输出详细信息，包括调试和信息级别的日志。\n- **debug**：输出调试信息，非常详细的日志输出。\n- **trace**：最详细的日志输出，用于极其详细的调试。")

                content_config["MORE"]["beam_size"] = beam_size
                content_config["MORE"]["temperature"] = temperature
                content_config["MORE"]["log"] = log

        with col2:
            if st.button("保存所有参数", type="primary", use_container_width=True):
                sac.divider(label='**参数提示**', icon='activity', align='center', color='gray')
                with open(config_dir + '/content.toml', 'w', encoding='utf-8') as file:
                    toml.dump(content_config, file)
                sac.alert(
                    label='**参数设置 已保存**',
                    description='**所有参数全部保存完毕**',
                    size='lg', radius=20, icon=True, closable=True, color='success')
            else:
                sac.divider(label='**参数提示**', icon='activity', align='center', color='gray')
                sac.alert(
                    label='**参数设置 可能未保存**',
                    description='重新设置后请点击保存',
                    size='lg', radius=20, icon=True, closable=True, color='error')

            if check_ffmpeg():
                if check_cuda_support():
                    sac.alert(
                        label='**FFmpeg GPU加速正常**',
                        description='FFmpeg**加速可用**',
                        size='lg', radius=20, icon=True, closable=True, color='success')
                else:
                    sac.alert(
                        label='**FFmpeg 状态正常**',
                        description='已**成功检测**到FFmpeg',
                        size='lg', radius=20, icon=True, closable=True, color='success')
            else:
                sac.alert(
                    label='**FFmpeg 状态错误**',
                    description='**未检测到**FFmpeg',
                    size='lg', radius=20, icon=True, closable=True, color='success')

            if openai_whisper_api:
                sac.alert(
                    label='**Whipser API调用已开启**',
                    description='确保**OPENAI相关配置不为空**',
                    size='lg', radius=20, icon=True, closable=True, color='warning')

            if not openai_whisper_api:
                if gpu:
                    sac.alert(
                        label='**GPU加速模式 已开启**',
                        description='**若未CUDA11请参阅[AAVT](https://zwho5v3j233.feishu.cn/wiki/OGcrwinzhi88MkkvEMVcLkDgnzc?from=from_copylink)**',
                        size='lg', radius=20, icon=True, closable=True, color='warning')

            if not openai_whisper_api:
                if local_on:
                    sac.alert(
                        label='**Whisper 本地加载已开启**',
                        description='[模型下载](https://huggingface.co/Systran) | [使用文档](https://zwho5v3j233.feishu.cn/wiki/OGcrwinzhi88MkkvEMVcLkDgnzc?from=from_copylink)',
                        size='lg', radius=20, icon=True, closable=True, color='warning')

            if not torch.cuda.is_available():
                sac.alert(
                    label='**CUDA/Pytorch 错误**',
                    description='请检查！**仅使用CPU请忽略**',
                    size='lg', radius=20, icon=True, closable=True, color='error')

            sac.divider(label='POWERED BY @CHENYME', icon="lightning-charge", align='center', color='gray', key="1")

    if name == "内容问答":
        col1, col2 = st.columns([0.75, 0.25])
        with col2:
            if st.button("开始识别", type="primary", use_container_width=True):
                if uploaded_file is not None:
                    st.session_state.video_name = "uploaded." + uploaded_file.name.split('.')[-1]
                    time1 = time.time()
                    msg = st.toast('开始生成!')
                    msg.toast('正在进行视频提取📽️')

                    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H-%M-%S")
                    output_file = cache_dir + current_time
                    os.makedirs(output_file)
                    with open(output_file + '/' + st.session_state.video_name, "wb") as file:
                        file.write(uploaded_file.getbuffer())
                    print(f"- 本次任务目录：{output_file}")
                    if uploaded_file.name.split(".")[-1] != "mp3":
                        file_to_mp3(log_setting, st.session_state.video_name, output_file)

                    time2 = time.time()
                    msg.toast('正在识别视频内容🔍')
                    if openai_whisper_api:
                        result = openai_whisper_result(openai_key, openai_base, output_file, "Don’t make each line too long.", temperature_setting)
                    else:
                        device = 'cuda' if gpu_setting else 'cpu'
                        model = faster_whisper_model
                        if faster_whisper_local:
                            model = faster_whisper_local_path
                        result = faster_whisper_result(output_file, device, model, "Don’t make each line too long.", temperature_setting, False, "自动识别", beam_size_setting, 500)
                    st.session_state.text = result["text"]
                    st.toast("已识别完成，开始对话叭！", icon=":material/task_alt:")
                else:
                    st.toast("请先上传文件！")

            with st.expander("模型选择", expanded=True):
                translate_option = sac.chip(
                    items=[
                        sac.ChipItem('gpt-3.5-turbo', icon='robot'),
                        sac.ChipItem('gpt-4-turbo', icon='robot'),
                        sac.ChipItem('gpt-4o', icon='robot'),
                        sac.ChipItem('gpt-4v', icon='robot'),
                        sac.ChipItem('moonshot-v1-8k', icon='robot'),
                        sac.ChipItem('moonshot-v1-32k', icon='robot'),
                        sac.ChipItem('moonshot-v1-128k', icon='robot'),
                        sac.ChipItem('glm-3-turbo', icon='robot'),
                        sac.ChipItem('glm-4v', icon='robot'),
                        sac.ChipItem('glm-4', icon='robot'),
                        sac.ChipItem('gpt-4o', icon='robot'),
                        sac.ChipItem('gpt-4v', icon='robot'),
                        sac.ChipItem('deepseek-chat', icon='robot'),
                        sac.ChipItem('Local', icon='robot'),
                    ], align='start', direction='vertical', radius='md', variant='filled', index=0
                )

        with col1:
            with st.popover("**对话设置**", use_container_width=True):
                height = st.number_input("对话框高度", min_value=300, step=100, value=590)
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

                if "gpt" in translate_option:
                    client = OpenAI(api_key=openai_key, base_url=openai_base)
                elif "moonshot" in translate_option:
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

        sac.divider(label='POWERED BY @CHENYME', icon="lightning-charge", align='center', color='gray', key="4")
