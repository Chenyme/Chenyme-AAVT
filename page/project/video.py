import os
import re
import json
import toml
import time
import datetime
import streamlit as st
from openai import OpenAI
from pydantic import BaseModel
import streamlit_antd_components as sac
from styles.global_style import style
from utils.public import (FileToMp3, OpenaiWhisperResult, runWhisperSeperateProc, translate, local_translate, encode_image,
                          generate_srt_from_result, generate_srt_from_result_2, srt_mv, parse_srt_file, convert_to_srt,
                          show_video, add_font_settings, srt_to_ass, srt_to_vtt, srt_to_sbv, extract_frames, write_llms)

style()

path = os.getcwd() + "/"
llms_path = path + "config/llms.toml"
whisper_path = path + "config/whisper.toml"
font_data_path = path + "config/font.txt"
video_config_path = path + "config/video.toml"
blog_config_path = path + "config/blog.toml"
prompt_config_path = path + "config/prompt.json"
project_config_path = path + "config/project.toml"
video_cache_path = path + "cache/video/"
blog_cache_path = path + "cache/blog/"

with open(llms_path, 'r', encoding="utf-8") as config_file:
    llms = toml.load(config_file)
with open(whisper_path, 'r', encoding="utf-8") as config_file:
    whispers = toml.load(config_file)
with open(video_config_path, 'r', encoding="utf-8") as config_file:
    video_config = toml.load(config_file)
with open(prompt_config_path, 'r', encoding='utf-8') as config_file:
    prompt = json.load(config_file)
with open(project_config_path, 'r', encoding='utf-8') as config_file:
    project = toml.load(config_file)
with open(font_data_path, 'r', encoding='utf-8') as file:
    lines = file.readlines()
    fonts = [line.strip() for line in lines]
with open(blog_config_path, 'r', encoding="utf-8") as config_file:
    blog_config = toml.load(config_file)

home_key = llms["Home"]["key"]  # home
home_url = llms["Home"]["url"]
home_model = llms["Home"]["model"]

local_key = llms["Local"]["key"]  # Local
local_url = llms["Local"]["url"]
local_model = llms["Local"]["model"]

custom_key = llms["Custom"]["key"]  # Custom
custom_base = llms["Custom"]["url"]
custom_model = llms["Custom"]["model"]

global_key = llms["Global"]["key"]  # Global
global_url = llms["Global"]["url"]

chatgpt_key = llms["ChatGPT"]["key"]  # Openai
chatgpt_url = llms["ChatGPT"]["url"]

claude_key = llms["Claude"]["key"]  # claude
claude_url = llms["Claude"]["url"]

gemini_key = llms["Gemini"]["key"]  # Gemini
gemini_url = llms["Gemini"]["url"]

deepseek_key = llms["DeepSeek"]["key"]  # deepseek
deepseek_url = llms["DeepSeek"]["url"]

kimi_key = llms["Kimi"]["key"]  # kimi
kimi_base = llms["Kimi"]["url"]

chatglm_key = llms["ChatGLM"]["key"]  # chatglm
chatglm_url = llms["ChatGLM"]["url"]

ai01_key = llms["Yi"]["key"]  # 01
ai01_url = llms["Yi"]["url"]

whisper_mode = whispers["Mode"]["WhisperMode"]  # whisper_mode

whisper_temp = whispers["OpenAI"]["Temp"]  # whisper_temp
whisper_prompt = whispers["OpenAI"]["Prompt"]  # whisper_mode

faster_gpu = whispers["Faster"]["GPU"]  # faster_gpu
faster_vad = whispers["Faster"]["VAD"]  # faster_vad
faster_temp = whispers["Faster"]["Temp"]  # faster_temp
faster_prompt = whispers["Faster"]["Prompt"]  # faster_prompt
faster_min_vad = whispers["Faster"]["min_vad"]  # faster_min_vad
faster_beam_size = whispers["Faster"]["beam_size"]  # faster_beam_size

faster_local_path = whispers["Faster_Local"]["path"]  # 模型路径
faster_local_gpu = whispers["Faster_Local"]["GPU"]  # GPU 加速
faster_local_vad = whispers["Faster_Local"]["VAD"]  # VAD
faster_local_temp = whispers["Faster_Local"]["Temp"]  # 温度
faster_local_prompt = whispers["Faster_Local"]["Prompt"]  # 提示词
faster_local_min_vad = whispers["Faster_Local"]["min_vad"]  # 最小 VAD 持续时间
faster_local_beam_size = whispers["Faster_Local"]["beam_size"]  # Beam Size

language = video_config["whisper"]["language_list"]
openai_whisper_model_list = video_config["whisper"]["openai_whisper_model_list"]
faster_whisper_model_list = video_config["whisper"]["faster_whisper_model_list"]
language_index = video_config["whisper"]["language_index"]
openai_whisper_model_index = video_config["whisper"]["openai_whisper_model_index"]
faster_whisper_model_index = video_config["whisper"]["faster_whisper_model_index"]
faster_whisper_model_local_index = video_config["whisper"]["faster_whisper_model_local_index"]

video_translate_index = video_config["translate"]["translate_index"]
video_language2 = video_config["translate"]["language_list"]
video_language2_index1 = video_config["translate"]["language_index1"]
video_language2_index2 = video_config["translate"]["language_index2"]
video_wait_time_setting = video_config["translate"]["wait_time"]
video_prompt_pre_setting = video_config["translate"]["prompt"]
system_prompt = prompt[video_prompt_pre_setting]["system_prompt"].replace("{language1}", video_language2_index1).replace("{language2}", video_language2_index2)
user_prompt = prompt[video_prompt_pre_setting]["user_prompt"].replace("{language1}", video_language2_index1).replace("{language2}", video_language2_index2)

subtitle_model_setting = video_config["subtitle"]["subtitle_model"]
font_setting = video_config["subtitle"]["font"]
soft_font_size_setting = video_config["subtitle"]["soft_font_size"]
hard_font_size_setting = video_config["subtitle"]["hard_font_size"]
srt_setting = video_config["subtitle"]["srt"]
font_color_setting = video_config["subtitle"]["font_color"]
video_readme = video_config["other"]["first"]

blog_language_list = blog_config["article"]["language_list"]
blog_language = blog_config["article"]["language"]
blog_token = blog_config["article"]["token"]
blog_view = blog_config["article"]["view"]
blog_temp = blog_config["article"]["temp"]
blog_write_index = blog_config["article"]["index"]
blog_time_interval = blog_config["article"]["time"]

log_setting = project["ffmpeg"]["log"]
crf_setting = project["ffmpeg"]["crf"]
quality_setting = project["ffmpeg"]["quality"]
ffmpeg_setting = project["ffmpeg"]["ffmpeg"]

translation_dict = {
    (0,): '无需翻译',
    (1,): 'Local / 本地模型',
    (2, 3): 'gpt-3.5-turbo',
    (2, 4): 'gpt-4o-mini',
    (2, 5): 'gpt-4',
    (2, 6): 'gpt-4-turbo',
    (2, 7): 'gpt-4o',
    (8, 9): 'claude-3-opus',
    (10, 8): 'claude-3-sonnet',
    (11, 8): 'claude-3-haiku',
    (12, 13): 'gemini-pro',
    (12, 14): 'gemini-1.0-pro',
    (12, 15): 'gemini-1.5-flash',
    (12, 16): 'gemini-1.5-pro',
    (17, 18): 'deepseek-chat',
    (17, 19): 'deepseek-coder',
    (20, 21): 'moonshot-v1-8k',
    (20, 22): 'moonshot-v1-32k',
    (20, 23): 'moonshot-v1-128k',
    (24, 25): 'glm-4',
    (24, 26): 'glm-4-0520',
    (24, 27): 'glm-4-flash',
    (24, 28): 'glm-4-air',
    (24, 29): 'glm-4-airx',
    (30, 31): 'yi-spark',
    (30, 32): 'yi-medium',
    (30, 33): 'yi-medium-200k',
    (30, 34): 'yi-vision',
    (30, 35): 'yi-large',
    (30, 36): 'yi-large-rag',
    (30, 37): 'yi-large-turbo',
    (30, 38): 'yi-large-preview'
}


