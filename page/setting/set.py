import os
import json
import toml
import streamlit as st
import pandas as pd
from styles.global_style import style
import streamlit_antd_components as sac
import anthropic
from openai import OpenAI
import google.generativeai as genai
import shutil
style()

path = os.getcwd() + "/"
llms_path = path + "config/llms.toml"
whisper_path = path + "config/whisper.toml"
font_data_path = path + "config/font.txt"
video_config_path = path + "config/video.toml"
prompt_config_path = path + "config/prompt.json"
project_config_path = path + "config/project.toml"
video_cache_path = path + "cache/video/"
model_path = path + "model/faster-whisper"
with open(llms_path, 'r', encoding="utf-8") as config_file:
    llms = toml.load(config_file)
with open(whisper_path, 'r', encoding="utf-8") as config_file:
    whispers = toml.load(config_file)
with open(prompt_config_path, 'r', encoding='utf-8') as config_file:
    prompt = json.load(config_file)
with open(project_config_path, 'r', encoding='utf-8') as config_file:
    project = toml.load(config_file)

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
all_in_one = llms["Global"]["all"]

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

log_setting = project["ffmpeg"]["log"]
crf_setting = project["ffmpeg"]["crf"]
quality_setting = project["ffmpeg"]["quality"]
ffmpeg_setting = project["ffmpeg"]["ffmpeg"]
open_protect = project["protect"]["open"]
password_protect = project["protect"]["password"]


@st.dialog('新增提示词')
def add(config_dir):
    name = st.text_input('提示词名称')
    system = st.text_area('新的系统提示词', height=100)
    user = st.text_area('新的用户提示词', height=100)
    if st.button("**保存提示词**", use_container_width=True, type="primary"):
        if name != "" and system != "" and user != "":
            new = {
                name:
                    {
                        "system_prompt": system,
                        "user_prompt": user
                    }
            }
            prompt.update(new)
            new_prompt = json.dumps(prompt, indent=2)
            with open(config_dir, 'w', encoding='utf-8') as json_file:
                json_file.write(new_prompt)
            st.session_state.new = True
            st.rerun()
        else:
            st.write("")
            st.error("### 所有参数不允许为空！", icon=":material/error:")
    st.write("")

@st.dialog('在这里上传或拖入')
def upload(config_dir):
    file = st.file_uploader("上传", label_visibility="collapsed")
    if file is not None:
        if file.name == "prompt.json":
            a = file.getvalue().decode("utf-8")
            with open(config_dir, 'w', encoding='utf-8') as json_file:
                json_file.write(a)
            st.session_state.save = True
            st.rerun()
        else:
            st.error("请上传`prompt.json`命名的json文件", icon=":material/error:")


if "save" in st.session_state:
    st.toast("已成功保存！", icon=":material/verified:")
    del st.session_state["save"]
if "new" in st.session_state:
    st.toast("新增成功！", icon=":material/verified:")
    del st.session_state["new"]
if "set_first" in st.session_state:
    st.toast("首次使用初始化成功！", icon=":material/verified:")
    del st.session_state["set_first"]
if "delete" in st.session_state:
    st.toast("已成功删除！", icon=":material/verified:")
    del st.session_state["delete"]

tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["**主页BOT**", "**识别设置**", "**翻译设置**", "**FFMpeg设置**", "**项目缓存**", "**其他设置**"])
with tab1:
    BOTSave = st.container()
    BOTSetting = st.container(border=True)
    with BOTSetting:
        st.write("")
        st.write("###### 助手 默认模型")
        st.caption("配置首页助手使用的大语言模型")
        HomeModel = sac.cascader(items=[
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
        ], label="", search=True, index=home_model, return_index=True)
        st.write("")
        st.write("###### 助手 BASE URL")
        st.caption("助手的 Proxy 地址，请与模型对应。内置地址：`https://api.chenyme.top/v1`")
        HomeUrl = st.text_input("**助手 BASE URL**", placeholder="Enter Your Url / 输入您的 Proxy 地址", value=home_url, label_visibility="collapsed")
        st.write("")
        st.write("###### 助手 API KEY")
        st.caption("助手的 API 密钥，请与模型对应。内置密钥：`sk-mTx1Qx04xagOqpHJB0DeF581E8C84370818c7aD5D15cA309`，仅用于项目公益服务，请勿用于其他用途！一经发现，我会立刻删除此密钥！")
        HomeKey = st.text_input("**助手 API KEY**", placeholder="Enter Your Key / 输入您的 API 密钥", value=home_key, label_visibility="collapsed")
        st.write("")

    with BOTSave:
        col1, col2 = st.columns([0.75, 0.25])
        with col2:
            st.write("")
            st.write("")
            if st.button("**保存更改**", type="primary", use_container_width=True):
                llms["Home"]["key"] = HomeKey
                llms["Home"]["url"] = HomeUrl
                llms["Home"]["model"] = HomeModel
                with open(llms_path, "w", encoding="utf-8") as file:
                    toml.dump(llms, file)
                st.session_state.save = True
                st.rerun()
        with col1:
            st.write("")
            st.write("")
            st.write("### 主页BOT设置")
            st.caption("Home BOT Settings")
            st.write("")

