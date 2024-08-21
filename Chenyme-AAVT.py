import os
import toml
import streamlit as st
from utils.get_font import get_font_data
from styles.global_style import style

style(True)
get_font_data()

os.environ['KMP_DUPLICATE_LIB_OK'] = 'True'  # 修复OMP

path = os.getcwd() + "/"
project_config_path = path + "config/project.toml"

with open(project_config_path, 'r', encoding='utf-8') as config_file:
    project = toml.load(config_file)
open_protect = project["protect"]["open"]
password_protect = project["protect"]["password"]


if not open_protect:
    st.session_state.verify = True

if "verify" in st.session_state:
    pages = {
        "Home": [
            st.Page(page="page/project/home.py", title="主页", icon=":material/home:"),
            st.Page("page/setting/set.py", title="设置", icon=":material/settings:")
        ],
        "Project": [
            st.Page(page="page/project/audio.py", title="音频识别", icon=":material/graphic_eq:"),
            st.Page(page="page/project/video.py", title="视频识别", icon=":material/subscriptions:"),
            st.Page(page="page/project/translate.py", title="字幕翻译", icon=":material/subtitles:"),
        ],
        "Test": [
            st.Page("page/tests/test.py", title="声音克隆", icon=":material/view_in_ar:"),
            st.Page(page="page/tests/tools.py", title="辅助工具", icon=":material/construction:")
        ],
    }

    pg = st.navigation(pages, position="sidebar")
    pg.run()
else:
    st.write("# ")
    st.markdown("<h1 style='text-align: center;'>Chenyme-AAVT V0.9.0</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: grey; font-size: 12px;'>&copy; 2024 Powered By @Chenyme</p>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    with col2:
        st.write("")
        st.write("")
        st.info("##### 请登录 \n\n 请验证密码后使用本项目！", icon=":material/lock:")
        st.write("")
        st.write("")
        password_protect2 = st.text_input("mm", placeholder="验证密码", label_visibility="collapsed")
        st.write("")
        st.write("")
        if st.button("**验证**", type="primary", use_container_width=True):
            if password_protect2 == password_protect:
                st.session_state.verify = True
                st.rerun()
            else:
                st.toast("**错误！** \n\n 请重新输入您的密码！", icon=":material/lock:")
