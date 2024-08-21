<div align="center">

<img src="https://github.com/Chenyme/Chenyme-AAVT/blob/main/cache/public/picture/chenymeaavt1.png" title="chenymeaavt.png" width="80%" />

<br>
<br>

[![English](https://img.shields.io/badge/English-blue)](./README-EN.md)
[![Downloads](https://img.shields.io/github/downloads/Chenyme/Chenyme-AAVT/total.svg?style=flat-square&label=Downloads)](https://github.com/Chenyme/Chenyme-AAVT/releases)
[![Telegram Group](https://img.shields.io/badge/Group-Telegram-blue?logo=telegram)](https://t.me/+j8SNSwhS7xk1NTc9)
[![Latest Release](https://img.shields.io/github/v/release/Chenyme/Chenyme-AAVT.svg?style=flat-square)](https://github.com/Chenyme/Chenyme-AAVT/releases)
![PyPI - Version](https://img.shields.io/pypi/v/AAVT?logo=pypi)
[![License](https://img.shields.io/github/license/Chenyme/Chenyme-AAVT.svg?style=flat-square)](https://github.com/Chenyme/Chenyme-AAVT/blob/main/LICENSE)
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Kirie233/Chenyme-AAVT/blob/main/AAVT.ipynb)

</div>

---

> [!NOTE]
> 🌟 **If this project is helpful to you, please give it a Star 🌟 as support~**
>
> 📝 **It's recommended to use the Large model for recognition to get a better experience! Due to upcoming exams, updates will be slower, thanks for your understanding!** 
>
> 📖[**Installation Guide**](https://blog.chenyme.top/blog/aavt-install) | ❓ [**FAQ**](https://blog.chenyme.top/blog/aavt-qa) | 💬 [**Telegram Group**](https://t.me/+j8SNSwhS7xk1NTc9)

<br>

## Project Overview
The **Chenyme-AAVT (AI Automatic Audio(Media) Translation)** project aims to provide a simple, efficient, and free media recognition and translation automation process. It helps you quickly complete tasks such as subtitle recognition, translation, and processing of audio and video. Currently, the project has evolved beyond just recognizing and translating sound. It can also automatically generate marketing content and individually translate subtitles. In the future, more exciting tools will be added based on the existing core features, such as real-time recognition, lip-sync correction, voice cloning, timbre recognition, and more!

Here are some of the basic features currently supported (not all features are listed):

- 【[Audio Recognition](?tab=readme-ov-file#audio-recognition)】|【[Video Recognition](?tab=readme-ov-file#video-recognition)】|【[Blog Generation](?tab=readme-ov-file#blog-generation)】|【[Subtitle Translation](?tab=readme-ov-file#subtitle-translation)】|【[Voice Simulation](?tab=readme-ov-file#voice-simulation)】

<br>

![20240820210851.jpg](https://github.com/Chenyme/Chenyme-AAVT/blob/main/cache/public/picture/home.jpg)

<br>

## Project Highlights

<details>
  <summary><b>📃 TODO | Tasks</b></summary>

<br>

### Recognition-Related
- [x] Replace with faster Whisper project
- [x] Support local model loading
- [x] Support custom-tuning of Whisper model
- [x] VAD assistance optimization
- [x] Word-level segmentation optimization
- [x] More language recognition

### Translation-Related
- [x] Translation optimization
- [x] More language translations
- [x] More translation models
- [x] More translation engines
- [x] Support local large language model translation

### Subtitle-Related
- [x] Personalized subtitles
- [x] More subtitle formats
- [x] Subtitle preview and real-time editing
- [ ] Automated subtitle text proofreading
- [ ] Dual subtitles

### Others
- [x] AI assistant
- [x] Video preview
- [x] Video blog generation
- [ ] Real-time speech translation
- [ ] Chinese video dubbing
- [ ] Timbre recognition
- [ ] Voice cloning
- [ ] Lip-sync correction

</details>

- Supports recognition and translation of **multiple languages**
- Supports **full localization and free deployment**
- Supports **one-click blog content generation and marketing media** from videos
- Supports **automated translation**, **secondary subtitle modification**, and **video preview**
- Supports **GPU acceleration**, **VAD assistance**, and **FFmpeg acceleration**
- Supports translation engines such as **ChatGPT**, **Claude**, **Gemini**, **DeepSeek**, and more large models

<br>

## Windows Deployment
> 💡 Note: Ensure that the pre-requisites are set before running `install.bat`!


<br>

<details>
  <summary><b>ℹ️ Prerequisites: Python, FFmpeg, CUDA Guide</b></summary>
<br>

### Python | 📖 [Guide](https://blog.chenyme.top/blog/aavt-install#47a521d01156)
  - 💡 Version: Python > 3.8
  - Download the installation package from the official Python website
  - During installation, make sure to select the "ADD TO PATH" option
### FFMpeg | 📖 [Guide](https://blog.chenyme.top/blog/aavt-install#1897915fc461)
  - 💡 If you don’t know how to install and compile it, download the `Full` version from the project Release section, which includes a pre-compiled FFmpeg
  - Download the compiled version of FFmpeg for Windows from the official FFmpeg website
  - Set FFmpeg as an environment variable
### CUDA (Optional for CPU users) | 📖 [Guide](https://blog.chenyme.top/blog/aavt-install#1faea2d7295f)
  - 💡 Recommended versions are CUDA11.8, 12.1, 12.4
  - Download the CUDA installer from the official CUDA website
  - Install CUDA
## &nbsp;
</details>

#### Run `1_Install.bat`
  - The script will first check if Python and FFmpeg are properly configured
  - After the check passes, follow the on-screen instructions to select the version
  - Wait for the script to complete the installation

#### Run `2_WebUI.bat` to start the project

<br>

## Docker Deployment
> 💡 Currently, the latest project version is V0.9.0. The Docker method is for version V0.8.x.
>
> Thanks to @Eisaichen for providing this version

For detailed usage, please refer to: 📖 [eisai/chenyme-aavt](https://hub.docker.com/r/eisai/chenyme-aavt)

```shell
docker pull eisai/chenyme-aavt
```

<br>

## Google Colab Deployment
> Thanks to @Kirie233 for providing this version

For detailed usage, please refer to:  [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Kirie233/Chenyme-AAVT/blob/main/AAVT.ipynb)

<br>

## MacOS Deployment

Support is available. A tutorial will be written soon.

<br>

## Other Environments Deployment

### Linux

Due to my PC being left at school, I haven’t had a chance to investigate yet. However, solving FFmpeg and CUDA issues should resolve most problems.

<br>

## Star History

[![Star History Chart](https://api.star-history.com/svg?repos=Chenyme/Chenyme-AAVT&type=Timeline)](https://star-history.com/#Chenyme/Chenyme-AAVT&Timeline)

<br>

### Homepage BOT

![11](https://github.com/Chenyme/Chenyme-AAVT/blob/main/cache/public/picture/bot.png)

<br>

### Some Settings

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