with tab2:
    WhisperSave = st.container()
    mode = ["OpenAIWhisper - API", "OpenAIWhisper - Local", "FasterWhisper - AutoDownload", "FasterWhisper - LocalModel", "WhisperX"]
    whisper_mode = st.selectbox("**Whisper 后端**", mode, index=mode.index(whisper_mode))
    st.write("")

    with st.container(border=True):
        if whisper_mode == "OpenAIWhisper - API":
            st.write("##### OpenAIWhisper - API调用")
            if not chatgpt_key:
                st.error("**配置问题：** \n\n 您选择了 OpenAIWhisper-API 模式，但尚未完全配置 OpenAI 的所有参数！请及时填写下面为空的参数，否则运行时会出错！", icon=":material/running_with_errors:")
                st.write("")
                col1, col2 = st.columns(2)
            else:
                st.write("")
                col1, col2 = st.columns(2)

            with col1:
                url = st.text_input("OpenAI API 地址", chatgpt_url, placeholder="OpenAI API 接口")
                whisper_temp = st.number_input("识别温度", min_value=0.0, max_value=1.0, step=0.1, value=whisper_temp)
            with col2:
                key = st.text_input("OpenAI API 密钥", chatgpt_key, placeholder="OpenAI API 密钥", type="password")
                whisper_prompt = st.text_input("提示词", whisper_prompt)
            st.write("")
            with WhisperSave:
                col1, col2 = st.columns([0.75, 0.3])
                with col2:
                    st.write("")
                    st.write("")
                    if st.button("**保存 OpenAI Mode 配置**", use_container_width=True, type="primary"):
                        if not key:
                            st.toast("若使用 OpenAIWhisper-API，则下方参数不允许为空！", icon=":material/release_alert:")
                        else:
                            with open(llms_path, 'w', encoding="utf-8") as f:
                                llms["ChatGPT"]["url"] = url
                                llms["ChatGPT"]["key"] = key
                                toml.dump(llms, f)
                            with open(whisper_path, 'w') as f:
                                whispers["Mode"]["WhisperMode"] = whisper_mode
                                whispers["OpenAI"]["Temp"] = whisper_temp
                                whispers["OpenAI"]["Prompt"] = whisper_prompt
                                toml.dump(whispers, f)
                            st.session_state.save = True
                            st.rerun()
                with col1:
                    st.write("")
                    st.write("")
                    st.subheader("识别后端设置")
                    st.caption("Identify Backend Settings")
                    st.write("")

        if whisper_mode == "OpenAIWhisper - Local":
            with WhisperSave:
                st.write("")
                st.write("")
                st.subheader("识别后端设置")
                st.caption("Identify Backend Settings")
                st.write("")
            st.write("##### OpenAIWhisper - 本地调用")
            st.warning("""
            **此方法作者已弃用或即将更新：**  

            &nbsp;  

            如有问题，可前往&nbsp;  **[GitHub](https://github.com/Chenyme/Chenyme-AAVT)** &nbsp; |&nbsp;  **[Telegram](https://t.me/+j8SNSwhS7xk1NTc9)** &nbsp; |&nbsp;  **[MyBlog](https://blog.chenyme.top)** &nbsp; 查看相关信息或提问反馈！  

            &nbsp;  
            """, icon=":material/error_med:")
            st.write("")

        if whisper_mode == "FasterWhisper - AutoDownload":
            st.write("##### FasterWhisper - 自动下载模型")
            st.info("**使用提示：** \n\n 此模式会自动从 Hugging Face 拉取模型，国内用户若在拉取过程中重复失败，可切换至 FasterWhisper - LocalModel 使用本地模型模式！", icon=":material/lightbulb:")
            st.write("")
            col1, col2 = st.columns(2)
            with col1:
                faster_gpu = st.checkbox("GPU 加速", value=faster_gpu)
                faster_vad = st.checkbox("VAD 辅助", value=faster_vad, help="语音活动检测")
                faster_min_vad = st.number_input("VAD 静音检测 (ms)", min_value=100, max_value=2000, step=100, value=faster_min_vad, disabled=not faster_vad)
            with col2:
                faster_temp = st.number_input("识别温度", min_value=0.0, max_value=1.0, step=0.1, value=faster_temp)
                faster_beam_size = st.number_input("束搜索大小", min_value=1, max_value=10, step=1, value=faster_beam_size)
            faster_prompt = st.text_input("提示词", faster_prompt)
            st.write("")

            with WhisperSave:
                col1, col2 = st.columns([0.75, 0.3])
                with col2:
                    st.write("")
                    st.write("")
                    if st.button("**保存 Faster Mode 配置**", use_container_width=True, type="primary"):
                        if not faster_prompt:
                            st.toast("Faster 提示词不能为空！", icon=":material/release_alert:")
                        else:
                            with open(whisper_path, 'w', encoding="utf-8") as f:
                                whispers["Mode"]["WhisperMode"] = whisper_mode
                                whispers["Faster"]["GPU"] = faster_gpu
                                whispers["Faster"]["VAD"] = faster_vad
                                whispers["Faster"]["Temp"] = faster_temp
                                whispers["Faster"]["Prompt"] = faster_prompt
                                whispers["Faster"]["min_vad"] = faster_min_vad
                                whispers["Faster"]["beam_size"] = faster_beam_size
                                toml.dump(whispers, f)
                            st.session_state.save = True
                            st.rerun()
                with col1:
                    st.write("")
                    st.write("")
                    st.subheader("识别后端设置")
                    st.caption("Identify Backend Settings")
                    st.write("")

        if whisper_mode == "FasterWhisper - LocalModel":
            st.write("##### FasterWhisper - 本地加载模型")
            st.info("**使用提示：** \n\n 此模式仅支持 **[Systran](https://huggingface.co/Systran)** 中的模型，如果您不知道如何使用，请阅读 **[本地加载模型](https://blog.chenyme.top/blog/aavt-install#bfd48658b23b)** 教程！", icon=":material/lightbulb:")
            st.write("")
            col1, col2 = st.columns(2)
            with col1:
                faster_local_gpu = st.checkbox("GPU 加速", value=faster_local_gpu)
                faster_local_vad = st.checkbox("VAD 辅助", value=faster_local_vad)
                faster_local_min_vad = st.number_input("VAD 静音检测 (ms)", min_value=100, max_value=2000, step=100, value=faster_local_min_vad, disabled=not faster_local_vad)
            with col2:
                faster_local_temp = st.number_input("识别温度", min_value=0.0, max_value=1.0, step=0.1, value=faster_local_temp)
                faster_local_beam_size = st.number_input("束搜索大小", min_value=1, max_value=10, step=1, value=faster_local_beam_size)
            faster_local_prompt = st.text_input("提示词", value=faster_local_prompt)
            faster_local_path = st.text_input("模型路径", value=faster_local_path)
            st.write("")

            with WhisperSave:
                col1, col2 = st.columns([0.75, 0.3])
                with col2:
                    st.write("")
                    st.write("")
                    if st.button("**保存 Faster Mode 配置**", use_container_width=True, type="primary"):
                        with open(whisper_path, 'w', encoding="utf-8") as f:
                            whispers["Mode"]["WhisperMode"] = whisper_mode
                            whispers["Faster_Local"]["path"] = faster_local_path
                            whispers["Faster_Local"]["GPU"] = faster_local_gpu
                            whispers["Faster_Local"]["VAD"] = faster_local_vad
                            whispers["Faster_Local"]["Temp"] = faster_local_temp
                            whispers["Faster_Local"]["Prompt"] = faster_local_prompt
                            whispers["Faster_Local"]["min_vad"] = faster_local_min_vad
                            whispers["Faster_Local"]["beam_size"] = faster_local_beam_size
                            toml.dump(whispers, f)
                        st.session_state.save = True
                        st.rerun()
                with col1:
                    st.write("")
                    st.write("")
                    st.subheader("识别后端设置")
                    st.caption("Identify Backend Settings")
                    st.write("")

        if whisper_mode == "WhisperX":
            with WhisperSave:
                st.write("")
                st.write("")
                st.subheader("识别后端设置")
                st.caption("Identify Backend Settings")
                st.write("")
            st.write("##### WhisperX")
            st.warning("""
            **此方法作者已弃用或即将更新：**  

            &nbsp;  

            如有问题，可前往&nbsp;  **[GitHub](https://github.com/Chenyme/Chenyme-AAVT)** &nbsp; |&nbsp;  **[Telegram](https://t.me/+j8SNSwhS7xk1NTc9)** &nbsp; |&nbsp;  **[MyBlog](https://blog.chenyme.top)** &nbsp; 查看相关信息或提问反馈！  

            &nbsp;  
            """, icon=":material/error_med:")
            st.write("")

