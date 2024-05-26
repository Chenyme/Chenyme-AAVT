import os
import toml
import time
import torch
import datetime
import streamlit as st
import streamlit_antd_components as sac
from project.utils.utils2 import (file_to_mp3, openai_whisper_result, faster_whisper_result, translate, local_translate,
                                  generate_srt_from_result, generate_srt_from_result_2, srt_mv, show_video, parse_srt_file,
                                  convert_to_srt, srt_to_ass, srt_to_stl, srt_to_vtt, check_cuda_support, check_ffmpeg)


def video():
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
    subtitle_model_setting = video_config["SUBTITLE"]["subtitle_model"]
    font_setting = video_config["SUBTITLE"]["font"]
    font_size_setting = video_config["SUBTITLE"]["font_size"]
    font_color_setting = video_config["SUBTITLE"]["font_color"]
    min_vad_setting = video_config["MORE"]["min_vad"]
    beam_size_setting = video_config["MORE"]["beam_size"]
    whisper_prompt_setting = video_config["MORE"]["whisper_prompt"]
    temperature_setting = video_config["MORE"]["temperature"]
    crf_setting = video_config["MORE"]["crf"]
    quality_setting = video_config["MORE"]["quality"]
    ffmpeg_setting = video_config["MORE"]["ffmpeg"]

    options = {'faster-whisper': {'models': {'tiny': 0, 'tiny.en': 1, 'base': 2, 'base.en': 3, 'small': 4,
                                             'small.en': 5, 'medium': 6, 'medium.en': 7, 'large-v1': 8,
                                             'large-v2': 9, 'large-v3': 10, 'large': 11, 'distil-small.en': 12,
                                             'distil-medium.en': 13, 'distil-large-v2': 14,
                                             'distil-large-v3': 15}}}

    with st.sidebar:
        uploaded_file = st.file_uploader("请在这里上传视频：", type=['mp4', 'mov', 'avi', 'm4v', 'webm', 'flv', 'ico'], label_visibility="collapsed")

    st.title("全自动视频翻译")
    st.write("AI Auto Video Translation")
    sac.divider(label='POWERED BY @CHENYME', align='center', color='gray')
    name = sac.segmented(
        items=[
            sac.SegmentedItem(label='参数设置'),
            sac.SegmentedItem(label='生成字幕'),
        ], align='center', size='sm', radius=20, color='red', divider=False, use_container_width=True
    )
    if name == '参数设置':
        col1, col2 = st.columns(2, gap="medium")
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
                        gpu = st.toggle('GPU加速', disabled=torch.cuda.is_available(), help='cuda、pytorch正确后才可使用！', value=gpu_setting)
                        vad = st.toggle('VAD辅助', help='启用语音活动检测（VAD）以过滤掉没有语音的音频部分', value=vad_setting)

                    with col4:
                        language = ['自动识别', 'zh', 'en', 'ja', 'ko', 'it', 'de']  # language
                        index = language.index(lang_setting)
                        lang = st.selectbox('视频语言', language, index=index, help="强制指定视频语言会提高识别准确度，但也可能会造成识别出错。")

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
                    sac.CasItem('ChatGPT-OpenAI', icon='node-plus-fill', children=[
                        sac.CasItem('gpt-3.5-turbo', icon='robot'),
                        sac.CasItem('gpt-4o', icon='robot'),
                        sac.CasItem('gpt-4', icon='robot')]),
                    sac.CasItem('Moonshot-月之暗面', icon='node-plus-fill', children=[
                        sac.CasItem('kimi-moonshot-v1-8k', icon='robot'),
                        sac.CasItem('kimi-moonshot-v1-32k', icon='robot'),
                        sac.CasItem('kimi-moonshot-v1-128k', icon='robot')]),
                    sac.CasItem('ChatGLM-智谱AI', icon='node-plus-fill', children=[
                        sac.CasItem('glm-3-turbo', icon='robot'),
                        sac.CasItem('glm-4v', icon='robot'),
                        sac.CasItem('glm-4', icon='robot')]),
                    sac.CasItem('DeepSeek-深度求索', icon='node-plus-fill', children=[
                        sac.CasItem('deepseek-v2', icon='robot')]),
                ], label='<span style="font-size: 14px;">翻译引擎</span>', search=True, index=translate_setting, return_index=True)
                video_config["TRANSLATE"]["translate_model"] = translate_option

                if translate_option != [0]:
                    language = ['中文', 'English', '日本語', '한국인', 'Italiano', 'Deutsch']

                    col3, col4, col5 = st.columns(3)
                    with col3:
                        language1 = st.selectbox('原始语言', language, index=language.index(language1_setting))
                    with col4:
                        language2 = st.selectbox('目标语言', language, index=language.index(language2_setting))
                    with col5:
                        wait_time = st.number_input('翻译间隔(s)', min_value=0.0, max_value=5.0, value=wait_time_setting, step=0.1, help="每次API调用的间隔。\n\n 当你的视频比较长，字幕很多时，导致翻译时会一直反复调用 API 太多次，这会达到每分钟速率最大限制。当遇到报错429，如：`Too Many Requests`、`RateLimitError`这种速率报错，那就需要适当增大间隔。")

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
                    font = st.selectbox('字体', fonts, index=fonts.index(font_setting), help="所有字体均从系统读取加载，支持用户自行安装字体。请注意商用风险！")

                col3, col4 = st.columns([0.85, 0.15], gap="medium")
                with col3:
                    font_size = st.number_input('大小', min_value=1, max_value=30, value=font_size_setting, step=1, help="推荐大小：18")
                with col4:
                    font_color = st.color_picker('颜色', value=font_color_setting)

                video_config["SUBTITLE"]["subtitle_model"] = subtitle_model
                video_config["SUBTITLE"]["font"] = font
                video_config["SUBTITLE"]["font_size"] = font_size
                video_config["SUBTITLE"]["font_color"] = font_color

            with st.expander("**高级设置**", expanded=False):
                min_vad = st.number_input("VAD静音检测(ms)", min_value=100, max_value=5000, value=min_vad_setting, step=100, disabled=openai_whisper_api, help="`min_silence_duration_ms`参数，最小静音持续时间，启用VAD辅助后生效！")
                beam_size = st.number_input("束搜索大小", min_value=1, max_value=20, value=beam_size_setting, step=1, disabled=openai_whisper_api, help="`beam_size`参数。用于定义束搜索算法中每个时间步保留的候选项数量。束搜索算法通过在每个时间步选择最有可能的候选项来构建搜索树，并根据候选项的得分进行排序和剪枝。较大的beam_size值会保留更多的候选项，扩大搜索空间，可能提高生成结果的准确性，但也会增加计算开销。相反，较小的beam_size值会减少计算开销，但可能导致搜索过早地放弃最佳序列。")
                whisper_prompt = st.text_input("Whisper提示词", value=whisper_prompt_setting, help="若您无更好的Whisper提示词，请勿随意修改！否则会影响断句效果")
                temperature = st.number_input("Whisper温度", min_value=0.0, max_value=1.0, value=temperature_setting, step=0.1, help="Whisper转录时模型温度，越大随机性（创造性）越高。")
                crf = st.selectbox("FFmpeg-恒定速率因子", [0, 18, 23, 28], index=[0, 18, 23, 28].index(crf_setting), help="CRF 值的范围通常为 0 到 51，数值越低，质量越高。建议值：\n- `0`: 无损压缩，质量最高，文件最大。\n- `18`: 视觉上接近无损，非常高的质量，文件较大。\n- `23`: 默认值，质量和文件大小的平衡点。\n- `28`: 较低的质量，文件较小。")
                quality_list = ["ultrafast", "superfast", "veryfast", "faster", "fast", "medium", "slow", "slower", "veryslow", "placebo"]
                quality = st.selectbox("FFmpeg-编码器预设(质量)", quality_list, index=quality_list.index(quality_setting), help="编码器预设(质量quality)，默认值为 `medium`。注意，下面有些值是不可使用的，若你不了解，请勿修改！可选值包括：\n- `ultrafast`: 最快的编码速度，但质量最低，文件最大。\n- `superfast`: 非常快的编码速度，质量和文件大小有所提升。\n- `veryfast`: 很快的编码速度，适用于实时编码或需要快速处理的情况。\n- `faster`: 比较快的编码速度，质量进一步提高。\n- `fast`: 快速编码速度，质量较好。\n- `medium`: 默认预设，编码速度和质量的平衡点。\n- `slow`: 较慢的编码速度，输出质量更高，文件更小。\n- `slower`: 更慢的编码速度，质量进一步提高。\n- `veryslow`: 非常慢的编码速度，质量最高，文件最小。\n- `placebo`: 极慢的编码速度，质量微小提升，不推荐使用，除非对质量有极高要求且不在意编码时间。")
                ffmpeg = st.selectbox("FFmpeg-编码器", ["h264_nvenc", "libx264"], index=["h264_nvenc", "libx264"].index(ffmpeg_setting), help="CUDA可用时，可选择h264_nvenc。否则默认libx264，注意h264_nvenc质量过高，输出文件会很大")
                video_config["MORE"]["min_vad"] = min_vad
                video_config["MORE"]["beam_size"] = beam_size
                video_config["MORE"]["whisper_prompt"] = whisper_prompt
                video_config["MORE"]["temperature"] = temperature
                video_config["MORE"]["crf"] = crf
                video_config["MORE"]["quality"] = quality
                video_config["MORE"]["ffmpeg"] = ffmpeg

        with open(config_dir + '/video.toml', 'w', encoding='utf-8') as file:
            toml.dump(video_config, file)

        with col2:
            sac.alert(
                label='**AAVT项目文档 已发布**',
                description='有问题可以**查阅文档**[AAVT](https://zwho5v3j233.feishu.cn/wiki/OGcrwinzhi88MkkvEMVcLkDgnzc?from=from_copylink)，或者**加群讨论**哦',
                size='lg', radius=20, icon=True, closable=True, color='info')

            sac.alert(
                label='**参数设置 已保存**',
                description='由于Streamlit机制，修改相同参数**不成功时请尝试重新选择**',
                size='lg', radius=20, icon=True, closable=True, color='success')

            if check_ffmpeg():
                sac.alert(
                    label='**FFmpeg 状态正常**',
                    description='检测到FFmpeg状态，**FFmpeg可用**',
                    size='lg', radius=20, icon=True, closable=True, color='success')
            else:
                sac.alert(
                    label='**FFmpeg 状态错误**',
                    description='未检测到FFmpeg状态，**FFmpeg不可用**，请添加环境变量',
                    size='lg', radius=20, icon=True, closable=True, color='success')

            if check_cuda_support():
                sac.alert(
                    label='**FFmpeg GPU加速状态正常**',
                    description='检测到CUDA状态，**FFmpeg加速可用**',
                    size='lg', radius=20, icon=True, closable=True, color='success')

            if not openai_whisper_api:
                if vad:
                    sac.alert(
                        label='**VAD辅助模式 已开启**',
                        description='启用语音活动检测（VAD）以过滤掉没有语音的音频部分',
                        size='lg', radius=20, icon=True, closable=True, color='success')

            if openai_whisper_api:
                sac.alert(
                    label='**OpenAI-API Whipser调用模式 已开启**',
                    description='请**确保OPENAI相关配置设置不为空**',
                    size='lg', radius=20, icon=True, closable=True, color='warning')

            if not openai_whisper_api:
                if gpu:
                    sac.alert(
                        label='**GPU加速模式 已开启**',
                        description='**支持CUDA12**，若为 CUDA11，请降级ctranslate2',
                        size='lg', radius=20, icon=True, closable=True, color='warning')

            if not openai_whisper_api:
                if local_on:
                    sac.alert(
                        label='**Whisper本地模型加载模式 已开启**',
                        description='模型下载：[Hugging Face](https://huggingface.co/Systran)，使用文档：[AAVT](https://zwho5v3j233.feishu.cn/wiki/OGcrwinzhi88MkkvEMVcLkDgnzc?from=from_copylink)',
                        size='lg', radius=20, icon=True, closable=True, color='warning')

            if translate_option == [1]:
                sac.alert(
                    label='**本地LLM调用翻译模式 已开启**',
                    description="请**确保相关参数正确无误**，无需key则设置时留空",
                    size='lg', radius=20, icon=True, closable=True, color='warning')

            if subtitle_model == "软字幕":
                sac.alert(
                    label='**软字幕 已开启**',
                    description='软字幕请用**一键生成**模式，且无法在网页中预览效果',
                    size='lg', radius=20, icon=True, closable=True, color='warning')

            if torch.cuda.is_available():
                sac.alert(
                    label='**未检测到CUDA状态或正确的Pytorch**',
                    description='GPU加速不可用，请检查CUDA、Pytorch！**仅使用CPU请忽略**',
                    size='lg', radius=20, icon=True, closable=True, color='error')

            if ffmpeg != "libx264":
                if not check_cuda_support():
                    sac.alert(
                        label='**编码器无效 请换回libx264**',
                        description='未检测到CUDA状态，FFmpeg加速不可用！',
                        size='lg', radius=20, icon=True, closable=True, color='error')
                else:
                    sac.alert(
                        label='**编码器设置 成功**',
                        description='检测到CUDA状态，编码器可用！',
                        size='lg', radius=20, icon=True, closable=True, color='success')

            sac.divider(label='**参数提示**', icon='box-fill', align='center', color='gray')

    if name == '生成字幕':
        with st.expander("video_preview", expanded=True):
            col5, col6 = st.columns(2, gap="medium")
        col1, col2 = st.columns([0.8, 0.2])

        with col2:
            with st.expander("setting", expanded=True):
                sac.divider(label='一键生成，无需修改', icon='box-fill', align='center', color='gray')
                if st.button("一键生成视频", type="primary", use_container_width=True, help="直接生成翻译并合并好的视频文件。\n\n如果觉得生成的字幕不符合预期，可以继续修改字幕点击下方`合并字幕`按钮进行合并"):
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
                            result = faster_whisper_result(output_file, device, model, whisper_prompt_setting, temperature_setting, vad_setting, lang_setting, beam_size_setting, min_vad_setting)

                        time3 = time.time()
                        translation_dict = {
                            tuple([0]): '无需翻译',
                            tuple([1]): '本地模型',
                            tuple([2, 3]): 'gpt-3.5-turbo',
                            tuple([2, 4]): 'gpt-4o',
                            tuple([2, 5]): 'gpt-4',
                            tuple([6, 7]): 'moonshot-v1-8k',
                            tuple([6, 8]): 'moonshot-v1-32k',
                            tuple([6, 9]): 'moonshot-v1-128k',
                            tuple([10, 11]): 'glm-3-turbo',
                            tuple([10, 12]): 'glm-4v',
                            tuple([10, 13]): 'glm-4',
                            tuple([14, 15]): 'deepseek-chat'
                        }
                        translate_option = translation_dict[tuple(translate_setting)]

                        if translate_option != '无需翻译':
                            print("***正在执行翻译***\n")
                            msg.toast('正在翻译文本🤖')
                            print("- 翻译模型:" + translate_option)
                            if translate_option == 'gpt-3.5-turbo' or translate_option == 'gpt-4o':
                                result = translate(openai_key, openai_base, translate_option, result, language1_setting, language2_setting, wait_time_setting)
                            elif 'kimi' in translate_option:
                                result = translate(kimi_key, kimi_base, translate_option, result, language1_setting, language2_setting, wait_time_setting)
                            elif 'glm' in translate_option:
                                result = translate(chatglm_key, chatglm_base, translate_option, result, language1_setting, language2_setting, wait_time_setting)
                            elif 'deepseek' in translate_option:
                                result = translate(deepseek_key, deepseek_base, translate_option, result, language1_setting, language2_setting, wait_time_setting)
                            elif translate_option == '本地模型':
                                result = local_translate(local_key, local_base, local_model, result, language1_setting, language2_setting)
                            print(" ")

                        time4 = time.time()
                        msg.toast('正在生成SRT字幕文件📃')
                        print("***正在生成SRT字幕文件***\n")
                        srt_content = generate_srt_from_result(result)
                        srt_content_style = generate_srt_from_result_2(result, font_setting, font_size_setting, font_color_setting)
                        with open(output_file + "/output.srt", 'w', encoding='utf-8') as srt_file:
                            srt_file.write(srt_content)
                        with open(output_file + "/output_with_style.srt", 'w', encoding='utf-8') as srt_file:
                            srt_file.write(srt_content_style)
                        st.session_state.output_file = output_file

                        time5 = time.time()
                        st.toast('正在合并视频，请耐心等待生成⚙️')
                        print("***正在合并视频***\n")
                        srt_mv(uploaded_file.name, crf_setting, quality_setting, ffmpeg_setting, st.session_state.output_file, font_setting, font_size_setting, font_color_setting, subtitle_model_setting)

                        time6 = time.time()
                        print("***已完成***\n")
                        total_time = time6 - time1
                        st.session_state.time = f"{total_time:.2f}"
                    else:
                        st.toast("未检测到文件", icon=":material/error:")

                sac.divider(label='字幕校对，合并字幕', icon='box-fill', align='center', color='gray')
                if st.button("生成字幕", type="primary", use_container_width=True, help="只生成字幕文件，您可以调整好后再继续点击下方`合并字幕`进行合并"):
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
                            result = faster_whisper_result(output_file, device, model, whisper_prompt_setting, temperature_setting, vad_setting, lang_setting, beam_size_setting, min_vad_setting)

                        time3 = time.time()
                        translation_dict = {
                            tuple([0]): '无需翻译',
                            tuple([1]): '本地模型',
                            tuple([2, 3]): 'gpt-3.5-turbo',
                            tuple([2, 4]): 'gpt-4o',
                            tuple([2, 5]): 'gpt-4',
                            tuple([6, 7]): 'moonshot-v1-8k',
                            tuple([6, 8]): 'moonshot-v1-32k',
                            tuple([6, 9]): 'moonshot-v1-128k',
                            tuple([10, 11]): 'glm-3-turbo',
                            tuple([10, 12]): 'glm-4v',
                            tuple([10, 13]): 'glm-4',
                            tuple([14, 15]): 'deepseek-chat'
                        }
                        translate_option = translation_dict[tuple(translate_setting)]

                        if translate_option != '无需翻译':
                            print("***正在执行翻译***\n")
                            msg.toast('正在翻译文本🤖')
                            print("- 翻译模型:" + translate_option)
                            if 'gpt' in translate_option:
                                result = translate(openai_key, openai_base, translate_option, result, language1, language2, wait_time)
                            elif 'kimi' in translate_option:
                                result = translate(kimi_key, kimi_base, translate_option, result, language1, language2, wait_time)
                            elif 'glm' in translate_option:
                                result = translate(chatglm_key, chatglm_base, translate_option, result, language1, language2, wait_time)
                            elif 'deepseek' in translate_option:
                                result = translate(deepseek_key, deepseek_base, translate_option, result, language1, language2, wait_time)
                            elif translate_option == '本地模型':
                                result = local_translate(local_key, local_base, local_model, result, language1, language2)
                            print(" ")

                        time4 = time.time()
                        msg.toast('正在生成SRT字幕文件📃')
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
                        total_time = time5 - time1
                        st.session_state.time = f"{total_time:.2f}"
                    else:
                        st.toast("未检测到文件", icon=":material/error:")

                if st.button("合并字幕", type="primary", use_container_width=True, help="进行字幕合并，若对一键生成的不满意也可以重新合并"):
                    try:
                        test = st.session_state.video_name
                        time1 = time.time()
                        st.toast('正在合并视频，请耐心等待生成⚙️')
                        print("***正在合并视频***\n")
                        srt_mv(uploaded_file.name, crf_setting, quality_setting, ffmpeg_setting, st.session_state.output_file, font_setting, font_size_setting, font_color_setting, subtitle_model_setting)
                        print("***已完成***\n")
                        time2 = time.time()
                        total_time = time2 - time1
                        st.session_state.time = f"{total_time:.2f}"
                    except:
                        st.toast("未检测到文件", icon=":material/error:")

                sac.divider(label='预览调整，字幕输出', icon='box-fill', align='center', color='gray')
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
                            file_name='output.vvt',
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
            with st.expander("srt_preview", expanded=True):
                try:
                    audio_file = open(st.session_state.output_file + "/output.mp3", 'rb')
                    audio_bytes = audio_file.read()
                    st.write("###### 音轨")
                    st.audio(audio_bytes)
                except:
                    sac.alert(
                        label='**运行后自动显示**',
                        description='有问题可以查阅文档[AAVT](https://zwho5v3j233.feishu.cn/wiki/OGcrwinzhi88MkkvEMVcLkDgnzc?from=from_copylink)，或者加群讨论哦',
                        size='lg', radius=20, icon=True, closable=True, color='info')
                try:
                    height = st.session_state.height
                except:
                    st.session_state.height = 400
                try:
                    with open(st.session_state.output_file + "/output.srt", 'r', encoding='utf-8') as srt_file:
                        srt_content = srt_file.read()
                    srt_data1 = parse_srt_file(srt_content)
                    if st.button('显示恢复', type="primary"):
                        st.session_state.height = st.session_state.height + 1
                        st.toast("已恢复！", icon=":material/task_alt:")
                    edited_data = st.data_editor(srt_data1, height=st.session_state.height, hide_index=True, use_container_width=True)
                    srt_data2 = convert_to_srt(edited_data)
                    st.session_state.srt_content_new = srt_data2
                    with open(st.session_state.output_file + "/output.srt", 'w', encoding='utf-8') as srt_file:
                        srt_file.write(st.session_state.srt_content_new)
                except:
                    srt_data = [{"index": "1", "start": "00:00:00,000", "end": "00:00:10,000", "content": "若出现Error: Minified React error #185，点击 显示恢复 即可！"}]
                    st.data_editor(srt_data, height=st.session_state.height, hide_index=True, use_container_width=True)

        try:
            sac.alert(
                label=f'总耗时：{st.session_state.time}s',
                size='lg', radius=20, icon=True, closable=True, color='success')
        except:
            sac.divider(label='结束线', icon='box-fill', align='center', color='gray')

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
