# Chenyme-AAVT V0.4

[![简体中文 badge](https://img.shields.io/badge/%E7%AE%80%E4%BD%93%E4%B8%AD%E6%96%87-Simplified%20Chinese-blue)](./README.md)
[![英文 badge](https://img.shields.io/badge/%E8%8B%B1%E6%96%87-English-blue)](./README-EN.md)
[![下载 Download](https://img.shields.io/github/downloads/Chenyme/Chenyme-AAVT/total.svg?style=flat-square)](https://github.com/Chenyme/Chenyme-AAVT/releases)

> AI Auto Vedio Translation

Thank you very much for visiting my AI Auto Video Translation V0.4 project! This project aims to provide an easy-to-use, fully automatic video translation tool to help you quickly recognize voices and translate subtitles, then merge the translated subtitles with the original video, allowing you to achieve video translation more efficiently.

![../public/photo1.png](https://github.com/Chenyme/Chenyme-AAMT/blob/main/public/photo1.png)

## Project Highlights
- Supports `faster-whisper` backend
- GPU acceleration support
- Supports `ChatGPT` and `KIMI` translations
- Supports multiple language recognition and translation
- Supports various subtitle format outputs
- Subtitle and video preview support

## How to Install
### Faster Installation (Skipping FFmpeg Download)
**See** [releases](https://github.com/Chenyme/Chenyme-AAMT/releases)
### Standard Installation

This project depends on the Python environment and FFmpeg, and may use CUDA and PyTorch.

1. **Install Python Environment**
   - You need to install Python 3.8 or higher.
   - You can download and install the latest version of Python from [Python's official website](https://www.python.org/downloads/).

2. **Install FFmpeg**
   - You need to install FFmpeg.
   - You can download and install FFmpeg from [FFmpeg's official website](https://www.ffmpeg.org/download.html).

3. **Set FFmpeg as an Environment Variable**
   - Press `Win+R` to open the Run dialog.
   - Type `rundll32 sysdm.cpl,EditEnvironmentVariables` in the pop-up box, then click OK.
   - Find `Path` in the user variables above and double-click it.
   - Click New and enter the path where you downloaded FFmpeg. Example: `D:\APP\ffmpeg` (Please adjust according to your actual path!).

4. **Run `install.bat`**
   - Run `install.bat` in the project root directory to install all dependencies.

## How to Use

1. **Set Parameters**
   - Set `OPENAI_API_KEY`, `OPENAI_BASE_URL`, `KIMI_API_KEY` in `config` to use the translation engines.
   - You can also set various parameters on the web page. The current version can automatically save them to `config`, so there's no need to reset.

![../public/photo2.png](https://github.com/Chenyme/Chenyme-AAMT/blob/main/public/photo2.png)

2. **Run the Program**
   - Run `webui.bat`.
   - Wait for the webpage to redirect. If it doesn't, manually enter http://localhost:8501/ in your browser.
   - If it's your first time using Streamlit, you may be asked to enter an email. Simply press `Enter` to skip.
   - Upload files, set the model, run the program, and wait patiently for processing.

## Prerequisites

1. Ensure your system has `Python` installed correctly, with a version number of 3.8 or higher.
2. Ensure `FFmpeg` is installed and set as an environment variable.
3. Ensure to run `install.bat` to install all dependencies.

## TODO

### Recognition Related
- [x] Switch to a faster Whisper project
- [ ] Support for personal fine-tuning of the Whisper model
- [ ] Automatic matching of recognition models
- [ ] VAD assistance optimization
- [x] Sentence breaking optimization at word level
- [x] More language recognition

### Translation Related
- [x] ChatGPT translation optimization
- [x] More language translations
- [x] More translation models
- [ ] More translation engines

### Subtitle Related
- [ ] Dual subtitles
- [x] More subtitle formats
- [x] Subtitle preview and real-time modification*
- [ ] Automated subtitle text proofreading
- [ ] Personalized subtitles

### Others
- [ ] Video summarization and key points listing
- [ ] Real-time voice translation
- [ ] Video dubbing in Mandarin
- [x] Video preview
- [x] AI assistant*

### Note: Features marked with `*` are still unstable and may have some bugs.

---

## Special Thanks
I am a beneficiary of the AI era, and the development of this project is largelybuilt on the shoulders of giants. It is primarily based on OpenAI's Whisper for voice recognition and LLMs for subtitle translation assistance, utilizes Streamlit for a fast-to-use WebUI interface, and employs FFmpeg for merging subtitles with videos.

### A huge thank you to the developers at OpenAI, Streamlit, FFmpeg, Faster-whisper, and Kimi!

#### If you have any questions or suggestions, please feel free to contact me!