with tab3:
    PromptSave = st.container()
    PromptSetting = st.container()

    with PromptSetting:
        st.write("")
        st.info("##### 提示词使用规则 \n\n&nbsp; **{language1}** 和 **{language2}** 分别对应 **原始语言** 和 **目标语言** ,你必须在提示词中使用此占位符！", icon=":material/view_in_ar:")
        st.write("")
        df = pd.DataFrame([(k, v['system_prompt'], v['user_prompt']) for k, v in prompt.items()], columns=['Prompt', 'system_prompt', 'user_prompt'])
        df2 = st.data_editor(df, hide_index=True, use_container_width=True, height=300, num_rows="dynamic")
        json_result = df2.set_index('Prompt').to_json(orient='index')
        prompt_json = json.dumps(json.loads(json_result), indent=4)
        st.write("")
        col1, col2, col3= st.columns(3)
        with col1:
            if st.download_button(
                    label="**下载提示词**",
                    data=prompt_json,
                    file_name="prompt.json",
                    mime="text/json",
                    use_container_width=True,
                    type="primary"
            ):
                with open(prompt_config_path, 'w', encoding='utf-8') as json_file:
                    json_file.write(prompt_json)
        with col2:
            if st.button("**新建提示词**", use_container_width=True, type="primary"):
                add(prompt_config_path)
        with col3:
            if st.button("**导入提示词**", use_container_width=True, type="primary"):
                upload(prompt_config_path)

    with PromptSave:
        col1, col2 = st.columns([0.75, 0.25])
        with col2:
            st.write("")
            st.write("")
            if st.button("**保存修改**", use_container_width=True, type="primary"):
                with open(prompt_config_path, 'w', encoding='utf-8') as json_file:
                    json_file.write(prompt_json)
                st.session_state.save = True
                st.rerun()
        with col1:
            st.write("")
            st.write("")
            st.write("### 预置提示词")
            st.caption("Preset Prompt Words")

    st.write("##### ")
    st.write("### 翻译引擎配置")
    st.caption("Translation Engine Configuration")
    st.write("")
    col1, col2 = st.columns(2, gap="medium")
    with col1:
        with st.container(border=True):
            st.write("##### LOCAL 本地模型")
            st.write("调用在本地环境中部署的模型作为项目的翻译引擎")
            if st.button("&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;**配置**&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;", key="local_button", type="primary"):
                @st.dialog('Local 本地调用')
                def local_setting(url, key, model):
                    st.write("")
                    st.write("配置后此模块可调用您在本地环境中部署的开源模型作为翻译引擎，本地部署的模型可以避免 **网络访问限制**、**调用并发限制**、**调用花费过高** 等诸多问题，推荐设备性能比较高的使用此方法！\n\n 请确保已部署本地**翻译模型** 且 **熟知此模型接口** 后再配置！")
                    st.write("")
                    url = st.text_input("**API 地址**", url, placeholder="Local 接口")
                    key = st.text_input("**API 密钥**", key, placeholder="Local 密钥，无需请留空！")
                    model = st.text_input("**模型名称**", model, placeholder="Local 模型")
                    st.write("")
                    if st.button("**保存配置**", use_container_width=True, type="primary"):
                        with open(llms_path, 'w', encoding="utf-8") as f:
                            llms["Local"]["url"] = url
                            llms["Local"]["key"] = key
                            llms["Local"]["model"] = model
                            toml.dump(llms, f)
                        st.session_state.save_success = True
                    if st.button("**接口测试**", use_container_width=True, type="primary"):
                        try:
                            client = OpenAI(api_key=key, base_url=url)
                            response = client.chat.completions.create(
                                model=model,
                                messages=[{"role": "user","content": "测试"}])
                            answer = response.choices[0].message.content
                            st.success("**测试成功！**", icon=":material/check:")
                        except Exception as e:
                            st.error(f"**测试失败：{e}**", icon=":material/error:")
                    if "save_success" in st.session_state:
                        st.success("**保存成功！**", icon=":material/check:")
                        del st.session_state["save_success"]
                local_setting(local_url, local_key, local_model)
        st.write("")

        with st.container(border=True):
            st.write("##### DeepSeek 深度求索")
            st.write("调用DeepSeek官方接口服务来作为项目的翻译引擎")
            if st.button("&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;**配置**&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;", key="deepseek_button", type="primary"):
                @st.dialog('DEEPSEEK 深度求索')
                def deepseek_setting(url, key):
                    st.write("官方网址：**[www.deepseek.com](https://www.deepseek.com/zh)** \n\n DeepSeek是一家专注于研究世界领先的通用人工智能底层模型与技术的公司。该模型支持的调用并发量非常高，翻译效果中等偏上，较**推荐**！")
                    st.write("")
                    url = st.text_input("**API 地址**", url, placeholder="DeepSeek API 接口", help="默认值：`https://api.deepseek.com/v1`")
                    key = st.text_input("**API 密钥**", key, placeholder="DeepSeek API 密钥")
                    st.write("")
                    if st.button("**保存配置**", use_container_width=True, type="primary"):
                        with open(llms_path, 'w') as f:
                            llms["DeepSeek"]["url"] = url
                            llms["DeepSeek"]["key"] = key
                            toml.dump(llms, f)
                        st.session_state.save_success = True
                    if st.button("**接口测试**", use_container_width=True, type="primary"):
                        try:
                            client = OpenAI(api_key=key, base_url=url)
                            response = client.chat.completions.create(
                                model="deepseek-chat",
                                messages=[{"role": "user", "content": "测试"}])
                            answer = response.choices[0].message.content
                            st.success("**测试成功！**", icon=":material/check:")
                        except Exception as e:
                            st.error(f"**测试失败：{e}**", icon=":material/error:")
                    if "save_success" in st.session_state:
                        st.success("**保存成功！**", icon=":material/check:")
                        del st.session_state["save_success"]
                deepseek_setting(deepseek_url, deepseek_key)
        st.write("")

        with st.container(border=True):
            st.write("##### Gemini Google")
            st.write("调用 谷歌Gemini 官方接口服务作为项目的翻译引擎")
            if st.button("&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;**配置**&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;", key="gemini_button", type="primary"):
                @st.dialog('GEMINI GOOGLE')
                def gemini_setting(url, key):
                    st.write("官方网址：**[deepmind.google](https://deepmind.google/technologies/gemini/)** \n\nGemini是Google Deepmind最新、最强大的AI模型。它原生支持多模态，具备跨模态推理能力，包括文本，图像，视频，音频和代码。Gemini在32个基准测试中的30个上取得了领先，涵盖了语言、编码、推理和多模态推理等任务。")
                    st.write("")
                    url = st.text_input("**API 地址**", url, placeholder="Gemini API 接口", help="除非您使用代理URL，否者无需配置，调用时会自动填写！")
                    key = st.text_input("**API 密钥**", key, placeholder="Gemini API 密钥")
                    st.write("")
                    if st.button("**保存配置**", use_container_width=True, type="primary"):
                        with open(llms_path, 'w') as f:
                            llms["Gemini"]["url"] = url
                            llms["Gemini"]["key"] = key
                            toml.dump(llms, f)
                            st.session_state.save_success = True
                    if st.button("**接口测试**", use_container_width=True, type="primary"):
                        try:
                            genai.configure(client_options={"api_key": key})
                            model = genai.GenerativeModel("gemini-1.5-flash")
                            answer = model.generate_content("测试")
                            st.success("**测试成功！**", icon=":material/check:")
                        except Exception as e:
                            st.error(f"**测试失败：{e}**", icon=":material/error:")
                    if "save_success" in st.session_state:
                        st.success("**保存成功！**", icon=":material/check:")
                        del st.session_state["save_success"]
                gemini_setting(gemini_url, gemini_key)
        st.write("")

        with st.container(border=True):
            st.write("##### ChatGLM 智谱清言")
            st.write("调用 ChatGLM 官方接口服务来作为项目的翻译引擎")
            if st.button("&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;**配置**&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;", key="chatglm_button", type="primary"):
                @st.dialog('CHATGLM 智谱清言')
                def chatglm_setting(url, key):
                    st.write("官方网址：**[open.bigmodel.cn](https://open.bigmodel.cn/)** \n\n 基于GLM模型开发的千亿参数对话模型，支持多轮对话，具备内容创作、信息归纳总结等能力。")
                    st.write("")
                    url = st.text_input("**API 地址**", url, placeholder="ChatGLM API 接口", help="默认值：`https://open.bigmodel.cn/api/paas/v4/`")
                    key = st.text_input("**API 密钥**", key, placeholder="ChatGLM API 密钥")
                    st.write("")
                    if st.button("**保存配置**", use_container_width=True, type="primary"):
                        with open(llms_path, 'w') as f:
                            llms["ChatGLM"]["url"] = url
                            llms["ChatGLM"]["key"] = key
                            toml.dump(llms, f)
                            st.session_state.save_success = True
                    if st.button("**接口测试**", use_container_width=True, type="primary"):
                        try:
                            client = OpenAI(api_key=key, base_url=url)
                            response = client.chat.completions.create(
                                model="glm-4-0520",
                                messages=[{"role": "user", "content": "测试"}])
                            answer = response.choices[0].message.content
                            st.success("**测试成功！**", icon=":material/check:")
                        except Exception as e:
                            st.error(f"**测试失败：{e}**", icon=":material/error:")
                    if "save_success" in st.session_state:
                        st.success("**保存成功！**", icon=":material/check:")
                        del st.session_state["save_success"]
                chatglm_setting(chatglm_url, chatglm_key)
        st.write("")

        with st.container(border=True):
            st.write("##### AI01 零一万物")
            st.write("调用 零一万物 官方接口服务来作为项目的翻译引擎")
            if st.button("&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;**配置**&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;", key="ai01_button", type="primary"):
                @st.dialog('AI01 零一万物')
                def ai01_setting(url, key):
                    st.write("官方网址：**[platform.lingyiwanwu.com](https://platform.lingyiwanwu.com/)**零一万物是一家秉持着坚定的技术愿景和人工智能信仰，致力于打造 AI 2.0 的创新企业，将 Human + AI 合作创造巨大的经济价值及社会价值。")
                    st.write("")
                    url = st.text_input("**API 地址**", url, placeholder="AI01 API 接口", help="默认值：`https://api.lingyiwanwu.com/v1`")
                    key = st.text_input("**API 密钥**", key, placeholder="AI01 API 密钥")
                    st.write("")
                    if st.button("**保存配置**", use_container_width=True, type="primary"):
                        with open(llms_path, 'w') as f:
                            llms["Yi"]["url"] = url
                            llms["Yi"]["key"] = key
                            toml.dump(llms, f)
                            st.session_state.save_success = True
                    if st.button("**接口测试**", use_container_width=True, type="primary"):
                        try:
                            client = OpenAI(api_key=key, base_url=url)
                            response = client.chat.completions.create(
                                model="yi-spark",
                                messages=[{"role": "user", "content": "测试"}])
                            answer = response.choices[0].message.content
                            st.success("**测试成功！**", icon=":material/check:")
                        except Exception as e:
                            st.error(f"**测试失败：{e}**", icon=":material/error:")
                    if "save_success" in st.session_state:
                        st.success("**保存成功！**", icon=":material/check:")
                        del st.session_state["save_success"]
                ai01_setting(ai01_url, ai01_key)

    with col2:
        with st.container(border=True):
            st.write("##### Global 全局模型")
            st.write("配置 API中转服务超市 的接口作为项目的翻译引擎")

            if st.button("&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;**配置**&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;", key="global_button", type="primary"):
                @st.dialog('Global 全局模型')
                def global_setting(url, key, all_in_one):
                    st.write("")
                    st.write("我的中转：**[api.chenyme.top](https://api.chenyme.top)** \n\n 调用 中转服务商（OpenAI 接口管理 & 分发系统）的提供统一密钥作为翻译模型参数，无需配置其他模型密钥 \n\n 翻译模型必须中转服务商支持才可使用。开启后，**配置其他引擎不再生效(本地引擎除外)**，以此方法的配置为准，若想用自己的参数，请**关闭应用到全局**！")
                    st.write("")
                    url = st.text_input("**API 地址**", url, placeholder="中转服务 API接口")
                    key = st.text_input("**API 密钥**", key, placeholder="中转服务 API密钥")
                    all_in_one = st.toggle("**应用到全局**", value=all_in_one, help="打开后将此方法的参数配置作为翻译参数全局参数，仅支持使用 OpenAI SDK 接口的项目开启调用模型")
                    st.write("")
                    if st.button("**保存配置**", use_container_width=True, type="primary"):
                        with open(llms_path, 'w') as f:
                            llms["Global"]["key"] = key
                            llms["Global"]["url"] = url
                            llms["Global"]["all"] = all_in_one
                            toml.dump(llms, f)
                            st.session_state.save_success = True
                    if st.button("**接口测试**", use_container_width=True, type="primary"):
                        try:
                            client = OpenAI(api_key=key, base_url=url)
                            response = client.chat.completions.create(
                                model="gpt-4o-mini",
                                messages=[{"role": "user", "content": "测试"}])
                            answer = response.choices[0].message.content
                            st.success("**测试成功！**", icon=":material/check:")
                        except Exception as e:
                            st.error(f"**测试失败：{e}**", icon=":material/error:")
                    if "save_success" in st.session_state:
                        st.success("**保存成功！**", icon=":material/check:")
                        del st.session_state["save_success"]
                global_setting(global_url, global_key, all_in_one)
        st.write("")

        with st.container(border=True):
            st.write("##### ChatGPT OpenAI")
            st.write("调用 ChatGPT 官方接口服务来作为项目的翻译引擎")
            if st.button("&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;**配置**&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;", key="chatgpt_button", type="primary"):
                @st.dialog('ChatGPT OPENAI')
                def openai_setting(url, key):
                    st.write("官方网址：**[openai.com](https://openai.com/api/)** \n\n ChatGPT 是由 OpenAI 开发的基于 GPT-4 架构的语言模型。它能够理解和生成类人文本，用于对话、问题回答和文本生成等任务。它通过预训练和微调，学习了大量语言数据，能够在各种上下文中进行流畅的交流和生成有意义的内容。")
                    st.write("")
                    url = st.text_input("**API 地址**", url, placeholder="OpenAI API 接口", help="默认值：`https://api.openai.com/v1`")
                    key = st.text_input("**API 密钥**", key, placeholder="OpenAI API 密钥")
                    st.write("")
                    if st.button("**保存配置**", use_container_width=True, type="primary"):
                        with open(llms_path, 'w') as f:
                            llms["ChatGPT"]["url"] = url
                            llms["ChatGPT"]["key"] = key
                            toml.dump(llms, f)
                            st.session_state.save_success = True
                    if st.button("**接口测试**", use_container_width=True, type="primary"):
                        try:
                            client = OpenAI(api_key=key, base_url=url)
                            response = client.chat.completions.create(
                                model="gpt-4o-mini",
                                messages=[{"role": "user", "content": "测试"}])
                            answer = response.choices[0].message.content
                            st.success("**测试成功！**", icon=":material/check:")
                        except Exception as e:
                            st.error(f"**测试失败：{e}**", icon=":material/error:")
                    if "save_success" in st.session_state:
                        st.success("**保存成功！**", icon=":material/check:")
                        del st.session_state["save_success"]
                openai_setting(chatgpt_url, chatgpt_key)
        st.write("")

        with st.container(border=True):
            st.write("##### Claude Anthropic")
            st.write("调用 Claude 的官方接口服务来作为项目的翻译引擎")
            if st.button("&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;**配置**&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;", key="claude_button", type="primary"):
                @st.dialog('CLAUDE Anthropic')
                def claude_setting(url, key):
                    st.write("官方接口: **[www.anthropic.com](https://www.anthropic.com/api)** \n\n Claude 是一种人工智能，由 Anthropic 使用 Constitutional AI 进行训练，确保其安全、准确且可靠 — 是您发挥最佳工作能力的最佳助手。")
                    st.write("")
                    url = st.text_input("**API 地址**", url, placeholder="Claude API 接口", help="默认值：`https://api.anthropic.com/v1/messages`")
                    key = st.text_input("**API 密钥**", key, placeholder="Claude API 密钥")
                    st.write("")
                    if st.button("**保存配置**", use_container_width=True, type="primary"):
                        with open(llms_path, 'w') as f:
                            llms["Claude"]["url"] = url
                            llms["Claude"]["key"] = key
                            toml.dump(llms, f)
                            st.session_state.save_success = True
                    if st.button("**接口测试**", use_container_width=True, type="primary"):
                        try:
                            client = anthropic.Anthropic(api_key=key, base_url=url)
                            message = client.messages.create(
                                model="claude-3-opus",
                                max_tokens=1024,
                                messages=[{"role": "user", "content": "测试"}]
                            )
                            st.success("**测试成功！**", icon=":material/check:")
                        except Exception as e:
                            st.error(f"**测试失败：{e}**", icon=":material/error:")
                    if "save_success" in st.session_state:
                        st.success("**保存成功！**", icon=":material/check:")
                        del st.session_state["save_success"]

                claude_setting(claude_url, claude_key)
        st.write("")

        with st.container(border=True):
            st.write("##### Kimi 月之暗面")
            st.write("调用 Kimi 的官方接口服务来作为本项目的翻译引擎")
            if st.button("&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;**配置**&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;", key="kimi_button", type="primary"):
                @st.dialog('KIMI 月之暗面')
                def kimi_setting(url, key):
                    st.write("官网网址：**[www.moonshot.cn](https://www.moonshot.cn/)** \n\n 月之暗面（Moonshot AI) 创立于2023年3月，是一家国内通用人工智能领域的创业公司。月之暗面致力于寻求将能源转化为智能的最优解，通过产品与用户共创智能。")
                    st.write("")
                    url = st.text_input("**API 地址**", url, placeholder="Kimi API 接口", help="默认值：`https://api.moonshot.cn/v1`")
                    key = st.text_input("**API 密钥**", key, placeholder="Kimi API 密钥")
                    st.write("")
                    if st.button("**保存配置**", use_container_width=True, type="primary"):
                        with open(llms_path, 'w') as f:
                            llms["Kimi"]["url"] = url
                            llms["Kimi"]["key"] = key
                            toml.dump(llms, f)
                            st.session_state.save_success = True
                    if st.button("**接口测试**", use_container_width=True, type="primary"):
                        try:
                            client = OpenAI(api_key=key, base_url=url)
                            response = client.chat.completions.create(
                                model="moonshot-v1-8k",
                                messages=[{"role": "user", "content": "测试"}])
                            answer = response.choices[0].message.content
                            st.success("**测试成功！**", icon=":material/check:")
                        except Exception as e:
                            st.error(f"**测试失败：{e}**", icon=":material/error:")
                    if "save_success" in st.session_state:
                        st.success("**保存成功！**", icon=":material/check:")
                        del st.session_state["save_success"]
                kimi_setting(kimi_base, kimi_key)
        st.write("")

        with st.container(border=True):
            st.write("##### Custom 自定义模型")
            st.write("调用 用户自定义的模型 名称来作为项目的翻译引擎")
            if st.button("&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;**配置**&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;", key="custom_button", type="primary"):
                @st.dialog('Custom 自定义模型')
                def custom_setting(url, key, model):
                    st.warning("""
                    ### 此方法作者已弃用或即将更新

                    &nbsp;  
                    此模块主要用于纠正各大服务商模型更新导致与项目模型信息冲突！支持使用自定义的最新模型名称来作为项目的翻译引擎，**目前尚未适配完毕！若要使用自定义模型，可先利用 Local本地模型 调用过渡！**

                    如有其他疑问，请前往
                    
                    - **[GitHub](https://github.com/Chenyme/Chenyme-AAVT)**
                    - **[Telegram](https://t.me/+j8SNSwhS7xk1NTc9)**
                    - **[MyBlog](https://blog.chenyme.top)**
                    
                    查看 相关信息 或 提交 Issue 反馈！  

                    &nbsp;  
                    """, icon=":material/error_med:")
                    # url = st.text_input("**API 地址**", url, placeholder="API 接口")
                    # key = st.text_input("**API 密钥**", key, placeholder="API 密钥")
                    # model = st.text_input("**模型名称**", model, placeholder="模型名称")
                    # st.write("")
                    # if st.button("**保存配置**", use_container_width=True, type="primary"):
                    #     with open(llms_path, 'w') as f:
                    #         llms["Custom"]["key"] = key
                    #         llms["Custom"]["url"] = url
                    #         llms["Custom"]["model"] = model
                    #         toml.dump(llms, f)
                    #         st.session_state.save_success = True
                    # if st.button("**接口测试**", use_container_width=True, type="primary"):
                    #     try:
                    #         client = OpenAI(api_key=key, base_url=url)
                    #         response = client.chat.completions.create(
                    #             model=model,
                    #             messages=[{"role": "user", "content": "测试"}])
                    #         answer = response.choices[0].message.content
                    #         st.success("**测试成功！**", icon=":material/check:")
                    #     except Exception as e:
                    #         st.error(f"**测试失败：{e}**", icon=":material/error:")
                    # if "save_success" in st.session_state:
                    #     st.success("**保存成功！**", icon=":material/check:")
                    #     del st.session_state["save_success"]
                custom_setting(custom_base, custom_key, custom_model)

