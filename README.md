# Chenyme-AAVT V0.7
> AI Auto Video(Audio) Translation

[![简体中文 badge](https://img.shields.io/badge/%E7%AE%80%E4%BD%93%E4%B8%AD%E6%96%87-Simplified%20Chinese-blue)](./README.md)
[![英文 badge](https://img.shields.io/badge/%E8%8B%B1%E6%96%87-English-blue)](./README-EN.md)
[![下载 Download](https://img.shields.io/github/downloads/Chenyme/Chenyme-AAVT/total.svg?style=flat-square)](https://github.com/Chenyme/Chenyme-AAVT/releases)

非常感谢您来到我的 AI Auto Video-Audio Translation 项目！该项目旨在提供一个简单易用的全自动视频（音频）识别、翻译工具，帮助您快速识别声音并翻译生成字幕文件，然后将翻译后的字幕与原视频合并，以便您更快速的实现视频翻译。

> - **Note ：字幕翻译的错位问题会逐步优化。由于考研，更新速度可能会放缓，感谢理解~~~**
> - **Tips：推荐选用 Faster-whisper 和 Large 模型以获得最好的断句、识别体验。**

#### 给一颗免费的星鼓励一下叭~感谢!!!

| 群聊二维码 | 说明 |
| ---- | ---- |
|<img src="https://github.com/Chenyme/Chenyme-AAVT/assets/118253778/993dcc53-03e1-4ab3-88e1-29dd43406949" alt="描述文字" width="70%" />| 我是一位学生，目前在备考可能不会及时看issues，还请多多担待。本项目开源，但由于个人技术水平有限，项目的很多地方还不尽人意，**在这里欢迎各位大佬和朋友加入群聊交流，有任何问题可以在群里提出**，让我们可以一起完善这个项目，感谢支持！|

![../public/photo5.png](https://github.com/Chenyme/Chenyme-AAVT/blob/main/public/photo5.png)

[测试效果 点击下载](https://github.com/Chenyme/Chenyme-AAVT/blob/main/public/test_vedio.mp4?raw=true)

## 项目亮点
> *   支持 `openai`调用和 `faster-whisper` 本地运行。
> *   支持 `GPU` 加速、`VAD`辅助。
> *   支持 `ChatGPT`、`KIMI`、`DeepSeek`翻译。
> *   支持本地大语言模型翻译。
> *   支持识别、翻译多种语言。
> *   支持输出多种字幕格式。
> *   支持对字幕修改、微调、预览。
> *   支持对音频直接进行AI总结、问答。


## 如何安装

<details open><summary><h3>使用 CPU 运行</h3></summary>

#### 1. 安装 [Python](https://www.python.org/downloads/) >= 3.8

#### 2. 安装 [FFmpeg](https://www.ffmpeg.org/download.html) , 并设置 FFmpeg 环境变量

- `Win+R` 快捷键打开运行对话框。
- 输入 `rundll32 sysdm.cpl,EditEnvironmentVariables`。
- 在用户变量中找到 `Path`。
- 点击新建，输入 FFmpeg 的路径。 示例：`D:\APP\ffmpeg`（请根据自己的实际路径调整）。

#### 3. 下载 依赖库
- 运行 `install.bat`，等待安装所有依赖库
- 运行 `webui.bat`，启动项目。

#

</details>

######

<details><summary><h3>使用 GPU 运行</h3></summary>

> 项目默认的 Pytorch 为CPU版本，若要使用 GPU，请重新安装 Pytorch

#### 1. 下载 CUDA
- 安装 [CUDA（必须12以上版本）](https://developer.nvidia.com/) 
- 对于 CUDA11，可以参考下方:`CUDA12 之前的版本如何使用`

#### 2. 安装 PyTorch

- 卸载之前的CPU版本（若已经运行过`install.bat`）

  ```py
  pip uninstall torch -y
  pip uninstall torchvision -y
  ```

- 安装**对应版本** [PyTorch](https://pytorch.org/)（请注意版本要和CUDA对应）

#### 3. CUDA12 之前的版本如何使用?

- 说明：由于Faster-whisper的最新版本仅支持 CUDA12。对于 CUDA11，当前的有效解决方法是降级ctranslate2。

  ```py
  pip install --force-reinsall ctranslate2==3.24
  ```

#

</details>


## 使用说明

1. **运行程序**
- 运行 `webui.bat`
- 等待网页跳转，如果没有跳转请自行在浏览器输入http://localhost:8501/
- 首次使用streamlit，可能会要求输入email，直接`Enter`跳过即可。

2. **设置项目参数**
- 在web页面中的设置界面，选择并配置好需要的 whisper识别模式、识别模型、API_key...。
- 目前可以自动保存到`config`中，下次启动无需重新设置。

## 注意事项

1. 请确保您的系统已经正确安装了 `Python`，并且版本号为 3.8 或更高。
2. 请确保已经安装了 `FFmpeg`，并设置 `FFmpeg` 为环境变量。
3. 请确保运行 `install.bat`，安装所有依赖库。
4. 使用 `GPU` 加速时请确保安装了正确的 `CUDA` 和 `Pytorch` 版本
5. 首次使用 Faster-whisper 模型时需下载模型，国内建议开启 VPN 下载。启用 GPU 加速需下载 CUDA 和 PyTorch，且保证PyTorch 版本与 CUDA 匹配，否则程序识别失败会默认禁用GPU加速。


## TODO

### 识别相关
- [x] 更换更快的Whisper项目
- [x] 支持本地模型加载
- [x] 支持个人微调Whisper模型
- [x] VAD辅助优化
- [x] 字词级断句优化
- [x] 更多的语种识别

### 翻译相关
- [x] ChatGPT翻译优化*
- [x] 更多的语种翻译
- [x] 更多的翻译模型
- [x] 更多的翻译引擎
- [x] 适配本地大语言模型接口

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
- [ ] 实时语音翻译
- [ ] 视频中文配音

### 注：含`*`的功能还不稳定，可能存在某些BUG。

## 特别鸣谢
本人是 AI 时代的受益者，本项目的开发基本是站在巨人的肩膀上实现的。主要基于 OpenAI 开发的 Whisper 来识别声音和 LLMs 辅助翻译字幕 ，利用 Streamlit 搭建快速使用的 WebUI 界面，以及 FFmpeg 来实现字幕与视频的合并。

### 非常感谢 OpenAI 、 Streamlit 、 FFmpeg 、Faster-whisper、kimi 等开发人员！

#### 如有问题和建议，随时联系我!

---

## 项目界面截图

### 主页面

![../public/photo1.png](https://github.com/Chenyme/Chenyme-AAVT/blob/main/public/photo1.png)

### 设置

![../public/photo2.png](https://github.com/Chenyme/Chenyme-AAVT/blob/main/public/photo2.png)

### 日志

![../public/photo3.png](https://github.com/Chenyme/Chenyme-AAVT/blob/main/public/photo3.png)

### 音频

![../public/photo6.png](https://github.com/Chenyme/Chenyme-AAVT/blob/main/public/phtot6.png)

### 视频
![../public/photo4.png](https://github.com/Chenyme/Chenyme-AAVT/blob/main/public/photo4.png)

### 视频生成

![../public/photo5.png](https://github.com/Chenyme/Chenyme-AAVT/blob/main/public/photo5.png)

### 视频二次修改
![../public/photo7.png](https://github.com/Chenyme/Chenyme-AAVT/blob/main/public/photo%20V0_6%202.png)
