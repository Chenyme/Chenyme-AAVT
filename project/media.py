import os
import json
import toml
import time
import torch
import datetime
import streamlit as st
import streamlit_antd_components as sac
from project.utils.utils2 import (file_to_mp3, openai_whisper_result, faster_whisper_result, translate, local_translate,
                                  generate_srt_from_result, generate_srt_from_result_2, srt_mv, show_video, parse_srt_file,
                                  convert_to_srt, srt_to_ass, srt_to_stl, srt_to_vtt, check_cuda_support, check_ffmpeg,
                                  add_font_settings)


def media():
    project_dir = os.path.dirname(os.path.abspath(__file__)).replace("\\", "/")
    config_dir = project_dir + "/config/"  # 配置文件
    cache_dir = project_dir + "/cache/"  # 本地缓存
    model_dir = project_dir.replace("project", "model")

    api_config = toml.load(config_dir + "api.toml")  # 加载配置
    gemini_key = api_config["GEMINI"]["gemini_key"]  # GEMINI
    gemini_base = api_config["GEMINI"]["gemini_base"]
    ai01_key = api_config["AI01"]["AI01_key"]  # 01
    ai01_base = api_config["AI01"]["AI01_base"]
    kimi_key = api_config["KIMI"]["kimi_key"]  # kimi
    kimi_base = api_config["KIMI"]["kimi_base"]
    chatglm_key = api_config["CHATGLM"]["chatglm_key"]  # chatglm
    chatglm_base = api_config["CHATGLM"]["chatglm_base"]
    openai_key = api_config["GPT"]["openai_key"]  # openai
    openai_base = api_config["GPT"]["openai_base"]
    claude_key = api_config["CLAUDE"]["claude_key"]  # claude
    claude_base = api_config["CLAUDE"]["claude_base"]
    deepseek_key = api_config["DEEPSEEK"]["deepseek_key"]  # deepseek
    deepseek_base = api_config["DEEPSEEK"]["deepseek_base"]
    local_key = api_config["LOCAL"]["api_key"]  # local
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
    translate_setting = video_config["TRANSLATE"]["translate_model"]
    language1_setting = video_config["TRANSLATE"]["language1"]
    language2_setting = video_config["TRANSLATE"]["language2"]
    wait_time_setting = video_config["TRANSLATE"]["wait_time"]
    prompt_pre_setting = video_config["TRANSLATE"]["prompt_pre"]
    subtitle_model_setting = video_config["SUBTITLE"]["subtitle_model"]
    font_setting = video_config["SUBTITLE"]["font"]
    soft_font_size_setting = video_config["SUBTITLE"]["soft_font_size"]
    hard_font_size_setting = video_config["SUBTITLE"]["hard_font_size"]
    font_color_setting = video_config["SUBTITLE"]["font_color"]
    srt_setting = video_config["SUBTITLE"]["srt"]
    min_vad_setting = video_config["MORE"]["min_vad"]
    beam_size_setting = video_config["MORE"]["beam_size"]
    whisper_prompt_setting = video_config["MORE"]["whisper_prompt"]
    temperature_setting = video_config["MORE"]["temperature"]
    crf_setting = video_config["MORE"]["crf"]
    quality_setting = video_config["MORE"]["quality"]
    ffmpeg_setting = video_config["MORE"]["ffmpeg"]
    log_setting = video_config["MORE"]["log"]

    with open(config_dir + 'prompt.json', 'r', encoding='utf-8') as file:
        prompt = json.load(file)  # 加载配置
    st.session_state.prompt = prompt
    system_prompt = prompt[prompt_pre_setting]["system_prompt"].replace("{language1}", language1_setting).replace("{language2}", language2_setting)
    user_prompt = prompt[prompt_pre_setting]["user_prompt"].replace("{language1}", language1_setting).replace("{language2}", language2_setting)

    options = {'faster-whisper': {'models': {'tiny': 0, 'tiny.en': 1, 'base': 2, 'base.en': 3, 'small': 4,
                                             'small.en': 5, 'medium': 6, 'medium.en': 7, 'large-v1': 8,
                                             'large-v2': 9, 'large-v3': 10, 'large': 11, 'distil-small.en': 12,
                                             'distil-medium.en': 13, 'distil-large-v2': 14,
                                             'distil-large-v3': 15}}}

    st.subheader("全自动识别翻译")
    st.caption("AI Auto Video Translation")

    name = sac.segmented(
        items=[
            sac.SegmentedItem(label="参数设置", icon="gear-wide-connected"),
            sac.SegmentedItem(label="音频识别", icon="mic"),
            sac.SegmentedItem(label="视频识别", icon="camera-video"),
            sac.SegmentedItem(label="GitHub", icon="github", href="https://github.com/Chenyme/Chenyme-AAVT"),
        ], align='center', size='sm', radius=20, color='red', divider=False, use_container_width=True
    )

    with st.sidebar:
        if name == '音频识别':
            st.write("#### 音频上传器")
            uploaded_file_audio = st.file_uploader("**音频上传器**", type=['mp3', 'wav'], label_visibility="collapsed")
        if name == '视频识别':
            st.write("#### 视频上传器")
            uploaded_file = st.file_uploader("**请在这里上传视频：**", type=['mp4', 'mov', 'avi', 'm4v', 'webm', 'flv', 'ico'], label_visibility="collapsed")

    if name == '参数设置':
        col1, col2 = st.columns([0.7, 0.3], gap="medium")
        with col1:
            with st.expander("**识别设置**", expanded=True):
                model = st.selectbox("Whisper模式", ("OpenAI-API 接口调用", "Faster-Whisper 本地部署"), index=0 if openai_whisper_api else 1, help="`OpenAI-API 接口调用`：使用OpenAI的官方接口进行识别，文件限制25MB（不是上传视频文件，是该项目转换后的音频文件，可以前往Cache查看每次的大小），过大会导致上传失败\n\n`Faster-Whisper 本地部署`：本地识别字幕，无需担心大小限制。请注意，若网络不佳请启用下方的本地模型加载")
                if model == "OpenAI-API 接口调用":
                    openai_whisper_api = True
                    video_config["WHISPER"]["openai_whisper_api"] = openai_whisper_api
                    local_on = False
                    video_config["WHISPER"]["faster_whisper_model_local"] = local_on

                else:
                    openai_whisper_api = False
                    video_config["WHISPER"]["openai_whisper_api"] = openai_whisper_api
                    local_on = st.checkbox('本地加载模型', faster_whisper_local, help="使用本地下载好的模型进行转录")
                    video_config["WHISPER"]["faster_whisper_model_local"] = local_on

                if not openai_whisper_api:
                    col3, col4, col5 = st.columns([0.3, 0.4, 0.4])
                    with col3:
                        gpu = st.toggle('GPU加速', disabled=not torch.cuda.is_available(), help='cuda、pytorch正确后才可使用！', value=gpu_setting)
                        vad = st.toggle('VAD辅助', help='启用语音活动检测（VAD）以过滤掉没有语音的音频部分', value=vad_setting)

                    with col4:
                        language = ['自动识别', 'zh', 'en', 'ja', 'ko', 'fr', 'it', 'de', 'th', 'pt', 'ar']  # language
                        index = language.index(lang_setting)
                        lang = st.selectbox('视频语言', language, index=index, help="强制指定视频语言会提高识别准确度，但也可能会造成识别出错。\n\n 'zh' - 中文 (Chinese) \n\n'en' - 英语 (English) \n\n 'ja' - 日本語 (Japanese) \n\n 'ko' - 한국어 (Korean) \n\n 'fr' - français (French) \n\n 'it' - Italiano (Italian) \n\n 'de' - Deutsch (German) \n\n 'th' - ภาษาไทย (Thai) \n\n 'pt' - Português (Portuguese) \n\n 'ar' - اللغة العربية (Arabic)")

                    with col5:
                        if local_on:
                            model_names = os.listdir(model_dir)
                            path = faster_whisper_local_path

                            try:
                                index_model = model_names.index(path.replace(model_dir + '/', ''))
                                local_option = st.selectbox('本地模型', model_names, index=index_model, help="模型下载：https://huggingface.co/Systran")
                            except:
                                local_option = st.selectbox('本地模型', model_names, index=0, help="模型下载：https://huggingface.co/Systran")
                            local_model_path = model_dir + '/' + local_option
                            video_config["WHISPER"]["faster_whisper_model_local_path"] = local_model_path

                        elif not local_on:
                            model_option = st.selectbox('识别模型', list(options['faster-whisper']['models'].keys()), index=options['faster-whisper']['models'][faster_whisper_model], help="推荐large模型")
                            video_config["WHISPER"]["faster_whisper_model_default"] = model_option

                    video_config["WHISPER"]["gpu"] = gpu
                    video_config["WHISPER"]["vad"] = vad
                    video_config["WHISPER"]["lang"] = lang

            with st.expander("**翻译设置**", expanded=True):
                translate_option = sac.cascader(items=[
                    sac.CasItem('无需翻译'),
                    sac.CasItem('本地模型', icon='house-up-fill'),
                    sac.CasItem('Gemini-Google', icon='node-plus-fill', children=[
                        sac.CasItem('gemini-pro', icon='robot'),
                        sac.CasItem('gemini-1.0-pro', icon='robot'),
                        sac.CasItem('gemini-1.5-flash', icon='robot'),
                        sac.CasItem('gemini-1.5-pro', icon='robot')]),
                    sac.CasItem('01AI-零一万物', icon='node-plus-fill', children=[
                        sac.CasItem('yi-spark', icon='robot'),
                        sac.CasItem('yi-medium', icon='robot'),
                        sac.CasItem('yi-medium-200k', icon='robot'),
                        sac.CasItem('yi-vision', icon='robot'),
                        sac.CasItem('yi-large', icon='robot'),
                        sac.CasItem('yi-large-rag', icon='robot'),
                        sac.CasItem('yi-large-turbo', icon='robot'),
                        sac.CasItem('yi-large-preview', icon='robot')]),
                    sac.CasItem('Moonshot-月之暗面', icon='node-plus-fill', children=[
                        sac.CasItem('kimi-moonshot-v1-8k', icon='robot'),
                        sac.CasItem('kimi-moonshot-v1-32k', icon='robot'),
                        sac.CasItem('kimi-moonshot-v1-128k', icon='robot')]),
                    sac.CasItem('ChatGLM-智谱AI', icon='node-plus-fill', children=[
                        sac.CasItem('glm-4', icon='robot'),
                        sac.CasItem('glm-4-0520', icon='robot'),
                        sac.CasItem('glm-4-flash', icon='robot'),
                        sac.CasItem('glm-4-air', icon='robot'),
                        sac.CasItem('glm-4-airx', icon='robot')]),
                    sac.CasItem('ChatGPT-OpenAI', icon='node-plus-fill', children=[
                        sac.CasItem('gpt-3.5-turbo', icon='robot'),
                        sac.CasItem('gpt-4', icon='robot'),
                        sac.CasItem('gpt-4-turbo', icon='robot'),
                        sac.CasItem('gpt-4o', icon='robot')]),
                    sac.CasItem('Claude-Anthropic', icon='node-plus-fill', children=[
                        sac.CasItem('claude-3-opus', icon='robot'),
                        sac.CasItem('claude-3-sonnet', icon='robot'),
                        sac.CasItem('claude-3-haiku', icon='robot')]),
                    sac.CasItem('DeepSeek-深度求索', icon='node-plus-fill', children=[
                        sac.CasItem('deepseek-chat', icon='robot'),
                        sac.CasItem('deepseek-coder', icon='robot')]),
                ], label='<span style="font-size: 14px;">翻译引擎</span>', search=True, index=translate_setting, return_index=True)

                video_config["TRANSLATE"]["translate_model"] = translate_option

                if translate_option != [0]:
                    language = ['中文', 'English', '日本語', '한국어', 'français', 'Italiano', 'Deutsch', 'ภาษาไทย', 'Português', 'اللغة العربية']

                    col3, col4, col5, col6 = st.columns(4)
                    with col3:
                        language1 = st.selectbox('原始语言', language, index=language.index(language1_setting))
                    with col4:
                        language2 = st.selectbox('目标语言', language, index=language.index(language2_setting))
                    with col5:
                        try:
                            prompt_pre_setting = st.selectbox('预设prompt', prompt.keys(), index=list(prompt.keys()).index(prompt_pre_setting))
                        except:
                            prompt_pre_setting = st.selectbox('预设prompt', prompt.keys())

                    with col6:
                        wait_time = st.number_input('翻译间隔(s)', min_value=0.0, max_value=5.0, value=wait_time_setting, step=0.1, help="每次API调用的间隔。\n\n 当你的视频比较长，字幕很多时，导致翻译时会一直反复调用 API 太多次，这会达到每分钟速率最大限制。当遇到报错429，如：`Too Many Requests`、`RateLimitError`这种速率报错，那就需要适当增大间隔。")

                    video_config["TRANSLATE"]["prompt_pre"] = prompt_pre_setting
                    video_config["TRANSLATE"]["language1"] = language1
                    video_config["TRANSLATE"]["language2"] = language2
                    video_config["TRANSLATE"]["wait_time"] = wait_time

            with st.expander("**字幕设置**", expanded=True):
                with open(config_dir + 'font_data.txt', 'r', encoding='utf-8') as file:
                    lines = file.readlines()
                    fonts = [line.strip() for line in lines]

                col3, col4 = st.columns(2)
                with col3:
                    subtitle_model = st.selectbox('字幕模式', ["硬字幕", "软字幕"], index=["硬字幕", "软字幕"].index(subtitle_model_setting), help="请注意：由于软字幕会导致部分字体会无法正常显示，因此可能会出现乱码！\n\n 同时，您无法在网页中预览字幕效果，请打开文件夹访问原视频并使用支持外挂字幕的视频播放器挂载字幕查看效果！")
                with col4:
                    font = st.selectbox('字幕字体', fonts, index=fonts.index(font_setting), help="所有字体均从系统读取加载，支持用户自行安装字体。请注意商用风险！")

                col3, col4, col5 = st.columns([0.5, 0.4, 0.1], gap="medium")
                with col3:
                    if subtitle_model == "软字幕":
                        soft_font_size = st.number_input('软字幕大小', min_value=30, max_value=90, value=soft_font_size_setting, step=1, help="推荐大小：60")
                        video_config["SUBTITLE"]["soft_font_size"] = soft_font_size
                    else:
                        hard_font_size = st.number_input('硬字幕大小', min_value=1, max_value=36, value=hard_font_size_setting, step=1, help="推荐大小：18")
                        video_config["SUBTITLE"]["hard_font_size"] = hard_font_size
                with col4:
                    srt_choose = ["关闭", "原始语言为首", "目标语言为首"]
                    srt = st.selectbox('双语字幕', srt_choose, index=srt_choose.index(srt_setting))
                with col5:
                    font_color = st.color_picker('颜色', value=font_color_setting)

                video_config["SUBTITLE"]["subtitle_model"] = subtitle_model
                video_config["SUBTITLE"]["font"] = font
                video_config["SUBTITLE"]["srt"] = srt
                video_config["SUBTITLE"]["font_color"] = font_color

            with st.expander("**高级设置**", expanded=False):
                col3, col4 = st.columns([0.5, 0.5], gap="medium")
                with col3:
                    min_vad = st.number_input("VAD静音检测(ms)", min_value=100, max_value=5000, value=min_vad_setting, step=100, disabled=openai_whisper_api, help="`min_silence_duration_ms`参数，最小静音持续时间，启用VAD辅助后生效！")
                    beam_size = st.number_input("束搜索大小", min_value=1, max_value=20, value=beam_size_setting, step=1, disabled=openai_whisper_api, help="`beam_size`参数。用于定义束搜索算法中每个时间步保留的候选项数量。束搜索算法通过在每个时间步选择最有可能的候选项来构建搜索树，并根据候选项的得分进行排序和剪枝。较大的beam_size值会保留更多的候选项，扩大搜索空间，可能提高生成结果的准确性，但也会增加计算开销。相反，较小的beam_size值会减少计算开销，但可能导致搜索过早地放弃最佳序列。")
                    whisper_prompt = st.text_input("Whisper提示词", value=whisper_prompt_setting, help="若您无更好的Whisper提示词，请勿随意修改！否则会影响断句效果")
                    temperature = st.number_input("Whisper温度", min_value=0.0, max_value=1.0, value=temperature_setting, step=0.1, help="Whisper转录时模型温度，越大随机性（创造性）越高。")
                with col4:
                    crf = st.selectbox("FFmpeg-恒定速率因子", [0, 18, 23, 28], index=[0, 18, 23, 28].index(crf_setting), help="CRF 值的范围通常为 0 到 51，数值越低，质量越高。建议值：\n- `0`: 无损压缩，质量最高，文件最大。\n- `18`: 视觉上接近无损，非常高的质量，文件较大。\n- `23`: 默认值，质量和文件大小的平衡点。\n- `28`: 较低的质量，文件较小。")
                    quality_list = ["ultrafast", "superfast", "veryfast", "faster", "fast", "medium", "slow", "slower", "veryslow", "placebo"]
                    quality = st.selectbox("FFmpeg-编码器预设(质量)", quality_list, index=quality_list.index(quality_setting), help="编码器预设(质量quality)，默认值为 `medium`。注意，下面有些值是不可使用的，若你不了解，请勿修改！可选值包括：\n- `ultrafast`: 最快的编码速度，但质量最低，文件最大。\n- `superfast`: 非常快的编码速度，质量和文件大小有所提升。\n- `veryfast`: 很快的编码速度，适用于实时编码或需要快速处理的情况。\n- `faster`: 比较快的编码速度，质量进一步提高。\n- `fast`: 快速编码速度，质量较好。\n- `medium`: 默认预设，编码速度和质量的平衡点。\n- `slow`: 较慢的编码速度，输出质量更高，文件更小。\n- `slower`: 更慢的编码速度，质量进一步提高。\n- `veryslow`: 非常慢的编码速度，质量最高，文件最小。\n- `placebo`: 极慢的编码速度，质量微小提升，不推荐使用，除非对质量有极高要求且不在意编码时间。")
                    ffmpeg = st.selectbox("FFmpeg-编码器", ["h264_nvenc", "libx264"], index=["h264_nvenc", "libx264"].index(ffmpeg_setting), help="CUDA可用时，可选择h264_nvenc。否则默认libx264，注意h264_nvenc质量过高，输出文件会很大")
                    log = st.selectbox("FFmpeg-日志级别", ["quiet", "panic", "fatal", "error", "warning", "info", "verbose", "debug", "trace"], index=["quiet", "panic", "fatal", "error", "warning", "info", "verbose", "debug", "trace"].index(log_setting), help="FFmpeg输出日志。\n- **quiet**：没有输出日志。\n- **panic**：仅在不可恢复的致命错误发生时输出日志。\n- **fatal**：仅在致命错误发生时输出日志。\n- **error**：在错误发生时输出日志。\n- **warning**：在警告级别及以上的事件发生时输出日志。\n- **info**：在信息级别及以上的事件发生时输出日志。\n- **verbose**：输出详细信息，包括调试和信息级别的日志。\n- **debug**：输出调试信息，非常详细的日志输出。\n- **trace**：最详细的日志输出，用于极其详细的调试。")

                video_config["MORE"]["min_vad"] = min_vad
                video_config["MORE"]["beam_size"] = beam_size
                video_config["MORE"]["whisper_prompt"] = whisper_prompt
                video_config["MORE"]["temperature"] = temperature
                video_config["MORE"]["crf"] = crf
                video_config["MORE"]["quality"] = quality
                video_config["MORE"]["ffmpeg"] = ffmpeg
                video_config["MORE"]["log"] = log

        with col2:
            if st.button("保存所有参数", type="primary", use_container_width=True):
                sac.divider(label='**参数提示**', icon='activity', align='center', color='gray')
                with open(config_dir + '/video.toml', 'w', encoding='utf-8') as file:
                    toml.dump(video_config, file)
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

            if not openai_whisper_api:
                if vad:
                    sac.alert(
                        label='**VAD辅助 已开启**',
                        description='将会**检测语音活动**',
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

            if translate_option == [1]:
                sac.alert(
                    label='**本地LLM调用 已开启**',
                    description="请**确保相关参数无误**",
                    size='lg', radius=20, icon=True, closable=True, color='warning')

            if subtitle_model == "软字幕":
                sac.alert(
                    label='**软字幕 已开启**',
                    description='软字幕**无法预览效果**',
                    size='lg', radius=20, icon=True, closable=True, color='warning')

            if not torch.cuda.is_available():
                sac.alert(
                    label='**CUDA/Pytorch 错误**',
                    description='请检查！**仅使用CPU请忽略**',
                    size='lg', radius=20, icon=True, closable=True, color='error')

            if ffmpeg != "libx264":
                if not check_cuda_support():
                    sac.alert(
                        label='**编码器无效 请换回libx264**',
                        description='**未检测到**h264_nvenc编码器',
                        size='lg', radius=20, icon=True, closable=True, color='error')
                else:
                    sac.alert(
                        label='**编码器设置 成功**',
                        description='**检测到**h264_nvenc编码器',
                        size='lg', radius=20, icon=True, closable=True, color='success')

            sac.divider(label='POWERED BY @CHENYME', icon="lightning-charge", align='center', color='gray', key="1")

    if name == '音频识别':
        with st.expander("Setting", expanded=True):
            col3, col4 = st.columns(2)
            with col3:
                st.write("###### 显示高度")
                height = st.number_input("字幕轴显示高度", min_value=400, step=100, value=400, label_visibility="collapsed")
                st.session_state.height = height

            with col4:
                st.write("###### 音频识别")
                if st.button("音频识别", type="primary", use_container_width=True):
                    if uploaded_file_audio is not None:
                        st.session_state.audio_name = "output." + uploaded_file_audio.name.split('.')[-1]
                        time1 = time.time()
                        st.toast('已开始生成，请不要在运行时切换菜单或修改参数!', icon=":material/person_alert:")
                        msg = st.toast('正在进行提取', icon=":material/play_circle:")

                        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H-%M-%S")
                        output_file = cache_dir + current_time
                        os.makedirs(output_file)
                        with open(output_file + '/' + st.session_state.audio_name, "wb") as file:
                            file.write(uploaded_file_audio.getbuffer())
                        print(f"- 本次任务目录：{output_file}")

                        time2 = time.time()
                        output_file1 = output_file + '/' + st.session_state.audio_name
                        msg.toast('正在识别视频内容', icon=":material/hearing:")
                        if openai_whisper_api:
                            result = openai_whisper_result(openai_key, openai_base, output_file1, whisper_prompt_setting, temperature_setting)
                        else:
                            device = 'cuda' if gpu_setting else 'cpu'
                            model = faster_whisper_model
                            if faster_whisper_local:
                                model = faster_whisper_local_path
                            result = faster_whisper_result(output_file1, device, model, whisper_prompt_setting, temperature_setting, vad_setting, lang_setting, beam_size_setting, min_vad_setting)

                        time3 = time.time()
                        translation_dict = {
                            tuple([0]): '无需翻译',
                            tuple([1]): '本地模型',
                            tuple([2, 3]): 'gemini-pro',
                            tuple([2, 4]): 'gemini-1.0-pro',
                            tuple([2, 5]): 'gemini-1.5-flash',
                            tuple([2, 6]): 'gemini-1.5-pro',
                            tuple([7, 8]): 'yi-spark',
                            tuple([7, 9]): 'yi-medium',
                            tuple([7, 10]): 'yi-medium-200k',
                            tuple([7, 11]): 'yi-vision',
                            tuple([7, 12]): 'yi-large',
                            tuple([7, 13]): 'yi-large-rag',
                            tuple([7, 14]): 'yi-large-turbo',
                            tuple([7, 15]): 'yi-large-preview',
                            tuple([16, 17]): 'moonshot-v1-8k',
                            tuple([16, 18]): 'moonshot-v1-32k',
                            tuple([16, 19]): 'moonshot-v1-128k',
                            tuple([20, 21]): 'glm-4',
                            tuple([20, 22]): 'glm-4-0520',
                            tuple([20, 23]): 'glm-4-flash',
                            tuple([20, 24]): 'glm-4-air',
                            tuple([20, 25]): 'glm-4-airx',
                            tuple([26, 27]): 'gpt-3.5-turbo',
                            tuple([26, 28]): 'gpt-4',
                            tuple([26, 29]): 'gpt-4-turbo',
                            tuple([26, 30]): 'gpt-4o',
                            tuple([31, 32]): 'claude-3-opus',
                            tuple([31, 33]): 'claude-3-sonnet',
                            tuple([31, 34]): 'claude-3-haiku',
                            tuple([35, 36]): 'deepseek-chat',
                            tuple([35, 37]): 'deepseek-coder',
                        }
                        translate_option = translation_dict[tuple(translate_setting)]

                        if translate_option != '无需翻译':
                            print("***正在执行翻译***\n")
                            msg.toast('正在翻译文本', icon=":material/translate:")
                            print("- 翻译模型:" + translate_option)
                            if translate_option == '本地模型':
                                result = local_translate(system_prompt, user_prompt, local_key, local_base, local_model, result, srt_setting)
                            elif 'gemini' in translate_option:
                                result = translate(system_prompt, user_prompt, gemini_key, gemini_base, translate_option, result, wait_time_setting, srt_setting)
                            elif 'yi' in translate_option:
                                result = translate(system_prompt, user_prompt, ai01_key, ai01_base, translate_option, result, wait_time_setting, srt_setting)
                            elif 'gpt' in translate_option:
                                result = translate(system_prompt, user_prompt, openai_key, openai_base, translate_option, result, wait_time_setting, srt_setting)
                            elif 'moonshot' in translate_option:
                                result = translate(system_prompt, user_prompt, kimi_key, kimi_base, translate_option, result, wait_time_setting, srt_setting)
                            elif 'glm' in translate_option:
                                result = translate(system_prompt, user_prompt, chatglm_key, chatglm_base, translate_option, result, wait_time_setting, srt_setting)
                            elif 'deepseek' in translate_option:
                                result = translate(system_prompt, user_prompt, deepseek_key, deepseek_base, translate_option, result, wait_time_setting, srt_setting)
                            elif 'claude' in translate_option:
                                result = translate(system_prompt, user_prompt, claude_key, claude_base, translate_option, result, wait_time_setting, srt_setting)
                            print(" ")

                        time4 = time.time()
                        msg.toast('正在生成SRT字幕文件', icon=":material/edit_note:")
                        print("***正在生成SRT字幕文件***\n")
                        srt_content = generate_srt_from_result(result)
                        with open(output_file + "/output.srt", 'w', encoding='utf-8') as srt_file:
                            srt_file.write(srt_content)
                            st.session_state.output_file_path = output_file
                        st.session_state.output_file_audio = output_file1

                        print("***已完成***\n")
                        st.toast("任务已完成！", icon=":material/task_alt:")
                    else:
                        st.toast("未检测到文件", icon=":material/error:")

        with st.expander("Srt_preview", expanded=True):
            try:
                audio_file = open(st.session_state.output_file_audio, 'rb')
                audio_bytes = audio_file.read()
                st.write("###### 音轨")
                st.audio(audio_bytes)
            except:
                sac.alert(
                    label='**运行后自动显示**',
                    description='有问题可以查阅文档[AAVT](https://zwho5v3j233.feishu.cn/wiki/OGcrwinzhi88MkkvEMVcLkDgnzc?from=from_copylink)，或者加群讨论',
                    size='lg', radius=20, icon=True, closable=True, color='info')

            try:
                with open(st.session_state.output_file_path + "/output.srt", 'r', encoding='utf-8') as srt_file:
                    srt_content = srt_file.read()
                srt_data1 = parse_srt_file(srt_content)
                edited_data = st.data_editor(srt_data1, height=st.session_state.height, hide_index=True, use_container_width=True)
                srt_data2 = convert_to_srt(edited_data)
                st.session_state.srt_content_new = srt_data2
            except:
                srt_data = [{"index": "", "start": "", "end": "", "content": ""}]
                st.data_editor(srt_data, height=st.session_state.height, hide_index=True, use_container_width=True)

        sac.divider(label='POWERED BY @CHENYME', icon='lightning-charge', align='center', color='gray', key="2")

    if name == '视频识别':
        with st.expander("Video_preview", expanded=True):
            col5, col6 = st.columns(2, gap="medium")
        col1, col2 = st.columns([0.8, 0.2])

        with col2:
            with st.expander("Setting", expanded=True):
                font_size_setting = hard_font_size_setting
                if subtitle_model_setting == "软字幕":
                    font_size_setting = soft_font_size_setting

                sac.divider(label='方案一：一键生成', icon='1-square', align='center', color='gray')
                if st.button("一键生成视频", type="primary", use_container_width=True, help="这里是方案一：您可以直接生成翻译并合并好的视频文件。\n\n如果觉得生成的字幕不符合预期，可以继续修改字幕点击下方`合并字幕`按钮进行合并"):
                    if uploaded_file is not None:
                        st.session_state.video_name = "uploaded." + uploaded_file.name.split('.')[-1]
                        time1 = time.time()
                        st.toast('已开始生成，请不要在运行时切换菜单或修改参数!', icon=":material/person_alert:")
                        msg = st.toast('正在进行视频提取', icon=":material/play_circle:")

                        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H-%M-%S")
                        output_file = cache_dir + current_time
                        os.makedirs(output_file)
                        with open(output_file + '/' + st.session_state.video_name, "wb") as file:
                            file.write(uploaded_file.getbuffer())
                        print(f"- 本次任务目录：{output_file}")
                        file_to_mp3(log_setting, st.session_state.video_name, output_file)

                        time2 = time.time()
                        msg.toast('正在识别视频内容', icon=":material/hearing:")
                        if openai_whisper_api:
                            result = openai_whisper_result(openai_key, openai_base, output_file, whisper_prompt_setting, temperature_setting)
                        else:
                            device = 'cuda' if gpu_setting else 'cpu'
                            model = faster_whisper_model
                            if faster_whisper_local:
                                model = faster_whisper_local_path
                            result = faster_whisper_result(output_file, device, model, whisper_prompt_setting, temperature_setting, vad_setting, lang_setting, beam_size_setting, min_vad_setting)

                        time3 = time.time()
                        translation_dict = {
                            tuple([0]): '无需翻译',
                            tuple([1]): '本地模型',
                            tuple([2, 3]): 'gemini-pro',
                            tuple([2, 4]): 'gemini-1.0-pro',
                            tuple([2, 5]): 'gemini-1.5-flash',
                            tuple([2, 6]): 'gemini-1.5-pro',
                            tuple([7, 8]): 'yi-spark',
                            tuple([7, 9]): 'yi-medium',
                            tuple([7, 10]): 'yi-medium-200k',
                            tuple([7, 11]): 'yi-vision',
                            tuple([7, 12]): 'yi-large',
                            tuple([7, 13]): 'yi-large-rag',
                            tuple([7, 14]): 'yi-large-turbo',
                            tuple([7, 15]): 'yi-large-preview',
                            tuple([16, 17]): 'moonshot-v1-8k',
                            tuple([16, 18]): 'moonshot-v1-32k',
                            tuple([16, 19]): 'moonshot-v1-128k',
                            tuple([20, 21]): 'glm-4',
                            tuple([20, 22]): 'glm-4-0520',
                            tuple([20, 23]): 'glm-4-flash',
                            tuple([20, 24]): 'glm-4-air',
                            tuple([20, 25]): 'glm-4-airx',
                            tuple([26, 27]): 'gpt-3.5-turbo',
                            tuple([26, 28]): 'gpt-4',
                            tuple([26, 29]): 'gpt-4-turbo',
                            tuple([26, 30]): 'gpt-4o',
                            tuple([31, 32]): 'claude-3-opus',
                            tuple([31, 33]): 'claude-3-sonnet',
                            tuple([31, 34]): 'claude-3-haiku',
                            tuple([35, 36]): 'deepseek-chat',
                            tuple([35, 37]): 'deepseek-coder',
                        }
                        translate_option = translation_dict[tuple(translate_setting)]

                        if translate_option != '无需翻译':
                            print("***正在执行翻译***\n")
                            msg.toast('正在翻译文本', icon=":material/translate:")
                            print("- 翻译模型:" + translate_option)
                            if translate_option == '本地模型':
                                result = local_translate(system_prompt, user_prompt, local_key, local_base, local_model, result, srt_setting)
                            elif 'gemini' in translate_option:
                                result = translate(system_prompt, user_prompt, gemini_key, gemini_base, translate_option, result, wait_time_setting, srt_setting)
                            elif 'yi' in translate_option:
                                result = translate(system_prompt, user_prompt, ai01_key, ai01_base, translate_option, result, wait_time_setting, srt_setting)
                            elif 'gpt' in translate_option:
                                result = translate(system_prompt, user_prompt, openai_key, openai_base, translate_option, result, wait_time_setting, srt_setting)
                            elif 'moonshot' in translate_option:
                                result = translate(system_prompt, user_prompt, kimi_key, kimi_base, translate_option, result, wait_time_setting, srt_setting)
                            elif 'glm' in translate_option:
                                result = translate(system_prompt, user_prompt, chatglm_key, chatglm_base, translate_option, result, wait_time_setting, srt_setting)
                            elif 'deepseek' in translate_option:
                                result = translate(system_prompt, user_prompt, deepseek_key, deepseek_base, translate_option, result, wait_time_setting, srt_setting)
                            elif 'claude' in translate_option:
                                result = translate(system_prompt, user_prompt, claude_key, claude_base, translate_option, result, wait_time_setting, srt_setting)
                            print(" ")

                        time4 = time.time()
                        msg.toast('正在生成SRT字幕文件', icon=":material/edit_note:")
                        print("***正在生成SRT字幕文件***\n")
                        srt_content = generate_srt_from_result(result)
                        srt_content_style = generate_srt_from_result_2(result, font_setting, font_size_setting, font_color_setting)
                        with open(output_file + "/output.srt", 'w', encoding='utf-8') as srt_file:
                            srt_file.write(srt_content)
                        with open(output_file + "/output_with_style.srt", 'w', encoding='utf-8') as srt_file:
                            srt_file.write(srt_content_style)
                        st.session_state.output_file = output_file

                        time5 = time.time()
                        st.toast('正在合并视频，请耐心等待生成', icon=":material/arrow_or_edge:")
                        print("***正在合并视频***\n")
                        srt_mv(log_setting, st.session_state.video_name, crf_setting, quality_setting, ffmpeg_setting, st.session_state.output_file, font_setting, font_size_setting, font_color_setting, subtitle_model_setting)

                        time6 = time.time()
                        print("***已完成***\n")
                        st.toast("任务已完成！", icon=":material/task_alt:")
                        total_time = time6 - time1
                        st.session_state.time = f"{total_time:.2f}"
                    else:
                        st.toast("未检测到文件", icon=":material/error:")

                sac.divider(label='方案二：分段合成', icon='2-square', align='center', color='gray')
                if st.button("生成字幕", type="primary", use_container_width=True, help="这里是方案二：您可以先仅生成字幕文件，调整好后再继续点击下方`合并字幕`进行合并"):
                    if uploaded_file is not None:
                        st.session_state.video_name = "uploaded." + uploaded_file.name.split('.')[-1]
                        time1 = time.time()
                        st.toast('已开始生成，请不要在运行时切换菜单或修改参数!', icon=":material/person_alert:")
                        msg = st.toast('正在进行视频提取', icon=":material/play_circle:")

                        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H-%M-%S")
                        output_file = cache_dir + current_time
                        os.makedirs(output_file)
                        with open(output_file + '/' + st.session_state.video_name, "wb") as file:
                            file.write(uploaded_file.getbuffer())
                        print(f"- 本次任务目录：{output_file}")
                        file_to_mp3(log_setting, st.session_state.video_name, output_file)

                        time2 = time.time()
                        msg.toast('正在识别视频内容', icon=":material/hearing:")
                        if openai_whisper_api:
                            result = openai_whisper_result(openai_key, openai_base, output_file, whisper_prompt_setting, temperature_setting)
                        else:
                            device = 'cuda' if gpu_setting else 'cpu'
                            model = faster_whisper_model
                            if faster_whisper_local:
                                model = faster_whisper_local_path
                            result = faster_whisper_result(output_file, device, model, whisper_prompt_setting, temperature_setting, vad_setting, lang_setting, beam_size_setting, min_vad_setting)

                        time3 = time.time()
                        translation_dict = {
                            tuple([0]): '无需翻译',
                            tuple([1]): '本地模型',
                            tuple([2, 3]): 'gemini-pro',
                            tuple([2, 4]): 'gemini-1.0-pro',
                            tuple([2, 5]): 'gemini-1.5-flash',
                            tuple([2, 6]): 'gemini-1.5-pro',
                            tuple([7, 8]): 'yi-spark',
                            tuple([7, 9]): 'yi-medium',
                            tuple([7, 10]): 'yi-medium-200k',
                            tuple([7, 11]): 'yi-vision',
                            tuple([7, 12]): 'yi-large',
                            tuple([7, 13]): 'yi-large-rag',
                            tuple([7, 14]): 'yi-large-turbo',
                            tuple([7, 15]): 'yi-large-preview',
                            tuple([16, 17]): 'moonshot-v1-8k',
                            tuple([16, 18]): 'moonshot-v1-32k',
                            tuple([16, 19]): 'moonshot-v1-128k',
                            tuple([20, 21]): 'glm-4',
                            tuple([20, 22]): 'glm-4-0520',
                            tuple([20, 23]): 'glm-4-flash',
                            tuple([20, 24]): 'glm-4-air',
                            tuple([20, 25]): 'glm-4-airx',
                            tuple([26, 27]): 'gpt-3.5-turbo',
                            tuple([26, 28]): 'gpt-4',
                            tuple([26, 29]): 'gpt-4-turbo',
                            tuple([26, 30]): 'gpt-4o',
                            tuple([31, 32]): 'claude-3-opus',
                            tuple([31, 33]): 'claude-3-sonnet',
                            tuple([31, 34]): 'claude-3-haiku',
                            tuple([35, 36]): 'deepseek-chat',
                            tuple([35, 37]): 'deepseek-coder',
                        }
                        translate_option = translation_dict[tuple(translate_setting)]

                        if translate_option != '无需翻译':
                            print("***正在执行翻译***\n")
                            msg.toast('正在翻译文本', icon=":material/translate:")
                            print("- 翻译模型:" + translate_option)
                            if translate_option == '本地模型':
                                result = local_translate(system_prompt, user_prompt, local_key, local_base, local_model, result, srt_setting)
                            elif 'gemini' in translate_option:
                                result = translate(system_prompt, user_prompt, gemini_key, gemini_base, translate_option, result, wait_time_setting, srt_setting)
                            elif 'yi' in translate_option:
                                result = translate(system_prompt, user_prompt, ai01_key, ai01_base, translate_option, result, wait_time_setting, srt_setting)
                            elif 'gpt' in translate_option:
                                result = translate(system_prompt, user_prompt, openai_key, openai_base, translate_option, result, wait_time_setting, srt_setting)
                            elif 'moonshot' in translate_option:
                                result = translate(system_prompt, user_prompt, kimi_key, kimi_base, translate_option, result, wait_time_setting, srt_setting)
                            elif 'glm' in translate_option:
                                result = translate(system_prompt, user_prompt, chatglm_key, chatglm_base, translate_option, result, wait_time_setting, srt_setting)
                            elif 'deepseek' in translate_option:
                                result = translate(system_prompt, user_prompt, deepseek_key, deepseek_base, translate_option, result, wait_time_setting, srt_setting)
                            elif 'claude' in translate_option:
                                result = translate(system_prompt, user_prompt, claude_key, claude_base, translate_option, result, wait_time_setting, srt_setting)
                            print(" ")

                        time4 = time.time()
                        msg.toast('正在生成SRT字幕文件', icon=":material/edit_note:")
                        print("***正在生成SRT字幕文件***\n")
                        srt_content = generate_srt_from_result(result)
                        srt_content_style = generate_srt_from_result_2(result, font_setting, font_size_setting, font_color_setting)
                        with open(output_file + "/output.srt", 'w', encoding='utf-8') as srt_file:
                            srt_file.write(srt_content)
                        with open(output_file + "/output_with_style.srt", 'w', encoding='utf-8') as srt_file:
                            srt_file.write(srt_content_style)
                        st.session_state.output_file = output_file

                        time5 = time.time()
                        print("***已完成***\n")
                        st.toast("任务已完成！", icon=":material/task_alt:")
                        total_time = time5 - time1
                        st.session_state.time = f"{total_time:.2f}"
                    else:
                        st.toast("未检测到文件", icon=":material/error:")

                if st.button("合并字幕", type="primary", use_container_width=True, help="进行字幕合并，若对一键生成的不满意也可以重新合并"):
                    try:
                        with open(st.session_state.output_file + "/output.srt", 'w', encoding='utf-8') as srt_file:
                            srt_file.write(st.session_state.srt_content_new)
                        with open(st.session_state.output_file + "/output_with_style.srt", 'w', encoding='utf-8') as srt_file:
                            srt_file.write(st.session_state.srt_data3)
                        test = st.session_state.video_name
                        time1 = time.time()
                        st.toast('正在合并视频，请耐心等待生成', icon=":material/arrow_or_edge:")
                        print("***正在合并视频***\n")
                        srt_mv(log_setting, st.session_state.video_name, crf_setting, quality_setting, ffmpeg_setting, st.session_state.output_file, font_setting, font_size_setting, font_color_setting, subtitle_model_setting)
                        print("***已完成***\n")
                        st.toast("任务已完成！", icon=":material/task_alt:")
                        time2 = time.time()
                        total_time = time2 - time1
                        st.session_state.time = f"{total_time:.2f}"
                    except:
                        st.toast("未检测到文件", icon=":material/error:")

                sac.divider(label='其他预览设置', icon='arrow-down-square', align='center', color='gray')
                height = st.number_input("字幕轴显示高度", min_value=400, step=100, value=400)
                st.session_state.height = height

                try:
                    captions_option = st.radio('更多字幕格式导出', ('vtt', 'ass', 'stl'), index=0, horizontal=True)
                    if captions_option == 'vtt':
                        vtt_content = srt_to_vtt(st.session_state.srt_content_new)
                        st.download_button(
                            label="下载VTT字幕",
                            data=vtt_content.encode('utf-8'),
                            key='vtt_download',
                            file_name='output.vtt',
                            mime='text/vtt',
                            use_container_width=True
                        )
                    elif captions_option == 'ass':
                        ass_content = srt_to_ass(st.session_state.srt_content_new, font_setting, font_size_setting, font_color_setting)
                        st.download_button(
                            label="下载ASS字幕",
                            data=ass_content.encode('utf-8'),
                            key='ass_download',
                            file_name='output.ass',
                            mime='text/ass',
                            use_container_width=True
                        )
                    elif captions_option == 'stl':
                        stl_content = srt_to_stl(st.session_state.srt_content_new)
                        st.download_button(
                            label="下载STL字幕",
                            data=stl_content.encode('utf-8'),
                            key='stl_download',
                            file_name='output.stl',
                            mime='text/stl',
                            use_container_width=True
                        )
                except:
                    if st.button('下载字幕', use_container_width=True):
                        st.toast("未检测到文件", icon=":material/error:")

                if st.button('打开文件目录', use_container_width=True):
                    try:
                        os.startfile(st.session_state.output_file)
                        st.toast("注意：文件夹已成功打开，可能未置顶显示，请检查任务栏！", icon=":material/task_alt:")
                    except:
                        st.toast("未检测到文件", icon=":material/error:")

        with col1:
            with st.expander("Srt_preview", expanded=True):
                try:
                    audio_file = open(st.session_state.output_file + "/output.mp3", 'rb')
                    audio_bytes = audio_file.read()
                    st.write("###### 音轨")
                    st.audio(audio_bytes)
                except:
                    sac.alert(
                        label='**运行后自动显示**',
                        description='有问题可以查阅文档[AAVT](https://zwho5v3j233.feishu.cn/wiki/OGcrwinzhi88MkkvEMVcLkDgnzc?from=from_copylink)或者加群讨论',
                        size='lg', radius=20, icon=True, closable=True, color='info')

                try:
                    with open(st.session_state.output_file + "/output.srt", 'r', encoding='utf-8') as srt_file:
                        srt_content = srt_file.read()
                    srt_data1 = parse_srt_file(srt_content)
                    edited_data = st.data_editor(srt_data1, height=st.session_state.height, hide_index=True, use_container_width=True)
                    srt_data2 = convert_to_srt(edited_data)
                    st.session_state.srt_data3 = add_font_settings(srt_data2, font_color_setting, font_setting, font_size_setting)
                    st.session_state.srt_content_new = srt_data2
                except:
                    srt_data = [{"index": "", "start": "", "end": "", "content": ""}]
                    st.data_editor(srt_data, height=st.session_state.height, hide_index=True, use_container_width=True)

        try:
            sac.alert(
                label=f'总耗时：{st.session_state.time}s',
                size='lg', radius=20, icon=True, closable=True, color='success')
        except:
            test = 1
        sac.divider(label='POWERED BY @CHENYME', icon='lightning-charge', align='center', color='gray', key="2")

        with col5:
            try:
                st.write("**原始的视频**")
                video_bytes = show_video(st.session_state.output_file, st.session_state.video_name)
                st.video(video_bytes)
            except:
                sac.alert(
                    label='**原始视频预览窗口**',
                    description='上传后自动显示预览结果',
                    size='lg', radius=20, icon=True, closable=True, color='info')
        with col6:
            try:
                st.write("**处理后的视频**")
                video_bytes = show_video(st.session_state.output_file, "output.mp4")
                st.video(video_bytes)
            except:
                sac.alert(
                    label='**生成视频预览窗口**',
                    description='运行后自动显示预览结果',
                    size='lg', radius=20, icon=True, closable=True, color='info')