@st.dialog("使用提示")
def VideoReadme():
    st.write("""
    ## 欢迎首次使用 AI全自动视频翻译 功能！

    为了确保顺利运行并获得最佳体验，请关闭此弹窗后，前往页面中的**参数设置**模块，进行必要的参数配置。根据您的需求调整设置，以提高翻译和图文博客生成的准确性和效率。

    如果您需要更多帮助，可以参考以下资源：
    - 📘 [相关教程](https://blog.chenyme.top/blog/aavt-install)
    - 📂 [项目地址](https://github.com/Chenyme/Chenyme-AAVT)
    - 💬 [交流群组](https://t.me/+j8SNSwhS7xk1NTc9)

    """)
    st.write("")

    if st.button("**我已知晓&nbsp;&nbsp;&nbsp;不再弹出**", type="primary", use_container_width=True, key="blog_first_button"):
        with open(video_config_path, 'w', encoding="utf-8") as f:
            video_config["other"]["first"] = True
            toml.dump(video_config, f)
        st.session_state.read = True
        st.rerun()
    st.write("")


if not video_readme:
    VideoReadme()
if "save" in st.session_state:
    st.toast("参数已成功保存", icon=":material/verified:")
    del st.session_state["save"]
if "read" in st.session_state:
    st.toast("欢迎使用 ~", icon=":material/verified:")
    del st.session_state["read"]
if "upload" in st.session_state:
    st.toast("文件上传成功！", icon=":material/verified:")
    del st.session_state["upload"]


