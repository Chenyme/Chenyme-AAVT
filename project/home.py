import os
import toml
import shutil
import streamlit as st
import streamlit_antd_components as sac
from openai import OpenAI
from project.utils.utils2 import cache, convert_size, get_folders_info


# 主页面
def home():
    st.title("🖥Chenyme-AAVT V0.8.1")
    st.caption("POWERED BY @CHENYME")

    project_dir = os.path.dirname(os.path.abspath(__file__)).replace("\\", "/")
    config_dir = project_dir + "/config/"  # 配置文件
    cache_dir = project_dir + "/cache/"  # 本地缓存
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
            client = OpenAI(api_key="sk-9f8e218e61664eabafdb2bbb8fb0cf79", base_url="https://api.deepseek.com/")  # 不是忘记删掉了哦
            st.session_state.messages.append({"role": "user", "content": prompt})
            messages.chat_message("user").write(prompt)
            response = client.chat.completions.create(model="deepseek-chat",
                                                      messages=[
                                                          {"role": "system", "content": "你是一个基于下面内容的AI小助手，请基于下面的内容和自己的知识回答用户问题。" + doc},
                                                          {"role": "user", "content": prompt}
                                                      ])
            msg = response.choices[0].message.content
            st.session_state.messages.append({"role": "assistant", "content": msg})
            messages.chat_message("assistant").write(msg)

    if select == "设置":
        config = toml.load(config_dir + "api.toml")  # 加载配置
        openai_key = config["GPT"]["openai_key"]
        openai_base = config["GPT"]["openai_base"]
        kimi_key = config["KIMI"]["kimi_key"]
        kimi_base = config["KIMI"]["kimi_base"]
        deepseek_key = config["DEEPSEEK"]["deepseek_key"]
        deepseek_base = config["DEEPSEEK"]["deepseek_base"]
        chatglm_key = config["CHATGLM"]["chatglm_key"]
        chatglm_base = config["CHATGLM"]["chatglm_base"]
        local_key = config["LOCAL"]["api_key"]
        local_base = config["LOCAL"]["base_url"]
        local_model = config["LOCAL"]["model_name"]

        st.session_state.openai_key = openai_key
        st.session_state.openai_base = openai_base
        st.session_state.kimi_key = kimi_key
        st.session_state.kimi_base = kimi_base
        st.session_state.deepseek_key = deepseek_key
        st.session_state.deepseek_base = deepseek_base
        st.session_state.chatglm_key = chatglm_key
        st.session_state.chatglm_base = chatglm_base
        st.session_state.local_key = local_key
        st.session_state.local_base = local_base
        st.session_state.local_model = local_model

        st.write("### 模型配置")
        col1, col2 = st.columns([0.4, 0.6], gap="large")
        with col1:
            st.write("")
            st.write("")
            item = sac.segmented([
                sac.SegmentedItem(label='选择你要配置的模型'),
                sac.SegmentedItem(label='OpenAI-ChatGPT', icon='key'),
                sac.SegmentedItem(label='MoonShot-Kimi', icon='key'),
                sac.SegmentedItem(label='智谱AI-ChatGLM', icon='key'),
                sac.SegmentedItem(label='深度-DeepSeek', icon='key'),
                sac.SegmentedItem(label='本地LLMs', icon='robot'),
                sac.SegmentedItem(label='更多支持?', icon='arrow-up-right-square-fill',
                                  href='https://github.com/Chenyme/Chenyme-AAVT/issues'),
            ], index=1, direction='vertical', radius='lg', use_container_width=True, return_index=True)

        with col2:
            area = st.container(height=350)
            if item == 1:
                area.write('''##### ```官网：https://openai.com/```''')
                area.write('')
                new_openai_key = area.text_input("**OPENAI-API-KEY：**", st.session_state.openai_key)
                area.write('')
                new_openai_base = area.text_input("**OPENAI-API-BASE：**", st.session_state.openai_base)
                st.session_state.openai_key = new_openai_key
                st.session_state.openai_base = new_openai_base
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
                area.write('''##### ```官网：https://www.deepseek.com/```''')
                area.write('')
                new_deepseek_key = area.text_input("**DEEPSEEK-API-KEY：**", st.session_state.deepseek_key)
                area.write('')
                new_deepseek_base = area.text_input("**DEEPSEEK-API-BASE：**", st.session_state.deepseek_base)
                st.session_state.deepseek_key = new_deepseek_key
                st.session_state.deepseek_base = new_deepseek_base
                area.write('')

            elif item == 5:
                new_local_key = area.text_input("**LOCAL-API-KEY：**", st.session_state.local_key)
                new_local_base = area.text_input("**LOCAL-API-BASE：**", st.session_state.local_base)
                new_local_model = area.text_input("**LOCAL-MODEL-NAME：**", st.session_state.local_model)
                st.session_state.local_key = new_local_key
                st.session_state.local_base = new_local_base
                st.session_state.local_model = new_local_model

            if item != 0:
                area.write("")
                if area.button('保存', use_container_width=True, type="primary"):
                    config["GPT"]["openai_key"] = st.session_state.openai_key
                    config["GPT"]["openai_base"] = st.session_state.openai_base
                    config["KIMI"]["kimi_key"] = st.session_state.kimi_key
                    config["KIMI"]["kimi_base"] = st.session_state.kimi_base
                    config["DEEPSEEK"]["deepseek_key"] = st.session_state.deepseek_key
                    config["DEEPSEEK"]["deepseek_base"] = st.session_state.deepseek_base
                    config["CHATGLM"]["chatglm_key"] = st.session_state.chatglm_key
                    config["CHATGLM"]["chatglm_base"] = st.session_state.chatglm_base
                    config["LOCAL"]["api_key"] = st.session_state.local_key
                    config["LOCAL"]["base_url"] = st.session_state.local_base
                    config["LOCAL"]["model_name"] = st.session_state.local_model
                    with open(config_dir + "/api.toml", 'w', encoding='utf-8') as file:
                        toml.dump(config, file)
                    st.toast("保存成功！", icon=":material/task_alt:")

            else:
                with area:
                    area.write("")
                    area.write("")
                    area.write("")
                    sac.buttons([sac.ButtonsItem(icon=sac.BsIcon(name='card-heading', size=50))], align='center',
                                variant='text', index=None)
                    sac.buttons([sac.ButtonsItem(icon=sac.BsIcon(name='check-square', size=50))], align='center',
                                variant='text', index=None)
                    sac.buttons([sac.ButtonsItem(icon=sac.BsIcon(name='caret-left-square', size=50))], align='center',
                                variant='text', index=None)
        st.write("")

        sac.divider(label='缓存识别', icon='box-fill', align='center', color='gray')

        col1, col2 = st.columns([0.4, 0.6], gap="large")
        with col1:
            st.write("### 本地缓存")
            st.metric(label="大小", label_visibility="collapsed", value=f"{convert_size(cache(cache_dir))}")
            folders_df = get_folders_info(cache_dir)
            st.dataframe(folders_df, hide_index=True, height=250, use_container_width=True)
            if st.button("📃清除所有", type="primary", help="注意：所有项目中的生成文件均会被删除", use_container_width=True):
                if not os.listdir(cache_dir):
                    st.toast("未检测到文件", icon=":material/error:")
                else:
                    for root, dirs, files in os.walk(cache_dir):
                        for file in files:
                            os.remove(os.path.join(root, file))
                        for adir in dirs:
                            shutil.rmtree(os.path.join(root, adir))
                    st.toast("已全部删除", icon=":material/task_alt:")

        sac.divider(label='项目修复', icon='box-fill', align='center', color='gray')

        col1, col2 = st.columns([0.4, 0.6], gap="large")
        with col1:
            st.write("### 闪退修复")
            sac.alert(
                label='如果运行时闪退可使用该服务尝试修复',
                description='如果您是非`install.bat`运行该服务可能不适用。',
                size='lg', radius=20, icon=True, closable=True, color='info')
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
