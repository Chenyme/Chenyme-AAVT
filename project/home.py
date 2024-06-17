import os
import time
import toml
import json
import pandas as pd
import shutil
import streamlit as st
import streamlit_antd_components as sac
from openai import OpenAI
from project.utils.utils2 import cache, convert_size, get_folders_info, get_info


@st.experimental_dialog('新增提示词')
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


@st.experimental_dialog('在这里上传或拖入')
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
    st.subheader("🖥Chenyme-AAVT V0.8.4")
    st.caption("POWERED BY @CHENYME")

    with st.sidebar:
        sac.buttons(items=[
            sac.ButtonsItem(label='来给我一颗星叭！', icon='github', href='https://github.com/Chenyme/Chenyme-AAVT')],
            variant='dashed', index=None, direction='vertical', use_container_width=True, align='center', color='dark')
        sac.alert(
            label='**项目文档 已发布**',
            description='**文档链接：**[AAVT](https://zwho5v3j233.feishu.cn/wiki/OGcrwinzhi88MkkvEMVcLkDgnzc?from=from_copylink)',
            size='lg', radius=20, icon=True, closable=True, color='info')

    project_dir = os.path.dirname(os.path.abspath(__file__)).replace("\\", "/")
    config_dir = project_dir + "/config/"  # 配置文件
    cache_dir = project_dir + "/cache/"  # 本地缓存1
    avtb_dir = project_dir + "/AVTB/output/"  # 本地缓存2
    avg_dir = project_dir + "/AVG/output/"
    doc_dir = project_dir + "/doc/"  # 知识库

    with open(doc_dir + "readme.md", 'r', encoding='utf-8') as file:
        doc = file.read()

    select = sac.tabs([
        sac.TabsItem(label='助手', icon='robot'),
        sac.TabsItem(label='设置', icon='gear')
    ], align='center', variant='outline', use_container_width=True, index=0)

    if select == "助手":
        messages = st.container(height=470)
        if "messages" not in st.session_state:
            st.session_state["messages"] = [
                {"role": "assistant", "content": "我是本项目的AI小助手，有什么可以帮你的么?"}]

        for msg in st.session_state.messages:
            messages.chat_message(msg["role"]).write(msg["content"])

        if prompt := st.chat_input(placeholder="有什么我可以帮你的么？【Tips：已自带Key，可直接使用】"):
            client = OpenAI(api_key="sk-9f8e218e61664eabafdb2bbb8fb0cf79",
                            base_url="https://api.deepseek.com/")  # 不是忘记删掉了哦
            st.session_state.messages.append({"role": "user", "content": prompt})
            messages.chat_message("user").write(prompt)
            response = client.chat.completions.create(model="deepseek-chat",
                                                      messages=[
                                                          {"role": "system",
                                                           "content": "你是一个基于下面内容的AI小助手，请基于下面的内容和自己的知识回答用户问题。" + doc},
                                                          {"role": "user", "content": prompt}
                                                      ])
            msg = response.choices[0].message.content
            st.session_state.messages.append({"role": "assistant", "content": msg})
            messages.chat_message("assistant").write(msg)

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

        st.session_state.gemini_key = gemini_key
        st.session_state.gemini_base = gemini_base
        st.session_state.ai01_key = ai01_key
        st.session_state.ai01_base = ai01_base
        st.session_state.kimi_key = kimi_key
        st.session_state.kimi_base = kimi_base
        st.session_state.chatglm_key = chatglm_key
        st.session_state.chatglm_base = chatglm_base
        st.session_state.openai_key = openai_key
        st.session_state.openai_base = openai_base
        st.session_state.claude_key = claude_key
        st.session_state.claude_base = claude_base
        st.session_state.deepseek_key = deepseek_key
        st.session_state.deepseek_base = deepseek_base
        st.session_state.local_key = local_key
        st.session_state.local_base = local_base
        st.session_state.local_model = local_model

        with open(config_dir + 'prompt.json', 'r', encoding='utf-8') as file:
            prompt = json.load(file)  # 加载配置
        st.session_state.prompt = prompt

        st.write("##### 模型配置")
        st.write("")
        col1, col2 = st.columns([0.4, 0.6], gap="large")
        with col1:
            item = sac.segmented([
                sac.SegmentedItem(label='Google-Gemini', icon='key'),
                sac.SegmentedItem(label='零一万物-01AI', icon='key'),
                sac.SegmentedItem(label='MoonShot-Kimi', icon='key'),
                sac.SegmentedItem(label='智谱AI-ChatGLM', icon='key'),
                sac.SegmentedItem(label='OpenAI-ChatGPT', icon='key'),
                sac.SegmentedItem(label='Anthropic-Claude', icon='key'),
                sac.SegmentedItem(label='深度求索-DeepSeek', icon='key'),
                sac.SegmentedItem(label='本地部署LLMs模型', icon='robot'),
                sac.SegmentedItem(label='更多支持?', icon='arrow-up-right-square-fill',
                                  href='https://github.com/Chenyme/Chenyme-AAVT/issues'),
            ], index=1, direction='vertical', radius='lg', use_container_width=True, return_index=True)

        with col2:
            area = st.container(height=350)
            if item == 0:
                area.write('''##### ```官网：https://ai.google.dev/aistudio/```''')
                area.write('')
                new_gemini_key = area.text_input("**GEMINI-API-KEY：**", st.session_state.gemini_key)
                area.write('')
                new_gemini_base = area.text_input("**GEMINI-API-BASE：**", st.session_state.gemini_base)
                st.session_state.gemini_key = new_gemini_key
                st.session_state.gemini_base = new_gemini_base
                area.write('')

            elif item == 1:
                area.write('''##### ```官网：https://platform.lingyiwanwu.com/```''')
                area.write('')
                new_ai01_key = area.text_input("**01AI-API-KEY：**", st.session_state.ai01_key)
                area.write('')
                new_ai01_base = area.text_input("**01AI-API-BASE：**", st.session_state.ai01_base)
                st.session_state.ai01_key = new_ai01_key
                st.session_state.ai01_base = new_ai01_base
                area.write('')

            elif item == 2:
                area.write('''##### ```官网：https://www.moonshot.cn/```''')
                area.write('')
                new_kimi_key = area.text_input("**KIMI-API-KEY：**", st.session_state.kimi_key)
                area.write('')
                new_kimi_base = area.text_input("**KIMI-API-BASE：**", st.session_state.kimi_base)
                st.session_state.kimi_key = new_kimi_key
                st.session_state.kimi_base = new_kimi_base
                area.write('')

            elif item == 3:
                area.write('''##### ```官网：https://open.bigmodel.cn/```''')
                area.write('')
                new_chatglm_key = area.text_input("**CHATGLM-API-KEY：**", st.session_state.chatglm_key)
                area.write('')
                new_chatglm_base = area.text_input("**CHATGLM-API-BASE：**", st.session_state.chatglm_base)
                st.session_state.chatglm_key = new_chatglm_key
                st.session_state.chatglm_base = new_chatglm_base
                area.write('')

            elif item == 4:
                area.write('''##### ```官网：https://openai.com/```''')
                area.write('')
                new_openai_key = area.text_input("**OPENAI-API-KEY：**", st.session_state.openai_key)
                area.write('')
                new_openai_base = area.text_input("**OPENAI-API-BASE：**", st.session_state.openai_base)
                st.session_state.openai_key = new_openai_key
                st.session_state.openai_base = new_openai_base
                area.write('')

            elif item == 5:
                area.write('''##### ```官网：https://www.anthropic.com/```''')
                area.write('')
                new_claude_key = area.text_input("**CLAUDE-API-KEY：**", st.session_state.claude_key)
                area.write('')
                new_claude_base = area.text_input("**CLAUDE-API-BASE：**", st.session_state.claude_base)
                st.session_state.claude_key = new_claude_key
                st.session_state.claude_base = new_claude_base
                area.write('')

            elif item == 6:
                area.write('''##### ```官网：https://www.deepseek.com/```''')
                area.write('')
                new_deepseek_key = area.text_input("**DEEPSEEK-API-KEY：**", st.session_state.deepseek_key)
                area.write('')
                new_deepseek_base = area.text_input("**DEEPSEEK-API-BASE：**", st.session_state.deepseek_base)
                st.session_state.deepseek_key = new_deepseek_key
                st.session_state.deepseek_base = new_deepseek_base
                area.write('')

            elif item == 7:
                new_local_key = area.text_input("**LOCAL-API-KEY：**", st.session_state.local_key)
                new_local_base = area.text_input("**LOCAL-API-BASE：**", st.session_state.local_base)
                new_local_model = area.text_input("**LOCAL-MODEL-NAME：**", st.session_state.local_model)
                st.session_state.local_key = new_local_key
                st.session_state.local_base = new_local_base
                st.session_state.local_model = new_local_model

            area.write("")
            if area.button('保存', use_container_width=True, type="primary"):

                config["GEMINI"]["gemini_key"] = st.session_state.gemini_key
                config["GEMINI"]["gemini_base"] = st.session_state.gemini_base
                config["AI01"]["AI01_key"] = st.session_state.ai01_key
                config["AI01"]["AI01_base"] = st.session_state.ai01_base
                config["KIMI"]["kimi_key"] = st.session_state.kimi_key
                config["KIMI"]["kimi_base"] = st.session_state.kimi_base
                config["CHATGLM"]["chatglm_key"] = st.session_state.chatglm_key
                config["CHATGLM"]["chatglm_base"] = st.session_state.chatglm_base
                config["GPT"]["openai_key"] = st.session_state.openai_key
                config["GPT"]["openai_base"] = st.session_state.openai_base
                config["CLAUDE"]["claude_key"] = st.session_state.claude_key
                config["CLAUDE"]["claude_base"] = st.session_state.claude_base
                config["DEEPSEEK"]["deepseek_key"] = st.session_state.deepseek_key
                config["DEEPSEEK"]["deepseek_base"] = st.session_state.deepseek_base
                config["LOCAL"]["api_key"] = st.session_state.local_key
                config["LOCAL"]["base_url"] = st.session_state.local_base
                config["LOCAL"]["model_name"] = st.session_state.local_model

                with open(config_dir + "/api.toml", 'w', encoding='utf-8') as file:
                    toml.dump(config, file)
                st.toast("保存成功！", icon=":material/task_alt:")

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
            if st.button("保存修改", use_container_width=True, type="primary"):
                with open(config_dir + '/prompt.json', 'w', encoding='utf-8') as json_file:
                    json_file.write(prompt_json)
        with col2:
            if st.download_button(
                label="下载提示词",
                data=prompt_json,
                file_name="prompt.json",
                mime="text/json",
                use_container_width=True,
                type="primary"
            ):
                with open(config_dir + '/prompt.json', 'w', encoding='utf-8') as json_file:
                    json_file.write(prompt_json)
        with col3:
            if st.button("新建提示词", use_container_width=True, type="primary"):
                add(config_dir)
        with col4:
            if st.button("导入提示词", use_container_width=True, type="primary"):
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
            if st.button("📃清除所有识别文件", type="primary", help="注意：所有项目中的生成文件均会被删除",
                         use_container_width=True):
                if not os.listdir(cache_dir):
                    st.toast("未检测到文件", icon=":material/error:")
                else:
                    for root, dirs, files in os.walk(cache_dir):
                        for file in files:
                            os.remove(os.path.join(root, file))
                        for adir in dirs:
                            shutil.rmtree(os.path.join(root, adir))
                    st.toast("已全部删除", icon=":material/task_alt:")
                    st.rerun()
        with col2:
            st.metric(label="**图文博客：**", value=f"{convert_size(cache(avtb_dir))}")
            folders_df = get_folders_info(avtb_dir)
            st.dataframe(folders_df, hide_index=True, height=200, use_container_width=True)
            st.write("")
            if st.button("📃清除所有图文生成", type="primary", help="注意：所有项目中的生成文件均会被删除",
                         use_container_width=True):
                if not os.listdir(avtb_dir):
                    st.toast("未检测到文件", icon=":material/error:")
                else:
                    for root, dirs, files in os.walk(avtb_dir):
                        for file in files:
                            os.remove(os.path.join(root, file))
                        for adir in dirs:
                            shutil.rmtree(os.path.join(root, adir))
                    st.toast("已全部删除", icon=":material/task_alt:")
                    st.rerun()
        with col3:
            st.metric(label="**人声模拟：**", value=f"{convert_size(cache(avg_dir))}")
            folders_df = get_info(avg_dir)
            st.dataframe(folders_df, hide_index=True, height=200, use_container_width=True)
            st.write("")
            if st.button("📃清除所有人声生成", type="primary", help="注意：所有项目中的生成文件均会被删除",
                         use_container_width=True):
                if not os.listdir(avg_dir):
                    st.toast("未检测到文件", icon=":material/error:")
                else:
                    for root, dirs, files in os.walk(avg_dir):
                        for file in files:
                            os.remove(os.path.join(root, file))
                        for adir in dirs:
                            shutil.rmtree(os.path.join(root, adir))
                    st.toast("已全部删除", icon=":material/task_alt:")
                    st.rerun()

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