tab1, tab2, tab3, tab4 = st.tabs(["**视频识别**", "**批量翻译**", "**图文博客**", "**参数设置**"])
with tab4:

    @st.dialog("语言说明")
    def Video_lang():
        st.write("**强制指定视频语言会提高识别准确度，但也可能会造成识别出错。** \n\n`自动识别` - 自动检测语言 (Auto Detect) \n\n`zh` - 中文 (Chinese) - 中文 \n\n`en` - 英语 (English) - English \n\n`ja` - 日语 (Japanese) - 日本語 \n\n`th` - 泰语 (Thai) - ภาษาไทย \n\n`de` - 德语 (German) - Deutsch \n\n`fr` - 法语 (French) - français \n\n`ru` - 俄语 (Russian) - Русский \n\n`ko` - 韩语 (Korean) - 한국어 \n\n`vi` - 越南语 (Vietnamese) - Tiếng Việt \n\n`it` - 意大利语 (Italian) - Italiano \n\n`ar` - 阿拉伯语 (Arabic) - العربية \n\n`es` - 西班牙语 (Spanish) - Español \n\n`bn` - 孟加拉语 (Bengali) - বাংলা \n\n`pt` - 葡萄牙语 (Portuguese) - Português \n\n`hi` - 印地语 (Hindi) - हिंदी")

    VideoSave = st.container()
    WhisperSetting = st.expander("**识别模型**", expanded=True, icon=":material/radio_button_checked:")
    VideoSetting = st.expander("**视频生成**", expanded=False, icon=":material/movie:")
    BlogSetting = st.expander("**图文博客**", expanded=False, icon=":material/rss_feed:")

    with WhisperSetting:
        st.write("#### Whisper 识别参数 ")
        st.write("")
        if whisper_mode == "OpenAIWhisper - API":
            st.write("###### 识别模型")
            st.caption("使用 OpenAI API 支持调用的 Whisper 模型 ")
            openai_whisper_model_index = st.selectbox("Whisper 模型", openai_whisper_model_list, openai_whisper_model_list.index(openai_whisper_model_index), label_visibility="collapsed")
            st.write("")
        if whisper_mode == "FasterWhisper - AutoDownload":
            st.write("###### 识别模型")
            st.caption("使用 FasterWhisper 支持调用的 Whisper 模型 ")
            faster_whisper_model_index = st.selectbox("Whisper 模型", faster_whisper_model_list, faster_whisper_model_list.index(faster_whisper_model_index), label_visibility="collapsed")
        if whisper_mode == "FasterWhisper - LocalModel":
            st.write("###### 识别模型")
            st.caption("使用已部署到本地的 FasterWhisper 模型 | [支持的模型](https://huggingface.co/Systran) | [使用教程](https://blog.chenyme.top/blog/aavt-install#bfd48658b23b)")
            model_names = os.listdir(faster_local_path)
            try:
                faster_whisper_model_local_index = st.selectbox("Whisper 本地模型", model_names, model_names.index(faster_whisper_model_local_index), label_visibility="collapsed")
            except:
                faster_whisper_model_local_index = st.selectbox("Whisper 本地模型", model_names)
        st.write("")
        if whisper_mode != "OpenAIWhisper - API":
            st.write("###### 视频语言")
            st.caption("强制指定视频语言")
            col1, col2 = st.columns([0.95, 0.05])
            with col1:
                language_index = st.selectbox('Media 语言', language, index=language.index(language_index), label_visibility="collapsed")
            with col2:
                if st.button("**?**", use_container_width=True):
                    Video_lang()
        st.write("")
    with VideoSetting:
        st.write("#### LLMs 翻译参数 ")
        st.write("")
        st.write("###### 翻译引擎")
        st.caption("翻译模块使用的引擎，请确保您已在全局设置中配置对应的引擎参数！")
        video_translate_index = sac.cascader(items=[
            sac.CasItem('无需翻译'),
            sac.CasItem('Local / 本地模型', icon='house-up-fill'),
            sac.CasItem('OpenAI / ChatGPT', icon='folder2', children=[
                sac.CasItem('gpt-3.5-turbo', icon='folder2-open'),
                sac.CasItem('gpt-4o-mini', icon='folder2-open'),
                sac.CasItem('gpt-4', icon='folder2-open'),
                sac.CasItem('gpt-4-turbo', icon='folder2-open'),
                sac.CasItem('gpt-4o', icon='folder2-open')]),
            sac.CasItem('Anthropic / Claude', icon='folder2', children=[
                sac.CasItem('claude-3-opus', icon='folder2-open'),
                sac.CasItem('claude-3-sonnet', icon='folder2-open'),
                sac.CasItem('claude-3-haiku', icon='folder2-open')]),
            sac.CasItem('谷歌公司 / Gemini', icon='folder2', children=[
                sac.CasItem('gemini-pro', icon='folder2-open'),
                sac.CasItem('gemini-1.0-pro', icon='folder2-open'),
                sac.CasItem('gemini-1.5-flash', icon='folder2-open'),
                sac.CasItem('gemini-1.5-pro', icon='folder2-open')]),
            sac.CasItem('深度求索 / DeepSeek', icon='folder2', children=[
                sac.CasItem('deepseek-chat', icon='folder2-open'),
                sac.CasItem('deepseek-coder', icon='folder2-open')]),
            sac.CasItem('月之暗面 / Kimi', icon='folder2', children=[
                sac.CasItem('kimi-moonshot-v1-8k', icon='folder2-open'),
                sac.CasItem('kimi-moonshot-v1-32k', icon='folder2-open'),
                sac.CasItem('kimi-moonshot-v1-128k', icon='folder2-open')]),
            sac.CasItem('智谱清言 / ChatGLM', icon='folder2', children=[
                sac.CasItem('glm-4', icon='folder2-open'),
                sac.CasItem('glm-4-0520', icon='folder2-open'),
                sac.CasItem('glm-4-flash', icon='folder2-open'),
                sac.CasItem('glm-4-air', icon='folder2-open'),
                sac.CasItem('glm-4-airx', icon='folder2-open')]),
            sac.CasItem('零一万物 / Yi', icon='folder2', children=[
                sac.CasItem('yi-spark', icon='folder2-open'),
                sac.CasItem('yi-medium', icon='folder2-open'),
                sac.CasItem('yi-medium-200k', icon='folder2-open'),
                sac.CasItem('yi-vision', icon='folder2-open'),
                sac.CasItem('yi-large', icon='folder2-open'),
                sac.CasItem('yi-large-rag', icon='folder2-open'),
                sac.CasItem('yi-large-turbo', icon='folder2-open'),
                sac.CasItem('yi-large-preview', icon='folder2-open')]),
        ], label='', search=True, index=video_translate_index, return_index=True)
        if video_translate_index != [0]:
            st.write("")
            col1, col2 = st.columns(2)
            with col1:
                st.write("###### 原始语言")
                st.caption("文件的原始语言")
                video_language2_index1 = st.selectbox('原始语言', video_language2, index=video_language2.index(video_language2_index1), label_visibility="collapsed")
            with col2:
                st.write("###### 目标语言")
                st.caption("文件的目标语言")
                video_language2_index2 = st.selectbox('目标语言', video_language2, index=video_language2.index(video_language2_index2), label_visibility="collapsed")
            st.write("")
            st.write("###### 翻译提示词")
            st.caption("翻译使用的提示词，可前往全局设置-翻译设置中配置新的提示词")
            try:
                video_prompt_pre_setting = st.selectbox('预设 prompt', prompt.keys(), index=list(prompt.keys()).index(video_prompt_pre_setting), label_visibility="collapsed")
            except:
                video_prompt_pre_setting = st.selectbox('预设 prompt', prompt.keys(), label_visibility="collapsed")
            st.write("")
            st.write("###### API 调用间隔 / s")
            st.caption("翻译时API的调用间隔。请参阅您的API服务商文档中的 每分钟调用最大限制速率 进行适当调整，若翻译时遇到报错 429：`Too Many Requests`、`RateLimitError` 请适当增大间隔。")
            video_wait_time_setting = st.number_input('翻译间隔(s)', min_value=0.0, max_value=5.0, value=video_wait_time_setting, step=0.1, label_visibility="collapsed")

        st.write("")
        st.write("#### 字幕样式参数 ")
        st.write("")
        st.write("###### 字幕模式")
        st.caption("最终视频字幕模式。注意：页面内无法预览软字幕效果！请自行打开任务目录使用支持外挂字幕的视频播放器挂载字幕查看效果！")
        subtitle_model_setting = st.selectbox('字幕模式', ["硬字幕", "软字幕"], index=["硬字幕", "软字幕"].index(subtitle_model_setting), label_visibility="collapsed")
        st.write("")

        col3, col4 = st.columns([0.85, 0.15])
        with col3:
            st.write("###### 字幕字体")
            st.caption("每次运行项目时字体会从系统自动读取加载。请注意字体商用风险！")
            try:
                font_setting = st.selectbox('字幕字体', fonts, index=fonts.index(font_setting), label_visibility="collapsed")
            except:
                font_setting = st.selectbox('字幕字体', fonts, label_visibility="collapsed")
        with col4:
            st.write("###### 颜色")
            st.caption("字体颜色")
            font_color_setting = st.color_picker('颜色', value=font_color_setting, label_visibility="collapsed")

        st.write("")
        if subtitle_model_setting == "软字幕":
            st.write("###### 软字幕大小")
            st.caption("软字幕的字体大小，推荐大小为`60`")
            soft_font_size_setting = st.number_input('软字幕大小', min_value=30, max_value=90, value=soft_font_size_setting, step=1, label_visibility="collapsed")
        else:
            st.write("###### 硬字幕大小")
            st.caption("硬字幕的字体大小，推荐大小为`18`")
            hard_font_size_setting = st.number_input('硬字幕大小', min_value=1, max_value=36, value=hard_font_size_setting, step=1, label_visibility="collapsed")
        st.write("")
        st.write("###### 双语字幕")
        st.caption("选择双语字幕的显示样式")
        srt_choose = ["关闭", "原始语言为首", "目标语言为首"]
        srt_setting = st.selectbox('双语字幕', srt_choose, index=srt_choose.index(srt_setting), label_visibility="collapsed")
        st.write("")
    with BlogSetting:
        st.write("")
        st.write("###### 视频截取频率")
        st.caption("每多少秒截取一次图片")
        blog_time_interval = st.number_input("频率", min_value=1, value=blog_time_interval, label_visibility="collapsed")
        st.write("###### 写作模型")
        st.caption("写作使用的大模型")
        blog_write_index = sac.cascader(items=[
            sac.CasItem('无需翻译', disabled=True),
            sac.CasItem('Local / 本地模型', icon='house-up-fill'),
            sac.CasItem('OpenAI / ChatGPT', icon='folder2', children=[
                sac.CasItem('gpt-3.5-turbo', icon='folder2-open'),
                sac.CasItem('gpt-4o-mini', icon='folder2-open'),
                sac.CasItem('gpt-4', icon='folder2-open'),
                sac.CasItem('gpt-4-turbo', icon='folder2-open'),
                sac.CasItem('gpt-4o', icon='folder2-open')]),
            sac.CasItem('Anthropic / Claude', icon='folder2', children=[
                sac.CasItem('claude-3-opus', icon='folder2-open'),
                sac.CasItem('claude-3-sonnet', icon='folder2-open'),
                sac.CasItem('claude-3-haiku', icon='folder2-open')]),
            sac.CasItem('谷歌公司 / Gemini', icon='folder2', children=[
                sac.CasItem('gemini-pro', icon='folder2-open'),
                sac.CasItem('gemini-1.0-pro', icon='folder2-open'),
                sac.CasItem('gemini-1.5-flash', icon='folder2-open'),
                sac.CasItem('gemini-1.5-pro', icon='folder2-open')]),
            sac.CasItem('深度求索 / DeepSeek', icon='folder2', children=[
                sac.CasItem('deepseek-chat', icon='folder2-open'),
                sac.CasItem('deepseek-coder', icon='folder2-open')]),
            sac.CasItem('月之暗面 / Kimi', icon='folder2', children=[
                sac.CasItem('kimi-moonshot-v1-8k', icon='folder2-open'),
                sac.CasItem('kimi-moonshot-v1-32k', icon='folder2-open'),
                sac.CasItem('kimi-moonshot-v1-128k', icon='folder2-open')]),
            sac.CasItem('智谱清言 / ChatGLM', icon='folder2', children=[
                sac.CasItem('glm-4', icon='folder2-open'),
                sac.CasItem('glm-4-0520', icon='folder2-open'),
                sac.CasItem('glm-4-flash', icon='folder2-open'),
                sac.CasItem('glm-4-air', icon='folder2-open'),
                sac.CasItem('glm-4-airx', icon='folder2-open')]),
            sac.CasItem('零一万物 / Yi', icon='folder2', children=[
                sac.CasItem('yi-spark', icon='folder2-open'),
                sac.CasItem('yi-medium', icon='folder2-open'),
                sac.CasItem('yi-medium-200k', icon='folder2-open'),
                sac.CasItem('yi-vision', icon='folder2-open'),
                sac.CasItem('yi-large', icon='folder2-open'),
                sac.CasItem('yi-large-rag', icon='folder2-open'),
                sac.CasItem('yi-large-turbo', icon='folder2-open'),
                sac.CasItem('yi-large-preview', icon='folder2-open')]),
        ], label='', search=True, index=blog_write_index, return_index=True)
        st.write("")
        st.write("###### 写作视角")
        st.caption("限制写作人视角")
        blog_view = st.text_input("写作视角", value=blog_view, label_visibility="collapsed")
        st.write("")
        st.write("###### 写作语言")
        st.caption("限制写作使用的语言")
        blog_language = st.selectbox("写作语言", blog_language_list, blog_language_list.index(blog_language), label_visibility="collapsed")
        st.write("")
        st.write("###### 写作字数")
        st.caption("限制写作最少字数")
        blog_token = st.number_input("写作字数", min_value=100, value=blog_token, label_visibility="collapsed")
        st.write("")
        st.write("###### 写作创新性")
        st.caption("数值越高，创新性越高，但也越不稳定")
        blog_temp = st.number_input("创造性", min_value=0.00, max_value=1.00, value=blog_temp, label_visibility="collapsed")
        st.write("")
    with VideoSave:
        col1, col2 = st.columns([0.75, 0.25])
        st.write("")
        with col2:
            st.write("")
            st.write("")
            if st.button("**保存更改**", use_container_width=True, type="primary"):
                with open(video_config_path, 'w', encoding="utf-8") as f:
                    video_config["whisper"]["language_index"] = language_index
                    video_config["whisper"]["openai_whisper_model_index"] = openai_whisper_model_index
                    video_config["whisper"]["faster_whisper_model_index"] = faster_whisper_model_index
                    video_config["whisper"]["faster_whisper_model_local_index"] = faster_whisper_model_local_index

                    video_config["translate"]["translate_index"] = video_translate_index
                    video_config["translate"]["language_index1"] = video_language2_index1
                    video_config["translate"]["language_index2"] = video_language2_index2
                    video_config["translate"]["wait_time"] = video_wait_time_setting
                    video_config["translate"]["prompt"] = video_prompt_pre_setting

                    video_config["subtitle"]["subtitle_model"] = subtitle_model_setting
                    video_config["subtitle"]["font"] = font_setting
                    video_config["subtitle"]["soft_font_size"] = soft_font_size_setting
                    video_config["subtitle"]["hard_font_size"] = hard_font_size_setting
                    video_config["subtitle"]["srt"] = srt_setting
                    video_config["subtitle"]["font_color"] = font_color_setting
                    toml.dump(video_config, f)

                with open(blog_config_path, 'w', encoding="utf-8") as f:
                    blog_config["article"]["language_list"] = blog_language_list
                    blog_config["article"]["language"] = blog_language
                    blog_config["article"]["token"] = blog_token
                    blog_config["article"]["view"] = blog_view
                    blog_config["article"]["temp"] = blog_temp
                    blog_config["article"]["index"] = blog_write_index
                    blog_config["article"]["time"] = blog_time_interval
                    toml.dump(blog_config, f)
                st.session_state.save = True
                st.rerun()
        with col1:
            st.write("")
            st.write("")
            st.write("### 更改参数设置")
            st.caption("Changing Parameter Settings")

