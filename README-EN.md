<div align="center">

# AI Auto Video(Audio) Translation

[![Simplified Chinese badge](https://img.shields.io/badge/Simplified%20Chinese-Simplified%20Chinese-blue)](./README.md)
[![English badge](https://img.shields.io/badge/English-English-blue)](./README-EN.md)
[![Download](https://img.shields.io/github/downloads/Chenyme/Chenyme-AAVT/total.svg?style=flat-square)](https://github.com/Chenyme/Chenyme-AAVT/releases)
![PyPI - Version](https://img.shields.io/pypi/v/AAVT)

Chenyme-AAVT V0.8.3
</div>

Thank you very much for coming to my **Automatic Video Translation** project! This project aims to provide a simple and easy-to-use automatic video (audio) recognition and translation tool to help you quickly recognize video subtitles and generate subtitle files, and then merge the translated subtitles with the original video for quick video translation.

> - **Note0: The subtitle translation misalignment issue will be gradually optimized. Due to postgraduate studies, the update speed may slow down, thank you for your understanding~~~**
> - **Note1: It is recommended to use the Faster-whisper and Large models for the best sentence breaking and recognition experience!**
> - **Note2: The new version has significant changes and many bugs, so updates are frequent recently, it is recommended to update!**
> - **Note3: After this version stabilizes, updates will slow down, studies are important, if you have any questions, you can join the group to discuss!**

#### This update really took a long time! Give a free star to encourage it~ Thank you! [AAVT Project Documentation](https://zwho5v3j233.feishu.cn/wiki/OGcrwinzhi88MkkvEMVcLkDgnzc?from=from_copylink)

<table>
  <tr>
    <td><img src="https://github.com/Chenyme/Chenyme-AAVT/assets/118253778/ecbde183-d4e5-413e-a584-d3762cd79d5d" /></td>
    <td><img src="https://github.com/Chenyme/Chenyme-AAVT/assets/118253778/b20ddf3c-34c7-460b-bf98-fe66d856c6be" /></td>
  </tr>
</table>


#### [Test effect click to download](https://github.com/Chenyme/Chenyme-AAVT/blob/main/public/test_vedio.mp4?raw=true)

## Project Highlights
> * Supports **OpenAI API interface calls** and **Faster-Whisper local operation**.
> * Supports **GPU acceleration**, **VAD assistance**.
> * Supports various translation modes such as **ChatGPT**, **KIMI**, **DeepSeek**, **ChatGLM**, **locally deployed models**.
> * Supports **adjusting various parameters** to meet customized needs.
> * Supports recognition and translation of **multiple languages** and **multiple file formats**.
> * Supports **one-click generation** of processed content.
> * Supports **subtitle modification, fine-tuning, preview**.
> * Supports direct **AI summary, Q&A** of content.
> * Supports direct **video generation of graphic blog posts**.

## How to Install

#### 1. Install [Python](https://www.python.org/downloads/)

- Please ensure that the Python version is greater than 3.8

#### 2. Install [FFmpeg](https://www.ffmpeg.org/download.html)

- The `Full` version in the [**Release**](https://github.com/Chenyme/Chenyme-AAVT/releases) already includes the FFmpeg library
- Set the FFmpeg environment variable
  - Use the `Win+R` shortcut to open the Run dialog box.
  - Enter `rundll32 sysdm.cpl,EditEnvironmentVariables`.
  - In User variables, find `Path`.
  - Click New and enter the path to FFmpeg. Example: `D:\APP\ffmpeg\bin` (please adjust according to your actual path).

#### 3. Run `install.bat`

- Choose the corresponding version of `install.bat` and wait for all dependencies to be installed.
- If running on CPU, select the CPU version, similarly for CUDA11.8, CUDA12.1.

## TODO

### Recognition Related
- [x] Replace with a faster Whisper project
- [x] Support local model loading
- [x] Support personal fine-tuning of Whisper models
- [x] VAD assistance optimization
- [x] Word-level sentence breaking optimization
- [x] More language recognition

### Translation Related
- [x] Translation optimization
- [x] More language translations
- [x] More translation models
- [x] More translation engines
- [x] Support local large language model translation

### Subtitle Related
- [x] Personalized subtitles
- [x] More subtitle formats
- [x] Subtitle preview, real-time modification
- [ ] Automated subtitle text proofreading
- [ ] Dual subtitles

### Other
- [x] Video summary, listing key points
- [x] Video preview
- [x] AI assistant
- [x] Video generation of blog posts*
- [ ] Real-time voice translation
- [ ] Video Chinese dubbing

#### Note: Features marked with `*` are still unstable and may have some bugs.

## Star History

[![Star History Chart](https://api.star-history.com/svg?repos=Chenyme/Chenyme-AAVT&type=Timeline)](https://star-history.com/#Chenyme/Chenyme-AAVT&Timeline)

## Project Interface Preview

### Main Page

![1716910190616](https://github.com/Chenyme/Chenyme-AAVT/assets/118253778/0bfebaf3-53c5-42ae-8031-b898dc27df6f)

### Settings

![1716910203660](https://github.com/Chenyme/Chenyme-AAVT/assets/118253778/49b89451-1129-4073-b1b5-0094af65f53e)

### Video Recognition

#### Parameter Settings

![d967ac4074d0c8ecba07b95de533730](https://github.com/Chenyme/Chenyme-AAVT/assets/118253778/72bc0e88-2148-486c-ac46-4f87a55e946b)

#### Running Interface

![b861c5019833b770f98344f7a4c73a4](https://github.com/Chenyme/Chenyme-AAVT/assets/118253778/ced915ec-a07b-43d2-9cf9-f92910033cb9)

#### Video Generation

![1716650985701](https://github.com/Chenyme/Chenyme-AAVT/assets/118253778/04bdf745-7ece-4c8b-a97b-f779b632dbc3)

#### Subtitle Fine-tuning

![1716651009788](https://github.com/Chenyme/Chenyme-AAVT/assets/118253778/33a02ef5-7386-4f34-ba0b-8947f17b78e3)

### Content Assistant

#### Parameter Settings

![461474f5d96b61b70bd239a9e3ddf8d](https://github.com/Chenyme/Chenyme-AAVT/assets/118253778/f22a11c2-3c58-4a92-ab4c-954e3710a254)

#### Running Interface

![14575fd5efbe138f364329626501b09](https://github.com/Chenyme/Chenyme-AAVT/assets/118253778/8a81ea44-95ae-488f-9412-014ff1c030e3)

### Subtitle Translation

![35bc5a96676c7f2b9d71042eb7c877f](https://github.com/Chenyme/Chenyme-AAVT/assets/118253778/635865b1-6ec1-41fd-858c-e1dcc87d684b)

### Video Blog

![09f60b8099f8ce19b83f4da63b26817](https://github.com/Chenyme/Chenyme-AAVT/assets/118253778/bbfca353-53d4-4a19-994f-7beddbbf17
