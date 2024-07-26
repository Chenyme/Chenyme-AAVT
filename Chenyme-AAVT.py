import streamlit as st
import streamlit_antd_components as sac
from project.media import media
from project.home import home
from project.content import content
from project.translation import translation
from project.AVTB.AVTB import avtb
from project.AVG.AVG import avg

st.set_page_config(
    page_title="Chenyme-AAVT v0.8.5",
    page_icon=":material/radio_button_checked:",
    layout="wide",
    initial_sidebar_state="expanded"
)

with st.sidebar.container():
    st.subheader("Chenyme-AAVT")
    menu = sac.menu(
        items=[
            sac.MenuItem('主页', icon='house-fill'),
            sac.MenuItem('主项目', icon='box-fill', children=[
                sac.MenuItem('媒体识别', icon='camera-reels'),
                sac.MenuItem('内容助手', icon='robot'),
                sac.MenuItem('字幕翻译', icon='file-earmark-break')]),
            sac.MenuItem('实验室', icon='buildings-fill', children=[
                sac.MenuItem('图文博客', icon='images'),
                sac.MenuItem('声音模拟', icon='person-bounding-box')])
        ],
        key='menu',
        open_index=[1]
    )
    sac.divider(label='POWERED BY @CHENYME', icon="lightning-charge", align='center', color='gray')


if menu == "主页":
    home()
elif menu == '内容助手':
    content()
elif menu == '媒体识别':
    media()
elif menu == '字幕翻译':
    translation()
elif menu == '图文博客':
    avtb()
elif menu == '声音模拟':
    avg()

