# UPDater
<img src="https://github.com/Renouncelove/UPDater/blob/main/Updater_icon.png" width="200" alt="UPDater App Icon">


## 简介 / Introduction

本项目旨在自动获取用户关注的哔哩哔哩（Bilibili）UP主的实时更新，并支持自动下载这些视频到本地。该工具对于追踪UP主发布的最新内容，并保留副本以供离线观看非常有用。

This project is designed to automatically fetch real-time updates from Bilibili UPs (content creators) followed by the user, and supports automatic downloading of these videos to the local system. This tool is very useful for tracking the latest content published by UPs and retaining copies for offline viewing.


## 安装指南 / Installation

要安装和设置此项目，请按照以下步骤操作：

To install and set up this project, follow these steps:

```bash
git clone [Your Repository URL]
cd [Your Repository Directory]
pip install -r requirements.txt
```

## 使用说明 / Usage

本项目设计为通过 `main.py` 脚本直接运行，以实现自动获取关注的Bilibili UP主的最新视频更新并下载功能。用户只需简单修改文件路径和cookie即可使用。

This project is designed to be run directly through the `main.py` script, enabling the automatic fetching and downloading of the latest video updates from the Bilibili UPs you follow. Users simply need to modify the file path and cookie to get started.

1. **配置 Cookie / Configure Cookie**:
   首先，您需要在 `main.py` 文件中设置您的Bilibili cookie。这是必要的步骤，以确保能够访问您关注的UP主的内容。

   First, you need to set your Bilibili cookie in the `main.py` file. This is a necessary step to ensure access to the content of the UPs you follow.

   ```python
   # 在 main.py 中设置您的cookie
   cookie = 'YOUR_BILIBILI_COOKIE'
   ```
2. **修改文件路径 / Modify File Paths:
   接下来，根据您的系统环境和需求，调整 main.py 中的文件路径设置。

   Next, adjust the file path settings in main.py according to your system environment and requirements.
   
3. **运行脚本 / Run the Script:
   完成上述配置后，您可以运行 main.py 脚本来启动整个程序。

   After completing the above configurations, you can run the main.py script to start the entire program.
   ```
   python main.py
   ```

## 致谢 / Acknowledgments

本项目使用了 [SocialSisterYi 的 Bilibili API Collect](https://github.com/SocialSisterYi/bilibili-API-collect) 中的部分内容。感谢该项目贡献者们在Bilibili API文档整理方面所做的宝贵工作。

This project utilizes parts of [Bilibili API Collect by SocialSisterYi](https://github.com/SocialSisterYi/bilibili-API-collect). We thank the contributors of this repository for their valuable work in compiling Bilibili API documentation.


## 许可证 / License
本项目在 MIT 许可证下发布 - 详情请见 LICENSE.md 文件

This project is released under the MIT License - see the LICENSE.md file for details
