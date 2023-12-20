# Chenyme-AAMT V0.2.2

临近期末，项目得暂时搁置 T.T ，有问题欢迎提交议题，考完试会继续更新完善，非常抱歉呜呜呜！>_<


---

非常感谢您来到我的 Chenyme-AAMT V0.2.2 项目！该项目旨在提供一个简单易用的全自动视频翻译工具，帮助您快速识别声音并翻译生成 SRT 字幕，然后将翻译后的 SRT 字幕与原视频合并，以便您更快速的实现视频翻译。


![image](https://github.com/Chenyme/Chenyme-AAMT/assets/118253778/eba25a5d-d9b0-4128-a141-6a8a0667962c)


## 如何安装
### 更快速的安装（省去下载FFmpeg）
**见**[releases](https://github.com/Chenyme/Chenyme-AAMT/releases)
### 正常安装

本项目需要依赖 Python 环境和 FFmpeg。

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



## 如何使用


1. **设置参数**
- 在`config`内设置 `OPENAI_API_KEY`
- 您也可以在网页中设置OPENAI参数，但这不会保存到下一次的使用中去。
     
![image](https://github.com/Chenyme/Chenyme-AAMT/assets/118253778/375992c2-a219-4640-8341-eb324694f923)

2. **运行程序**
- 运行 `webui.bat`
- 等待网页跳转，如果没有跳转请自行在浏览器输入http://localhost:8501/
- 在侧边栏输入你的 `API_KEY`，若要使用代理请输入 `API_BASE`
- 上传文件，设置模型，运行程序，耐心等待处理


## 注意事项

1. 请确保您的系统已经正确安装了 `Python`，并且版本号为 3.8 或更高。
2. 请确保已经安装了 `FFmpeg`，并设置 `FFmpeg` 为环境变量。
3. 请确保运行 `install.bat`，安装所有依赖库。


## TODO

### 识别相关
- [ ] 更换更快的Whisper项目
- [ ] 支持个人微调Whisper模型
- [ ] 自动匹配识别模型
- [ ] 字词级断句优化
- [ ] 更多的语种识别

### 翻译相关
- [ ] ChatGPT翻译优化
- [ ] 更多的语种翻译
- [ ] 更多的翻译模型

### 字幕相关
- [ ] 双字幕
- [ ] 更多字幕格式
- [ ] 字幕预览、实时修改
- [ ] 自动化字幕文本校对
- [ ] 个性化字幕

### 其他
- [ ] 视频总结、罗列重点
- [ ] 实时语音翻译
- [ ] 视频中文配音

---

## 特别鸣谢
本人是 AI 时代的受益者，本项目的开发基本是站在巨人的肩膀上实现的。主要基于 OpenAI 开发的 Whisper 来识别声音和 ChatGPT辅助翻译字幕 ，利用 Streamlit 搭建快速使用的 WebUI 界面，以及 FFmpeg 来实现字幕与视频的合并。

### 非常感谢 OpenAI 、 Streamlit 、 FFmpeg 的开发人员！

#### 如有问题和建议，随时联系我!
