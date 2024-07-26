import os
import json
import toml
import datetime
import streamlit as st
import streamlit_antd_components as sac
from project.utils.utils2 import read_srt_file, parse_srt_file, convert_to_srt, translate_srt, local_translate_srt


def translation():
    project_dir = os.path.dirname(os.path.abspath(__file__)).replace("\\", "/")
    config_dir = project_dir + "/config/"  # 配置文件
    cache_dir = project_dir + "/cache/"  # 本地缓存

    api_config = toml.load(config_dir + "api.toml")  # 加载配置
    gemini_key = api_config["GEMINI"]["gemini_key"]  # GEMINI
    gemini_base = api_config["GEMINI"]["gemini_base"]
    ai01_key = api_config["AI01"]["AI01_key"]  # 01
    ai01_base = api_config["AI01"]["AI01_base"]
    kimi_key = api_config["KIMI"]["kimi_key"]  # kimi
    kimi_base = api_config["KIMI"]["kimi_base"]
    chatglm_key = api_config["CHATGLM"]["chatglm_key"]  # chatglm
    chatglm_base = api_config["CHATGLM"]["chatglm_base"]
    openai_key = api_config["GPT"]["openai_key"]  # openai
    openai_base = api_config["GPT"]["openai_base"]
    claude_key = api_config["CLAUDE"]["claude_key"]  # claude
    claude_base = api_config["CLAUDE"]["claude_base"]
    deepseek_key = api_config["DEEPSEEK"]["deepseek_key"]  # deepseek
    deepseek_base = api_config["DEEPSEEK"]["deepseek_base"]
    local_key = api_config["LOCAL"]["api_key"]  # local
    local_base = api_config["LOCAL"]["base_url"]
    local_model = api_config["LOCAL"]["model_name"]

    translate_config = toml.load(config_dir + "translate.toml")  # 加载API配置
    language1_setting = translate_config["TRANSLATE"]["language1"]
    language2_setting = translate_config["TRANSLATE"]["language2"]
    srt_setting = translate_config["TRANSLATE"]["srt"]
    wait_time_setting = translate_config["TRANSLATE"]["wait_time"]
    prompt_pre_setting = translate_config["TRANSLATE"]["prompt_pre"]

    with open(config_dir + 'prompt.json', 'r', encoding='utf-8') as file:
        prompt = json.load(file)  # 加载配置
    st.session_state.prompt = prompt

    st.subheader("AI SRT字幕翻译")
    st.caption("AI SRT subtitle translation")
    sac.divider(label='POWERED BY @CHENYME', icon="lightning-charge", align='center', color='gray', key="1")

    with st.sidebar:
        st.write("#### SRT上传器")
        uploaded_file = st.file_uploader("上传您的SRT文件", type=["srt"], label_visibility="collapsed")

    col1, col2 = st.columns([0.7, 0.3])
    with col2:
        try:
            prompt_pre_setting = st.selectbox('预设prompt', prompt.keys(),
                                              index=list(prompt.keys()).index(prompt_pre_setting))
        except:
            prompt_pre_setting = st.selectbox('预设prompt', prompt.keys())

        translate_option = sac.menu([
                sac.MenuItem('本地模型', icon='house-up-fill'),
                sac.MenuItem('DeepSeek-深度求索', icon='node-plus-fill', children=[
                    sac.MenuItem('deepseek-chat', icon='robot'),
                    sac.MenuItem('deepseek-coder', icon='robot')
                ]),
                sac.MenuItem('ChatGLM-智谱AI', icon='node-plus-fill', children=[
                    sac.MenuItem('glm-4', icon='robot'),
                    sac.MenuItem('glm-4-0520', icon='robot'),
                    sac.MenuItem('glm-4-flash', icon='robot'),
                    sac.MenuItem('glm-4-air', icon='robot'),
                    sac.MenuItem('glm-4-airx', icon='robot')
                ]),
                sac.MenuItem('ChatGPT-OpenAI', icon='node-plus-fill', children=[
                    sac.MenuItem('gpt-4o-mini', icon='robot'),
                    sac.MenuItem('gpt-4', icon='robot'),
                    sac.MenuItem('gpt-4-turbo', icon='robot'),
                    sac.MenuItem('gpt-4o', icon='robot')
                ]),
                sac.MenuItem('Moonshot-月之暗面', icon='node-plus-fill', children=[
                    sac.MenuItem('moonshot-v1-8k', icon='robot'),
                    sac.MenuItem('moonshot-v1-32k', icon='robot'),
                    sac.MenuItem('moonshot-v1-128k', icon='robot')
                ]),
                sac.MenuItem('Gemini-Google', icon='node-plus-fill', children=[
                    sac.MenuItem('gemini-pro', icon='robot'),
                    sac.MenuItem('gemini-1.0-pro', icon='robot'),
                    sac.MenuItem('gemini-1.5-flash', icon='robot'),
                    sac.MenuItem('gemini-1.5-pro', icon='robot')
                ]),
                sac.MenuItem('Claude-Anthropic', icon='node-plus-fill', children=[
                    sac.MenuItem('claude-3-opus', icon='robot'),
                    sac.MenuItem('claude-3-sonnet', icon='robot'),
                    sac.MenuItem('claude-3-haiku', icon='robot')
                ]),
                sac.MenuItem('01AI-零一万物', icon='node-plus-fill', children=[
                    sac.MenuItem('yi-spark', icon='robot'),
                    sac.MenuItem('yi-medium', icon='robot'),
                    sac.MenuItem('yi-medium-200k', icon='robot'),
                    sac.MenuItem('yi-vision', icon='robot'),
                    sac.MenuItem('yi-large', icon='robot'),
                    sac.MenuItem('yi-large-rag', icon='robot'),
                    sac.MenuItem('yi-large-turbo', icon='robot'),
                    sac.MenuItem('yi-large-preview', icon='robot')
                ]),
            ], height=650, size='sm', indent=20, open_all=True)

    with col1:
        col6, col7, col8, col9 = st.columns(4)
        language = ['中文', 'English', '日本語', '한국인', 'Italiano', 'Deutsch']
        with col6:
            language1 = st.selectbox('原始语言', language, index=language.index(language1_setting))
        with col7:
            language2 = st.selectbox('目标语言', language, index=language.index(language2_setting))
        with col8:
            srt_choose = ["关闭", "原始语言为首", "目标语言为首"]
            srt = st.selectbox('双语字幕', srt_choose, index=srt_choose.index(srt_setting))
        with col9:
            wait_time = st.number_input('翻译间隔(s)', min_value=0.0, max_value=5.0, value=wait_time_setting, step=0.1, help="每次API调用的间隔。\n\n 当你的视频比较长，字幕很多时，导致翻译时会一直反复调用 API 太多次，这会达到每分钟速率最大限制。当遇到报错429，如：`Too Many Requests`、`RateLimitError`这种速率报错，那就需要适当增大间隔。")

        system_prompt = prompt[prompt_pre_setting]["system_prompt"].replace("{language1}", language1).replace("{language2}", language2)
        user_prompt = prompt[prompt_pre_setting]["user_prompt"].replace("{language1}", language1).replace("{language2}", language2)
        col3, col4, col5, col6 = st.columns(4)
        with col3:
            if st.button("执行字幕翻译", type="primary", use_container_width=True):
                if uploaded_file is not None:
                    st.session_state.video_name = "uploaded.srt"
                    st.toast('已开始生成，请不要在运行时切换菜单或修改参数!', icon=":material/person_alert:")
                    msg = st.toast('正在进行视频提取', icon=":material/play_circle:")

                    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H-%M-%S")
                    output_file = cache_dir + current_time
                    os.makedirs(output_file)
                    with open(output_file + '/' + st.session_state.video_name, "wb") as file:
                        file.write(uploaded_file.getbuffer())
                    print(f"- 本次任务目录：{output_file}")

                    srt_content = read_srt_file(output_file + '/' + st.session_state.video_name)

                    if translate_option == '本地模型':
                        result = local_translate_srt(system_prompt, user_prompt, local_key, local_base, local_model, srt_content, srt_setting)
                    elif 'gemini' in translate_option:
                        result = translate_srt(system_prompt, user_prompt, gemini_key, gemini_base, translate_option, srt_content, wait_time_setting, srt_setting)
                    elif 'yi' in translate_option:
                        result = translate_srt(system_prompt, user_prompt, ai01_key, ai01_base, translate_option, srt_content, wait_time_setting, srt_setting)
                    elif 'gpt' in translate_option:
                        result = translate_srt(system_prompt, user_prompt, openai_key, openai_base, translate_option, srt_content, wait_time_setting, srt_setting)
                    elif 'moonshot' in translate_option:
                        result = translate_srt(system_prompt, user_prompt, kimi_key, kimi_base, translate_option, srt_content, wait_time_setting, srt_setting)
                    elif 'glm' in translate_option:
                        result = translate_srt(system_prompt, user_prompt, chatglm_key, chatglm_base, translate_option, srt_content, wait_time_setting, srt_setting)
                    elif 'deepseek' in translate_option:
                        result = translate_srt(system_prompt, user_prompt, deepseek_key, deepseek_base, translate_option, srt_content, wait_time_setting, srt_setting)
                    elif 'claude' in translate_option:
                        result = translate_srt(system_prompt, user_prompt, claude_key, claude_base, translate_option, srt_content, wait_time_setting, srt_setting)
                    print(" ")

                    srt_content = ""
                    for i, subtitle in enumerate(result, start=1):
                        srt_content += f"{i}\n"
                        srt_content += f"{subtitle['time']}\n"
                        srt_content += subtitle['text'].replace('\n', '\n') + "\n\n"
                    st.session_state.path = output_file
                    st.session_state.srt_content = srt_content
                    with open(st.session_state.path + '/translate.srt', 'w', encoding='utf-8') as file:
                        file.write(srt_content)
                    msg.toast("翻译文件已成功保存", icon=":material/task_alt:")
                else:
                    st.toast("未检测到文件", icon=":material/error:")

        with col6:
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
        with col5:
            if st.button('保存翻译参数', type="primary", use_container_width=True):
                translate_config["TRANSLATE"]["language1"] = language1
                translate_config["TRANSLATE"]["language2"] = language2
                translate_config["TRANSLATE"]["wait_time"] = wait_time
                translate_config["TRANSLATE"]["srt"] = srt
                translate_config["TRANSLATE"]["prompt_pre"] = prompt_pre_setting

                with open(config_dir + '/translate.toml', 'w', encoding='utf-8') as file:
                    toml.dump(translate_config, file)

        try:
            srt_data1 = parse_srt_file(st.session_state.srt_content)
            edited_data = st.data_editor(srt_data1, height=600, hide_index=True, use_container_width=True)
            srt_data2 = convert_to_srt(edited_data)
            st.session_state.srt = srt_data2
        except:
            srt_data = [{"index": "", "start": "", "end": "", "content": ""}]
            st.data_editor(srt_data, height=600, hide_index=True, use_container_width=True)

    sac.divider(label='POWERED BY @CHENYME', icon="lightning-charge", align='center', color='gray', key="132")
