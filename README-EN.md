<div align="center">

<img src="https://github.com/Chenyme/Chenyme-AAVT/blob/main/cache/public/picture/chenymeaavt1.png" title="chenymeaavt.png" width="80%" />

<br>

[![English](https://img.shields.io/badge/%E8%8B%B1%E6%96%87-English-blue)](./README-EN.md)
[![Downloads](https://img.shields.io/github/downloads/Chenyme/Chenyme-AAVT/total.svg?style=flat-square&label=下载)](https://github.com/Chenyme/Chenyme-AAVT/releases)
[![Telegram Group](https://img.shields.io/badge/群组-Telegram-blue?logo=telegram)](https://t.me/+j8SNSwhS7xk1NTc9)
[![Latest Release](https://img.shields.io/github/v/release/Chenyme/Chenyme-AAVT.svg?style=flat-square)](https://github.com/Chenyme/Chenyme-AAVT/releases)
![PyPI - Version](https://img.shields.io/pypi/v/AAVT?logo=pypi)
[![License](https://img.shields.io/github/license/Chenyme/Chenyme-AAVT.svg?style=flat-square)](https://github.com/Chenyme/Chenyme-AAVT/blob/main/LICENSE)
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Kirie233/Chenyme-AAVT/blob/main/AAVT.ipynb)

</div>

---

> [!NOTE]
> 🌟 **If this project is helpful to you, don't forget to give it a Star 🌟!**
>
> 📝 **It's recommended to use the Large model for better recognition experience! Due to exam preparation, the update speed will be slower. Thank you for understanding!** 
>
> 📖[**Installation Guide**](https://blog.chenyme.top/blog/aavt-install) | ❓ [**FAQ**](https://blog.chenyme.top/blog/aavt-qa) | 💬 [**Telegram Group**](https://t.me/+j8SNSwhS7xk1NTc9)

<br>

## Project Introduction
**Chenyme-AAVT Automatic Video Translation Project** is dedicated to providing a simple, efficient, and free media recognition and translation automation process, helping you quickly complete a variety of functions such as audio and video subtitle recognition, translation, and processing. The project has evolved beyond just recognizing and translating audio; it can also automatically generate marketing content and translate subtitles separately. Future plans include adding more exciting tools based on the current functionality, such as real-time recognition, lip-sync correction, voice cloning, tone identification, and more. Stay tuned!

The currently completed **basic** features include:

- 【[Audio Recognition](#音频识别)】|【[Video Recognition](#视频识别)】|【[Subtitle Translation](#字幕翻译)】|【[Blog Generation](#图文博客)】|【[Voice Simulation](#声音模拟)】

<br>

![20240820210851.jpg](https://github.com/Chenyme/Chenyme-AAVT/blob/main/cache/public/picture/home.jpg)

<br>

## Project Highlights

<details>
  <summary><b>TODO | Pending Tasks</b></summary>

### Recognition Related
- [x] Replace with a faster Whisper project
- [x] Support local model loading
- [x] Support personal fine-tuning of Whisper models
- [x] VAD-assisted optimization
- [x] Word-level sentence segmentation optimization
- [x] More language recognition support

### Translation Related
- [x] Translation optimization
- [x] Support for more languages
- [x] More translation models
- [x] More translation engines
- [x] Support for local large language model translation

### Subtitle Related
- [x] Personalized subtitles
- [x] Support for more subtitle formats
- [x] Subtitle preview and real-time editing
- [ ] Automated subtitle proofreading
- [ ] Dual subtitles

### Others
- [x] AI Assistant
- [x] Video preview
- [x] Blog generation from videos
- [ ] Real-time voice translation
- [ ] Chinese video dubbing
- [ ] Tone identification
- [ ] Voice cloning
- [ ] Lip-sync correction

</details>

- Support for recognition and translation of **multiple languages**
- Support for **full localization and free deployment**
- Support for **one-click blog content and marketing material generation** from videos
- Support for **automated translation**, **secondary subtitle editing**, and **video preview**
- Support for enabling **GPU acceleration**, **VAD assistance**, and **FFmpeg acceleration**
- Support for using **ChatGPT**, **Claude**, **Gemini**, **DeepSeek**, and other large model translation engines

<br>

## How to Deploy

### Windows Deployment
📖[**Installation Guide**](https://blog.chenyme.top/blog/aavt-install) | Releases labeled `Full` include the FFmpeg library.

1. Install [Python](https://www.python.org/downloads/) (Ensure your Python version is above 3.8!)
   
2. Install [FFmpeg](https://www.ffmpeg.org/download.html) (Don't forget to add it to the system environment variables!)
   
3. Install [CUDA](https://developer.nvidia.com/cuda-toolkit) (Ignore for CPU deployment; recommended versions are CUDA 11.8, 12.1, or 12.4!)

4. Run `0_Check.bat` (Check for any missing environments to avoid errors)

5. Run `1_Install.bat` (After passing the environment check, select your corresponding version for installation)

6. Run `2_WebUI.bat` (Successful execution will launch the web interface)

<br>

### Docker Deployment
Note: The current project version is V0.9.0, while this Docker version is 0.8.x.

```shell
docker pull eisai/chenyme-aavt
```
For detailed usage instructions, please refer to: [eisai/chenyme-aavt](https://hub.docker.com/r/eisai/chenyme-aavt), special thanks to @Eisaichen for providing this version.

<br>

### Google Colab Deployment

Please click to read the relevant deployment guide | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Kirie233/Chenyme-AAVT/blob/main/AAVT.ipynb), special thanks to @Kirie233 for providing this version.

<br>

### Other Environment Deployments

- #### MacOS
In theory, MacOS deployment is feasible. The latest version has optimized parts incompatible with Mac. I don't have a Mac to test it, but many users in the Telegram group have successfully deployed it.

- #### Linux
I haven't tested it recently because my computer is at school, but solving FFmpeg and CUDA issues should make it work.

<br>

## Star History

[![Star History Chart](https://api.star-history.com/svg?repos=Chenyme/Chenyme-AAVT&type=Timeline)](https://star-history.com/#Chenyme/Chenyme-AAVT&Timeline)

<br>

### Home BOT

![11](https://github.com/Chenyme/Chenyme-AAVT/blob/main/cache/public/picture/bot.png)

<br>

### Settings Page

![12](https://github.com/Chenyme/Chenyme-AAVT/blob/main/cache/public/picture/setting.png)

<br>

### Audio Recognition

![13](https://github.com/Chenyme/Chenyme-AAVT/blob/main/cache/public/picture/audio.png)

<br>

### Video Recognition

![14](https://github.com/Chenyme/Chenyme-AAVT/blob/main/cache/public/picture/video.png)

<br>

### Blog Generation

![15](https://github.com/Chenyme/Chenyme-AAVT/blob/main/cache/public/picture/blog.png)

<br>

### Subtitle Translation

![16](https://github.com/Chenyme/Chenyme-AAVT/blob/main/cache/public/picture/srt.png)

<br>

### Voice Simulation

![17](https://github.com/Chenyme/Chenyme-AAVT/blob/main/cache/public/picture/opentts.png)

<br>

## Acknowledgements

I have greatly benefited from the AI era, and this project has largely been realized by standing on the shoulders of giants. Thanks to the open-source spirit, and thanks to the developers of OpenAI, Streamlit, FFmpeg, Faster-whisper, and more!