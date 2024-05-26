import streamlit as st
import streamlit_antd_components as sac
from project.video import video
from project.home import home
from project.audio import audio
from project.AVTB.AVTB import avtb
st.set_page_config(
    page_title="AAVT v0.8.2",
    page_icon="🎞️",
    layout="wide",  # 设置布局样式为宽展示
    initial_sidebar_state="expanded"  # 设置初始边栏状态为展开
)


with st.sidebar.container():
    menu = sac.menu(
        items=[
            sac.MenuItem('主页', icon='house-fill'),
            sac.MenuItem('我的项目', icon='box-fill', children=[
                sac.MenuItem('内容助手', icon='file-earmark-break', tag=[sac.Tag('Update', color='red')]),
                sac.MenuItem('视频翻译', icon='camera-reels', tag=[sac.Tag('Update', color='red')]),
                sac.MenuItem('实验室', icon='sliders', children=[
                    sac.MenuItem('视频博客', icon='subtitles')])
                ])],
        key='menu',
        open_index=[1]
    )
    sac.divider(label='POWERED BY @CHENYME', icon="lightning-charge", align='center', color='gray')

with st.container():
    if menu == "主页":
        home()
    elif menu == '内容助手':
        audio()
    elif menu == '视频翻译':
        video()
    elif menu == '视频博客':
        avtb()

