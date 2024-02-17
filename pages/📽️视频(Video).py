import os
import torch
import datetime
import streamlit as st
from utils.utils import (get_whisper_result, kimi_translate, openai_translate1, openai_translate2,
                         generate_srt_from_result, srt_mv, srt_to_vtt, srt_to_ass, srt_to_stl, show_video,
                         parse_srt_file, convert_to_srt)


project_dir = os.path.dirname(os.path.abspath(__file__)).replace("\\", "/")
log_dir = project_dir + "/public/log.md"  # 更新日志
read_dir = project_dir + "/public/README.md"  # 项目文档
cache_dir = project_dir + "/cache/"  # 本地缓存

st.title("AI全自动视频翻译📽️")

col1, col2 = st.columns(2, gap="medium")
with col1:
    # 文件上传
    uploaded_file = st.file_uploader("请在这里上传视频：", type=['mp4', 'mov'])
    col3, col4 = st.columns(2, gap="medium")
    with col3:
        # GPU加速
        wdc = not torch.cuda.is_available()
        GPU_on = st.toggle('启用GPU加速*', disabled=wdc, help='请确保您正确安装了cuda、pytorch，否则该选项开启无效！')
        device = 'cuda' if GPU_on else 'cpu'
    with col4:
        # VAD辅助
        VAD_on = st.toggle('启用VAD辅助*', help='请使用faster-whisper模型，否则该选项无法开启！')
        vad = 'True' if GPU_on else 'False'

    with open(project_dir.replace("/pages", "/config") + '/font_data.txt', 'r', encoding='utf-8') as file:
        lines = file.readlines()
    # 创建字体列表
    fonts = [line.strip() for line in lines]
    font = st.selectbox('选择字幕字体格式：', fonts, help="所有字体均从系统读取加载，支持用户自行安装字体。请注意商用风险！", key="微软雅黑")

    # 翻译模型
    translate_option = st.selectbox('请在这里选择翻译模型：', ('kimi', 'gpt-3.5-turbo', 'gpt-4', '无需翻译'), index=0)
    if translate_option != '无需翻译':
        col3, col4 = st.columns(2)
        with col3:
            language1 = st.selectbox('原始语言', ('中文', 'English', '日本語', '한국인', 'Italiano', 'Deutsch'),
                                     index=1)
        with col4:
            language2 = st.selectbox('目标语言', ('中文', 'English', '日本語', '한국인', 'Italiano', 'Deutsch'),
                                     index=0)
        if st.button('运行程序'):
            if uploaded_file is not None:
                with st.spinner('正在加载视频缓存...'):
                    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H-%M-%S")
                    output_file = cache_dir + current_time
                    os.makedirs(output_file)
                    with open(output_file + "/uploaded.mp4", "wb") as file:
                        file.write(uploaded_file.getbuffer())

                with st.spinner('正在识别视频内容...'):
                    # whisper识别
                    result = get_whisper_result(uploaded_file, output_file, device, st.session_state.w_model_option,
                                                st.session_state.w_name, vad)
                    print("whisper识别：" + result['text'])

                with st.spinner('正在翻译文本...'):
                    if translate_option == 'kimi':
                        result = kimi_translate(st.session_state.kimi_key, result, language1,
                                                language2)  # 使用kimi翻译成目标语言
                    elif translate_option == 'gpt-3.5-turbo':
                        result = openai_translate1(st.session_state.openai_key, st.session_state.openai_base, st.session_state.proxy_on,
                                                   result, language1, language2)  # 使用gpt3.5翻译成目标语言
                    elif translate_option == 'gpt-4':
                        result = openai_translate2(st.session_state.openai_key, st.session_state.openai_base, st.session_state.proxy_on,
                                                   result, language1, language2, )  # 使用gpt4翻译成目标语言

                with st.spinner('正在生成SRT字幕文件...'):
                    srt_content = generate_srt_from_result(result)  # 生成SRT字幕内容
                    with open(output_file + "/output.srt", 'w', encoding='utf-8') as srt_file:  # 将SRT内容写入SRT文件
                        srt_file.write(srt_content)

                with st.spinner('正在合并视频，请耐心等待视频生成...'):
                    srt_mv(output_file, font)

                st.session_state.srt_content = srt_content
                st.session_state.output = output_file
            else:
                st.warning("请先上传视频")

    elif translate_option == '无需翻译':
        if st.button('运行程序'):
            if uploaded_file is not None:
                with st.spinner('正在加载视频缓存...'):
                    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H-%M-%S")
                    output_file = cache_dir + current_time
                    os.makedirs(output_file)
                    with open(output_file + "/uploaded.mp4", "wb") as file:
                        file.write(uploaded_file.getbuffer())

                with st.spinner('正在识别视频内容...'):
                    # whisper识别
                    result = get_whisper_result(uploaded_file, cache_dir, device, st.session_state.w_model_option,
                                                st.session_state.w_name, vad)

                    print("whisper识别：" + result['text'])

                with st.spinner('正在生成SRT字幕文件...'):
                    srt_content = generate_srt_from_result(result)  # 生成SRT字幕内容
                    with open(output_file + "/output.srt", 'w', encoding='utf-8') as srt_file:  # 将SRT内容写入SRT文件
                        srt_file.write(srt_content)

                with st.spinner('正在合并视频，请耐心等待视频生成...'):
                    srt_mv(output_file, font)

                st.session_state.srt_content = srt_content
                st.session_state.output = output_file
            else:
                st.warning("请先上传视频")

