### Chenyme-AAVT V0.6.4
> AI Auto Video(Audio) Translation

#### Note ：字幕翻译的错位问题会逐步优化。由于开始准备考研，更新速度可能会放缓，感谢理解~~~

非常感谢您来到我的 AI Auto Video-Audio Translation 项目！该项目旨在提供一个简单易用的全自动视频（音频）识别、翻译工具，帮助您快速识别声音并翻译生成字幕文件，然后将翻译后的字幕与原视频合并，以便您更快速的实现视频翻译。

> **Tips：推荐选用 Faster-whisper 和 Large 模型以获得最好的断句、识别体验。**

**注意：** 首次使用 Whisper 模型时需下载，国内建议开启 VPN 下载。启用 GPU 加速需下载 CUDA 和 PyTorch，且保证PyTorch 版本与 CUDA 匹配，否则程序识别失败会默认禁用GPU加速。

#### 给一颗免费的星鼓励一下叭~感谢!!!

![../public/photo5.png](https://github.com/Chenyme/Chenyme-AAVT/blob/main/public/photo5.png)

[测试效果 点击下载](https://github.com/Chenyme/Chenyme-AAVT/blob/main/public/test_vedio.mp4?raw=true)

---

##### 项目亮点
> - 支持 `faster-whisper` 后端。
> - 支持 `GPU` 加速。
> - 支持 `VAD` 辅助识别。
> - 支持 `ChatGPT`、`KIMI` 翻译。
> - 支持多种语言识别、翻译。
> - 支持多种字幕格式输出。
> - 支持字幕修改，二次精翻。
> - 支持字幕、视频预览。
> - 支持AI总结、问答。

##### 如何安装

###### 更快速的安装（省去下载FFmpeg）

**见**[releases](https://github.com/Chenyme/Chenyme-AAMT/releases)

###### 正常安装

本项目需要依赖 Python 环境和 FFmpeg,可能会用到 CUDA 和 PyTorch 。

1. **安装 Python 环境**
- 您需要安装 Python 3.8 或更高版本。
- 您可以从 [Python官网](https://www.python.org/downloads/) 下载并安装最新版本的 Python。

2. **安装 FFmpeg**
- 您需要安装 FFmpeg。
- 您可以从 [FFmpeg官网](https://www.ffmpeg.org/download.html) 下载并安装 FFmpeg。

3. **设置 FFmpeg 为环境变量**
- 按下 `Win+R` 快捷键打开运行对话框。
- 在弹出的框中输入 `rundll32 sysdm.cpl,EditEnvironmentVariables`，然后点击确定。
- 在上面的用户变量中找到 `Path`，双击。
- 点击新建，输入刚刚下载的 FFmpeg 的路径。示例：`D:\APP\ffmpeg`（请根据自己的实际路径调整！）。

4. **运行 `install.bat`**
- 在项目根目录下运行 `install.bat` 来安装所有依赖库。

---

#### Note ：项目默认的Pytorch为CPU版本，若要使用GPU，请下载 [CUDA（建议11.8）](https://developer.nvidia.com/cuda-11-8-0-download-archive) 并从 [PyTorch官网](https://pytorch.org/) 下载对应版本的Pytorch

---
##### 如何使用


1. **设置参数**
- 您可以在网页中设置各项参数，目前版本已经可以自动保存到`config`中，无需重新设置。
     
![Local Image](photo2.png)

2. **运行程序**
- 运行 `webui.bat`
- 等待网页跳转，如果没有跳转请自行在浏览器输入http://localhost:8501/
- 首次使用streamlit，可能会要求输入email，直接`Enter`跳过即可。
- 上传文件，设置模型，运行程序，耐心等待处理

---

##### 注意事项

1. 请确保您的系统已经正确安装了 `Python`，并且版本号为 3.8 或更高。
2. 请确保已经安装了 `FFmpeg`，并设置 `FFmpeg` 为环境变量。
3. 请确保运行 `install.bat`，安装所有依赖库。
4. 使用 `GPU` 加速时请确保安装了正确的 `CUDA` 和 `Pytorch` 版本
5. 推荐使用 `faster-whisper` 和 `Large` 模型，以获得最好的断句体验，但模型需要从 `Huggingface` 下载。

---

#### Todo

##### 识别相关
- [x] 更换更快的Whisper项目
- [x] 支持本地模型加载
- [x] 支持个人微调Whisper模型
- [x] VAD辅助优化
- [x] 字词级断句优化
- [x] 更多的语种识别

##### 翻译相关
- [x] ChatGPT翻译优化*
- [x] 更多的语种翻译
- [x] 更多的翻译模型
- [x] 更多的翻译引擎

##### 字幕相关
- [x] 个性化字幕
- [x] 更多字幕格式
- [x] 字幕预览、实时修改
- [ ] 自动化字幕文本校对
- [ ] 双字幕

##### 其他
- [x] 视频总结、罗列重点
- [x] 视频预览
- [x] AI助手
- [ ] 实时语音翻译
- [ ] 视频中文配音

##### 注：含`*`的功能还不稳定，可能存在某些BUG。

---

##### 特别鸣谢
本人是 AI 时代的受益者，本项目的开发基本是站在巨人的肩膀上实现的。主要基于 OpenAI 开发的 Whisper 来识别声音和 LLMs 辅助翻译字幕 ，利用 Streamlit 搭建快速使用的 WebUI 界面，以及 FFmpeg 来实现字幕与视频的合并。

###### 非常感谢 OpenAI 、 Streamlit 、 FFmpeg 、Faster-whisper、kimi的开发人员！

如有问题和建议，随时联系我!
