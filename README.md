<div align="center">

<img src="https://img.picui.cn/free/2024/08/20/66c499e2c8e10.png" alt="chenymeaavtpng.png" title="chenymeaavtpng.png" width="75%" />

[![英文](https://img.shields.io/badge/%E8%8B%B1%E6%96%87-English-blue)](./README-EN.md)
[![下载](https://img.shields.io/github/downloads/Chenyme/Chenyme-AAVT/total.svg?style=flat-square&label=下载)](https://github.com/Chenyme/Chenyme-AAVT/releases)
[![群组](https://img.shields.io/badge/群组-Telegram-blue?logo=telegram)](https://t.me/+j8SNSwhS7xk1NTc9)
[![Latest Release](https://img.shields.io/github/v/release/Chenyme/Chenyme-AAVT.svg?style=flat-square)](https://github.com/Chenyme/Chenyme-AAVT/releases)
![PyPI - Version](https://img.shields.io/pypi/v/AAVT?logo=pypi)
[![License](https://img.shields.io/github/license/Chenyme/Chenyme-AAVT.svg?style=flat-square)](https://github.com/Chenyme/Chenyme-AAVT/blob/main/LICENSE)
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Kirie233/Chenyme-AAVT/blob/main/AAVT.ipynb)

</div>

---

> [!NOTE]
> 🌟 **如果本项目对您有帮助，记得 Star 🌟 支持一下吧~**
>
> 📝 **推荐识别时使用 Large 模型以获取更好的体验！由于正在备考，更新速度会放缓，感谢理解！** 
>
> 📖[**安装教程**](https://blog.chenyme.top/blog/aavt-install) | ❓ [ **常见问题**](https://blog.chenyme.top/blog/aavt-qa) | 💬 [ **电报群组**](https://t.me/+j8SNSwhS7xk1NTc9)

<br>

## 项目介绍
**Chenyme-AAVT 全自动视频翻译项目** 致力于提供一个简便高效且免费的媒体识别与翻译自动化流程，帮助您快速完成音视频字幕的识别、翻译和处理等多种功能，当然目前项目已经不仅仅是帮您识别并翻译声音，还可以自动化生成营销图文、对字幕单独翻译。计划未来会基于现有基本功能继续加入更多有意思的工具，比如 实时识别、口型校正、声音克隆、音色辨别 等等，敬请期待！

当前已完成的**基本**功能：

- 【音频识别】|【视频识别】|【字幕翻译】|【图文博客】|【声音模拟】|【批量翻译】

<br>

![20240820210851.jpg](https://img.picui.cn/free/2024/08/20/66c4959ec9c2d.jpg)

项目亮点：
- 支持识别和翻译**多种语言**
- 支持 **全流程本地化、免费化部署**
- 支持对视频 **一键生成博客内容、营销图文**
- 支持 **自动化翻译**、**二次修改字幕**、**预览视频**
- 支持开启 **GPU 加速**、**VAD 辅助**、**FFmpeg 加速**
- 支持使用 **ChatGPT**、**Claude**、**Gemini**、**DeepSeek** 等多家大模型翻译引擎


## 如何部署

### 在 Windows 中部署
> 📖[**安装教程**](https://blog.chenyme.top/blog/aavt-install)
>
> [**Release**](https://github.com/Chenyme/Chenyme-AAVT/releases) 中带有 `Full` 的是已打包了FFmpeg库的版本

### 1.手动部署

1. 安装 [Python](https://www.python.org/downloads/)，请确保Python版本大于3.8！
2. 安装 [FFmpeg](https://www.ffmpeg.org/download.html)，并设置为环境变量！
3. （CPU部署可忽略）安装 [CUDA](https://developer.nvidia.com/cuda-toolkit)，推荐版本为 CUDA11.8、12.1、12.4！
4. 运行 `0_Check.bat` 检查有哪些环境还没有正确安装！
5. (环境检查通过后) 运行 `install.bat`，选择您对应的版本继续安装！

### 使用 docker 部署
> 注：目前 项目最新版本为 V0.9.0 此 Docker 的版本为0.8.x
>
> 感谢 @Eisaichen 提供此版本

```
docker pull eisai/chenyme-aavt
```

具体使用方法，请查阅：[eisai/chenyme-aavt]([https://www.ffmpeg.org/download.html](https://hub.docker.com/r/eisai/chenyme-aavt))

### 使用 Google Colab
> 感谢 @Kirie233 提供此版本

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Kirie233/Chenyme-AAVT/blob/main/AAVT.ipynb)

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
