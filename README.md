<div align="center">
  
# AI Auto Video(Audio) Translation 


[![简体中文 badge](https://img.shields.io/badge/%E7%AE%80%E4%BD%93%E4%B8%AD%E6%96%87-Simplified%20Chinese-blue)](./README.md)
[![英文 badge](https://img.shields.io/badge/%E8%8B%B1%E6%96%87-English-blue)](./README-EN.md)
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Kirie233/Chenyme-AAVT/blob/main/AAVT.ipynb)
[![Download](https://img.shields.io/github/downloads/Chenyme/Chenyme-AAVT/total.svg?style=flat-square)](https://github.com/Chenyme/Chenyme-AAVT/releases)
![PyPI - Version](https://img.shields.io/pypi/v/AAVT)
[![](https://img.shields.io/badge/Telegram-电报群组-blue.svg?logo=data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAyNCAyNCI+PHBhdGggZD0iTTEyIDI0YzYuNjI3IDAgMTItNS4zNzMgMTItMTJTMTguNjI3IDAgMTIgMCAwIDUuMzczIDAgMTJzNS4zNzMgMTIgMTIgMTJaIiBmaWxsPSJ1cmwoI2EpIi8+PHBhdGggZmlsbC1ydWxlPSJldmVub2RkIiBjbGlwLXJ1bGU9ImV2ZW5vZGQiIGQ9Ik01LjQyNSAxMS44NzFhNzk2LjQxNCA3OTYuNDE0IDAgMCAxIDYuOTk0LTMuMDE4YzMuMzI4LTEuMzg4IDQuMDI3LTEuNjI4IDQuNDc3LTEuNjM4LjEgMCAuMzIuMDIuNDcuMTQuMTIuMS4xNS4yMy4xNy4zMy4wMi4xLjA0LjMxLjAyLjQ3LS4xOCAxLjg5OC0uOTYgNi41MDQtMS4zNiA4LjYyMi0uMTcuOS0uNSAxLjE5OS0uODE5IDEuMjI5LS43LjA2LTEuMjI5LS40Ni0xLjg5OC0uOS0xLjA2LS42ODktMS42NDktMS4xMTktMi42NzgtMS43OTgtMS4xOS0uNzgtLjQyLTEuMjA5LjI2LTEuOTA4LjE4LS4xOCAzLjI0Ny0yLjk3OCAzLjMwNy0zLjIyOC4wMS0uMDMuMDEtLjE1LS4wNi0uMjEtLjA3LS4wNi0uMTctLjA0LS4yNS0uMDItLjExLjAyLTEuNzg4IDEuMTQtNS4wNTYgMy4zNDgtLjQ4LjMzLS45MDkuNDktMS4yOTkuNDgtLjQzLS4wMS0xLjI0OC0uMjQtMS44NjgtLjQ0LS43NS0uMjQtMS4zNDktLjM3LTEuMjk5LS43OS4wMy0uMjIuMzMtLjQ0Ljg5LS42NjlaIiBmaWxsPSIjZmZmIi8+PGRlZnM+PGxpbmVhckdyYWRpZW50IGlkPSJhIiB4MT0iMTEuOTkiIHkxPSIwIiB4Mj0iMTEuOTkiIHkyPSIyMy44MSIgZ3JhZGllbnRVbml0cz0idXNlclNwYWNlT25Vc2UiPjxzdG9wIHN0b3AtY29sb3I9IiMyQUFCRUUiLz48c3RvcCBvZmZzZXQ9IjEiIHN0b3AtY29sb3I9IiMyMjlFRDkiLz48L2xpbmVhckdyYWRpZW50PjwvZGVmcz48L3N2Zz4K)](https://t.me/+j8SNSwhS7xk1NTc9)



Chenyme-AAVT V0.8.5
</div>


非常感谢您来到我的 **全自动视频翻译** 项目！该项目旨在提供一个简单易用的自动识别、翻译工具和其他视频辅助工具，帮助快速识别视频字幕、翻译字幕、辅助图文。

> - **Note1 ：推荐选用 Faster-whisper 和 Large 模型以获得最好的断句、识别体验！**
> - **Note2 ：由于考研，更新速度可能会放缓，学业为重，感谢理解~~~ 大家有想法、有问题、想交流的朋友们可以加群一起讨论噢！**
> - **【紧急公告】Pytorch近期 2.4.x 版本，部分用户会直接报错：OSError找不到指定的模块fbgemm.dll，目前尚未知任何原因！**
> 
> 若发生此类错误，请尝试将对应的安装脚本(.bat文件)中的 torch 版本 修改为 2.3.1 并删除已安装 env 文件，重新运行安装脚本！
> 
> （示例）原：pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
> 
> （示例）改：pip install torch==2.3.1 torchvision==0.18.1 torchaudio==2.3.1 --index-url https://download.pytorch.org/whl/cu121


#### 给一颗免费的星支持一下叭~感谢！[AAVT安装教程](https://blog.chenyme.top/blog/aavt-install) | [AAVT项目文档](https://zwho5v3j233.feishu.cn/wiki/OGcrwinzhi88MkkvEMVcLkDgnzc?from=from_copylink) | [AAVT电报群组](https://t.me/+j8SNSwhS7xk1NTc9)

#### 本项目开源可魔改，发布请保留原作者 @chenyme 和 项目链接，感谢支持！请勿在任何平台收费项目源码！（代码这么烂也能收？）

由于微信群聊人数限制，入群请直接在电报私信我。
<br>




<img src="https://github.com/Chenyme/Chenyme-AAVT/assets/118253778/b20ddf3c-34c7-460b-bf98-fe66d856c6be" />


#### [测试效果 点击下载](https://github.com/Chenyme/Chenyme-AAVT/blob/main/public/test_vedio.mp4?raw=true)

## 项目亮点
> *   支持 **OpenAI API** 和 **Faster-Whisper** 识别后端。
> *   支持 **GPU 加速**、**VAD辅助**、**FFmpeg加速**。
> *   支持 **本地部署模型**、**ChatGPT**、**KIMI**、**DeepSeek**、**ChatGLM**、**Claude**等多种引擎翻译。
> *   支持识别、翻译 **多种语言** 和 **多种文件格式** 。
> *   支持对 **一键生成**、**字幕微调**、**视频预览**。
> *   支持对内容直接进行 **AI总结、问答**。
> *   支持视频 **生成图文博客**。


## 如何安装
> **修复闪退.bat请在 出现闪退/报错OMP/报错NoneType 的情况下 再运行，不要直接运行！**

### 使用 Windows

1. 安装 [Python](https://www.python.org/downloads/)，请确保Python版本大于3.8

2. 安装 [FFmpeg](https://www.ffmpeg.org/download.html)，[**Release**](https://github.com/Chenyme/Chenyme-AAVT/releases) 中`Full`版本已经打包了FFmpeg库

3. 运行 `install.bat`

### 使用 docker

```
docker pull eisai/chenyme-aavt
```

具体使用方法，请查阅：[eisai/chenyme-aavt]([https://www.ffmpeg.org/download.html](https://hub.docker.com/r/eisai/chenyme-aavt))

感谢 @Eisaichen 提供此版本

### 使用 Colab

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Kirie233/Chenyme-AAVT/blob/main/AAVT.ipynb)

感谢 @Kirie233 提供此版本

## TODO

### 识别相关
- [x] 更换更快的Whisper项目
- [x] 支持本地模型加载
- [x] 支持个人微调Whisper模型
- [x] VAD辅助优化
- [x] 字词级断句优化
- [x] 更多的语种识别

### 翻译相关
- [x] 翻译优化
- [x] 更多的语种翻译
- [x] 更多的翻译模型
- [x] 更多的翻译引擎
- [x] 支持本地大语言模型翻译

### 字幕相关
- [x] 个性化字幕
- [x] 更多字幕格式
- [x] 字幕预览、实时修改
- [ ] 自动化字幕文本校对
- [ ] 双字幕

### 其他
- [x] 视频总结、罗列重点
- [x] 视频预览
- [x] AI助手
- [x] 视频生成博客*
- [ ] 实时语音翻译
- [ ] 视频中文配音

##### 注：含`*`的功能还不稳定，可能存在某些BUG。

## Star History

[![Star History Chart](https://api.star-history.com/svg?repos=Chenyme/Chenyme-AAVT&type=Timeline)](https://star-history.com/#Chenyme/Chenyme-AAVT&Timeline)

## 项目界面预览

### 主页面

![1716910190616](https://github.com/Chenyme/Chenyme-AAVT/assets/118253778/0bfebaf3-53c5-42ae-8031-b898dc27df6f)

### 设置

![1716910203660](https://github.com/Chenyme/Chenyme-AAVT/assets/118253778/49b89451-1129-4073-b1b5-0094af65f53e)

### 视频识别

##### 参数设置

![d967ac4074d0c8ecba07b95de533730](https://github.com/Chenyme/Chenyme-AAVT/assets/118253778/72bc0e88-2148-486c-ac46-4f87a55e946b)

##### 运行界面

![b861c5019833b770f98344f7a4c73a4](https://github.com/Chenyme/Chenyme-AAVT/assets/118253778/ced915ec-a07b-43d2-9cf9-f92910033cb9)

##### 视频生成

![1716650985701](https://github.com/Chenyme/Chenyme-AAVT/assets/118253778/04bdf745-7ece-4c8b-a97b-f779b632dbc3)

##### 字幕微调

![1716651009788](https://github.com/Chenyme/Chenyme-AAVT/assets/118253778/33a02ef5-7386-4f34-ba0b-8947f17b78e3)

### 内容助手

##### 参数设置

![461474f5d96b61b70bd239a9e3ddf8d](https://github.com/Chenyme/Chenyme-AAVT/assets/118253778/f22a11c2-3c58-4a92-ab4c-954e3710a254)

##### 运行界面

![14575fd5efbe138f364329626501b09](https://github.com/Chenyme/Chenyme-AAVT/assets/118253778/8a81ea44-95ae-488f-9412-014ff1c030e3)

### 字幕翻译

![35bc5a96676c7f2b9d71042eb7c877f](https://github.com/Chenyme/Chenyme-AAVT/assets/118253778/635865b1-6ec1-41fd-858c-e1dcc87d684b)


### 视频博客

![09f60b8099f8ce19b83f4da63b26817](https://github.com/Chenyme/Chenyme-AAVT/assets/118253778/bbfca353-53d4-4a19-994f-7beddbbf17d7)


## 鸣谢

#### 本人是 AI 时代的受益者，本项目的开发基本是站在巨人的肩膀上实现的。主要基于 OpenAI 开发的 Whisper 来识别声音和 LLMs 辅助翻译字幕 ，利用 Streamlit 搭建快速使用的 WebUI 界面，以及 FFmpeg 来实现字幕与视频的合并。
#### 非常感谢 OpenAI 、 Streamlit 、 FFmpeg 、Faster-whisper 等开发人员！
