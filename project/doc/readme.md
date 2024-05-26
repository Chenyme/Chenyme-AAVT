https://zwho5v3j233.feishu.cn/wiki/OGcrwinzhi88MkkvEMVcLkDgnzc?from=from_copylink
项目介绍
项目名称： 全自动视频翻译

项目描述：
全自动视频翻译（AAVT）是一款基于AI技术的视频翻译工具。该工具旨在提供一站式的视频翻译解决方案，支持多种视频格式和语言的自动识别、翻译和字幕生成。项目主要特点包括：

支持OpenAI Whisper API和本地Faster Whisper模型的调用。
提供多种翻译引擎，包括OpenAI GPT、KIMI、ChatGLM和DeepSeek等。
能够生成多种字幕格式（SRT、ASS、STL等）。
支持GPU加速和VAD（语音活动检测）辅助。
使用说明
环境配置
安装依赖项
确保安装了以下依赖项：

Python
Streamlit
Streamlit Antd Components
OpenAI
MoviePy
Faster Whisper
FFmpeg
配置文件
项目配置文件存放在config/目录下，包括API密钥和模型配置。主要配置文件为api.toml和video.toml。

使用步骤
启动项目
运行以下命令启动Streamlit应用：

sh
复制代码
streamlit run app.py
上传视频文件
在侧边栏上传需要翻译的视频文件，支持的格式包括mp4、mov、avi、m4v、webm、flv、ico等。

选择模型和设置参数
根据需求选择使用的识别和翻译模型，可以选择OpenAI API接口调用或本地Faster Whisper模型。配置参数包括：

识别设置：选择Whisper模式（API调用或本地部署）、GPU加速、VAD辅助、视频语言等。
翻译设置：选择翻译引擎（如ChatGPT、Kimi、ChatGLM等），设置原始语言和目标语言、翻译间隔等。
字幕设置：选择字幕模式（硬字幕或软字幕）、字体、字体大小、字体颜色等。
高级设置：包括VAD静音检测、束搜索大小、Whisper提示词、翻译最大token限制等。
生成字幕
在“生成字幕”选项卡中，点击“一键生成视频”按钮，开始视频提取、识别、翻译和字幕生成的过程。生成完成后，可以下载生成的字幕文件和处理后的视频。

注意事项
API调用限制：使用API时需注意调用频率限制，避免出现RateLimitError错误。
本地模型加载：若选择本地模型加载模式，请确保模型文件正确下载和配置。
FFmpeg状态：确保FFmpeg和CUDA状态正常，以支持GPU加速和视频合成。
希望这份详细的项目介绍和使用说明能帮助您更好地了解和使用AAVT项目。如有任何问题，请查阅项目文档或联系项目维护者。

常见问题报告（FAQ）
1. 如何安装和配置AAVT项目？
回答：

安装依赖项：确保安装Python、Streamlit、Streamlit Antd Components、OpenAI、MoviePy、Faster Whisper和FFmpeg。
配置文件：编辑config/目录下的api.toml和video.toml文件，填入相应的API密钥和模型配置。
2. 支持哪些视频格式？
回答：

AAVT支持多种视频格式，包括mp4、mov、avi、m4v、webm、flv和ico等。
3. 如何选择识别和翻译模型？
回答：

在侧边栏的“识别设置”中，可以选择Whisper模式（OpenAI API接口调用或本地Faster Whisper模型）。
在“翻译设置”中，选择需要使用的翻译引擎（如ChatGPT、Kimi、ChatGLM、DeepSeek等），并设置原始语言和目标语言。
4. 为什么生成字幕时会出现RateLimitError错误？
回答：

这是由于API调用频率超过限制导致的。可以在“翻译设置”中适当增加翻译间隔（wait time），以减少API调用频率。
5. 如何解决GPU加速和CUDA问题？
回答：

确保系统已正确安装CUDA和Pytorch，并在配置文件中启用GPU加速。如果仍然无法使用GPU，可以检查CUDA和Pytorch的安装是否成功。
6. 如何处理本地模型加载问题？
回答：

确保本地模型文件已正确下载并存放在指定目录。在侧边栏的“识别设置”中选择本地模型加载模式，并指定正确的模型路径。
7. 生成字幕文件支持哪些格式？
回答：

AAVT支持生成多种字幕格式，包括SRT、ASS、STL和VTT等。
8. 如何查看和下载生成的字幕文件？
回答：

在生成字幕的过程中，生成的字幕文件会存放在指定的输出目录中。完成后，可以在侧边栏下载生成的字幕文件。
9. 为什么生成的视频无法预览？
回答：

可能是由于FFmpeg或CUDA状态异常导致的。请确保FFmpeg已正确安装，并检查CUDA状态。如果CUDA不可用，可以选择使用CPU模式生成视频。
10. 如何解决项目运行中的闪退问题？
回答：

可以查阅https://zwho5v3j233.feishu.cn/wiki/OGcrwinzhi88MkkvEMVcLkDgnzc?from=from_copylink或者在使用修复功能。如果问题仍未解决，请前往环境目录删除/Lib/site-packages/torch/lib/libiomp5md.dll文件。
如有其他问题，请查阅项目文档或联系项目维护者。