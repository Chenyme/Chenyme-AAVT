@echo off
chcp 65001 > nul
echo 正在安装库...
pip install streamlit -i https://pypi.tuna.tsinghua.edu.cn/simple some-package
pip install -U openai-whisper -i https://pypi.tuna.tsinghua.edu.cn/simple some-package
pip install openai -i https://pypi.tuna.tsinghua.edu.cn/simple some-package
pip install langchain -i https://pypi.tuna.tsinghua.edu.cn/simple some-package
pip install torch torchvision torchaudio -i https://pypi.tuna.tsinghua.edu.cn/simple some-package
echo 安装完成
pause