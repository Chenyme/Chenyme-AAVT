import os
import toml
import datetime
import streamlit as st
from openai import OpenAI
import streamlit_antd_components as sac


def avg():
    col1, col2 = st.columns(2, gap="large")

    with col1:
        st.write("#### OpenAI TTS")

        project_dir = os.path.dirname(os.path.abspath(__file__)).replace("\\", "/")
        cache_dir = project_dir + "/output/"

        config_dir = project_dir.replace("AVG", "") + "config/api.toml"
        config = toml.load(config_dir)
        st.session_state.base_url = config["GPT"]["openai_base"]
        st.session_state.api_key = config["GPT"]["openai_key"]

        model = st.selectbox("model", ["tts-1", "tts-1-hd"])
        voice = st.selectbox("voice", ["alloy", "echo", "fable", "onyx", "nova", "shimmer"])
        input = st.text_area("input_text", value="Today is a wonderful day to build something people love!", height=300)
        client = OpenAI(api_key=st.session_state.api_key, base_url=st.session_state.base_url)

        if st.button("生成", use_container_width=True, type="primary"):
            current_time = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            speech_file_path = cache_dir + current_time + ".mp3"
            response = client.audio.speech.create(
              model=model,
              voice=voice,
              input=input
            )
            response.stream_to_file(speech_file_path)
            st.session_state.path = speech_file_path

        try:
            audio_file = open(st.session_state.path, 'rb')
            audio_bytes = audio_file.read()
            st.write("###### 音频")
            st.audio(audio_bytes)
        except:
            sac.alert(
                label='**运行后自动显示结果**',
                description="这里会显示生成的音频",
                size='lg', radius=20, icon=True, closable=True, color='info')

    with col2:
        st.write("#### Exemple")
        name = ["alloy", "echo", "fable", "onyx", "nova", "shimmer"]
        for i in name:
            audio_file = open(project_dir + "/res/" + i + ".wav", 'rb')
            audio_bytes = audio_file.read()
            st.write(f"###### {i}")
            st.audio(audio_bytes)

    st.write("#### ChatTTS")
    sac.alert(
        label='**敬请期待**',
        description="由于学业，可能会鸽到12月，还请谅解",
        size='lg', radius=20, icon=True, closable=True, color='info')



