<div align="center">

<img src="https://github.com/Chenyme/Chenyme-AAVT/blob/main/cache/public/picture/chenymeaavt1.png" title="chenymeaavt.png" width="80%" />

<br>
<br>

[![中文](https://img.shields.io/badge/Chinese-中文-blue)](./README.md)
[![Downloads](https://img.shields.io/github/downloads/Chenyme/Chenyme-AAVT/total.svg?style=flat-square&label=Downloads)](https://github.com/Chenyme/Chenyme-AAVT/releases)
[![Telegram Group](https://img.shields.io/badge/Telegram-Group-blue?logo=telegram)](https://t.me/+j8SNSwhS7xk1NTc9)
[![Latest Release](https://img.shields.io/github/v/release/Chenyme/Chenyme-AAVT.svg?style=flat-square)](https://github.com/Chenyme/Chenyme-AAVT/releases)
![PyPI - Version](https://img.shields.io/pypi/v/AAVT?logo=pypi)
[![License](https://img.shields.io/github/license/Chenyme/Chenyme-AAVT.svg?style=flat-square)](https://github.com/Chenyme/Chenyme-AAVT/blob/main/LICENSE)
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Kirie233/Chenyme-AAVT/blob/main/AAVT.ipynb)

</div>

---

> [!NOTE]
> 🌟 **If this project helps you, please remember to give it a Star 🌟 for support!**
>
> 📝 **It is recommended to use the **Large** model for better experience.** 
>
> 📖 [**Installation Guide**](https://blog.chenyme.top/blog/aavt-install) | ❓ [**FAQ**](https://blog.chenyme.top/blog/aavt-qa) | 💬 [**Telegram Group**](https://t.me/+j8SNSwhS7xk1NTc9)

<br>

## Project Introduction
**Chenyme-AAVT Automatic Video Translation Project** aims to provide a simple, efficient, and free automation process for media recognition and translation, helping you quickly complete tasks such as audio and video subtitle recognition, translation, and processing. Currently, the project not only helps you recognize and translate sound but also automates the generation of marketing blog content, and even performs separate subtitle translations. Future plans include adding more interesting tools based on existing basic functions, such as real-time recognition, lip-sync correction, voice cloning, timbre differentiation, and more. Stay tuned!

Basic supported features, not all features:

- 【[Audio Recognition](?tab=readme-ov-file#audio-recognition)】|【[Video Recognition](?tab=readme-ov-file#video-recognition)】|【[Blog Generation](?tab=readme-ov-file#blog-generation)】|【[Subtitle Translation](?tab=readme-ov-file#subtitle-translation)】|【[Voice Simulation](?tab=readme-ov-file#voice-simulation)】

<br>

![20240820210851.jpg](https://github.com/Chenyme/Chenyme-AAVT/blob/main/cache/public/picture/home.jpg)

<br>

## Project Highlights

<details>
  <summary><b>📃 TODO | Tasks</b></summary>
<br>

### Recognition
- [x] Replaced with faster Whisper project
- [x] Supports local model loading
- [x] Supports personal fine-tuning of Whisper models
- [x] VAD-assisted optimization
- [x] Word-level sentence segmentation optimization
- [x] More language recognition

### Translation
- [x] Translation optimization
- [x] More language translations
- [x] More translation models
- [x] More translation engines
- [x] Supports local large language model translation

### Subtitles
- [x] Personalized subtitles
- [x] More subtitle formats
- [x] Subtitle preview, real-time editing
- [ ] Automated subtitle text proofreading
- [ ] Dual subtitles

### Other
- [x] AI Assistant
- [x] Video preview
- [x] Blog generation from videos
- [ ] Real-time voice translation
- [ ] Chinese voiceover for videos
- [ ] Timbre differentiation
- [ ] Voice cloning
- [ ] Lip-sync correction

</details>

- Supports recognition and translation of **multiple languages**
- Supports **localized, free deployment** of the entire process
- Supports **one-click generation of blog content, marketing blog** from videos
- Supports **automated translation**, **secondary subtitle editing**, **video preview**
- Supports **GPU acceleration**, **VAD assistance**, **FFmpeg acceleration**
- Supports using various large models like **ChatGPT**, **Claude**, **Gemini**, **DeepSeek** for translation engines

<br>

## Windows Deployment
<details>
  <summary><b>👉 Prerequisites: Python, FFmpeg, CUDA Instructions </b></summary>
<br>
  
### Python | 📖 [Guide](https://blog.chenyme.top/blog/aavt-install#47a521d01156)
  - 💡 Choose Python version > 3.8
  - Go to the official Python website to download the installer
  - Run the installation and make sure to check the ADD TO PATH option
### FFMpeg | 📖 [Guide](https://blog.chenyme.top/blog/aavt-install#1897915fc461)
  - 💡 If you are unsure how to install and compile, directly download the `Win` version from the project’s Release page, which comes with a pre-compiled FFmpeg
  - Go to the official FFmpeg website to download the compiled Windows version
  - Set FFmpeg as an environment variable
### CUDA (Skip for CPU) | 📖 [Guide](https://blog.chenyme.top/blog/aavt-install#1faea2d7295f)
  - 💡 Recommended versions are CUDA 11.8, 12.1, 12.4
  - Go to the CUDA website to download the installer
  - Install CUDA
## &nbsp;
</details>

<br>

> ‼️ Make sure the prerequisites are ready before proceeding to the following steps‼️ 
> ### 1. Run Deployment Script
>  - Go to the Release page to download the latest `Win` version (Win/Small)
>  - Run `1_Install.bat` and wait for the script to check
>  - After passing, follow the prompts to choose the version for installation
> ### 2. Run the Project Web
>  - Run `2_WebUI.bat`
>  - Enter `chenymeaavt` to access the project (this is a protection feature of the new version, can be turned off)
>
> &nbsp;
>
> ℹ️ **The WebUI will automatically launch, if it doesn’t, manually enter `localhost:8501` in your browser**

<br>

## Mac OS Deployment
<details>
  <summary><b>👉 Prerequisites: Python, Brew Instructions </b></summary>
<br>
  
### Python
  - 💡 Choose Python version > 3.8
  - Go to the Python website to download the PGK installer
  - Run the installation and select the standard install on the page
### Brew
  - 💡 Use the following command for one-click installation of `brew`
```
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```
## &nbsp;
</details>
<br>

> ‼️ Make sure the prerequisites are ready before proceeding to the following steps‼️ 
> ### 1. Install FFmpeg
> ```
> brew install FFMpeg
> ```
> ### 2. Install Project Dependencies
> - Go to the Release page to download the latest `Mac` version (Mac/Small)
> - cd to the project root directory
> ```
> pip3 install -r requirements.txt
> ```
> ### 3. Run the Project Web
> ```
> streamlit run Chenyme-AAVT.py
> ```
>  - Enter `chenymeaavt` to access the project (this is a protection feature of the new version, can be turned off)
>
> &nbsp;
>
> ℹ️ **The WebUI will automatically launch, if it doesn’t, manually enter `localhost:8501` in your browser**

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

## Other Deployment Methods

### Google Colab Deployment
> Thanks to @Kirie233 for providing this version

For detailed usage instructions, please refer to: [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Kirie233/Chenyme-AAVT/blob/main/AAVT.ipynb)

<br>

### Docker Deployment
> 💡 The current latest project version is V0.9.0. This Docker method is for version V0.8.x,
>
> Thanks to @Eisaichen for providing this version

```commandline
docker pull eisai/chenyme-aavt
```
For detailed usage instructions, please refer to: 📖 [eisai/chenyme-aavt](https://hub.docker.com/r/eisai/chenyme-aavt)

<br>

### Linux Deployment

> As my computer is currently left at school, I haven’t studied this yet. However, I believe solving FFmpeg and CUDA should work fine.

<br>

<br>


## Star History

[![Star History Chart](https://api.star-history.com/svg?repos=Chenyme/Chenyme-AAVT&type=Timeline)](https://star-history.com/#Chenyme/Chenyme-AAVT&Timeline)

<br>
<br>

### Homepage BOT

<br>

![11](https://github.com/Chenyme/Chenyme-AAVT/blob/main/cache/public/picture/bot.png)

<br>

### Some Settings

<br>

![12](https://github.com/Chenyme/Chenyme-AAVT/blob/main/cache/public/picture/setting.png)

<br>

### Audio Recognition

<br>

![13](https://github.com/Chenyme/Chenyme-AAVT/blob/main/cache/public/picture/audio.png)

<br>

### Video Recognition

<br>

![14](https://github.com/Chenyme/Chenyme-AAVT/blob/main/cache/public/picture/video.png)

<br>

### Blog Generation

<br>

![15](https://github.com/Chenyme/Chenyme-AAVT/blob/main/cache/public/picture/blog.png)

<br>

### Subtitle Translation

<br>

![16](https://github.com/Chenyme/Chenyme-AAVT/blob/main/cache/public/picture/srt.png)

<br>

### Voice Simulation

<br>

![17](https://github.com/Chenyme/Chenyme-AAVT/blob/main/cache/public/picture/opentts.png)

<br>

## Acknowledgements

I have greatly benefited from the AI era, and this project has largely been realized by standing on the shoulders of giants. Thanks to the open-source spirit, and thanks to the developers of OpenAI, Streamlit, FFmpeg, Faster-whisper, and more!
