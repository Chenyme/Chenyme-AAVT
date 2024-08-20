import streamlit as st


def style(home=False):  # 定义应用自定义字体的函数
    if home:
        st.set_page_config(page_title="Chenyme-AAVT", layout="wide",
                           menu_items={
                               'Get Help': 'https://blog.chenyme.top/blog/aavt-install',
                               'Report a bug': "https://github.com/Chenyme/Chenyme-AAVT/issues",
                               'About': "#### @2024 Chenyme-AAVT 版权所有"
                           }
                           )
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@300;400;500;700&display=swap');
        
        /* 全局样式 */
        body {
            font-family: 'Noto Sans SC', sans-serif;
            background-color: #F8F8F8;
            color: #1C1C1E;
        }
        
        /* 全局样式 */
        .st-emotion-cache-y4bq5x {
            font-family: 'Noto Sans SC', sans-serif;
            font-size: 0.5em;
        }
        
        /* 全局字体 */        
        p {
            font-family: 'Noto Sans SC', sans-serif;
        }
        
        .st-bp{
            font-family: 'Noto Sans SC', sans-serif;
        }
        
        .st-ce {
            font-size: 0.9rem;
        }
        
        hr {
            margin: 0.8em 0px;
            padding: 0px;
            color: inherit;
            background-color: transparent;
            border-top: none;
            border-right: none;
            border-left: none;
            border-image: initial;
            border-bottom: 1px solid rgba(28, 28, 30, 0.2);
        }
        
        h1 {
            font-family: 'Noto Sans SC', sans-serif;
            font-size: 36px;
            color: #1C1C1E;
            margin-bottom: 16px;
            font-weight: 600;
        }
        
        h2 {
            font-family: 'Noto Sans SC', sans-serif;
            font-size: 30px;
            color: #1C1C1E;
            margin-bottom: 16px;
            font-weight: 600;
        }
        
        h3 {
            font-family: 'Noto Sans SC', sans-serif;
            color: #1C1C1E;
            padding-top: 0px;
            margin-bottom: 5px;
            font-weight: 600;
        }
        
        h4 {
            font-family: 'Noto Sans SC', sans-serif;
            font-size: 20px;
            color: #1C1C1E;
            margin-bottom: 0px;
            font-weight: 600;
        }
        
        h5 {
            font-family: 'Noto Sans SC', sans-serif;
            font-size: 17px;
            color: #1C1C1E;
            margin-bottom: 0px;
            font-weight: 600;
        }
        
        h6 {
            font-family: 'Noto Sans SC', sans-serif;
            color: #1C1C1E;
            margin-bottom: -25px;
            font-weight: 600;
        }
        
        /* 全局布局 */
        .block-container {
            padding-top: 40px;
            padding-left: 70px;
            padding-right: 70px;
        }
        
        @media (max-width: 600px) {
            .block-container {
                padding-top: 55px;
                padding-left: 24px;
                padding-right: 24px;
            }
        }
        
        /* 全局按钮 */
        .stButton > button {
            color: #FFFFFF;
            background-color: #007AFF;
            border-radius: 15px;
            font-weight: 600;
            font-family: 'Noto Sans SC', sans-serif;
            font-size: 15px;
            border: none;
            cursor: pointer;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            transition: background-color 0.3s ease, box-shadow 0.3s ease, transform 0.1s ease;
        }
        
        .stButton > button:hover {
            background-color: #005bb5;
            box-shadow: 0 6px 8px rgba(0, 0, 0, 0.2);
        }
        
        .stButton > button:active {
            background-color: #004080;
            color: white;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            transform: scale(0.98);
        }
        
        .stButton > button:disabled {
            background-color: #b0b0b0;
            color: #f0f0f0;
            cursor: not-allowed;
            box-shadow: none;
        }
        
        .stButton > button:focus:not(:focus-visible) {
            outline: none;
            font-family: 'Noto Sans SC', sans-serif;
        }

        .stTextInput > div > input {
            font-family: 'Noto Sans SC', sans-serif;
            border-radius: 10px;
            border: 1px solid #D1D1D6;
            box-shadow: inset 0 1px 3px rgba(0, 0, 0, 0.05);
            transition: box-shadow 0.3s ease;
        }

        .stTextInput > div > input:focus {
            font-family: 'Noto Sans SC', sans-serif;
            box-shadow: 0 0 0 3px rgba(0, 122, 255, 0.3);
            border-color: #007AFF;
        }
        
        /* 上传器样式 */
        section[data-testid="stFileUploaderDropzone"] {
            display: flex;
            align-items: center;
            justify-content: space-between;
            border-radius: 15px;
            padding: 13px 20px;
            border: 1px dashed #007AFF;
            text-align: center;
            color: white;
            font-family: 'Noto Sans SC', sans-serif;
            max-width: 100%;
            box-sizing: border-box;
        }
        
        .st-emotion-cache-u8hs99 {
            display: flex;
            align-items: center;
            justify-content: space-between;
            width: 100%;
        }
        
        .st-emotion-cache-1fttcpj {
            flex-grow: 1;
        }
        
        .st-emotion-cache-1v7f65g .e1b2p2ww15 {
            display: flex;
            justify-content: center;
            align-items: center;
        }
        
        span.st-emotion-cache-9ycgxx {
            color: white;
            text-align: center;
            font-size: 17px;
            color: #007AFF;
            font-weight: bold;
            cursor: pointer;
        }
        
        small.st-emotion-cache-15rwkn9 {
            text-align: center;
            color: #666;
            font-size: 12px;
            cursor: pointer;
        }
        
        button[data-testid="baseButton-secondary"] {
            font-family: 'Noto Sans SC', sans-serif;
            border-radius: 15px;
            color: white;
            font-size: 15px;
            font-weight: bold;
            background-color: #007AFF;
            border: none;
            cursor: pointer;
            transition: background-color 0.3s ease, color 0.3s ease;
            padding: 3px 16px;
        }
        
        button[data-testid="baseButton-secondary"]:hover {
            background-color: #005BB5;
            color: white;
        }
        
        button[data-testid="baseButton-secondary"]:active {
            background-color: #005BB5;
            color: white;
        }
        
        @media (max-width: 600px) {
            section[data-testid="stFileUploaderDropzone"] {
                flex-direction: column;
                padding: 15px;
                text-align: center;
            }
            
            .st-emotion-cache-u8hs99 {
                flex-direction: column;
                align-items: center;
            }
        
            .st-emotion-cache-e6zcxy {
                margin-bottom: 10px;
            }
        
            button[data-testid="baseButton-secondary"] {
                margin-top: 15px;
                width: 100%;
            }
        }
        
        /* 标签容器 */
        .st-emotion-cache-19k6lld {
            border-radius: 15px;
            font-weight: 600;
            font-family: 'Noto Sans SC', sans-serif;
            border: none;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            transition: background-color 0.3s ease, box-shadow 0.3s ease, transform 0.1s ease;
        }
        
        .st-emotion-cache-19k6lld:hover {
            color: white;
            box-shadow: 0 6px 8px rgba(0, 0, 0, 0.2);
        }
        
        .st-emotion-cache-19k6lld:active {
            color: white;
            background-color: #004080;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            transform: scale(0.98);
        }
        
        .st-emotion-cache-19k6lld:focus:not(:focus-visible) {
            color: white;
            outline: none;
        }
        
        .stDownloadButton > button {
            border-radius: 15px;
            font-weight: 600;
            font-family: 'Noto Sans SC', sans-serif;
            border: none;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            transition: background-color 0.3s ease, box-shadow 0.3s ease, transform 0.1s ease;
        }

        .stDownloadButton > button:hover {
            color: white;
            box-shadow: 0 6px 8px rgba(0, 0, 0, 0.2);
        }

        .stDownloadButton > button:active {
            color: white;
            background-color: #004080;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            transform: scale(0.98);
        }

        .stDownloadButton > button:focus:not(:focus-visible) {
            color: white;
            outline: none;
        }
        
        div[data-baseweb="tabs"] {
            display: flex;
            justify-content: center;
            margin-bottom: 0px;
            padding-bottom: 0px;
            border-bottom: none;
        }
    
        button[data-baseweb="tab"] {
            background-color: #F7F7F7;
            border: none;
            border-radius: 16px 16px 0 0;
            margin: 0 8px;
            font-family: 'SF Pro Text', sans-serif;
            font-weight: 500;
            font-size: 15px;
            color: #666666;
            padding: 12px 18px;
            transition: background-color 0.3s ease, color 0.3s ease, box-shadow 0.3s ease;
            cursor: pointer;
            box-shadow: none;
        }
    
        button[data-baseweb="tab"][aria-selected="true"] {
            background-color: white;
            color: #007AFF;
            font-weight: 600;
            font-size: 17px;
            border-radius: 16px 16px 0 0;
            box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
            position: relative;
            top: 0px;
        }
    
        button[data-baseweb="tab"]:hover {
            background-color: #E0E0E0;
            color: #007AFF;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
        }
    
        div[data-baseweb="tab-content"] {
            background-color: #FFFFFF;
            border: 1px solid #E0E0E0;
            border-radius: 0 0 16px 16px;
            box-shadow: 0px 6px 10px rgba(0, 0, 0, 0.08);
            margin-top: -6px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