with col2:
    c = st.container(border=True, height=500)
    c.write('预览和下载（Preview & Download）')
    captions_option = c.radio('下载的字幕格式：', ('srt', 'vtt', 'ass', 'stl'), index=0, horizontal=True)
    try:
        if captions_option == 'srt':
            c.download_button(
                label="点击下载SRT字幕文件",
                data=st.session_state.srt_content.encode('utf-8'),
                key='srt_download',
                file_name='output.srt',
                mime='text/srt',
            )
        elif captions_option == 'vtt':
            vtt_content = srt_to_vtt(st.session_state.srt_content)
            c.download_button(
                label="点击下载VTT字幕文件",
                data=vtt_content.encode('utf-8'),
                key='vtt_download',
                file_name='output.vvt',
                mime='text/vtt',
            )
        elif captions_option == 'ass':
            ass_content = srt_to_ass(st.session_state.srt_content)
            c.download_button(
                label="点击下载ASS字幕文件",
                data=ass_content.encode('utf-8'),
                key='ass_download',
                file_name='output.ass',
                mime='text/ass',
            )
        elif captions_option == 'stl':
            stl_content = srt_to_stl(st.session_state.srt_content)
            c.download_button(
                label="点击下载STL字幕文件",
                data=stl_content.encode('utf-8'),
                key='stl_download',
                file_name='output.stl',
                mime='text/stl',
            )

    except:
        if uploaded_file is not None:
            c.success("视频上传成功")
        c.warning('这里是预览窗口，运行后自动显示预览结果。')

    try:
        video_bytes = show_video(st.session_state.output)
        c.video(video_bytes)
    except:
        c.write('')

st.write('''
------
##### 实验功能🧪
''')
st.caption("运行程序后自动显示，实际可能会有BUG，后续版本会逐步完善并实装！")
try:
    st.caption("Tips：文本内容可以在左侧表格进行修改微调")
    high = st.slider('文本预览表格的高度', 100, 1000, 500, 50)
    col1, col2 = st.columns(2, gap="medium")
    with col1:
        srt_data = parse_srt_file(st.session_state.srt_content)
        st.dataframe(srt_data, height=high, hide_index=True, use_container_width=True)
        st.download_button(
            label="下载原始的文件（SRT格式）",
            data=st.session_state.srt_content.encode('utf-8'),
            file_name='output_old.txt'
        )
    with col2:
        edited_data = st.data_editor(srt_data, height=high, hide_index=True, use_container_width=True)
        srt = convert_to_srt(edited_data)
        st.download_button(
            label="下载修改的文件（SRT格式）",
            data=srt.encode('utf-8'),
            file_name='output_new.txt'
        )
except:
    st.write('')
