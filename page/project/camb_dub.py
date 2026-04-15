import os
import toml
import datetime
import streamlit as st
from styles.global_style import style
from utils.public import CambDubbing

style()

path = os.getcwd() + "/"
llms_path = path + "config/llms.toml"
dub_cache_path = path + "cache/camb_dub/"
os.makedirs(dub_cache_path, exist_ok=True)

with open(llms_path, 'r', encoding="utf-8") as config_file:
    llms = toml.load(config_file)

camb_cfg = llms.get("Camb", {})
camb_key = camb_cfg.get("key", "") or os.environ.get("CAMB_API_KEY", "")

st.subheader("Camb AI 一键视频配音")
st.caption("Camb One-shot Dubbing — 跳过 Whisper/翻译/TTS 全流程，直接由 Camb AI 完成端到端视频配音")

if not camb_key:
    st.warning("尚未配置 `CAMB_API_KEY`。请前往 **设置 → 翻译设置 → Camb AI** 配置后再使用。",
               icon=":material/running_with_errors:")

with st.expander("**参数设置**", expanded=True, icon=":material/settings:"):
    col1, col2 = st.columns(2)
    with col1:
        st.caption("源语言 (BCP-47 short_name)")
        source_language = st.text_input("源语言", value="en-us", label_visibility="collapsed")
    with col2:
        st.caption("目标语言 (BCP-47 short_name)")
        target_language = st.text_input("目标语言", value="es-es", label_visibility="collapsed")

st.write("")
col1, col2 = st.columns([0.75, 0.25])
with col1:
    st.write("")
    st.caption("支持的视频格式：mp4, mov, avi, mkv, webm")
    uploaded_file = st.file_uploader("上传要配音的视频", type=['mp4', 'mov', 'avi', 'mkv', 'webm', 'm4v'],
                                     key="camb_dub_upload")
with col2:
    st.write("")
    st.write("")
    run = st.button("**开始配音**", type="primary", use_container_width=True)

if run:
    if uploaded_file is None:
        st.toast("请先上传视频文件", icon=":material/release_alert:")
    elif not camb_key:
        st.toast("请先在设置中配置 CAMB_API_KEY", icon=":material/release_alert:")
    else:
        current_time = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        run_dir = os.path.join(dub_cache_path, current_time)
        os.makedirs(run_dir, exist_ok=True)
        input_path = os.path.join(run_dir, uploaded_file.name)
        output_path = os.path.join(run_dir, "dubbed_" + uploaded_file.name)
        with open(input_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        msg = st.toast("正在提交 Camb 配音任务...", icon=":material/rocket_launch:")
        try:
            CambDubbing(
                api_key=camb_key,
                video_path=input_path,
                source_language=source_language,
                target_language=target_language,
                output_path=output_path,
            )
            msg.toast("Camb 配音完成！", icon=":material/verified:")
            st.session_state.camb_dub_output = output_path
        except Exception as e:
            st.error(f"Camb 配音失败：{e}", icon=":material/error:")

if "camb_dub_output" in st.session_state and os.path.isfile(st.session_state.camb_dub_output):
    st.write("")
    st.success("配音完成", icon=":material/check:")
    with open(st.session_state.camb_dub_output, "rb") as f:
        data = f.read()
    st.video(data)
    st.download_button("**下载配音视频**", data=data,
                       file_name=os.path.basename(st.session_state.camb_dub_output),
                       mime="video/mp4", type="primary", use_container_width=True)
