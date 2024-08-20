import os
import toml
import datetime
import streamlit as st
from openai import OpenAI
import streamlit_antd_components as sac
from styles.global_style import style

style()
path = os.getcwd() + "/"
llms_path = path + "config/llms.toml"
translate_config_path = path + "config/translate.toml"
prompt_config_path = path + "config/prompt.json"
project_config_path = path + "config/project.toml"
tts_cache_path = path + "cache/tts/"
public_path = path + "cache/public/"

with open(llms_path, 'r', encoding="utf-8") as config_file:
    llms = toml.load(config_file)
with open(translate_config_path, 'r', encoding="utf-8") as config_file:
    translate_config = toml.load(config_file)
with open(project_config_path, 'r', encoding='utf-8') as config_file:
    project = toml.load(config_file)

chatgpt_key = llms["ChatGPT"]["key"]  # Openai
chatgpt_url = llms["ChatGPT"]["url"]

tab1, tab2 = st.tabs(["**OpenTTS**", "**ChatTTS**"])
with tab1:
    col1, col2 = st.columns([0.75, 0.25])
    TTSSetting = st.expander("**Settings / 设置**", expanded=False, icon=":material/settings:")
    TTSPreview = st.expander("**TTS Preview / TTS 预览**", expanded=True, icon=":material/record_voice_over:")


    with TTSPreview:
        st.write("")
        st.caption("模拟文本")
        input = st.text_area("模拟的文本", value="Today is a wonderful day to build something people love!", height=150, label_visibility="collapsed")

    with TTSSetting:
        st.write("")
        col3, col4 = st.columns(2, gap="large")
        with col3:
            st.caption("OpenTTS 模型")
            model = st.selectbox("模型", ["tts-1", "tts-1-hd"], label_visibility="collapsed")
        with col4:
            st.caption("生成音色")
            voice = st.selectbox("音色", ["alloy", "echo", "fable", "onyx", "nova", "shimmer"], label_visibility="collapsed")
        audio_file = open(public_path + "res/" + voice + ".wav", 'rb')
        audio_bytes = audio_file.read()
        st.caption(f"{voice} 声音效果预览")
        st.audio(audio_bytes)

    with col1:
        st.write("")
        st.write("")
        st.write("### OpenAI TTS")
        st.caption("OpenAI 文本到语音")
    with col2:
        st.write("")
        st.write("")
        if st.button("**开始生成**", use_container_width=True, type="primary"):
            current_time = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
            open_cache_path = tts_cache_path + current_time
            os.makedirs(open_cache_path)
            open_tts_path = f"{open_cache_path}/TTSOutput.mp3"

            client = OpenAI(api_key=chatgpt_key, base_url=chatgpt_url)
            response = client.audio.speech.create(
              model=model,
              voice=voice,
              input=input
            )
            response.stream_to_file(open_tts_path)
            st.session_state.tts_path = open_tts_path

    with TTSPreview:
        try:
            audio_file = open(st.session_state.tts_path, 'rb')
            audio_bytes = audio_file.read()
            st.caption("生成的音频")
            st.audio(audio_bytes)
        except:
            st.info("##### 结果预览框 \n\n&nbsp;**生成完毕后会在此区域自动显示**", icon=":material/view_in_ar:")
with tab2:
    st.write("")
    st.write("")

    st.warning("""
    **此方法作者已弃用或即将更新：**  

    &nbsp;  

    如有问题，可前往&nbsp;  **[GitHub](https://github.com/Chenyme/Chenyme-AAVT)** &nbsp; |&nbsp;  **[Telegram](https://t.me/+j8SNSwhS7xk1NTc9)** &nbsp; |&nbsp;  **[MyBlog](https://blog.chenyme.top)** &nbsp; 查看相关信息或提问反馈！  

    &nbsp;  
    """, icon=":material/error_med:")