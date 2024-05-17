import os
import toml
import time
import torch
import datetime
import streamlit as st
import streamlit_antd_components as sac
from utils.utils import (get_whisper_result, kimi_translate, openai_translate1, openai_translate2, chatglm_translate,
                         local_translate, generate_srt_from_result, srt_mv, srt_to_vtt, srt_to_ass, srt_to_stl, show_video,
                         parse_srt_file, convert_to_srt, generate_srt_from_result_2, deepseek_translate, openai_whisper)


def video():
    project_dir = os.path.dirname(os.path.abspath(__file__)).replace("\\", "/")
    cache_dir = project_dir + "/cache/"  # 本地缓存
    config_dir = project_dir.replace("/project", "") + "/config/"  # 配置文件

    # 加载配置
    config = toml.load(config_dir + "config.toml")
    openai_api_key = config["GPT"]["openai_key"]
    openai_api_base = config["GPT"]["openai_base"]
    kimi_api_key = config["KIMI"]["kimi_key"]
    deepseek_api_key = config["DEEPSEEK"]["deepseek_key"]
    chatglm_api_key = config["CHATGLM"]["chatglm_key"]
    faster_whisper_model = config["WHISPER"]["faster_whisper_model_default"]
    faster_whisper_model_local = config["WHISPER"]["faster_whisper_model_local"]
    faster_whisper_model_path = config["WHISPER"]["faster_whisper_model_local_path"]
    openai_whisper_api = config["WHISPER"]["openai_whisper_api"]

    # 页面缓存
    st.session_state.openai_base = openai_api_base
    st.session_state.openai_key = openai_api_key
    st.session_state.kimi_key = kimi_api_key
    st.session_state.deepseek_key = deepseek_api_key
    st.session_state.chatglm_key = chatglm_api_key
    st.session_state.model_local = faster_whisper_model_local
    st.session_state.model_path = faster_whisper_model_path
    st.session_state.faster_whisper_model = faster_whisper_model
    st.session_state.openai_whisper_api = openai_whisper_api

    # 启用设置
    opt_g = 1
    if "distil" not in faster_whisper_model or torch.cuda.is_available():
        opt_g = 0

    # 主页面
    st.title("AI全自动视频翻译📽️")
    st.write("")

    with st.sidebar:
        st.write("### 文件上传器")
        uploaded_file = st.file_uploader("请在这里上传视频：", type=['mp4', 'mov'], label_visibility="collapsed")

    col1, col2 = st.columns(2, gap="medium")
    with col1:
        if not openai_whisper_api:
            with st.expander("**识别设置**", expanded=True):
                col3, col4 = st.columns(2)
                with col3:
                    GPU_on = st.toggle('启用GPU加速', disabled=opt_g, help='自动检测cuda、pytorch可用后开启！')  # GPU
                    VAD_on = st.toggle('启用VAD辅助',
                                       help='启用语音活动检测（VAD）以过滤掉没有语音的音频部分,仅支持faster-whisper使用。')  # VAD
                    device = 'cuda' if GPU_on else 'cpu'
                    vad = 'True' if VAD_on else 'False'
                with col4:
                    language = ('自动识别', 'zh', 'en', 'ja', 'ko', 'it', 'de')  # language
                    lang = st.selectbox('选择视频语言', language, index=0,
                                        help="强制指定视频语言会提高识别准确度，但也可能会造成识别出错。")
        else:
            with st.expander("**API调用模式**", expanded=True):
                proxy_on = st.toggle('启用代理', help='如果你能直接访问openai.com，则无需启用。')

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
            ], label='翻译引擎', search=True, index=0)
            translate_option = translate_option[-1]

            if translate_option == '本地模型':
                col3, col4, col5 = st.columns(3)
                with col3:
                    base_url = st.text_input('模型接口', help='样例: http://127.0.0.1:8888/', value='http://xxx')
                with col4:
                    api_key = st.text_input('模型密钥', help='若无需key，请留空', value='')
                with col5:
                    model_name = st.text_input('模型调用名称', help='样例: chatglm3-6B', value='xxx')

            elif '译' not in translate_option:
                language = ('中文', 'English', '日本語', '한국인', 'Italiano', 'Deutsch')
                col3, col4, col5 = st.columns(3)
                with col3:
                    language1 = st.selectbox('选择原始语言', language, index=1)
                with col4:
                    language2 = st.selectbox('选择目标语言', language, index=0)
                with col5:
                    waittime = st.number_input('翻译间隔设置', min_value=0.0, max_value=5.0, value=0.1, step=0.1)
            else:
                a = None
            if 'gpt' in translate_option and not openai_whisper_api:
                proxy_on = st.toggle('启用代理', help='如果你能直接访问openai.com，则无需启用。')

        with st.expander("**字幕设置**", expanded=True):
            with open(project_dir.replace("/project", "/config") + '/font_data.txt', 'r', encoding='utf-8') as file:
                lines = file.readlines()
                fonts = [line.strip() for line in lines]
                col3, col4 = st.columns(2, gap="medium")
                with col3:
                    subtitle_model = st.selectbox('字幕方式：', ("硬字幕", "软字幕"),
                                                  help="请注意：由于软字幕会导致部分字体会无法正常显示，因此可能会出现乱码！同时，您无法在网页中预览字幕效果，请打开文件夹访问原视频并使用支持外挂字幕的视频播放器挂载字幕查看效果！")
                with col4:
                    font = st.selectbox('视频字幕字体：', fonts,
                                        help="所有字体均从系统读取加载，支持用户自行安装字体。请注意商用风险！")
                    st.session_state.font = font
                col3, col4 = st.columns([0.9, 0.1], gap="medium")
                with col3:
                    font_size = st.number_input('字幕字体大小', min_value=1, max_value=30, value=18, step=1,
                                                help="推荐大小：18")
                    st.session_state.font_size = font_size
                with col4:
                    font_color = st.color_picker('颜色', '#FFFFFF')
                    st.session_state.font_color = font_color
    with col2:
        with st.expander("**高级设置**"):
            if not openai_whisper_api:
                min_vad = st.number_input('VAD静音检测(ms)', min_value=100, max_value=5000, value=500, step=100,
                                          help="启用VAD辅助后生效！对应`min_silence_duration_ms`参数，最小静音持续时间。")
                beam_size = st.number_input('束搜索大小', min_value=1, max_value=20, value=5, step=1,
                                            help="`beam_size`参数。用于定义束搜索算法中每个时间步保留的候选项数量。束搜索算法通过在每个时间步选择最有可能的候选项来构建搜索树，并根据候选项的得分进行排序和剪枝。较大的beam_size值会保留更多的候选项，扩大搜索空间，可能提高生成结果的准确性，但也会增加计算开销。相反，较小的beam_size值会减少计算开销，但可能导致搜索过早地放弃最佳序列。")
            else:
                whisper_prompt = st.text_input('Whisper提示词', value='Don’t make each line too long.')
                temperature = st.number_input('Whisper温度', min_value=0.0, max_value=1.0, value=0.8, step=0.1)
            token_num = st.number_input('翻译最大token限制', min_value=10, max_value=500, value=100, step=10,
                                        help="最大token量为：500*翻译最大token限制")
    with col1:
        if st.button("运行程序", use_container_width=True, type="primary"):
            if uploaded_file is not None:
                msg = st.toast('开始生成!')
                time1 = time.time()
                msg.toast('正在进行视频读取📽️')
                current_time = datetime.datetime.now().strftime("%Y-%m-%d %H-%M-%S")
                output_file = cache_dir + current_time
                print(output_file)
                os.makedirs(output_file)
                with open(output_file + "/uploaded.mp4", "wb") as file:
                    file.write(uploaded_file.getbuffer())

                time2 = time.time()
                msg.toast('正在识别视频内容🔍')
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

                time3 = time.time()
                if translate_option != '译':
                    msg.toast('正在翻译文本🤖')
                    print("---\n翻译模型:" + translate_option)
                    if translate_option == 'gpt-3.5-turbo' or translate_option == 'gpt-4o':
                        result = openai_translate1(st.session_state.openai_key, st.session_state.openai_base,
                                                   proxy_on, result, language1, language2, waittime)
                    elif translate_option == 'gpt-4':
                        result = openai_translate2(st.session_state.openai_key, st.session_state.openai_base,
                                                   proxy_on, result, language1, language2, token_num, waittime)
                    elif translate_option == 'deepseek-v2':
                        result = deepseek_translate(st.session_state.deepseek_key, result, language2, waittime)
                    elif 'glm' in translate_option:
                        result = chatglm_translate(st.session_state.chatglm_key, translate_option, result, language2,
                                                   waittime)
                    elif 'kimi' in translate_option:
                        result = kimi_translate(st.session_state.kimi_key, translate_option, result, language1,
                                                language2, token_num, waittime)
                    elif translate_option == '本地模型':
                        result = local_translate(base_url, api_key, model_name, result, language2)

                time4 = time.time()
                msg.toast('正在生成SRT字幕文件📃')
                srt_content = generate_srt_from_result(result)
                srt_content2 = generate_srt_from_result_2(result, font, font_size, font_color)
                with open(output_file + "/output.srt", 'w', encoding='utf-8') as srt_file:
                    srt_file.write(srt_content2)

                time5 = time.time()
                msg.toast('正在合并视频，请耐心等待生成⚙️')
                srt_mv(output_file, font, font_size, font_color, subtitle_model)

                time6 = time.time()
                st.toast("🎉🎉🎉")
                st.session_state.srt_content = srt_content
                st.session_state.output = output_file
                st.session_state.current = current_time
                st.session_state.time = time6 - time1
                formatted_result = f"{st.session_state.time:.2f}"
                msg.toast('运行成功！总用时：' + str(formatted_result) + "秒")
            else:
                st.toast("请先上传视频")

    with col2:
        with st.expander("**视频预览**", expanded=True):
            try:
                video_bytes = show_video(st.session_state.output)
                st.video(video_bytes)

                if sac.buttons([sac.ButtonsItem(label='查看文件目录', icon='calendar2-minus-fill')], index=None, align='center', variant='filled', use_container_width=True):
                    os.startfile(st.session_state.output)
                    st.toast("注意：文件夹已成功打开，可能未置顶显示，请检查任务栏！")
            except:
                with st.container(height=300):
                    st.write("")
                st.success('''
                    **这里是视频预览窗口**                             
                    **运行后自动显示预览结果**
                ''')

    st.write('''------''')
    st.write('**字幕时间轴**(运行后自动显示)')
    try:
        srt_data1 = parse_srt_file(st.session_state.srt_content)
        edited_data = st.data_editor(srt_data1, height=300, hide_index=True, use_container_width=True)
        srt_data2 = convert_to_srt(edited_data)
        st.session_state.srt_content_new = srt_data2
    except:
        srt_data = [{"index": "", "start": "", "end": "", "content": ""}]
        edited_data = st.data_editor(srt_data, height=300, hide_index=True, use_container_width=True)
    st.write('''
    ------
    ##### 实验功能🧪
    ''')
    st.caption("运行程序后自动显示，实际可能会有BUG，后续版本会逐步完善并实装！")

    col1, col2 = st.columns(2, gap="medium")
    with col1:
        with st.expander("**更多字幕格式**", expanded=True):
            try:
                captions_option = st.radio('字幕导出格式：', ('srt', 'vtt', 'ass', 'stl'), index=0, horizontal=True)
                if captions_option == 'srt':
                    st.download_button(
                        label="点击下载SRT字幕文件",
                        data=st.session_state.srt_content_new.encode('utf-8'),
                        key='srt_download',
                        file_name='output.srt',
                        mime='text/srt',
                        type="primary",
                        use_container_width=True
                    )
                elif captions_option == 'vtt':
                    vtt_content = srt_to_vtt(st.session_state.srt_content_new)
                    st.download_button(
                        label="点击下载VTT字幕文件",
                        data=vtt_content.encode('utf-8'),
                        key='vtt_download',
                        file_name='output.vvt',
                        mime='text/vtt',
                        type="primary",
                        use_container_width=True
                    )
                elif captions_option == 'ass':
                    print(st.session_state.font)
                    print(st.session_state.font_size)
                    print(st.session_state.font_color)
                    ass_content = srt_to_ass(st.session_state.srt_content_new, st.session_state.font,
                                             st.session_state.font_size, st.session_state.font_color)
                    print(1)
                    st.download_button(
                        label="点击下载ASS字幕文件",
                        data=ass_content.encode('utf-8'),
                        key='ass_download',
                        file_name='output.ass',
                        mime='text/ass',
                        type="primary",
                        use_container_width=True
                    )
                elif captions_option == 'stl':
                    stl_content = srt_to_stl(st.session_state.srt_content_new)
                    st.download_button(
                        label="点击下载STL字幕文件",
                        data=stl_content.encode('utf-8'),
                        key='stl_download',
                        file_name='output.stl',
                        mime='text/stl',
                        type="primary",
                        use_container_width=True
                    )
            except:
                st.warning('这里是字幕窗口，运行后自动显示下载按钮。')

        with st.expander("**重新合成**", expanded=True):
            with open(project_dir.replace("/project", "/config") + '/font_data.txt', 'r', encoding='utf-8') as file:
                lines = file.readlines()
                fonts = [line.strip() for line in lines]
                font = st.selectbox('字幕字体：', fonts,
                                    help="所有字体均从系统读取加载，支持用户自行安装字体。请注意商用风险！")
                col3, col4 = st.columns([0.9, 0.1], gap="medium")
                with col3:
                    font_size = st.number_input('字体大小', min_value=1, max_value=30, value=18, step=1,
                                                help="推荐大小：18")
                with col4:
                    font_color = st.color_picker('字体颜色', '#FFFFFF')

            if st.button("重新合成", use_container_width=True, type="primary"):
                st.session_state.output2 = cache_dir + st.session_state.current
                with open(st.session_state.output2 + "/output.srt", 'w', encoding='utf-8') as srt_file:
                    srt_file.write(st.session_state.srt_content_new)

                with st.spinner('正在合并视频，请耐心等待视频生成...'):
                    srt_mv(st.session_state.output2, font, font_size, font_color, subtitle_model)

    with col2:
        with st.expander("**修改后的视频预览**", expanded=True):
            try:
                print(st.session_state.output2)
                video_bytes = show_video(st.session_state.output2)
                st.video(video_bytes)
                print(1)
                if st.button('查看文件', use_container_width=True):
                    os.startfile(st.session_state.output2)
                    st.warning("注意：文件夹已成功打开，可能未置顶显示，请检查任务栏！")
            except:
                st.warning('这里是第二次的视频预览窗口，运行后自动显示预览结果。')