with tab1:
    # 配置处理
    font_size_setting = hard_font_size_setting
    if subtitle_model_setting == "软字幕":
        font_size_setting = soft_font_size_setting
    faster_whisper_model_local_index = faster_local_path + "/" + faster_whisper_model_local_index

    col1, col2 = st.columns([0.75, 0.28])  # 置顶标题、执行按钮流程模块

    # 标题模块
    with col1:
        st.write("")
        st.write("")
        st.subheader("AI 全自动视频翻译")
        st.caption("AI Automatic Video Translation")

    # 执行按钮流程模块
    with col2:
        st.write("")
        allow = st.checkbox("**本次不合并视频**", help="勾选后，本次识别过程中仅识别并翻译(如果有)视频字幕，不主动合并字幕。")
        if st.button("**开始识别**", type="primary", use_container_width=True):
            if "uploaded_file_video" in st.session_state:
                uploaded_file_video = st.session_state.uploaded_file_video
                print("\n" + "=" * 50)
                print("\n\033[1;39m*** Chenyme-AAVT AI音频识别 ***\033[0m")
                st.toast('任务开始执行！请勿在运行时切换菜单或修改参数!', icon=":material/rocket_launch:")

                msg_ved = st.toast('正在对视频进行预处理', icon=":material/movie:")
                current_time = datetime.datetime.now().strftime("_%Y%m%d%H%M%S")
                st.session_state.video_name_original = uploaded_file_video.name.split('.')[0]
                st.session_state.srt_name = "uploaded." + uploaded_file_video.name.split('.')[-1]
                output_file = video_cache_path + st.session_state.video_name_original + current_time
                os.makedirs(output_file)
                with open(f"{output_file}/{st.session_state.srt_name}", "wb") as file:
                    file.write(uploaded_file_video.getbuffer())

                print("\n\033[1;34m🚀 任务开始执行\033[0m")
                print(f"\033[1;34m📂 本次任务目录:\033[0m\033[1;34m {output_file} \033[0m")
                print("\033[1;33m⚠️ 请不要在任务运行期间切换菜单或修改参数！\033[0m")
                msg_ved.toast("视频预处理完成", icon=":material/movie:")
                FileToMp3(log_setting, f"{output_file}/{st.session_state.srt_name}", output_file)

                msg_whs = st.toast("正在识别视频内容", icon=":material/troubleshoot:")
                if whisper_mode == "OpenAIWhisper - API":
                    result = OpenaiWhisperResult(chatgpt_key, chatgpt_url, output_file, openai_whisper_model_index, whisper_prompt, whisper_temp)
                if whisper_mode == "FasterWhisper - AutoDownload":
                    result = runWhisperSeperateProc(output_file, faster_gpu, faster_whisper_model_index, faster_prompt, faster_temp, faster_vad, language_index, faster_beam_size, faster_min_vad)
                if whisper_mode == "FasterWhisper - LocalModel":
                    result = runWhisperSeperateProc(output_file, faster_local_gpu, faster_whisper_model_local_index, faster_local_prompt, faster_local_temp, faster_local_vad, language_index, faster_local_beam_size, faster_local_min_vad)
                if 'error' in result:
                    print(f"\033[1;31m❌ Whisper识别异常: {result['error']}\033[0m")
                    st.error(f"处理失败，错误信息：{result['error']}")
                    st.stop()
                print("\033[1;34m🎉 Whisper 识别成功！\033[0m")
                msg_whs.toast("视频内容识别完成", icon=":material/colorize:")

                translate_option = translation_dict[tuple(video_translate_index)]
                if translate_option != '无需翻译':
                    msg_tra = st.toast("正在翻译字幕", icon=":material/translate:")
                    if '本地模型' in translate_option:
                        result = local_translate(system_prompt, user_prompt, local_key, local_url, local_model, result, srt_setting)
                    elif 'gemini' in translate_option:
                        result = translate(system_prompt, user_prompt, gemini_key, gemini_url, translate_option, result, video_wait_time_setting, srt_setting)
                    elif 'yi' in translate_option:
                        result = translate(system_prompt, user_prompt, ai01_key, ai01_url, translate_option, result, video_wait_time_setting, srt_setting)
                    elif 'gpt' in translate_option:
                        result = translate(system_prompt, user_prompt, chatgpt_key, chatgpt_url, translate_option, result, video_wait_time_setting, srt_setting)
                    elif 'moonshot' in translate_option:
                        result = translate(system_prompt, user_prompt, kimi_key, kimi_base, translate_option, result, video_wait_time_setting, srt_setting)
                    elif 'glm' in translate_option:
                        result = translate(system_prompt, user_prompt, chatglm_key, chatglm_url, translate_option, result, video_wait_time_setting, srt_setting)
                    elif 'deepseek' in translate_option:
                        result = translate(system_prompt, user_prompt, deepseek_key, deepseek_url, translate_option, result, video_wait_time_setting, srt_setting)
                    elif 'claude' in translate_option:
                        result = translate(system_prompt, user_prompt, claude_key, claude_url, translate_option, result, video_wait_time_setting, srt_setting)
                    print("\033[1;34m🎉 字幕翻译已完成！\033[0m")
                    msg_tra.toast("翻译任务结束！", icon=":material/translate:")

                msg_srt = st.toast('正在生成SRT字幕文件', icon=":material/edit_note:")
                print("\n\033[1;35m*** 正在生成 SRT 字幕文件 ***\033[0m\n")
                srt_content = generate_srt_from_result(result)
                srt_content_style = generate_srt_from_result_2(result, font_setting, font_size_setting, font_color_setting)
                with open(output_file + "/output.srt", 'w', encoding='utf-8') as srt_file:
                    srt_file.write(srt_content)
                with open(output_file + "/output_with_style.srt", 'w', encoding='utf-8') as srt_file:
                    srt_file.write(srt_content_style)
                st.session_state.output_file = output_file

                if not allow:
                    st.toast('正在合并视频，请耐心等待生成', icon=":material/arrow_or_edge:")
                    print("\033[1;35m*** 正在合并视频 ***\033[0m\n")
                    srt_mv(log_setting, st.session_state.srt_name, crf_setting, quality_setting, ffmpeg_setting, st.session_state.output_file, font_setting, font_size_setting, font_color_setting, subtitle_model_setting)

                print("\033[1;34m🎉 任务成功结束！\033[0m")
                print("\n" + "=" * 50 + "\n")
            else:
                st.toast("请先在工具栏中上传音频文件！", icon=":material/release_alert:")

    st.write("")
    with st.expander("**Video Preview / 视频预览**", expanded=True, icon=":material/movie:"):
        col5, col6 = st.columns(2, gap="medium")

    st.write("")
    col1, col2 = st.columns([0.75, 0.25])
    with col2:
        with st.expander("**Tool / 工具**", expanded=True, icon=":material/construction:"):
            st.caption("上传文件")

            @st.dialog("上传视频文件")
            def upload_audio():
                st.write("")
                st.write("在这里上传您需要处理的视频文件。")
                st.write("请注意，除关闭 CMD 外，执行任务后无法取消任务！请勿在执行时点击任何 项目按钮 或 切换菜单，以免导致识别报错！")
                st.write("")
                uploaded_file_video = st.file_uploader("上传您的视频文件", type=['mp4', 'mov', 'avi', "mpeg", 'm4v', 'webm'], label_visibility="collapsed")
                st.write("")
                if st.button("**点击上传**", use_container_width=True, type="primary"):
                    st.session_state.uploaded_file_video = uploaded_file_video
                    st.session_state.upload = True
                    st.rerun()
                st.write("")

            if st.button('**文件上传**', use_container_width=True, type="primary", key="upload_audio_button"):
                upload_audio()

            st.caption("字幕工具")
            if st.button('**保存修改**', use_container_width=True, type="primary"):
                try:
                    with open(st.session_state.output_file + "/output.srt", 'w', encoding='utf-8') as srt_file:
                        srt_file.write(st.session_state.srt_content_new)
                    with open(st.session_state.output_file + "/output_with_style.srt", 'w', encoding='utf-8') as srt_file:
                        srt_file.write(st.session_state.srt_data3)
                    st.toast("已成功保存", icon=":material/task_alt:")
                except:
                    st.toast("未检测到运行后的字幕文件", icon=":material/error:")

            if st.button("**重新合并**", type="primary", use_container_width=True):
                try:
                    with open(st.session_state.output_file + "/output.srt", 'w', encoding='utf-8') as srt_file:
                        srt_file.write(st.session_state.srt_content_new)
                    with open(st.session_state.output_file + "/output_with_style.srt", 'w', encoding='utf-8') as srt_file:
                        srt_file.write(st.session_state.srt_data3)
                    test = st.session_state.srt_name

                    st.toast('正在合并视频，请耐心等待生成', icon=":material/arrow_or_edge:")
                    print("\033[1;35m*** 正在合并视频 ***\033[0m\n")

                    srt_mv(log_setting, st.session_state.srt_name, crf_setting, quality_setting, ffmpeg_setting, st.session_state.output_file, font_setting, font_size_setting, font_color_setting, subtitle_model_setting)
                    print("\033[1;34m🎉 任务成功结束！\033[0m\n")
                except:
                    st.toast("未进行识别，无法重新合并！", icon=":material/error:")

            if st.button('**打开目录**', use_container_width=True, type="primary"):
                try:
                    os.startfile(st.session_state.output_file)
                    st.toast("注意：文件夹已成功打开，可能未置顶显示，请检查系统任务栏！", icon=":material/task_alt:")
                except:
                    st.toast("未进行识别，目录尚未生成！", icon=":material/error:")
            st.divider()
            if "output_file" not in st.session_state:
                st.write("")
            if st.toggle("**更多功能**"):
                st.caption("字幕轴高度")
                height = st.number_input("高度显示", min_value=300, step=100, value=490, label_visibility="collapsed")
                st.session_state.height_video = height
                st.caption("其他字幕格式")
                try:
                    captions_option = st.radio('更多字幕格式导出', ('VTT', 'ASS', 'SBV'), index=0, label_visibility="collapsed")
                    if captions_option == 'VTT':
                        vtt_content = srt_to_vtt(st.session_state.srt_content_new)
                        st.download_button(
                            label="**VTT 下载**",
                            data=vtt_content.encode('utf-8'),
                            key='vtt_download',
                            file_name='output.vtt',
                            mime='text/vtt',
                            use_container_width=True,
                            type="primary"
                        )
                    elif captions_option == 'ASS':
                        sbv_content = srt_to_ass(st.session_state.srt_content_new, font_setting, font_size_setting, font_color_setting)
                        st.download_button(
                            label="**ASS 下载**",
                            data=sbv_content.encode('utf-8'),
                            key='ass_download',
                            file_name='output.ass',
                            mime='text/ass',
                            use_container_width=True,
                            type="primary"
                        )
                    elif captions_option == 'SBV':
                        sbv_content = srt_to_sbv(st.session_state.srt_content_new)
                        st.download_button(
                            label="**SBV 下载**",
                            data=sbv_content.encode('utf-8'),
                            key='sbv_download',
                            file_name='output.sbv',
                            mime='text/sbv',
                            use_container_width=True,
                            type="primary"
                        )
                except:
                    if st.button('**下载字幕**', use_container_width=True, type="primary"):
                        st.toast("未检测到字幕生成！", icon=":material/error:")
            if "output_file" not in st.session_state:
                st.write("")
            if "height_video" not in st.session_state:
                st.session_state.height_video = 490

    with col1:
        with st.expander("**Subtitle Preview / 字幕预览**", expanded=True, icon=":material/subtitles:"):
            try:
                st.caption("视频音轨")
                audio_file = open(st.session_state.output_file + "/output.mp3", 'rb')
                audio_bytes = audio_file.read()
                st.audio(audio_bytes)
            except:
                st.info("##### 音轨预览区域 \n\n&nbsp;**运行后自动显示 | 查看 [项目文档](https://blog.chenyme.top/blog/aavt-install) | 加入 [交流群组](https://t.me/+j8SNSwhS7xk1NTc9)**", icon=":material/view_in_ar:")
            try:
                st.caption("字幕时间轴")
                with open(st.session_state.output_file + "/output.srt", 'r', encoding='utf-8') as srt_file:
                    srt_content = srt_file.read()
                srt_data1 = parse_srt_file(srt_content)
                edited_data = st.data_editor(srt_data1, height=st.session_state.height_video, hide_index=True, use_container_width=True)
                srt_data2 = convert_to_srt(edited_data)
                st.session_state.srt_data3 = add_font_settings(srt_data2, font_color_setting, font_setting, font_size_setting, srt_setting)
                st.session_state.srt_content_new = srt_data2
            except:
                st.info("##### 结果预览区域 \n\n&nbsp; \n\n **生成完毕后会在此区域自动显示字幕时间轴** \n\n 运行前，请在右侧使用上传文件工具导入你的视频文件！ \n\n&nbsp;", icon=":material/view_in_ar:")

    with col5:
        try:
            st.caption("原始视频")
            video_bytes = show_video(st.session_state.output_file, st.session_state.srt_name)
            st.video(video_bytes)
        except:
            if "uploaded_file_video" in st.session_state:
                st.success(
                    "##### 视频导入成功 \n\n&nbsp;**运行后自动显示**", icon=":material/view_in_ar:")
                st.write("")
            else:
                st.info(
                    "##### 视频预览区域 \n\n&nbsp;**运行后自动显示**", icon=":material/view_in_ar:")
                st.write("")

    with col6:
        try:
            st.caption("生成视频")
            video_bytes = show_video(st.session_state.output_file, "output.mp4")
            st.video(video_bytes)
        except:
            st.info(
                "##### 视频预览区域 \n\n&nbsp;**运行后自动显示**", icon=":material/view_in_ar:")
            st.write("")

