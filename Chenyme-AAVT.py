import streamlit as st
import streamlit_antd_components as sac
from project.video import video
from project.home import home
from project.content import content
from project.translation import translation
from project.AVTB.AVTB import avtb

st.set_page_config(
    page_title="Chenyme-AAVT v0.8.3",
    page_icon=":material/radio_button_checked:",
    layout="wide",  # 设置布局样式为宽展示
    initial_sidebar_state="expanded"  # 设置初始边栏状态为展开
)


with st.sidebar.container():
    st.subheader("Chenyme-AAVT")
    menu = sac.menu(
        items=[
            sac.MenuItem('项目主页', icon='house-fill'),
            sac.MenuItem('我的项目', icon='box-fill', children=[
                sac.MenuItem('视频识别', icon='camera-reels', tag=[sac.Tag('Update', color='red')]),
                sac.MenuItem('内容助手', icon='robot', tag=[sac.Tag('New', color='green')]),
                sac.MenuItem('字幕翻译', icon='file-earmark-break', tag=[sac.Tag('New', color='green')]),
            ]),
            sac.MenuItem('实验室', icon='postage-fill', children=[
                sac.MenuItem('图文博客', icon='images')])
            ],
        key='menu',
        open_index=[1]
    )
    sac.divider(label='POWERED BY @CHENYME', icon="lightning-charge", align='center', color='gray')

with st.container():
    if menu == "项目主页":
        home()
    elif menu == '内容助手':
        content()
    elif menu == '视频识别':
        video()
    elif menu == '字幕翻译':
        translation()
    elif menu == '图文博客':
        avtb()

