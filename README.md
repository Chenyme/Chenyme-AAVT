<div align="center">

<img src="https://github.com/Chenyme/Chenyme-AAVT/blob/main/cache/public/picture/chenymeaavt1.png" title="chenymeaavt.png" width="80%" />

<br>
<br>

[![英文](https://img.shields.io/badge/%E8%8B%B1%E6%96%87-English-blue)](./README-EN.md)
[![下载](https://img.shields.io/github/downloads/Chenyme/Chenyme-AAVT/total.svg?style=flat-square&label=下载)](https://github.com/Chenyme/Chenyme-AAVT/releases)
[![Latest Release](https://img.shields.io/github/v/release/Chenyme/Chenyme-AAVT.svg?style=flat-square)](https://github.com/Chenyme/Chenyme-AAVT/releases)
![PyPI - Version](https://img.shields.io/pypi/v/AAVT?logo=pypi)
[![License](https://img.shields.io/github/license/Chenyme/Chenyme-AAVT.svg?style=flat-square)](https://github.com/Chenyme/Chenyme-AAVT/blob/main/LICENSE)
[![群组](https://img.shields.io/badge/群组-Telegram-blue?logo=telegram)](https://t.me/+j8SNSwhS7xk1NTc9)
![Docker Image Version](https://img.shields.io/docker/v/chenyme/chenyme-aavt?logo=docker&color=blue&link=https%3A%2F%2Fhub.docker.com%2Flayers%2Fchenyme%2Fchenyme-aavt%2Fv0.9.0%2Fimages%2Fsha256-5f704a4a3aba20396ad0f3c94a1ffcd0b9d89d82a33aa1b16601fd7613a74e6c%3Fcontext%3Drepo)
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Kirie233/Chenyme-AAVT/blob/main/AAVT.ipynb)
</div>

---

> [!NOTE]
> 🌟 **如果本项目对您有帮助，记得 Star 🌟 支持一下吧~**
>
> 📝 **推荐识别时使用 Large 模型以获取更好的体验！由于正在备考，更新速度会放缓，感谢理解！** 
> 
> 📖 [**安装教程**](https://blog.chenyme.top/blog/aavt-install) | ❓ [ **常见问题**](https://blog.chenyme.top/blog/aavt-qa) | 💬 [ **电报群组**](https://t.me/+j8SNSwhS7xk1NTc9)

<br>

## 项目介绍
**Chenyme-AAVT 全自动视频翻译项目** 致力于提供一个简便高效且免费的媒体识别与翻译自动化流程，帮助您快速完成音视频字幕的识别、翻译和处理等多种功能，当然目前项目已经不仅仅是帮您识别并翻译声音，还可以自动化生成营销图文、对字幕单独翻译。计划未来会基于现有基本功能继续加入更多有意思的工具，比如 实时识别、口型校正、声音克隆、音色辨别 等等，敬请期待！

当前已支持的**基本**功能，非全部功能：

- 【[音频识别](?tab=readme-ov-file#音频识别)】|【[视频识别](?tab=readme-ov-file#视频识别)】|【[图文博客](?tab=readme-ov-file#图文博客)】|【[字幕翻译](?tab=readme-ov-file#字幕翻译)】|【[声音模拟](?tab=readme-ov-file#声音模拟)】

<br>

![20240820210851.jpg](https://github.com/Chenyme/Chenyme-AAVT/blob/main/cache/public/picture/home.jpg)

<br>

## 项目亮点

<details>
  <summary><b>👉 TODO | 待办事项</b></summary>
<br>

### 识别相关
- [x] 更换更快的Whisper项目
- [x] 支持本地模型加载
- [x] 支持个人微调Whisper模型
- [x] VAD辅助优化
- [x] 字词级断句优化
- [x] 更多的语种识别
- [ ] 音色辨别
- [ ] 实时语音翻译

### 翻译相关
- [x] 翻译优化
- [x] 更多的语种翻译
- [x] 更多的翻译模型
- [x] 更多的翻译引擎
- [x] 支持本地大语言模型翻译

### 视频相关
- [x] 个性化字幕
- [x] 更多字幕格式
- [x] 字幕预览、实时修改
- [ ] 自动化字幕文本校对
- [ ] 双字幕
- [ ] 视频中文配音
- [ ] 声音克隆
- [ ] 口型校对

#### 图文博客
- [x] 生成图文
- [ ] 更多写作风格
- [ ] 优化生成效率
- [ ] 提高成品率

### 其他
- [x] AI助手
- [x] 视频预览

</details>

- 支持识别和翻译**多种语言**
- 支持 **全流程本地化、免费化部署**
- 支持对视频 **一键生成博客内容、营销图文**
- 支持 **自动化翻译**、**二次修改字幕**、**预览视频**
- 支持开启 **GPU 加速**、**VAD 辅助**、**FFmpeg 加速**
- 支持使用 **ChatGPT**、**Claude**、**Gemini**、**DeepSeek** 等众多大模型翻译引擎

<br>

> [!WARNING]
> ### 关于 dll 缺失的公告
>
> 以下解决方法经过本人验证可有效解决，**麻烦给颗🌟Star吧**!
>
> &nbsp;
> 
> #### 1. ❌ `fbgemm.dll` 缺失。此为 pytorch 对 win 的 mkl 文件构建错误，官方已在 2.4.1 Beta 版本中修正，请遇到后重新 Install.bat，并在菜单栏选择 修复版本（2.4.1）修正
>
> #### 2. ❌ `cudnn_ops_infer64_8.dll` 缺失，导致启用 GPU 失败。请前往 [Releases](https://github.com/Chenyme/Chenyme-AAVT/releases/tag/V0.9) 中下载 CUDA_dll.zip 压缩包解压到CUDA目录 `C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v12.4\bin` 修复

<br>

## Windows 部署
<details>
  <summary><b>👉 前置环境：Python、FFmpeg、CUDA 说明 </b></summary>
<br>
  
### Python | 📖 [教程](https://blog.chenyme.top/blog/aavt-install#47a521d01156)
  - 💡 选择 Python > 3.8 的版本
  - 前往 Python 官网下载 安装程序
  - 运行安装，在安装时请点击 ADD TO PATH 选项
### FFMpeg | 📖 [教程](https://blog.chenyme.top/blog/aavt-install#1897915fc461)
  - 💡 若您不知道如何安装编译，请直接在项目Release中的下载 `Win` 版本，自带编译后的FFMpeg
  - 前往 FFMpeg 官网下载编译好的 Windows 版本
  - 设置 FFmpeg 为环境变量
### CUDA(CPU 可忽略) | 📖 [教程](https://blog.chenyme.top/blog/aavt-install#1faea2d7295f)
  - 💡 推荐使用版本为 CUDA11.8、12.1、12.4
  - 前往 CUDA 官网下载 CUDA 安装程序
  - 安装 CUDA
## &nbsp;
</details>

<br>

> ‼️ 请确保前置环境已准备好后再继续下面的步骤‼️ 
> 
> ### 1. 运行部署脚本
>  - 前往 Release 页面下载 `Win` 的最新发行版 （Win/Small）
>  - 运行 `1_Install.bat`，等待脚本检查，通过后根据界面内提示选择版本安装
> ### 2. 运行项目Web
>  - 运行 `2_WebUI.bat`
>  - 等待 WebUI 自动拉起，或输入网址 `localhost:8501`
>  - 项目验证密码 `chenymeaavt`（此为新版本的保护功能，可关闭）

<br>

## Mac OS 部署
<details>
  <summary><b>👉 前置环境：Python、Brew、FFMpeg 说明 </b></summary>
<br>
  
### Python
  - 选择 Python > 3.8 的版本
  - 前往 Python 官网下载 PGK 安装包
  - 运行安装，页面内选择标准安装
### Brew
  - 💡 使用下面的命令进行一键安装安装 `brew`
    ```
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    ```
### FFMpeg
  - 💡 使用下面的命令进行一键安装安装 `FFMpeg`
    ```
    brew install FFMpeg
    ```
## &nbsp;
</details>

<br>

> ‼️ 请确保前置环境已准备好后再继续下面的步骤‼️
> ### 1. 安装项目依赖
> - 前往 Release 页面下载 `Mac` 的最新发行版 （Mac/Small）
> ```
> cd Chenyme-AAVT
> pip3 install -r requirements.txt
> ```
> ### 2. 运行项目Web
> ```
> streamlit run Chenyme-AAVT.py
> ```
> - 等待 WebUI 自动拉起，或输入网址 `localhost:8501`
> - 项目验证密码 `chenymeaavt`（此为新版本的保护功能，可关闭）

<br>

## Docker 部署
>![Docker Image Version](https://img.shields.io/docker/v/chenyme/chenyme-aavt?logo=docker&color=blue&link=https%3A%2F%2Fhub.docker.com%2Flayers%2Fchenyme%2Fchenyme-aavt%2Fv0.9.0%2Fimages%2Fsha256-5f704a4a3aba20396ad0f3c94a1ffcd0b9d89d82a33aa1b16601fd7613a74e6c%3Fcontext%3Drepo)
>
> 感谢 [@Eisaichen](https://github.com/Eisaichen) 协助构建此镜像

> ### docker
> ```
> docker pull chenyme/chenyme-aavt:latest
> ```
> - 完成后，输入 `<您的服务器IP>:8501` 访问
> - 项目验证密码 `chenymeaavt`（此为新版本的保护功能，可关闭）

> ### docker-compose
> ```
> git clone https://github.com/Chenyme/Chenyme-AAVT
> cd Chenyme-AAVT
> docker-compose up -d
> ```
> - 完成后，输入 `<您的服务器IP>:8501` 访问
> - 项目验证密码 `chenymeaavt`（此为新版本的保护功能，可关闭）

<br>

## Linux 部署
> 💡此版本为 AAVT V0.8.6 的 Linux CUDA 12.1 Docker 版本，最新版本为 V0.9.0
>
> 感谢 [@dhlsam](https://github.com/dhlsam) 提供此版本
>
> 具体使用方法，请查阅：📖 [issues/36](https://github.com/Chenyme/Chenyme-AAVT/issues/36#issuecomment-2284331590)

<br>

## Google Colab 部署
> [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Kirie233/Chenyme-AAVT/blob/main/AAVT.ipynb)
>
> 感谢 [@Kirie233](https://github.com/Kirie233) 提供 Colab 版本
>
> 具体使用方法，请查阅：📖 [AAVT.ipynb](https://github.com/Chenyme/Chenyme-AAVT/blob/main/AAVT.ipynb)


<br>

## 感谢项目的贡献者

[![][github-contrib-shield]][github-contrib-link]

<!-- LINK GROUP -->

[github-contrib-shield]: https://contrib.rocks/image?repo=Chenyme/Chenyme-AAVT
[github-contrib-link]: https://github.com/Chenyme/Chenyme-AAVT/graphs/contributors

<br>

## Star History

[![Star History Chart](https://api.star-history.com/svg?repos=Chenyme/Chenyme-AAVT&type=Timeline)](https://star-history.com/#Chenyme/Chenyme-AAVT&Timeline)

<br>

### 主页BOT

<br>

![11](https://github.com/Chenyme/Chenyme-AAVT/blob/main/cache/public/picture/bot.png)

<br>

### 部分设置

<br>

![12](https://github.com/Chenyme/Chenyme-AAVT/blob/main/cache/public/picture/setting.png)

<br>

### 音频识别

<br>

![13](https://github.com/Chenyme/Chenyme-AAVT/blob/main/cache/public/picture/audio.png)

<br>

### 视频识别

<br>

![14](https://github.com/Chenyme/Chenyme-AAVT/blob/main/cache/public/picture/video.png)

<br>

### 图文博客

<br>

![15](https://github.com/Chenyme/Chenyme-AAVT/blob/main/cache/public/picture/blog.png)

<br>

### 字幕翻译

<br>

![16](https://github.com/Chenyme/Chenyme-AAVT/blob/main/cache/public/picture/srt.png)

<br>

### 声音模拟

<br>

![17](https://github.com/Chenyme/Chenyme-AAVT/blob/main/cache/public/picture/opentts.png)

<br>