with tab2:
    col1, col2 = st.columns([0.7, 0.3])  # 置顶标题、执行按钮流程模块
    st.caption("")
    col7, col8 = st.columns([0.7, 0.3])
    with col7:
        with st.expander("**Operation / 运行状况**", expanded=True, icon=":material/switch_access_2:"):
            placeholder = st.empty()
            with placeholder.container(border=False):
                st.write("")
                st.info("##### 结果预览区域 \n\n&nbsp;\n\n**生成完毕后会在此区域自动显示字幕时间轴**\n\n 运行前，请在右侧使用上传文件工具导入你的音频文件！\n\n&nbsp;\n\n&nbsp;", icon=":material/view_in_ar:")
                st.write("")
            container = st.container()

    # 标题模块
    with col1:
        st.caption("")
        st.caption("")
        st.subheader("AI 全自动视频批量翻译")
        st.caption("AI Automatic Batch Translation Of Videos")

    # 执行按钮流程模块
    with col2:
        st.caption("")
        st.caption("")
        if st.button('**启动任务**', use_container_width=True, type="primary"):
            if "output_file_batch" in st.session_state:
                placeholder.empty()
                print("\n" + "=" * 50)
                print("\n\033[1;39m*** Chenyme-AAVT 视频批量翻译 ***\033[0m")
                st.toast('任务开始执行！请勿在运行时切换菜单或修改参数!', icon=":material/rocket_launch:")

                for i in st.session_state.video_name_list:
                    container.caption(f"{i}")
                    video_name = "uploaded" + ".mp4"
                    output_file = f"{st.session_state.output_file_batch}/{i}"

                    print("\n\033[1;34m🚀 任务开始执行\033[0m")
                    print(f"\033[1;34m📂 本次任务目录:\033[0m\033[1;34m {output_file} \033[0m")
                    print("\033[1;33m⚠️ 请不要在任务运行期间切换菜单或修改参数！\033[0m")

                    msg = st.toast('正在识别视频内容', icon=":material/hearing:")
                    if whisper_mode == "OpenAIWhisper - API":
                        result = OpenaiWhisperResult(chatgpt_key, chatgpt_url, output_file, openai_whisper_model_index, whisper_prompt, whisper_temp)
                    if whisper_mode == "FasterWhisper - AutoDownload":
                        result = runWhisperSeperateProc(output_file, faster_gpu, faster_whisper_model_index, faster_prompt, faster_temp, faster_vad, language_index,  faster_beam_size, faster_min_vad)
                    if whisper_mode == "FasterWhisper - LocalModel":
                        result = runWhisperSeperateProc(output_file, faster_local_gpu, faster_whisper_model_local_index, faster_local_prompt, faster_local_temp, faster_local_vad, language_index, faster_local_beam_size, faster_local_min_vad)
                    if 'error' in result:
                        print(f"\033[1;31m❌ Whisper识别异常: {result['error']}\033[0m")
                        container.error(f"**识别时发生异常**\n\n {result['error']}", icon=":material/running_with_errors:")
                        st.stop()

                    print("\033[1;34m🎉 Whisper 识别成功！\033[0m")
                    container.success(f"**视频内容识别成功！**", icon=":material/rocket_launch:")

                    translate_option = translation_dict[tuple(video_translate_index)]
                    if translate_option != '无需翻译':
                        if '本地模型' in translate_option:
                            result = local_translate(system_prompt, user_prompt, local_key, local_url, local_model, result, srt_setting)
                        elif 'gemini' in translate_option:
                            result = translate(system_prompt, user_prompt, gemini_key, gemini_url, translate_option, result, video_wait_time_setting, srt_setting)
                        elif 'yi' in translate_option:
                            result = translate(system_prompt, user_prompt, ai01_key, ai01_url, translate_option, result, video_wait_time_setting, srt_setting)
                        elif 'gpt' in translate_option:
                            result = translate(system_prompt, user_prompt, chatgpt_key, chatgpt_url, translate_option, result, video_wait_time_setting, srt_setting)
                        elif 'moonshot' in translate_option:
                            result = translate(system_prompt, user_prompt, kimi_key, kimi_base, translate_option, result, video_wait_time_setting, srt_setting)
                        elif 'glm' in translate_option:
                            result = translate(system_prompt, user_prompt, chatglm_key, chatglm_url, translate_option, result, video_wait_time_setting, srt_setting)
                        elif 'deepseek' in translate_option:
                            result = translate(system_prompt, user_prompt, deepseek_key, deepseek_url, translate_option, result, video_wait_time_setting, srt_setting)
                        elif 'claude' in translate_option:
                            result = translate(system_prompt, user_prompt, claude_key, claude_url, translate_option, result, video_wait_time_setting, srt_setting)
                        container.success(f"**字幕翻译成功！**", icon=":material/rocket_launch:")
                        print("\033[1;34m🎉 字幕翻译已完成！\033[0m")

                    print("\n\033[1;36m*** 正在生成 SRT 字幕文件 ***\033[0m\n")
                    srt_content = generate_srt_from_result(result)
                    srt_content_style = generate_srt_from_result_2(result, font_setting, font_size_setting, font_color_setting)
                    with open(output_file + "/output.srt", 'w', encoding='utf-8') as srt_file:
                        srt_file.write(srt_content)
                    with open(output_file + "/output_with_style.srt", 'w', encoding='utf-8') as srt_file:
                        srt_file.write(srt_content_style)
                    container.success(f"**生成SRT字幕文件成功！**", icon=":material/rocket_launch:")

                    print("\033[1;36m*** 正在合并视频 ***\033[0m\n")

                    srt_mv(log_setting, video_name, crf_setting, quality_setting, ffmpeg_setting, output_file, font_setting, font_size_setting, font_color_setting, subtitle_model_setting)
                    container.success(f"**视频合并成功！**", icon=":material/rocket_launch:")

                    print("\033[1;34m🎉 任务成功结束！\033[0m")
                    container.success(f"**任务已完成！**", icon=":material/verified:")
                print("\n" + "=" * 50 + "\n")
            else:
                st.toast("请先在工具栏中批量上传视频文件！", icon=":material/release_alert:")

    with col8:
        with st.expander("**Tool / 工具**", expanded=True, icon=":material/construction:"):
            st.write("")

            @st.dialog("上传多视频文件")
            def uploaded():
                st.write("")
                st.write("在这里上传您需要处理的所有视频文件。")
                st.write("请注意，除关闭 CMD 外，执行任务后无法取消任务！请勿在执行时点击任何 项目按钮 或 切换菜单，以免导致识别报错！")
                st.write("")
                uploaded_file_list = st.file_uploader("**请上传视频：**", type=['mp4', 'mov', 'avi', 'm4v', 'webm', 'flv'], label_visibility="collapsed", accept_multiple_files=True)
                st.write("")
                if st.button('**上传并处理**', use_container_width=True, type="primary"):
                    if uploaded_file_list is not None:
                        my_bar = st.progress(0, text="视频预处理中，请等待")
                        current_time = datetime.datetime.now().strftime("_%Y%m%d%H%M%S")
                        output_file = video_cache_path + "BatchProcessVideos" + current_time
                        os.makedirs(output_file)
                        print(f"\033[1;32m✔️ 当前任务目录：\033[0m\033[1;34m {output_file} \033[0m")
                        num = len(uploaded_file_list)
                        start = 0.00
                        a = 1 / num
                        video_list = []
                        for uploaded_file in uploaded_file_list:
                            video_list.append(uploaded_file.name.split('.')[0])
                            file_name = f"{output_file}/{uploaded_file.name.split('.')[0]}"
                            video_name = "uploaded." + uploaded_file.name.split('.')[-1]
                            os.makedirs(file_name)

                            with open(f"{file_name}/{video_name}", "wb") as file:
                                file.write(uploaded_file.getbuffer())

                            FileToMp3(log_setting, f"{file_name}/{video_name}", file_name)
                            start += a
                            my_bar.progress(start, text=f"视频 {uploaded_file.name} 预处理中，请等待...")
                        my_bar.progress(start, text=f"处理完毕！")
                        st.session_state.video_name_list = video_list
                        st.session_state.output_file_batch = output_file
                        st.success(f"视频预处理成功！", icon=":material/change_circle:")
                        time.sleep(1)
                        st.session_state.upload = True
                        st.rerun()
                st.write("")

            if st.button('**文件上传**', use_container_width=True, type="primary"):
                uploaded()

            if st.button('**打开目录**', use_container_width=True, type="primary", key="view"):
                try:
                    os.startfile(st.session_state.output_file_batch)
                    st.toast("注意：文件夹已成功打开，可能未置顶显示，请检查系统任务栏！", icon=":material/task_alt:")
                except:
                    st.toast("未进行识别，目录尚未生成！", icon=":material/error:")

        with st.expander("**Task List / 任务列表**", expanded=True, icon=":material/list_alt:"):
            try:
                a = 1
                for i in st.session_state.video_name_list:
                    st.write(f"###### {a}. {i}")
                    a += 1
                st.write("")
            except:
                st.info("##### 任务列表 \n\n**上传后自动显示**",icon=":material/view_in_ar:")

