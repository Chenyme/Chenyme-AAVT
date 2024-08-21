<div align="center">

<img src="https://github.com/Chenyme/Chenyme-AAVT/blob/main/cache/public/picture/chenymeaavt1.png" title="chenymeaavt.png" width="80%" />

<br>
<br>

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

当前已支持的**基本**功能，非全部功能：

- 【[音频识别](?tab=readme-ov-file#音频识别)】|【[视频识别](?tab=readme-ov-file#视频识别)】|【[图文博客](?tab=readme-ov-file#图文博客)】|【[字幕翻译](?tab=readme-ov-file#字幕翻译)】|【[声音模拟](?tab=readme-ov-file#声音模拟)】

<br>

![20240820210851.jpg](https://github.com/Chenyme/Chenyme-AAVT/blob/main/cache/public/picture/home.jpg)

<br>

## 项目亮点

<details>
  <summary><b>📃 TODO | 待办</b></summary>

<br>

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
- [x] AI助手
- [x] 视频预览
- [x] 视频生成博客
- [ ] 实时语音翻译
- [ ] 视频中文配音
- [ ] 音色辨别
- [ ] 声音克隆
- [ ] 口型校对

</details>

- 支持识别和翻译**多种语言**
- 支持 **全流程本地化、免费化部署**
- 支持对视频 **一键生成博客内容、营销图文**
- 支持 **自动化翻译**、**二次修改字幕**、**预览视频**
- 支持开启 **GPU 加速**、**VAD 辅助**、**FFmpeg 加速**
- 支持使用 **ChatGPT**、**Claude**、**Gemini**、**DeepSeek** 等众多大模型翻译引擎

<br>

## Windows 部署
> 💡 注：请确保安装前前置环境就绪后再运行 install.bat！


<br>

<details>
  <summary><b>ℹ️ 前置环境：Python、FFmpeg、CUDA 说明 </b></summary>
<br>

### Python | 📖 [教程](https://blog.chenyme.top/blog/aavt-install#47a521d01156)
  - 💡 Python > 3.8 的版本
  - 前往 Python 官网下载 安装程序
  - 运行安装，在安装时请点击 ADD TO PATH 选项
### FFMpeg | 📖 [教程](https://blog.chenyme.top/blog/aavt-install#1897915fc461)
  - 💡 若您不知道如何安装编译，请在项目Release中的下载 `Full` 版本，自带编译后的FFMpeg
  - 前往 FFMpeg 官网下载编译好的 Windows 版本
  - 设置 FFmpeg 为环境变量
### CUDA(CPU 可忽略) | 📖 [教程](https://blog.chenyme.top/blog/aavt-install#1faea2d7295f)
  - 💡 推荐使用版本为 CUDA11.8、12.1、12.4
  - 前往 CUDA 官网下载 CUDA 安装程序
  - 安装 CUDA
## &nbsp;
</details>


#### 运行 `1_Install.bat`
  -  脚本会先检测是否成功配置 Python、FFMpeg 
  -  脚本检查通过后，根据界面内提示选择版本
  -  等待脚本执行安装完成

#### 运行 `2_WebUI.bat` 启动项目

<br>

## Docker 部署
> 💡 目前 项目最新版本为 V0.9.0 此 Docker 方法的版本为 V0.8.x，
>
> 感谢 @Eisaichen 提供此版本

具体使用方法，请查阅：📖 [eisai/chenyme-aavt]([https://www.ffmpeg.org/download.html](https://hub.docker.com/r/eisai/chenyme-aavt))

```
docker pull eisai/chenyme-aavt
```
<br>


## Google Colab 部署
> 感谢 @Kirie233 提供此版本


具体使用方法，请查阅：📖 [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Kirie233/Chenyme-AAVT/blob/main/AAVT.ipynb)，

<br>

## Mac os 部署

已支持，近期会写教程

<br>

## 其他环境部署

### Linux

由于近期那台电脑丢在学校，暂时没研究，其实我觉得解决 FFMpeg 和 Cuda，应该就没问题了

<br>

## Star History

[![Star History Chart](https://api.star-history.com/svg?repos=Chenyme/Chenyme-AAVT&type=Timeline)](https://star-history.com/#Chenyme/Chenyme-AAVT&Timeline)

<br>

### 主页BOT

![11](https://github.com/Chenyme/Chenyme-AAVT/blob/main/cache/public/picture/bot.png)

<br>

### 部分设置

![12](https://github.com/Chenyme/Chenyme-AAVT/blob/main/cache/public/picture/setting.png)

<br>

### 音频识别

![13](https://github.com/Chenyme/Chenyme-AAVT/blob/main/cache/public/picture/audio.png)

<br>

### 视频识别

![14](https://github.com/Chenyme/Chenyme-AAVT/blob/main/cache/public/picture/video.png)

<br>

### 图文博客

![15](https://github.com/Chenyme/Chenyme-AAVT/blob/main/cache/public/picture/blog.png)

<br>

### 字幕翻译

![16](https://github.com/Chenyme/Chenyme-AAVT/blob/main/cache/public/picture/srt.png)

<br>

### 声音模拟

![17](https://github.com/Chenyme/Chenyme-AAVT/blob/main/cache/public/picture/opentts.png)

<br>