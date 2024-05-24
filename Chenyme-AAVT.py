import os
import toml
import shutil
import streamlit as st
from openai import OpenAI
from utils.utils import (convert_size, cache)
import streamlit_antd_components as sac
from project.audio import audio
from project.video import video
from project.AVTB.AVTB import avtb


st.set_page_config(
    page_title="AAVT v0.8",
    page_icon="🎞️",
    layout="wide",  # 设置布局样式为宽展示
    initial_sidebar_state="expanded"  # 设置初始边栏状态为展开
)


with st.sidebar.container():
    menu = sac.menu(
        items=[
            sac.MenuItem('主页', icon='house-fill'),
            sac.MenuItem('我的项目', icon='box-fill', children=[
                sac.MenuItem('音频', icon='mic'),
                sac.MenuItem('视频', icon='camera-reels'),
                sac.MenuItem('实验室', icon='sliders', tag=[sac.Tag('New', color='red')], children=[
                    sac.MenuItem('视频生成博客', icon='subtitles', tag=[sac.Tag('Beta', color='green')])])
                ])],
        key='menu',
        open_index=[1]
    )
    sac.divider('没有更多啦~', align='center', color='gray')

with st.container():
    if menu == '音频':
        audio()
    elif menu == '视频':
        video()
    elif menu == '视频生成博客':
        avtb()

    else:
        # 主页面
        project_dir = os.path.dirname(os.path.abspath(__file__)).replace("\\", "/")
        log_dir = project_dir + "/public/log.md"  # 更新日志
        read_dir = project_dir + "/public/README.md"  # 项目文档
        model_dir = project_dir + "/models"  # 模型目录
        config_dir = project_dir + "/config/"  # 配置文件
        cache_dir = project_dir + "/project/cache/"  # 本地缓存

        with open(read_dir, 'r', encoding='utf-8') as file:
            markdown_content = file.read()

        st.title("🖥Chenyme-AAVT V0.8")
        st.caption("POWERED BY @CHENYME")

        tab1, tab2 = st.tabs(["主页", "设置"])
        with tab1:  # 主界面功能
            messages = st.container(height=400)
            if "messages" not in st.session_state:
                st.session_state["messages"] = [
                    {"role": "assistant", "content": "我是本项目的AI小助手，有什么可以帮你的么?"}]

            for msg in st.session_state.messages:
                messages.chat_message(msg["role"]).write(msg["content"])

            if prompt := st.chat_input():
                client = OpenAI(api_key=st.session_state.openai_key)
                st.session_state.messages.append({"role": "user", "content": prompt})
                messages.chat_message("user").write(prompt)
                response = client.chat.completions.create(model="gpt-3.5-turbo", messages=[{"role": "system", "content": "你是一个基于下面内容的AI小助手，请基于下面的内容和自己的知识回答用户问题。" + markdown_content},
                                                                                           {"role": "user", "content": prompt}])
                msg = response.choices[0].message.content
                st.session_state.messages.append({"role": "assistant", "content": msg})
                messages.chat_message("assistant").write(msg)

        with tab2:
            config = toml.load(config_dir + "config.toml")  # 加载配置
            openai_api_key = config["GPT"]["openai_key"]
            openai_api_base = config["GPT"]["openai_base"]
            kimi_api_key = config["KIMI"]["kimi_key"]
            deepseek_api_key = config["DEEPSEEK"]["deepseek_key"]
            chatglm_api_key = config["CHATGLM"]["chatglm_key"]
            openai_whisper_api = config["WHISPER"]["openai_whisper_api"]  # openai_whisper配置
            faster_whisper_model = config["WHISPER"]["faster_whisper_model_default"]  # faster_whisper配置
            faster_whisper_local = config["WHISPER"]["faster_whisper_model_local"]  # 本地模型加载
            faster_whisper_local_path = config["WHISPER"]["faster_whisper_model_local_path"]  # 本地模型路径

            st.session_state.openai_key = openai_api_key  # 缓存key
            st.session_state.openai_base = openai_api_base  # 缓存base
            st.session_state.kimi_key = kimi_api_key  # 缓存key
            st.session_state.deepseek_key = deepseek_api_key  # 缓存key
            st.session_state.chatglm_key = chatglm_api_key  # 缓存key

            options = {'faster-whisper': {'models': {'tiny': 0, 'tiny.en': 1, 'base': 2, 'base.en': 3, 'small': 4,
                                                     'small.en': 5, 'medium': 6, 'medium.en': 7, 'large-v1': 8,
                                                     'large-v2': 9, 'large-v3': 10, 'large': 11, 'distil-small.en': 12,
                                                     'distil-medium.en': 13, 'distil-large-v2': 14,
                                                     'distil-large-v3': 15}}}

            # Whisper模型
            st.write("#### Whisper识别设置")
            index = 1
            if openai_whisper_api:
                index = 0
            set_model = st.selectbox("选择whisper识别模式", ("Openai-api 接口调用", "Faster-whisper 本地部署"),
                                     index=index)

            if set_model == "Faster-whisper 本地部署":
                w_local = st.checkbox('启用本地模型', faster_whisper_local)
                if w_local:
                    model_names = os.listdir(model_dir)
                    path = faster_whisper_local_path
                    try:
                        index_model = model_names.index(path.replace(model_dir + '/', ''))
                    except:
                        index_model = 0
                    w_local_option = st.selectbox('选择本地模型', model_names, index=index_model)
                    w_local_model_path = model_dir + '/' + w_local_option
                    st.write("```推荐使用 large 模型获得最佳断句、识别体验！！！```")
                    st.write(
                        "```若开启GPU请注意：最新版本仅支持 CUDA 12。对于 CUDA 11，当前的解决方法是降级 ctranslate2==3.24.0。```")
                    st.write("```模型下载：```" + "[Huggingface.co / Systran](https://huggingface.co/Systran)")
                    config["WHISPER"]["faster_whisper_model_local"] = w_local
                    config["WHISPER"]["faster_whisper_model_local_path"] = w_local_model_path
                else:
                    w_model_option = st.selectbox('选择识别模型', list(options['faster-whisper']['models'].keys()),
                                                  index=options['faster-whisper']['models'][faster_whisper_model])
                    st.write("```推荐使用 large 模型获得最佳断句、识别体验！！！```")
                    st.write(
                        "```若开启GPU请注意：最新版本仅支持 CUDA 12。对于 CUDA 11，当前的解决方法是降级 ctranslate2==3.24.0。```")
                    config["WHISPER"]["faster_whisper_model_local"] = w_local
                    config["WHISPER"]["faster_whisper_model_default"] = w_model_option
                config["WHISPER"]["openai_whisper_api"] = False
            else:
                config["WHISPER"]["openai_whisper_api"] = True
                st.write("请注意API调用必须在下方翻译设置中配置好OPENAI相关设置，否则无法使用！！！")

            with open(config_dir + '/config.toml', 'w', encoding='utf-8') as file:
                toml.dump(config, file)

            st.write('---')
            st.write("#### 翻译设置")
            col1, col2 = st.columns(2, gap="large")
            with col1:
                st.write("")
                item = sac.segmented([
                    sac.SegmentedItem(label='选择你要配置的模型'),
                    sac.SegmentedItem(label='OpenAI-ChatGPT', icon='chat-quote-fill'),
                    sac.SegmentedItem(label='月之暗面-Kimi', icon='chat-quote-fill'),
                    sac.SegmentedItem(label='智谱AI-ChatGLM', icon='chat-quote-fill'),
                    sac.SegmentedItem(label='深度求索-DeepSeek', icon='chat-quote-fill'),
                    sac.SegmentedItem(label='现已支持本地部署调用', icon='robot'),
                    sac.SegmentedItem(label='更多支持?', icon='arrow-up-right-square-fill', href='https://github.com/Chenyme/Chenyme-AAVT/issues'),
                ], index=1, direction='vertical', radius='lg', color='red', bg_color='gray', use_container_width=True, return_index=True)
            with col2:
                area = st.container(height=290)
                if item == 1:
                    new_openai_key = area.text_input("**OPENAI-API-KEY：**", st.session_state.openai_key)
                    new_openai_base = area.text_input("**OPENAI-API-BASE：**", st.session_state.openai_base)
                    area.write('''```官网：https://openai.com/```''')
                    st.session_state.openai_key = new_openai_key
                    st.session_state.openai_base = new_openai_base
                elif item == 2:
                    new_kimi_key = area.text_input("**KIMI-API-KEY：**", st.session_state.kimi_key)
                    area.write('''```欢迎探索月之暗面，寻求将能源转化为智能的最优解。Kimi 是由月之暗面团队的超长记忆 AI 助手。```''')
                    area.write('''```官网：https://www.moonshot.cn/```''')
                    st.session_state.kimi_key = new_kimi_key
                elif item == 3:
                    new_chatglm_key = area.text_input("**CHATGLM-API-KEY：**", st.session_state.chatglm_key)
                    area.write('''```基于领先的千亿级多语言、多模态预训练模型，打造高效率、通用化的“模型即服务”AI开发新范式```''')
                    area.write('''```官网：https://open.bigmodel.cn/```''')
                    st.session_state.chatglm_key = new_chatglm_key
                elif item == 4:
                    new_deepseek_key = area.text_input("**DEEPSEEK-API-KEY：**", st.session_state.deepseek_key)
                    area.write('''```DeepSeek 发布全球最强开源 MoE 模型 DeepSeek-V2，对话官网/API 已全面升级，支持 32K 上下文```''')
                    area.write('''```官网：https://www.deepseek.com/```''')
                    st.session_state.deepseek_key = new_deepseek_key

                if item not in [0, 5]:
                    kimi_key = st.session_state.kimi_key
                    openai_key = st.session_state.openai_key
                    openai_base = st.session_state.openai_base
                    deepseek_key = st.session_state.deepseek_key
                    chatglm_key = st.session_state.chatglm_key

                    area.write("")
                    if area.button('保存', use_container_width=True, type="primary"):
                        config["KIMI"]["kimi_key"] = kimi_key
                        config["GPT"]["openai_base"] = openai_base
                        config["GPT"]["openai_key"] = openai_key
                        config["DEEPSEEK"]["deepseek_key"] = deepseek_key
                        config["CHATGLM"]["chatglm_key"] = chatglm_key
                        with open(config_dir + "/config.toml", 'w', encoding='utf-8') as file:
                            toml.dump(config, file)
                        st.toast("已保存!!!")
                else:
                    with area:
                        sac.buttons([sac.ButtonsItem(icon=sac.BsIcon(name='card-heading', size=50))], align='center',
                                    variant='text', index=None)
                        sac.buttons([sac.ButtonsItem(icon=sac.BsIcon(name='check-square', size=50))], align='center',
                                    variant='text', index=None)
                        sac.buttons([sac.ButtonsItem(icon=sac.BsIcon(name='caret-left-square', size=50))], align='center',
                                    variant='text', index=None)

            st.write('---')

            # 本地缓存
            st.write("#### 本地缓存")
            col1, col2 = st.columns([0.45, 0.55])
            col2.metric(label="大小", value=f"{convert_size(cache(cache_dir))}")

            if st.button("清除缓存", type="primary", use_container_width=True):
                if not os.listdir(cache_dir):
                    st.error("无本地缓存文件。")
                else:
                    for root, dirs, files in os.walk(cache_dir):
                        for file in files:
                            os.remove(os.path.join(root, file))
                        for adir in dirs:
                            shutil.rmtree(os.path.join(root, adir))
                    st.success("所有缓存文件已成功删除。")