with tab4:
    ProjectSave = st.container()
    ProjectSetting = st.container(border=True)
    with ProjectSetting:
        st.write("")
        st.write("###### 恒定速率因子")
        st.caption("CRF 值的范围通常为 0 到 51，数值越低，质量越高。建议值：\n- `0`: 无损压缩，质量最高，文件最大。\n- `18`: 视觉上接近无损，非常高的质量，文件较大。\n- `23`: 默认值，质量和文件大小的平衡点。\n- `28`: 较低的质量，文件较小。")
        crf = st.selectbox("FFmpeg-恒定速率因子", [0, 18, 23, 28], index=[0, 18, 23, 28].index(crf_setting), label_visibility="collapsed")
        st.write("")
        st.write("###### 编码器")
        st.caption("当 CUDA 可用时，可选择 `h264_nvenc` 编码，否则请默认 `libx264` 编码。\n\n 请注意 `h264_nvenc` 的编码质量高，输出文件会很大！")
        ffmpeg = st.selectbox("FFmpeg-编码器", ["h264_nvenc", "libx264"], index=["h264_nvenc", "libx264"].index(ffmpeg_setting), label_visibility="collapsed")
        st.write("")
        st.write("###### 编码器预设(质量)")
        st.caption("编码器预设(质量quality)，默认值为 `medium`。注意，下面有些值是不可使用的，若你不了解，请勿修改！可选值包括：\n- `ultrafast`: 最快的编码速度，但质量最低，文件最大。\n- `superfast`: 非常快的编码速度，质量和文件大小有所提升。\n- `veryfast`: 很快的编码速度，适用于实时编码或需要快速处理的情况。\n- `faster`: 比较快的编码速度，质量进一步提高。\n- `fast`: 快速编码速度，质量较好。\n- `medium`: 默认预设，编码速度和质量的平衡点。\n- `slow`: 较慢的编码速度，输出质量更高，文件更小。\n- `slower`: 更慢的编码速度，质量进一步提高。\n- `veryslow`: 非常慢的编码速度，质量最高，文件最小。\n- `placebo`: 极慢的编码速度，质量微小提升，不推荐使用，除非对质量有极高要求且不在意编码时间。")
        quality_list = ["ultrafast", "superfast", "veryfast", "faster", "fast", "medium", "slow", "slower", "veryslow", "placebo"]
        quality = st.selectbox("FFmpeg-编码器预设(质量)", quality_list, index=quality_list.index(quality_setting), label_visibility="collapsed")
        st.write("")
        st.write("###### 日志级别")
        st.caption("FFmpeg输出日志参数说明：\n- `quiet`：没有输出日志。\n- `panic`：仅在不可恢复的致命错误发生时输出日志。\n- `fatal`：仅在致命错误发生时输出日志。\n- `error`：在错误发生时输出日志。\n- `warning`：在警告级别及以上的事件发生时输出日志。\n- `info`：在信息级别及以上的事件发生时输出日志。\n- `verbose`：输出详细信息，包括调试和信息级别的日志。\n- `debug`：输出调试信息，非常详细的日志输出。\n- `trace`：最详细的日志输出，用于极其详细的调试。")
        log = st.selectbox("FFmpeg-日志级别", ["quiet", "panic", "fatal", "error", "warning", "info", "verbose", "debug", "trace"], index=["quiet", "panic", "fatal", "error", "warning", "info", "verbose", "debug", "trace"].index(log_setting), label_visibility="collapsed")
        st.write("")

    with ProjectSave:
        col1, col2 = st.columns([0.75, 0.25])
        st.write("")
        with col2:
            st.write("")
            st.write("")
            if st.button("**保存更改**", use_container_width=True, type="primary", key="ffmpeg"):
                with open(project_config_path, 'w', encoding="utf-8") as f:
                    project["ffmpeg"]["log"] = log
                    project["ffmpeg"]["crf"] = crf
                    project["ffmpeg"]["quality"] = quality
                    project["ffmpeg"]["ffmpeg"] = ffmpeg
                    toml.dump(project, f)
                st.session_state.save = True
                st.rerun()

        with col1:
            st.write("")
            st.write("")
            st.write("### FFMpeg 设置")
            st.caption("FFMpeg Settings")

