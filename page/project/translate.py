import os
import json
import toml
import datetime
import streamlit as st
from io import StringIO
from styles.global_style import style
import streamlit_antd_components as sac
from utils.public import (parse_srt_file, convert_to_srt, read_srt_file, local_translate_srt, translate_srt,
                          srt_to_sbv, srt_to_vtt, srt_to_ass)

style()
path = os.getcwd() + "/"
llms_path = path + "config/llms.toml"
translate_config_path = path + "config/translate.toml"
prompt_config_path = path + "config/prompt.json"
project_config_path = path + "config/project.toml"
translate_cache_path = path + "cache/translate/"

with open(llms_path, 'r', encoding="utf-8") as config_file:
    llms = toml.load(config_file)
with open(translate_config_path, 'r', encoding="utf-8") as config_file:
    translate_config = toml.load(config_file)
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

translate_index = translate_config["translate"]["translate_index"]
language_index1 = translate_config["translate"]["language_index1"]
language_index2 = translate_config["translate"]["language_index2"]
wait_time_setting = translate_config["translate"]["wait_time"]
prompt_pre_setting = translate_config["translate"]["prompt"]
srt_setting = translate_config["translate"]["srt"]
translate_readme = translate_config["other"]["first"]
system_prompt = prompt[prompt_pre_setting]["system_prompt"].replace("{language1}", language_index1).replace("{language2}", language_index2)
user_prompt = prompt[prompt_pre_setting]["user_prompt"].replace("{language1}", language_index1).replace("{language2}", language_index2)

translation_dict = {
    (0,): '无需翻译',
    (1,): 'Local / 本地模型',
    (2, 3): 'gpt-3.5-turbo',
    (2, 4): 'gpt-4o-mini',
    (2, 5): 'gpt-4',
    (2, 6): 'gpt-4-turbo',
    (2, 7): 'gpt-4o',
    (8, 9): 'claude-3-opus',
    (10, 8): 'claude-3-sonnet',
    (11, 8): 'claude-3-haiku',
    (12, 13): 'gemini-pro',
    (12, 14): 'gemini-1.0-pro',
    (12, 15): 'gemini-1.5-flash',
    (12, 16): 'gemini-1.5-pro',
    (17, 18): 'deepseek-chat',
    (17, 19): 'deepseek-coder',
    (20, 21): 'moonshot-v1-8k',
    (20, 22): 'moonshot-v1-32k',
    (20, 23): 'moonshot-v1-128k',
    (24, 25): 'glm-4',
    (24, 26): 'glm-4-0520',
    (24, 27): 'glm-4-flash',
    (24, 28): 'glm-4-air',
    (24, 29): 'glm-4-airx',
    (30, 31): 'yi-spark',
    (30, 32): 'yi-medium',
    (30, 33): 'yi-medium-200k',
    (30, 34): 'yi-vision',
    (30, 35): 'yi-large',
    (30, 36): 'yi-large-rag',
    (30, 37): 'yi-large-turbo',
    (30, 38): 'yi-large-preview'
}


@st.dialog("使用提示")
def TranslateReadme():
    st.write("""
    ## 欢迎首次使用 SRT字幕翻译 功能！

    为了确保顺利运行并获得最佳体验，请关闭此弹窗后，前往页面中的**参数设置**模块，进行必要的参数配置。根据您的需求调整设置，以提高翻译生成的准确性和效率。

    如果您需要更多帮助，可以参考以下资源：
    - 📘 [相关教程](https://blog.chenyme.top/blog/aavt-install)
    - 📂 [项目地址](https://github.com/Chenyme/Chenyme-AAVT)
    - 💬 [交流群组](https://t.me/+j8SNSwhS7xk1NTc9)

    感谢您的使用，期待为您提供优质的体验！
    """)
    st.write("")
    if st.button("**我已知晓&nbsp;&nbsp;&nbsp;不再弹出**", type="primary", use_container_width=True,
                 key="blog_first_button"):
        with open(translate_config_path, 'w', encoding="utf-8") as f:
            translate_config["other"]["first"] = True
            toml.dump(translate_config, f)
        st.session_state.read = True
        st.rerun()
    st.write("")


if not translate_readme:
    TranslateReadme()
if "save" in st.session_state:
    st.toast("参数已成功保存", icon=":material/verified:")
    del st.session_state["save"]
if "read" in st.session_state:
    st.toast("欢迎使用 ~", icon=":material/verified:")
    del st.session_state["read"]
