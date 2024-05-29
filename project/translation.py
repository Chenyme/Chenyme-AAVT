import os
import toml
import datetime
from openai import OpenAI
import streamlit as st
import streamlit_antd_components as sac
from project.utils.utils2 import read_srt_file, parse_srt_file, convert_to_srt, translate_srt, local_translate_srt


def translation():
    project_dir = os.path.dirname(os.path.abspath(__file__)).replace("\\", "/")
    config_dir = project_dir + "/config/"  # 配置文件
    cache_dir = project_dir + "/cache/"  # 本地缓存

    api_config = toml.load(config_dir + "api.toml")  # 加载API配置
    openai_key = api_config["GPT"]["openai_key"]
    openai_base = api_config["GPT"]["openai_base"]
    kimi_key = api_config["KIMI"]["kimi_key"]
    kimi_base = api_config["KIMI"]["kimi_base"]
    deepseek_key = api_config["DEEPSEEK"]["deepseek_key"]
    deepseek_base = api_config["DEEPSEEK"]["deepseek_base"]
    chatglm_key = api_config["CHATGLM"]["chatglm_key"]
    chatglm_base = api_config["CHATGLM"]["chatglm_base"]
    local_key = api_config["LOCAL"]["api_key"]
    local_base = api_config["LOCAL"]["base_url"]
    local_model = api_config["LOCAL"]["model_name"]

    translate_config = toml.load(config_dir + "translate.toml")  # 加载API配置
    language1_setting = translate_config["TRANSLATE"]["language1"]
    language2_setting = translate_config["TRANSLATE"]["language2"]
    wait_time_setting = translate_config["TRANSLATE"]["wait_time"]

    st.subheader("AI SRT字幕翻译")
    st.caption("AI SRT subtitle translation")
    sac.divider(label='POWERED BY @CHENYME', icon="lightning-charge", align='center', color='gray', key="1")

    with st.sidebar:
        uploaded_file = st.file_uploader("上传您的SRT文件", type=["srt"])

    col1, col2 = st.columns([0.75, 0.25])
    with col2:
        with st.expander("模型选择", expanded=True):
            sac.divider(label='Choose', icon='activity', align='center', color='gray', key="a")

            translate_option = sac.chip(
                items=[
                    sac.ChipItem('gpt-3.5-turbo', icon='robot'),
                    sac.ChipItem('gpt-4-turbo', icon='robot'),
                    sac.ChipItem('gpt-4o', icon='robot'),
                    sac.ChipItem('gpt-4v', icon='robot'),
                    sac.ChipItem('moonshot-v1-8k', icon='robot'),
                    sac.ChipItem('moonshot-v1-32k', icon='robot'),
                    sac.ChipItem('moonshot-v1-128k', icon='robot'),
                    sac.ChipItem('glm-3-turbo', icon='robot'),
                    sac.ChipItem('glm-4v', icon='robot'),
                    sac.ChipItem('glm-4', icon='robot'),
                    sac.ChipItem('deepseek-chat', icon='robot'),
                    sac.ChipItem('Local', icon='robot'),
                ], align='start', direction='vertical', radius='md', variant='filled', index=0
            )

            sac.divider(label='Choose', icon='activity', align='center', color='gray', key="b")

    with col1:
        col6, col7, col8 = st.columns(3)
        language = ['中文', 'English', '日本語', '한국인', 'Italiano', 'Deutsch']
        with col6:
            language1 = st.selectbox('原始语言', language, index=language.index(language1_setting))
        with col7:
            language2 = st.selectbox('目标语言', language, index=language.index(language2_setting))
        with col8:
            wait_time = st.number_input('翻译间隔(s)', min_value=0.0, max_value=5.0, value=wait_time_setting, step=0.1, help="每次API调用的间隔。\n\n 当你的视频比较长，字幕很多时，导致翻译时会一直反复调用 API 太多次，这会达到每分钟速率最大限制。当遇到报错429，如：`Too Many Requests`、`RateLimitError`这种速率报错，那就需要适当增大间隔。")

        col3, col4, col5 = st.columns(3)
        with col3:
            if st.button("执行字幕翻译", type="primary", use_container_width=True):
                if uploaded_file is not None:
                    st.session_state.video_name = "uploaded.srt"
                    st.toast('开始翻译!')

                    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H-%M-%S")
                    output_file = cache_dir + current_time
                    os.makedirs(output_file)
                    with open(output_file + '/' + st.session_state.video_name, "wb") as file:
                        file.write(uploaded_file.getbuffer())
                    print(f"- 本次任务目录：{output_file}")

                    srt_content = read_srt_file(output_file + '/' + st.session_state.video_name)

                    if 'gpt' in translate_option:
                        result = translate_srt(openai_key, openai_base, translate_option, srt_content, language1_setting, language2_setting, wait_time_setting)
                    elif 'moonshot' in translate_option:
                        result = translate_srt(kimi_key, kimi_base, translate_option, srt_content, language1_setting, language2_setting, wait_time_setting)
                    elif 'glm' in translate_option:
                        result = translate_srt(chatglm_key, chatglm_base, translate_option, srt_content, language1_setting, language2_setting, wait_time_setting)
                    elif 'deepseek' in translate_option:
                        result = translate_srt(deepseek_key, deepseek_base, translate_option, srt_content, language1_setting, language2_setting, wait_time_setting)
                    elif translate_option == '本地模型':
                        result = local_translate_srt(local_key, local_base, local_model, srt_content, language1_setting, language2_setting)

                    srt_content = ""
                    for i, subtitle in enumerate(result, start=1):
                        srt_content += f"{i}\n"
                        srt_content += f"{subtitle['time']}\n"
                        srt_content += subtitle['text'].replace('\n', '\n') + "\n\n"
                    st.session_state.path = output_file
                    st.session_state.srt_content = srt_content
                    with open(st.session_state.path + '/translate.srt', 'w', encoding='utf-8') as file:
                        file.write(srt_content)
                    st.toast("已成功保存", icon=":material/task_alt:")
                else:
                    st.toast("未检测到文件", icon=":material/error:")

        with col5:
            if st.button('打开文件目录', type="primary", use_container_width=True):
                try:
                    os.startfile(st.session_state.path)
                    st.toast("注意：文件夹已成功打开，可能未置顶显示，请检查任务栏！", icon=":material/task_alt:")
                except:
                    st.toast("未检测到文件", icon=":material/error:")

        with col4:
            if st.button('保存修改字幕', type="primary", use_container_width=True):
                try:
                    with open(st.session_state.path + '/translate.srt', 'w', encoding='utf-8') as file:
                        file.write(st.session_state.srt)
                    st.toast("已成功保存", icon=":material/task_alt:")
                except:
                    st.toast("未检测到文件", icon=":material/error:")

            translate_config["TRANSLATE"]["language1"] = language1
            translate_config["TRANSLATE"]["language2"] = language2
            translate_config["TRANSLATE"]["wait_time"] = wait_time

            with open(config_dir + '/translate.toml', 'w', encoding='utf-8') as file:
                toml.dump(translate_config, file)

        try:
            srt_data1 = parse_srt_file(st.session_state.srt_content)
            edited_data = st.data_editor(srt_data1, height=520, hide_index=True, use_container_width=True)
            srt_data2 = convert_to_srt(edited_data)
            st.session_state.srt = srt_data2
        except:
            srt_data = [{"index": "", "start": "", "end": "", "content": ""}]
            st.data_editor(srt_data, height=520, hide_index=True, use_container_width=True)