with tab5:
    cache_path = "cache"
    modules = ["tts", "blog", "audio", "video", "translate"]
    module_sizes = {}
    module_file_counts = {}
    module_folder_details = {}
    for module in modules:
        module_path = os.path.join(cache_path, module)
        total_size = 0
        file_count = 0
        folder_details = {}

        if os.path.exists(module_path):
            for dirpath, dirnames, filenames in os.walk(module_path):
                for filename in filenames:
                    filepath = os.path.join(dirpath, filename)
                    total_size += os.path.getsize(filepath)
                    file_count += 1
                if dirpath not in folder_details:
                    folder_size = sum([os.path.getsize(os.path.join(dirpath, f)) for f in filenames])
                    folder_details[dirpath] = {'size': folder_size / (1024 * 1024), 'file_count': len(filenames)}

        module_sizes[module] = total_size
        module_file_counts[module] = file_count
        module_folder_details[module] = folder_details

    total_size = sum(module_sizes.values())
    total_files = sum(module_file_counts.values())

    st.write("")
    st.write("")
    st.markdown(f"""
    <div style="background-color: #FAFAFA; padding: 20px; border-radius: 20px; box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1); margin-bottom: 20px;">
        <div style="font-size: 20px; font-weight: 600; color: #1C1C1E;">总缓存占用 Total Cache Usage</div>
        <div style="font-size: 34px; font-weight: bold; color: #007AFF;">{total_size / (1024 * 1024):.2f} MB</div>
        <div style="font-size: 16px; color: #8E8E93;">总文件数: {total_files}</div>
    </div>
    """, unsafe_allow_html=True)

    st.write("")
    st.write("#### 选择要清理的模块")
    st.write("")
    col1, col2 = st.columns([0.75, 0.25])
    with col1:
        selected_module = st.selectbox("选择要清理的模块", modules, label_visibility="collapsed")
    with col2:
        if st.button(f"**清空模块**", use_container_width=True, type="primary"):
            selected_module_path = os.path.join(cache_path, selected_module)
            if os.path.exists(selected_module_path):
                has_content = False
                for root, dirs, files in os.walk(selected_module_path):
                    if files or dirs:
                        has_content = True
                        for file in files:
                            os.remove(os.path.join(root, file))
                        for dir in dirs:
                            shutil.rmtree(os.path.join(root, dir))
                    break
                if has_content:
                    st.session_state.delete = True
                    st.rerun()
                else:
                    st.toast(f"{selected_module} 模块为空，无需清理。", icon=":material/error:")
            else:
                st.toast(f"{selected_module} 模块不存在或已经被清理。", icon=":material/error:")
    st.write("")
    with st.container(border=True):
        st.write("")
        st.write("###### 模块数据总览")
        st.write("")
        size = module_sizes[selected_module]
        st.markdown(f"""
        <div style="background-color: #FAFAFA; padding: 20px; border-radius: 20px; box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1); margin-bottom: 20px;">
            <div style="font-size: 20px; font-weight: 600; color: #1C1C1E;">模块：{selected_module}</div>
            <div style="font-size: 34px; font-weight: bold; color: #007AFF;">{size / (1024 * 1024):.2f} MB</div>
            <div style="font-size: 16px; color: #8E8E93;">文件数: {module_file_counts[selected_module]}</div>
        </div>
        """, unsafe_allow_html=True)

        folders = module_folder_details[selected_module]
        folder_data = []
        for folder, details in folders.items():
            folder_data.append([folder, f"{details['size']:.2f} MB", details['file_count']])

        folder_df = pd.DataFrame(folder_data, columns=["文件夹", "大小", "文件数"])

        st.write("")
        st.write("###### 模块文件情况")
        st.write("")
        st.dataframe(folder_df, hide_index=True, use_container_width=True)

        st.write("")
        st.write("###### 删除模块文件")
        st.write("")
        col1, col2 = st.columns([0.75, 0.25])
        with col1:
            selected_folder = st.selectbox(f"选择要删除的文件夹 ({selected_module})", folder_df["文件夹"], label_visibility="collapsed")

        with col2:
            if st.button(f"**点击删除**", use_container_width=True, type="primary"):
                try:
                    if os.path.basename(selected_folder) not in selected_module:
                        shutil.rmtree(selected_folder)
                        st.session_state.delete = True
                        st.rerun()
                    else:
                        st.toast(f"不能删除模块根目录 ({selected_module})", icon=":material/error:")
                except Exception as e:
                    st.toast(f"删除文件夹失败({e})", icon=":material/error:")

        st.write("")
        st.write("###### 模块缓存图")
        st.write("")
        st.write("")
        module_size_mb = {module: size / (1024 * 1024) for module, size in module_sizes.items()}
        st.bar_chart(pd.DataFrame(module_size_mb.values(), index=modules, columns=["大小(MB)"]), color="#007AFF", height=200, horizontal=True)