if "upload" in st.session_state:
    st.toast("文件上传成功！", icon=":material/verified:")
    del st.session_state["upload"]

tab1, tab2 = st.tabs(["**字幕翻译**", "**参数设置**"])
with tab2:
    TranslateSave = st.container()
    TranslateSetting = st.container(border=True)

    with TranslateSetting:
        st.write("")
        st.write("###### 翻译引擎")
        st.caption("翻译模块使用的引擎，请确保您已在全局设置中配置对应的引擎参数！")
        translate_index = sac.cascader(items=[
            sac.CasItem('无需翻译', icon='x-octagon-fill', disabled=True),
            sac.CasItem('Local / 本地模型', icon='house-up-fill'),
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
        ], label='', search=True, index=translate_index, return_index=True)

        st.write("")
        col6, col7 = st.columns(2)
        language = ["简体中文", "繁体中文", "英语", "日语", "泰语", "德语", "法语", "俄语", "韩国语", "越南语", "意大利语", "阿拉伯语", "西班牙语", "孟加拉语", "葡萄牙语", "印地语（北印度语）", ]
        with col6:
            st.write("###### 原始语言")
            st.caption("文件的原始语言")
            language1 = st.selectbox('原始语言', language, index=language.index(language_index1), label_visibility="collapsed")
        with col7:
            st.write("###### 目标语言")
            st.caption("文件的目标语言")
            language2 = st.selectbox('目标语言', language, index=language.index(language_index2), label_visibility="collapsed")
        st.write("")
        srt_choose = ["关闭", "原始语言为首", "目标语言为首"]
        st.write("###### 双语字幕")
        st.caption("选择双语字幕的显示样式")
        srt = st.selectbox('双语字幕', srt_choose, index=srt_choose.index(srt_setting), label_visibility="collapsed")
        st.write("")
        st.write("###### API 调用间隔 / s")
        st.caption(
            "翻译时API的调用间隔。请参阅您的API服务商文档中的 每分钟调用最大限制速率 进行适当调整，若翻译时遇到报错 429：`Too Many Requests`、`RateLimitError` 请适当增大间隔。")
        wait_time = st.number_input('翻译间隔(s)', min_value=0.0, max_value=5.0, value=wait_time_setting, step=0.1, label_visibility="collapsed")
        st.write("")
        st.write("###### 翻译提示词")
        st.caption("翻译使用的提示词，可前往全局设置-翻译设置中配置新的提示词")
        try:
            prompt_pre_setting = st.selectbox('预设prompt', prompt.keys(), index=list(prompt.keys()).index(prompt_pre_setting), label_visibility="collapsed")
        except:
            prompt_pre_setting = st.selectbox('预设prompt', prompt.keys(), label_visibility="collapsed")
        system_prompt = prompt[prompt_pre_setting]["system_prompt"].replace("{language1}", language1).replace("{language2}", language2)
        user_prompt = prompt[prompt_pre_setting]["user_prompt"].replace("{language1}", language1).replace("{language2}", language2)
        st.write("")

    with TranslateSave:
        col1, col2 = st.columns([0.75, 0.25])
        st.write("")
        with col2:
            st.write("")
            st.write("")
            if st.button("**保存更改**", type="primary", use_container_width=True):
                with open(translate_config_path, 'w', encoding='utf-8') as file:
                    translate_config["translate"]["translate_index"] = translate_index
                    translate_config["translate"]["language_index1"] = language1
                    translate_config["translate"]["language_index2"] = language2
                    translate_config["translate"]["wait_time"] = wait_time
                    translate_config["translate"]["srt"] = srt
                    translate_config["translate"]["prompt"] = prompt_pre_setting
                    translate_config["translate"]["language_index1"] = language1
                    toml.dump(translate_config, file)
                st.session_state.save = True
                st.rerun()
        with col1:
            st.write("")
            st.write("")
            st.write("### 更改参数设置")
            st.caption("Changing Parameter Settings")