with tab3:
    col1, col2 = st.columns([0.75, 0.25])  # 置顶标题、执行按钮流程模块
    st.write("")
    with st.expander("**Upload Video / 上传视频**", expanded=True, icon=":material/drive_folder_upload:"):
        st.caption("上传视频")
        uploaded_file = st.file_uploader("**上传器**", type=['mp4', 'mov', 'avi', 'm4v', 'webm'], label_visibility="collapsed")

    # 标题模块
    with col1:
        st.write("")
        st.write("")
        st.subheader("AI 自动视频生成博客")
        st.caption("AI Automatic Video Generation Blog")

    # 警告模块
    if not chatgpt_key:
        st.write("")
        with st.expander("**Warning / 警告**", expanded=True, icon=":material/bug_report:"):
            st.warning("##### 关键参数缺失 \n\n 请务必配置 OpenAI 相关参数才可使用此服务！", icon=":material/crisis_alert:")
            st.write("")
            col3, col4 = st.columns(2)
            with col3:
                url = st.text_input("OpenAI API 地址", chatgpt_url, placeholder="OpenAI API 接口")
            with col4:
                key = st.text_input("OpenAI API 密钥", chatgpt_key, placeholder="OpenAI API 密钥", type="password")

            st.write("")
            if st.button("**保存 OpenAI 配置**", use_container_width=True, type="primary"):
                if not key:
                    st.toast("未正确配置相关参数，保存失败！", icon=":material/release_alert:")
                else:
                    with open(llms_path, 'w', encoding="utf-8") as f:
                        llms["ChatGPT"]["url"] = url
                        llms["ChatGPT"]["key"] = key
                        toml.dump(llms, f)
                    st.session_state.save = True
                    st.rerun()
            st.write("")

    # 执行按钮流程模块
    with col2:
        st.write("")
        st.write("")
        if st.button("**开始生成**", type="primary", use_container_width=True):
            if uploaded_file is not None:
                print("\n" + "=" * 50)
                print("\n\033[1;39m*** Chenyme-AAVT 图文博客***\033[0m")
                st.toast('任务开始执行！请勿在运行时切换菜单或修改参数!', icon=":material/rocket_launch:")

                current_time = datetime.datetime.now().strftime("_%Y%m%d%H%M%S")
                video_name_original = re.sub(r'[/:*?"<>|()\[\]{}\-_,.，。！？；：“”‘’（）【】《》—一-鿿]', '', uploaded_file.name.split('.')[0].replace(' ', ''))  # 移除不识别的符号
                photos_path = blog_cache_path + video_name_original + current_time + '/'
                st.session_state.photos_path = photos_path
                os.makedirs(photos_path)
                with open(photos_path + "/uploaded.mp4", "wb") as file:
                    file.write(uploaded_file.getbuffer())

                print("\n\033[1;34m🚀 任务开始执行\033[0m")
                print(f"\033[1;34m📂 本次任务目录:\033[0m\033[1;34m {photos_path} \033[0m")
                print("\033[1;33m⚠️ 请不要在任务运行期间切换菜单或修改参数！\033[0m")

                print("\n\033[1;34m⏳ 正在提取视频关键帧\033[0m")
                msg_ext = st.toast("正在提取视频关键帧", icon=":material/colorize:")
                extract_frames(photos_path + "/uploaded.mp4", photos_path, blog_time_interval)
                print("\033[1;34m🎉 视频关键帧提取完成\033[0m")
                msg_ext.toast("视频关键帧提取完成", icon=":material/colorize:")

                msg_whs = st.toast("正在识别视频内容", icon=":material/troubleshoot:")
                FileToMp3(log_setting, f"{photos_path}/uploaded.mp4", photos_path)
                if whisper_mode == "OpenAIWhisper - API":
                    result = OpenaiWhisperResult(chatgpt_key, chatgpt_url, photos_path, openai_whisper_model_index, whisper_prompt, whisper_temp)
                if whisper_mode == "FasterWhisper - AutoDownload":
                    result = runWhisperSeperateProc(photos_path, faster_gpu, faster_whisper_model_index, faster_prompt, faster_temp, faster_vad, language_index, faster_beam_size, faster_min_vad)
                if whisper_mode == "FasterWhisper - LocalModel":
                    result = runWhisperSeperateProc(photos_path, faster_local_gpu, faster_whisper_model_local_index, faster_local_prompt, faster_local_temp, faster_local_vad, language_index, faster_local_beam_size, faster_local_min_vad)
                if 'error' in result:
                    print(f"\033[1;31m❌ Whisper识别异常: {result['error']}\033[0m")
                    st.error(f"处理失败，错误信息：{result['error']}")
                    st.stop()
                print("\033[1;34m🎉 Whisper识别成功！\033[0m")
                msg_whs.toast("视频内容识别完成", icon=":material/colorize:")

                msg_wrt = st.toast("正在执行写作", icon=":material/history_edu:")
                print("\n\033[1;34m📝 正在执行写作\033[0m")
                write_model = translation_dict[tuple(blog_write_index)]
                text = result['text']
                if write_model == '本地模型':
                    content = write_llms(blog_view, blog_language, local_key, local_url, local_model, text, blog_token, blog_temp)
                elif 'gemini' in write_model:
                    content = write_llms(blog_view, blog_language, gemini_key, gemini_url, write_model, text, blog_token, blog_temp)
                elif 'yi' in write_model:
                    content = write_llms(blog_view, blog_language, ai01_key, ai01_url, write_model, text, blog_token, blog_temp)
                elif 'gpt' in write_model:
                    content = write_llms(blog_view, blog_language, chatgpt_key, chatgpt_url, write_model, text, blog_token, blog_temp)
                elif 'moonshot' in write_model:
                    content = write_llms(blog_view, blog_language, kimi_key, kimi_base, write_model, text, blog_token, blog_temp)
                elif 'glm' in write_model:
                    content = write_llms(blog_view, blog_language, chatglm_key, chatglm_url, write_model, text, blog_token, blog_temp)
                elif 'deepseek' in write_model:
                    content = write_llms(blog_view, blog_language, deepseek_key, deepseek_url, write_model, text, blog_token, blog_temp)
                elif 'claude' in write_model:
                    content = write_llms(blog_view, blog_language, claude_key, chatgpt_key, write_model, text, blog_token, blog_temp)
                msg_wrt.toast("写作任务完成", icon=":material/colorize:")
                print("\033[1;34m🎉 写作任务完成！\033[0m")

                print("\n\033[1;34m🖼️ 正在选择关键帧\033[0m")
                msg_cho = st.toast("正在选择关键帧", icon=":material/photo_size_select_large:")
                num = len(os.listdir(photos_path)) * blog_time_interval
                srt_content = generate_srt_from_result(result)

                class ImportantFrames(BaseModel):  # 定义回答格式
                    important_frames: list[str]

                client = OpenAI(api_key=chatgpt_key, base_url=chatgpt_url)
                completion = client.beta.chat.completions.parse(
                    model="gpt-4o-2024-08-06",
                    messages=[
                        {"role": "system", "content": "Professional assistant for selecting keyframes."},
                        {"role": "user", "content": f"现有一个时长为{str(num)}秒的视频，该视频已被提取为每{str(blog_time_interval)}秒一帧的图片，图片名称依次为'frame_1'到'frame_{str(num)}'。下面请根据视频的字幕内容，仔细阅读并分析后，选出你认为在写撰写博客时最重要的几个关键帧，这些几个关键帧将作为博客中的图片内容。图片的数量适中，确保所选图片编号不会超过'frame_{str(num)}'。请你直接返回最重要的几张关键帧，返回方式为图片名称，如 ['frame_1', 'frame_30', 'frame_46']。\n字幕内容：{srt_content}"},
                    ],
                    response_format=ImportantFrames)
                event = completion.choices[0].message.parsed
                choose_photos = event.important_frames
                list_result = [item + '.png' for item in choose_photos]
                all_files = os.listdir(photos_path)

                for name in list_result:
                    if name not in all_files:
                        st.warning("选择图片出现错误！", icon=":material/crisis_alert:")
                        st.stop()

                for file in all_files:
                    if file not in list_result:
                        os.remove(os.path.join(photos_path, file))

                msg_cho.toast("关键帧选择完成", icon=":material/colorize:")
                print("\033[1;34m🎉 关键帧选择完成！\033[0m")

                print("\n\033[1;34m📝 正在合并最终文章\033[0m")
                msg_mer = st.toast("正在合并最终文章", icon=":material/arrow_or_edge:")
                image_list = [
                    {"type": "text",
                     "text": f"你是一名专业的内容创作者，擅长撰写吸引读者的博客文章。你的任务是帮助我根据特定主题撰写一篇博客文章。以下是具体要求：请以{name}的视角写一篇{blog_token}字的{blog_language}博客，选择你认为重要的图片插入到文章合适的地方，最终只允许返回 markdown 代码，文章的排版必须高质量，逻辑清晰、引人入胜，图片尽可能不要相邻，图片从前到后的名称依次为{str(list_result)}。文本内容如下：{content}"}
                ]
                for i in range(len(list_result)):
                    image_path = photos_path + list_result[i]
                    base64_image = encode_image(image_path)
                    image_list.append({
                        "type": "image_url",
                        "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}
                    })
                client = OpenAI(api_key=chatgpt_key, base_url=chatgpt_url)
                response = client.chat.completions.create(
                    model="gpt-4o",
                    messages=[{"role": "user", "content": image_list}],
                    temperature=blog_temp)
                answer = response.choices[0].message.content

                # 处理不规则字符
                answer = answer.replace("```markdown\n", "")
                answer = answer.replace("images" + os.path.sep, "")
                answer = answer.replace("photos" + os.path.sep, "")
                answer = answer.rstrip("`")

                with open(photos_path + 'output.md', 'w', encoding='utf-8') as file:
                    file.write(answer)
                st.session_state.success = False
                st.session_state.answer = answer
                msg_mer.toast("文章生成完毕", icon=":material/verified:")
                print("\033[1;34m🎉 文章生成完毕！\033[0m")
                print("\n" + "=" * 50 + "\n")
            else:
                st.toast("请先在工具栏中上传音频文件！", icon=":material/release_alert:")
            if not chatgpt_key:
                st.toast("请确保 OpenAI 相关参数不为空！", icon=":material/release_alert:")

    # 效果预览模块
    with st.expander("**Article Preview / 文章预览**", expanded=True, icon=":material/full_coverage:"):
        try:
            st.caption("图文博客")
            answer = st.session_state.answer
            st.write("")
            pattern = r'!\[.*?\]\((.*?)\)'
            matches = re.findall(pattern, answer)
            parts = re.split(pattern, answer)

            for part in parts:
                if part in matches:
                    part = part.strip('(').replace(')', '')
                    st.image(st.session_state.photos_path + part, width=500)
                else:
                    st.markdown(part)

            sac.divider(label='文章结束', align='center', color='gray')
            if st.button('**&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;打开任务目录&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;**', type="primary"):
                os.startfile(st.session_state.photos_path)
                st.warning("##### 系统提示 \n\n**文件夹已成功打开，可能未置顶显示，请检查系统任务栏！**", icon=":material/crisis_alert:")
            st.write("")
        except:
            st.info("##### 结果预览区域 \n\n&nbsp;\n\n&nbsp;\n\n&nbsp;**生成完毕后会在此区域自动显示文章** \n\n&nbsp;\n\n&nbsp;\n\n&nbsp;", icon=":material/view_in_ar:")
            st.write("")