with tab6:
    OtherSave = st.container()
    st.write("")
    OtherSetting = st.container(border=True)

    with OtherSetting:
        open_protect = st.toggle("**开启使用保护**", value=open_protect)

        st.write("")
        st.write("###### 保护密码")
        st.caption("开启后必须输入密码才能进入项目页面，保护您在服务器上部署的项目")
        password_protect = st.text_input("password", placeholder="填入您的保护密码", type="password", label_visibility="collapsed", value=password_protect)
        if open_protect and password_protect != "" and len(password_protect) < 8:
            st.error("##### 密码过于简单 \n\n 为了您的安全，请设置大于8位的密码！", icon=":material/lock:")
        st.write("")

    with OtherSave:
        col1, col2 = st.columns([0.75, 0.25])
        with col1:
            st.write("")
            st.write("")
            st.subheader("项目保护*")
            st.caption("Project Protection (Beta)")
        with col2:
            st.write("")
            st.write("")
            if st.button("**&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;保存设置&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;**", type="primary", use_container_width=True):
                if open_protect and len(password_protect) < 8:
                    st.toast("密码过于简单！", icon=":material/lock:")
                else:
                    with open(project_config_path, 'w', encoding="utf-8") as f:
                        project["protect"]["open"] = open_protect
                        project["protect"]["password"] = password_protect
                        toml.dump(project, f)
                    st.session_state.save = True
                    st.rerun()
