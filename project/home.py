import os
import time
import toml
import json
import pandas as pd
import shutil
import streamlit as st
import streamlit_antd_components as sac
from project.utils.utils2 import cache, convert_size, get_folders_info, get_info


@st.dialog('新增提示词')
def add(config_dir):
    name = st.text_input('提示词名称')
    system = st.text_area('新的系统提示词', height=100)
    user = st.text_area('新的用户提示词', height=100)
    if st.button("保存提示词", use_container_width=True):
        new = {
            name:
                {
                    "system_prompt": system,
                    "user_prompt": user
                }
        }
        st.session_state.prompt.update(new)
        new_prompt = json.dumps(st.session_state.prompt, indent=2)
        with open(config_dir + '/prompt.json', 'w', encoding='utf-8') as json_file:
            json_file.write(new_prompt)
        st.rerun()


@st.dialog('在这里上传或拖入')
def upload(config_dir):
    file = st.file_uploader("上传", label_visibility="collapsed")
    if file is not None:
        if file.name == "prompt.json":
            a = file.getvalue().decode("utf-8")
            with open(config_dir + '/prompt.json', 'w', encoding='utf-8') as json_file:
                json_file.write(a)
            st.success("导入成功！", icon=":material/task_alt:")
            time.sleep(0.5)
            st.success("即将自动刷新界面！", icon=":material/task_alt:")
            time.sleep(1.5)
            st.rerun()
        else:
            st.error("请上传`prompt.json`命名的json文件", icon=":material/error:")


