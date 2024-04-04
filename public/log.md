#### v0.6.3 更新日志


##### Whisper相关
- 优化faster-whisper模型设置。
- 新增多个whisper识别模型（仅支持`faster-whisper`）。
  - `tiny.en`
  - `base.en`
  - `small.en`
  - `medium.en`
  - `distil-small.en`
  - `distil-medium.en`
  - `distil-large-v2`
- 修复更改模型时触发错误的问题。
- 修复本地模型调用冲突。


---

##### 字幕相关
- 支持输出软字幕。
- 修改SRT字幕保存格式。
- 修复ASS字幕字体格式未写入的问题。


---

##### 其他
- 音频助手支持`gpt-4`模型。
- 更新全局缓存内容。
- 优化`toml`配置内容。
- 优化`音频`界面的使用。
- 移除`音频`界面的对比功能。
- 重写项目部分功能的使用说明。
- 修复二次生成失败的问题。
- 修复二次生成视频无法重新加载的问题。