with tab1:
    col1, col2 = st.columns([0.75, 0.25])  # 置顶标题、执行按钮流程模块

    # 标题模块
    with col1:
        st.write("")
        st.write("")
        st.subheader("AI SRT 字幕翻译")
        st.caption("AI SRT Subtitle Translation")

    # 执行按钮流程模块
    with col2:
        st.write("")
        st.write("")
        if st.button("**开始翻译**", type="primary", use_container_width=True):
            if "uploaded_file_translate" in st.session_state:
                uploaded_file = st.session_state.uploaded_file_translate
                print("\n" + "=" * 50)
                print("\n\033[1;39m*** Chenyme-AAVT AI字幕翻译 ***\033[0m")
                st.toast('任务开始执行！请勿在运行时切换菜单或修改参数!', icon=":material/rocket_launch:")

                msg_ved = st.toast('正在对字幕进行预处理', icon=":material/video_settings:")
                st.session_state.srt_name = "uploaded.srt"
                current_time = datetime.datetime.now().strftime("_%Y%m%d%H%M%S")
                st.session_state.audio_name_original = uploaded_file.name.split('.')[0]
                output_file = translate_cache_path + st.session_state.audio_name_original + current_time
                os.makedirs(output_file)
                with open(f"{output_file}/{st.session_state.srt_name}", "wb") as file:
                    file.write(uploaded_file.getbuffer())
                msg_ved.toast("字幕预处理完成", icon=":material/video_settings:")

                print("\n\033[1;34m🚀 任务开始执行\033[0m")
                print(f"\033[1;34m📂 本次任务目录:\033[0m\033[1;34m {output_file} \033[0m")
                print("\033[1;33m⚠️ 请不要在任务运行期间切换菜单或修改参数！\033[0m")

                srt_content = read_srt_file(output_file + '/' + st.session_state.srt_name)
                translate_option = translation_dict[tuple(translate_index)]

                msg_tra = st.toast("正在翻译字幕", icon=":material/translate:")
                if '本地模型' in translate_option:
                    result = local_translate_srt(system_prompt, user_prompt, local_key, local_url, local_model, srt_content, srt_setting)
                elif 'gemini' in translate_option:
                    result = translate_srt(system_prompt, user_prompt, gemini_key, gemini_url, translate_option, srt_content, wait_time_setting, srt_setting)
                elif 'yi' in translate_option:
                    result = translate_srt(system_prompt, user_prompt, ai01_key, ai01_url, translate_option, srt_content, wait_time_setting, srt_setting)
                elif 'gpt' in translate_option:
                    result = translate_srt(system_prompt, user_prompt, chatgpt_key, chatgpt_url, translate_option, srt_content, wait_time_setting, srt_setting)
                elif 'moonshot' in translate_option:
                    result = translate_srt(system_prompt, user_prompt, kimi_key, kimi_base, translate_option, srt_content, wait_time_setting, srt_setting)
                elif 'glm' in translate_option:
                    result = translate_srt(system_prompt, user_prompt, chatglm_key, chatglm_url, translate_option, srt_content, wait_time_setting, srt_setting)
                elif 'deepseek' in translate_option:
                    result = translate_srt(system_prompt, user_prompt, deepseek_key, deepseek_url, translate_option, srt_content, wait_time_setting, srt_setting)
                elif 'claude' in translate_option:
                    result = translate_srt(system_prompt, user_prompt, claude_key, chatglm_url, translate_option, srt_content, wait_time_setting, srt_setting)
                print("\033[1;34m🎉 字幕翻译已完成！\033[0m")
                msg_tra.toast("翻译任务结束！", icon=":material/translate:")

                srt_content = ""
                for i, subtitle in enumerate(result, start=1):
                    srt_content += f"{i}\n"
                    srt_content += f"{subtitle['time']}\n"
                    srt_content += subtitle['text'].replace('\n', '\n') + "\n\n"
                st.session_state.path = output_file
                st.session_state.srt_content_translate = srt_content

                with open(st.session_state.path + '/translate.srt', 'w', encoding='utf-8') as file:
                    file.write(srt_content)
                print("\n\033[1;34m🎉 任务成功结束！\033[0m")
                print("\n" + "=" * 50 + "\n")
                st.toast("翻译任务结束！", icon=":material/verified:")
            else:
                st.toast("请先在工具栏中上传SRT文件！", icon=":material/release_alert:")

    st.write("")
    col3, col4 = st.columns([0.75, 0.25])
    with col4:
        with st.expander("**Tool / 工具**", expanded=True, icon=":material/construction:"):
            st.caption("上传文件")


            @st.dialog("上传SRT文件")
            def upload_SRT():
                st.write("")
                st.write("在这里上传您需要处理的SRT文件。")
                st.write(
                    "请注意，除关闭 CMD 外，执行任务后无法取消任务！请勿在执行时点击任何 项目按钮 或 切换菜单，以免导致识别报错！")
                st.write("")
                uploaded_file_translate = st.file_uploader("上传您的音频文件", type=["srt"], label_visibility="collapsed")
                st.write("")
                if st.button("**点击上传**", use_container_width=True, type="primary"):
                    st.session_state.uploaded_file_translate = uploaded_file_translate
                    st.session_state.upload = True
                    st.rerun()
                st.write("")


            if st.button('**文件上传**', use_container_width=True, type="primary", key="upload_audio_button"):
                upload_SRT()

            st.caption("字幕工具")
            if st.button('**保存修改**', type="primary", use_container_width=True):
                try:
                    with open(st.session_state.path + '/translate.srt', 'w', encoding='utf-8') as file:
                        file.write(st.session_state.srt_translate)
                    st.toast("已成功保存", icon=":material/task_alt:")
                except:
                    st.toast("未检测到运行后的字幕文件", icon=":material/error:")

            if st.button('**打开目录**', type="primary", use_container_width=True):
                try:
                    os.startfile(st.session_state.path)
                    st.toast("注意：文件夹已成功打开，可能未置顶显示，请检查任务栏！", icon=":material/task_alt:")
                except:
                    st.toast("未进行识别，目录尚未生成！", icon=":material/error:")

            st.divider()
            if st.toggle("**更多功能**"):
                st.caption("字幕轴高度")
                height = st.number_input("显示", min_value=300, step=100, value=530, label_visibility="collapsed")
                st.session_state.height_srt = height
                st.caption("更多字幕格式")
                try:
                    captions_option = st.radio('更多字幕格式导出', ('VTT', 'ASS', 'SBV'), index=0,
                                               label_visibility="collapsed")
                    if captions_option == 'VTT':
                        vtt_content = srt_to_vtt(st.session_state.srt_translate)
                        st.download_button(
                            label="**VTT 下载**",
                            data=vtt_content.encode('utf-8'),
                            key='vtt_download',
                            file_name='output.vtt',
                            mime='text/vtt',
                            use_container_width=True,
                            type="primary"
                        )
                    elif captions_option == 'ASS':
                        sbv_content = srt_to_ass(st.session_state.srt_translate, "Arial", "18", "#FFFFFF")
                        st.download_button(
                            label="**ASS 下载**",
                            data=sbv_content.encode('utf-8'),
                            key='ass_download',
                            file_name='output.ass',
                            mime='text/ass',
                            use_container_width=True,
                            type="primary"
                        )
                    elif captions_option == 'SBV':
                        sbv_content = srt_to_sbv(st.session_state.srt_translate)
                        st.download_button(
                            label="**SBV 下载**",
                            data=sbv_content.encode('utf-8'),
                            key='sbv_download',
                            file_name='output.sbv',
                            mime='text/sbv',
                            use_container_width=True,
                            type="primary"
                        )
                except:
                    if st.button('**下载字幕**', use_container_width=True, type="primary"):
                        st.toast("未检测到字幕生成！", icon=":material/error:")
            if "height_srt" not in st.session_state:
                st.session_state.height_srt = 530

        with col3:
            with st.expander("**Subtitle Preview / 字幕预览**", expanded=True, icon=":material/subtitles:"):
                try:
                    st.caption("字幕时间轴")
                    srt_data1 = parse_srt_file(st.session_state.srt_content_translate, srt_setting)
                    edited_data = st.data_editor(srt_data1, height=st.session_state.height_srt, hide_index=True, use_container_width=True)
                    srt_data2 = convert_to_srt(edited_data, srt_setting)
                    st.session_state.srt_translate = srt_data2
                    st.write("")
                except:
                    try:
                        uploaded_file = st.session_state.uploaded_file_translate
                        stringio = StringIO(uploaded_file.getvalue().decode("utf-8")).read()
                        srt_data1 = parse_srt_file(stringio, srt_setting="关闭")
                        edited_data = st.data_editor(srt_data1, height=st.session_state.height_srt, hide_index=True, use_container_width=True)
                        srt_data2 = convert_to_srt(edited_data, srt_setting="关闭")
                        st.session_state.srt_translate = srt_data2
                        st.write("")
                    except:
                        st.info("##### 结果预览区域 \n\n&nbsp;\n\n **生成完毕后会在此区域自动显示字幕时间轴** \n\n 运行前，请在右侧使用上传文件工具导入你的音频文件！\n\n&nbsp;\n\n&nbsp;", icon=":material/view_in_ar:")
                        st.write("")