# 主页面
def home():
    st.subheader("🖥Chenyme-AAVT V0.8.5")
    st.caption("POWERED BY @CHENYME")

    with st.sidebar:
        st.write("[![](https://img.shields.io/badge/Telegram-点我加入交流群-blue.svg?logo=data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAyNCAyNCI+PHBhdGggZD0iTTEyIDI0YzYuNjI3IDAgMTItNS4zNzMgMTItMTJTMTguNjI3IDAgMTIgMCAwIDUuMzczIDAgMTJzNS4zNzMgMTIgMTIgMTJaIiBmaWxsPSJ1cmwoI2EpIi8+PHBhdGggZmlsbC1ydWxlPSJldmVub2RkIiBjbGlwLXJ1bGU9ImV2ZW5vZGQiIGQ9Ik01LjQyNSAxMS44NzFhNzk2LjQxNCA3OTYuNDE0IDAgMCAxIDYuOTk0LTMuMDE4YzMuMzI4LTEuMzg4IDQuMDI3LTEuNjI4IDQuNDc3LTEuNjM4LjEgMCAuMzIuMDIuNDcuMTQuMTIuMS4xNS4yMy4xNy4zMy4wMi4xLjA0LjMxLjAyLjQ3LS4xOCAxLjg5OC0uOTYgNi41MDQtMS4zNiA4LjYyMi0uMTcuOS0uNSAxLjE5OS0uODE5IDEuMjI5LS43LjA2LTEuMjI5LS40Ni0xLjg5OC0uOS0xLjA2LS42ODktMS42NDktMS4xMTktMi42NzgtMS43OTgtMS4xOS0uNzgtLjQyLTEuMjA5LjI2LTEuOTA4LjE4LS4xOCAzLjI0Ny0yLjk3OCAzLjMwNy0zLjIyOC4wMS0uMDMuMDEtLjE1LS4wNi0uMjEtLjA3LS4wNi0uMTctLjA0LS4yNS0uMDItLjExLjAyLTEuNzg4IDEuMTQtNS4wNTYgMy4zNDgtLjQ4LjMzLS45MDkuNDktMS4yOTkuNDgtLjQzLS4wMS0xLjI0OC0uMjQtMS44NjgtLjQ0LS43NS0uMjQtMS4zNDktLjM3LTEuMjk5LS43OS4wMy0uMjIuMzMtLjQ0Ljg5LS42NjlaIiBmaWxsPSIjZmZmIi8+PGRlZnM+PGxpbmVhckdyYWRpZW50IGlkPSJhIiB4MT0iMTEuOTkiIHkxPSIwIiB4Mj0iMTEuOTkiIHkyPSIyMy44MSIgZ3JhZGllbnRVbml0cz0idXNlclNwYWNlT25Vc2UiPjxzdG9wIHN0b3AtY29sb3I9IiMyQUFCRUUiLz48c3RvcCBvZmZzZXQ9IjEiIHN0b3AtY29sb3I9IiMyMjlFRDkiLz48L2xpbmVhckdyYWRpZW50PjwvZGVmcz48L3N2Zz4K)](https://t.me/+j8SNSwhS7xk1NTc9)")
        st.write("![GitHub Repo stars](https://img.shields.io/github/stars/chenyme/chenyme-aavt)")
        st.write("#### [项目文档](https://zwho5v3j233.feishu.cn/wiki/OGcrwinzhi88MkkvEMVcLkDgnzc?from=from_copylink) | [常见问题](https://zwho5v3j233.feishu.cn/wiki/C7akw4w44iFEEPky8fScjqFWnbf?from=from_copylink)")
    project_dir = os.path.dirname(os.path.abspath(__file__)).replace("\\", "/")
    config_dir = project_dir + "/config/"  # 配置文件
    cache_dir = project_dir + "/cache/"  # 本地缓存1
    avtb_dir = project_dir + "/AVTB/output/"  # 本地缓存2
    avg_dir = project_dir + "/AVG/output/"
    doc_dir = project_dir + "/doc/"  # 知识库

    with open(doc_dir + "readme.md", 'r', encoding='utf-8') as file:
        doc = file.read()

    select = sac.tabs([
        sac.TabsItem(label='说明', icon='robot'),
        sac.TabsItem(label='设置', icon='gear')
    ], align='center', variant='outline', use_container_width=True, index=0)

    if select == "说明":
        st.markdown("""
        #### 项目使用说明

        1. 本项目为开源项目，仅供学习交流使用，不得用于商业用途。
        2. 请勿将本项目用于违法用途，否则后果自负。
        3. 项目使用过程中遇到问题，可加入[Telegram交流群](https://t.me/+j8SNSwhS7xk1NTc9)进行交流。
        4. 本项目可以魔改，但请保留原作者信息，请勿将源码收费卖出！

        #### 项目使用方式

        项目总体分为：识别 + 翻译 + 合并 三个步骤

        1. **关于识别：** 识别前请先配置好对应的参数，识别有两种方式，一种是 OpenAI API 接口调用，一种是 Faster Whisper 本地调用，个人推荐使用 Faster-Whisper + 本地模型调用，可以避免文件大小限制、模型下载慢等诸多问题。

        2. **关于翻译：** 翻译前请先在 主页-设置-翻译模型设置 中配置好对应的参数，翻译有多种模型可供选择，包括 GEMINI、CHATGLM、KIMI、AI01、OPENAI、CLAUDE、DEEPSEEK、LOCAL，个人推荐使用 LOCAL 本地调用，可以避免并发限制、Token花费等诸多问题。

        3. **关于合并：** 合并前请先确认FFmpeg是否正确安装并配置环境，否则可能会出现合并失败的情况。
        
        请确认以上步骤配置正确后再开始识别！！！
        
        ps：由于小助手内置Key过期了，因此删去了助手服务，请自行阅读以上说明进行配置！

        """)

    if select == "设置":
        config = toml.load(config_dir + "api.toml")  # 加载配置
        gemini_key = config["GEMINI"]["gemini_key"]  # GEMINI
        gemini_base = config["GEMINI"]["gemini_base"]
        ai01_key = config["AI01"]["AI01_key"]  # 01
        ai01_base = config["AI01"]["AI01_base"]
        kimi_key = config["KIMI"]["kimi_key"]  # kimi
        kimi_base = config["KIMI"]["kimi_base"]
        chatglm_key = config["CHATGLM"]["chatglm_key"]  # chatglm
        chatglm_base = config["CHATGLM"]["chatglm_base"]
        openai_key = config["GPT"]["openai_key"]  # openai
        openai_base = config["GPT"]["openai_base"]
        claude_key = config["CLAUDE"]["claude_key"]  # claude
        claude_base = config["CLAUDE"]["claude_base"]
        deepseek_key = config["DEEPSEEK"]["deepseek_key"]  # deepseek
        deepseek_base = config["DEEPSEEK"]["deepseek_base"]
        local_key = config["LOCAL"]["api_key"]  # local
        local_base = config["LOCAL"]["base_url"]
        local_model = config["LOCAL"]["model_name"]

        with open(config_dir + 'prompt.json', 'r', encoding='utf-8') as file:
            prompt = json.load(file)  # 加载配置
        st.session_state.prompt = prompt

        st.write("##### 模型配置")
        col1, col2 = st.columns(2, gap="medium")
        with col1:
            with st.container(border=True):
                st.write("#### LOCAL 本地)")
                st.write("调用您在本地部署的模型，可以避免并发限制、Token花费等诸多问题。<PS：若不用本地模型，也可当作自定义接口>")
                if st.button("**修改设置**", key="local_toggle"):
                    @st.dialog('LOCAL 本地调用')
                    def local_setting(local_base, local_key, local_model):
                        st.divider()
                        st.write("**配置正确后，将支持调用您在本地部署的模型，本地部署的模型可以避免网络限制、并发过高、Token花费等诸多问题，推荐使用此方式进行翻译！**")
                        st.write("")
                        local_base = st.text_input("**您的API地址**", local_base, key="local_base", placeholder="您的本地模型调用接口")
                        local_key = st.text_input("**您的API密钥**", local_key, key="local_key", placeholder="您的本地模型调用密钥，若不需要此参数，请留空！")
                        local_model = st.text_input("**您的模型名称**", local_model, key="local_model", placeholder="您的本地模型调用名称")
                        st.write("")
                        if st.button("**保存配置**", use_container_width=True, key="local_button"):
                            with open(config_dir + 'api.toml', 'w', encoding='utf-8') as file:
                                config["LOCAL"]["api_key"] = local_key
                                config["LOCAL"]["base_url"] = local_base
                                config["LOCAL"]["model_name"] = local_model
                                toml.dump(config, file)
                            st.write("")
                            st.success("**保存成功！**", icon=":material/check:")
                    local_setting(local_base, local_key, local_model)
            st.write("")

            with st.container(border=True):
                st.write("#### DEEPSEEK 深度求索")
                st.write("DeepSeek是一家专注于研究世界领先的通用人工智能底层模型与技术的公司。")
                if st.button("**修改设置**", key="deepseek_toggle"):
                    @st.dialog('DEEPSEEK 深度求索')
                    def deepseek_setting(deepseek_base, deepseek_key):
                        st.divider()
                        st.write("**DeepSeek是一家专注于研究世界领先的通用人工智能底层模型与技术的公司，此模型服务的并发量很高，个人比较推荐使用！**")
                        st.write("")
                        deepseek_base = st.text_input("**您的API地址**", deepseek_base, placeholder="DeepSeek API 接口地址")
                        deepseek_key = st.text_input("**您的API密钥**", deepseek_key, placeholder="您的 DeepSeek API 密钥")
                        st.write("")
                        if st.button("**保存配置**", use_container_width=True, key="deepseek_button"):
                            config = toml.load(config_dir + 'api.toml')
                            with open(config_dir + 'api.toml', 'w', encoding='utf-8') as file:
                                config["DEEPSEEK"]["deepseek_base"] = deepseek_base
                                config["DEEPSEEK"]["deepseek_key"] = deepseek_key
                                toml.dump(config, file)
                            st.write("")
                            st.success("**保存成功！**", icon=":material/check:")
                    deepseek_setting(deepseek_base, deepseek_key)
            st.write("")

            with st.container(border=True):
                st.write("#### GEMINI 谷歌")
                st.write("Gemini 人工智能模型 于2023年12月6日 发布，是谷歌迄今为止最强大、最通用的模型。")
                if st.button("**修改设置**", key="gemini_toggle"):
                    @st.dialog('GEMINI 谷歌')
                    def gemini_setting(gemini_base, gemini_key):
                        st.divider()
                        st.write("**Gemini是一款由 Google DeepMind 于2023年12月6日发布的人工智能模型。Gemini 是谷歌迄今为止最强大、最通用的模型，它在许多领先的基准测试中都展现出了先进的性能。**")
                        st.write("")
                        gemini_base = st.text_input("**您的API地址**", gemini_base, placeholder="Gemini API 接口地址")
                        gemini_key = st.text_input("**您的API密钥**", gemini_key, placeholder="您的 Gemini API 密钥")
                        st.write("")
                        if st.button("**保存配置**", use_container_width=True, key="gemini_button"):
                            with open(config_dir + 'api.toml', 'w', encoding='utf-8') as file:
                                config["GEMINI"]["gemini_base"] = gemini_base
                                config["GEMINI"]["gemini_key"] = gemini_key
                                toml.dump(config, file)
                            st.write("")
                            st.success("**保存成功！**", icon=":material/check:")
                    gemini_setting(gemini_base, gemini_key)
            st.write("")

            with st.container(border=True):
                st.write("#### CHATGLM 智谱清言")
                st.write("ChatGLM 是基于GLM预训练框架的双语对话模型，针对中文问答和对话进行了优化。")
                if st.button("**修改设置**", key="chatglm_toggle"):
                    @st.dialog('CHATGLM 智谱清言')
                    def chatglm_setting(chatglm_base, chatglm_key):
                        st.divider()
                        st.write("**ChatGLM是基于GLM预训练框架的双语对话模型，针对中文问答和对话进行了优化。**")
                        st.write("")
                        chatglm_base = st.text_input("**您的API地址**", chatglm_base, placeholder="ChatGLM API 接口地址")
                        chatglm_key = st.text_input("**您的API密钥**", chatglm_key, placeholder="您的 ChatGLM API 密钥")
                        st.write("")
                        if st.button("**保存配置**", use_container_width=True, key="chatglm_button"):
                            with open(config_dir + 'api.toml', 'w', encoding='utf-8') as file:
                                config["CHATGLM"]["chatglm_base"] = chatglm_base
                                config["CHATGLM"]["chatglm_key"] = chatglm_key
                                toml.dump(config, file)
                            st.write("")
                            st.success("**保存成功！**", icon=":material/check:")
                    chatglm_setting(chatglm_base, chatglm_key)
            st.write("")

        with col2:
            with st.container(border=True):
                st.write("#### ChatGPT OPENAI")
                st.write("OpenAI 是一家开放人工智能研究和部署公司，其使命是用人工智能造福全人类。")
                if st.button("**修改设置**", key="openai_toggle"):
                    @st.dialog('ChatGPT OPENAI')
                    def openai_setting(openai_base, openai_key):
                        st.divider()
                        st.write("**OpenAI 是一家开放人工智能研究和部署公司，其使命是用人工智能造福全人类。**")
                        st.write("")
                        openai_base = st.text_input("**您的API地址**", openai_base, placeholder="OpenAI API 接口地址")
                        openai_key = st.text_input("**您的API密钥**", openai_key, placeholder="您的 OpenAI API 密钥")
                        st.write("")
                        if st.button("**保存配置**", use_container_width=True, key="openai_button"):
                            with open(config_dir + 'api.toml', 'w', encoding='utf-8') as file:
                                config["GPT"]["openai_base"] = openai_base
                                config["GPT"]["openai_key"] = openai_key
                                toml.dump(config, file)
                            st.write("")
                            st.success("**保存成功！**", icon=":material/check:")
                    openai_setting(openai_base, openai_key)
            st.write("")

            with st.container(border=True):
                st.write("#### CLAUDE Anthropic")
                st.write("Claude 是由 Anthropic 开发的大型语言模型，旨在革新您与 AI 交互的方式。")
                if st.button("**修改设置**", key="claude_toggle"):
                    @st.dialog('CLAUDE Anthropic')
                    def claude_setting(claude_base, claude_key):
                        st.divider()
                        st.write("**Claude 是由 Anthropic 开发的大型语言模型，旨在革新您与 AI 交互的方式。**")
                        st.write("")
                        claude_base = st.text_input("**您的API地址**", claude_base, placeholder="Claude API 接口地址")
                        claude_key = st.text_input("**您的API密钥**", claude_key, placeholder="您的 Claude API 密钥")
                        st.write("")
                        if st.button("**保存配置**", use_container_width=True, key="claude_button"):
                            with open(config_dir + 'api.toml', 'w', encoding='utf-8') as file:
                                config["CLAUDE"]["claude_base"] = claude_base
                                config["CLAUDE"]["claude_key"] = claude_key
                                toml.dump(config, file)
                            st.write("")
                            st.success("**保存成功！**", icon=":material/check:")
                    claude_setting(claude_base, claude_key)
            st.write("")

            with st.container(border=True):
                st.write("#### KIMI 月之暗面")
                st.write("月之暗面致力于寻求将能源转化为智能的最优解，通过产品与用户共创智能。")
                if st.button("**修改设置**", key="kimi_toggle"):
                    @st.dialog('KIMI 月之暗面')
                    def kimi_setting(kimi_base, kimi_key):
                        st.divider()
                        st.write("**月之暗面（Moonshot AI ) 创立于2023年3月，是一家国内通用人工智能领域的创业公司。月之暗面致力于寻求将能源转化为智能的最优解，通过产品与用户共创智能。Kimi 是一个的AI 智能问答助手,文案写作、信息搜索、速读长文样样精通。**")
                        st.write("")
                        kimi_base = st.text_input("**您的API地址**", kimi_base, placeholder="Kimi API 接口地址")
                        kimi_key = st.text_input("**您的API密钥**", kimi_key, placeholder="您的 Kimi API 密钥")
                        st.write("")
                        if st.button("**保存配置**", use_container_width=True, key="kimi_button"):
                            with open(config_dir + 'api.toml', 'w', encoding='utf-8') as file:
                                config["KIMI"]["kimi_base"] = kimi_base
                                config["KIMI"]["kimi_key"] = kimi_key
                                toml.dump(config, file)
                            st.write("")
                            st.success("**保存成功！**", icon=":material/check:")
                    kimi_setting(kimi_base, kimi_key)
            st.write("")

            with st.container(border=True):
                st.write("#### AI01 零一万物")
                st.write("零一万物是一家秉持着坚定的技术愿景和人工智能信仰，致力于打造 AI 2.0 的创新企业。")
                if st.button("**修改设置**", key="ai01_toggle"):
                    @st.dialog('AI01 零一万物')
                    def ai01_setting(ai01_base, ai01_key):
                        st.divider()
                        st.write("**零一万物是一家秉持着坚定的技术愿景和人工智能信仰，致力于打造 AI 2.0 的创新企业。AI 应当以人为本，Human + AI 将合作创造巨大的经济价值及社会价值。**")
                        st.write("")
                        ai01_base = st.text_input("**您的API地址**", ai01_base, placeholder="AI01 API 接口地址")
                        ai01_key = st.text_input("**您的API密钥**", ai01_key, placeholder="您的 AI01 API 密钥")
                        st.write("")
                        if st.button("**保存配置**", use_container_width=True, key="ai01_button"):
                            with open(config_dir + 'api.toml', 'w', encoding='utf-8') as file:
                                config["AI01"]["AI01_base"] = ai01_base
                                config["AI01"]["AI01_key"] = ai01_key
                                toml.dump(config, file)
                            st.write("")
                            st.success("**保存成功！**", icon=":material/check:")
                    ai01_setting(ai01_base, ai01_key)

        st.write("")
        sac.divider(label='预置提示词', icon='terminal', align='center', color='gray')
        st.write("##### 预置提示词（BETA）")
        st.write("")

        sac.alert(
            label='**修改请遵循修改规则**',
            description='**注意：**`{language1}`和`{language2}`分别对应**原始语言**和**目标语言**,你可以在提示词中使用该参数',
            size='lg', radius=20, icon=True, closable=True, color='warning')

        st.write("")
        df = pd.DataFrame([(k, v['system_prompt'], v['user_prompt']) for k, v in prompt.items()], columns=['Prompt', 'system_prompt', 'user_prompt'])
        df2 = st.data_editor(df, hide_index=True, use_container_width=True, height=300, num_rows="dynamic")
        json_result = df2.set_index('Prompt').to_json(orient='index')
        prompt_json = json.dumps(json.loads(json_result), indent=4)

        st.write("")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            if st.button("**保存修改**", use_container_width=True):
                with open(config_dir + '/prompt.json', 'w', encoding='utf-8') as json_file:
                    json_file.write(prompt_json)
        with col2:
            if st.download_button(
                label="**下载提示词**",
                data=prompt_json,
                file_name="prompt.json",
                mime="text/json",
                use_container_width=True,
            ):
                with open(config_dir + '/prompt.json', 'w', encoding='utf-8') as json_file:
                    json_file.write(prompt_json)
        with col3:
            if st.button("**新建提示词**", use_container_width=True):
                add(config_dir)
        with col4:
            if st.button("**导入提示词**", use_container_width=True):
                upload(config_dir)

        st.write("")
        sac.divider(label='缓存识别', icon='file-earmark-binary', align='center', color='gray')
        st.write("##### 本地缓存")
        st.write("")

        col1, col2, col3 = st.columns(3)
        with col1:

            st.metric(label="**媒体识别：**", value=f"{convert_size(cache(cache_dir))}")
            folders_df = get_folders_info(cache_dir)
            st.dataframe(folders_df, hide_index=True, height=200, use_container_width=True)
            st.write("")
            if st.button("**清除所有识别文件**", help="注意：所有项目中的生成文件均会被删除", use_container_width=True):
                if not os.listdir(cache_dir):
                    st.toast("未检测到文件", icon=":material/error:")
                else:
                    for root, dirs, files in os.walk(cache_dir):
                        for file in files:
                            os.remove(os.path.join(root, file))
                        for adir in dirs:
                            shutil.rmtree(os.path.join(root, adir))
                    st.toast("已全部删除", icon=":material/task_alt:")
        with col2:
            st.metric(label="**图文博客：**", value=f"{convert_size(cache(avtb_dir))}")
            folders_df = get_folders_info(avtb_dir)
            st.dataframe(folders_df, hide_index=True, height=200, use_container_width=True)
            st.write("")
            if st.button("**清除所有图文生成**", help="注意：所有项目中的生成文件均会被删除", use_container_width=True):
                if not os.listdir(avtb_dir):
                    st.toast("未检测到文件", icon=":material/error:")
                else:
                    for root, dirs, files in os.walk(avtb_dir):
                        for file in files:
                            os.remove(os.path.join(root, file))
                        for adir in dirs:
                            shutil.rmtree(os.path.join(root, adir))
                    st.toast("已全部删除", icon=":material/task_alt:")
        with col3:
            st.metric(label="**人声模拟：**", value=f"{convert_size(cache(avg_dir))}")
            folders_df = get_info(avg_dir)
            st.dataframe(folders_df, hide_index=True, height=200, use_container_width=True)
            st.write("")
            if st.button("**清除所有人声生成**", help="注意：所有项目中的生成文件均会被删除", use_container_width=True):
                if not os.listdir(avg_dir):
                    st.toast("未检测到文件", icon=":material/error:")
                else:
                    for root, dirs, files in os.walk(avg_dir):
                        for file in files:
                            os.remove(os.path.join(root, file))
                        for adir in dirs:
                            shutil.rmtree(os.path.join(root, adir))
                    st.toast("已全部删除", icon=":material/task_alt:")

        st.write("")
        sac.divider(label='项目修复', icon='wrench-adjustable', align='center', color='gray')
        st.write("##### 闪退修复")
        st.write("")

        sac.alert(
            label='**如果运行时闪退可使用该服务尝试修复**',
            description='若非`install.bat`安装，该功能可能不适用',
            size='lg', radius=20, icon=True, closable=True, color='warning')
        if st.button("⚙️执行修复", type="primary", use_container_width=True):
            envs_dir = project_dir.replace("project", "") + "/env/Library/bin/libiomp5md.dll"
            if os.path.exists(envs_dir):
                try:
                    os.remove(envs_dir)
                    sac.alert(
                        label='已修复！',
                        size='lg', radius=20, icon=True, closable=True, color='success')
                except:
                    sac.alert(
                        label=f'文件被拒绝访问！请关闭项目，前往 {envs_dir} 手动卸载！',
                        size='lg', radius=20, icon=True, closable=True, color='error')
            else:
                sac.alert(
                    label='**未找到指定目录，或者目录已经删除**',
                    description='如果您是自行安装的环境，请前往环境目录删除多余libiomp5md.dll',
                    size='lg', radius=20, icon=True, closable=True, color='warning')

        st.write("")
        sac.divider(label='POWERED BY @CHENYME', icon="lightning-charge", align='center', color='gray', key="5")
