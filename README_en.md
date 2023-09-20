![Logo](doc/logo.png)
# ChatPaper2XMind

[中文](README.md) | **English**

ChatPaper2XMind is a tool for generating concise XMind notes from PDF papers using ChatGPT, including images and formulas, to improve reading efficiency.

**Note: Due to the limitations of the ChatGPT generation model's accuracy, the generated XMind notes are more suitable as note drafts, which can be used as a basis for creating reading notes, rather than directly using them for paper reading.**

**Contents**
- [Functionality Showcase](#functionality-showcase)
- [Installation and Usage](#installation-and-usage)
  - [1. Environment Setup](#1-environment-setup)
  - [2. Configuration (config.py)](#2-configuration-configpy)
  - [3. Getting Started](#3-getting-started)
- [Common Errors](#common-errors)
- [Future Work](#future-work)
- [Acknowledgements](#acknowledgements)

## Functionality Showcase
![Document Conversion](doc/feature-Paper2Xmind.png)

## Installation and Usage
### 1. Environment Setup
```
git clone --recursive https://github.com/MasterYip/ChatPaper2Xmind.git
cd <work-dir>
pip install -r requirements.txt
pip install -r ./XmindCopilot/requirements.txt
```
### 2. Configuration (config.py)
**OpenAI API Settings**
```
"""OpenAI API"""
APIBASE = ""                    # OpenAI API base, default is "https://api.openai.com/v1" for now (Leave it as empty if you are not sure)
APIKEYS = [""]                  # Your OpenAI API keys
MODEL = "gpt-3.5-turbo"         # GPT model name
LANGUAGE = "English"            # Only partially support Chinese
KEYWORD = "Science&Engineering" # Keyword for GPT model (What field you want the model to focus on)
PROXY = None                    # Your proxy address
# Note: If you are in China, you may need to use a proxy to access the OpenAI API
# (If your system's global proxy is set, you can leave it as None)
# PROXY = "http://127.0.0.1:7890"
```
- **APIBASE**: URL of the OpenAI model request server
  - You can replace it with any model that supports OpenAI request format (ChatGLM/LLaMA, etc.)
- **APIKEYS (Must be configured)**: API keys for OpenAI model requests
  - Multiple API keys can be added to support multi-threaded requests
  - If using a different model, the length of the APIKEYS list determines the number of request threads; the content can be any value
  - **For those without API keys, you can refer to [ChatGPT_API_NoKey](https://github.com/MasterYip/ChatGPT_API_NoKey) to configure a fake API server and change openai.api_base to achieve fake API access**; in this case, APIKEY should be set to any value (cannot be empty)
- MODEL: Select OpenAI model
- LANGUAGE: Generated language
- KEYWORD: Field to which the paper belongs
- **PROXY**: Proxy server
  - If you are in the China region, you may need to use a proxy to access the OpenAI website
  - When left as None, it will follow the system's global proxy

**Generation Format Settings**
```
"""Generation"""
GEN_IMGS = True
GEN_EQUATIONS = True

# PDFFigure2
USE_PDFFIGURE2 = True       # Use PDFFigure2 to generate images & tables (This requires you to install JVM)
SNAP_WITH_CAPTION = True    # Generate images & tables with captions (Only valid when USE_PDFFIGURE2 is True)

# Max generation item number
TEXT2LIST_MAX_NUM = 4       # Max number of items for each list
TEXT2TREE_MAX_NUM = 4       # Max number of subtopics for each topic
FAKE_GPT_RESPONSE = "Fake"  # Fake GPT response when GPT_ENABLE is False
if True:  # Use the true GPT model
    GPT_ENABLE = True
    THREAD_RATE_LIMIT = 100       # Each APIKEY can send 3 requests per minute (limited by OpenAI)
else:    # Use the fake GPT model
    GPT_ENABLE = False
    THREAD_RATE_LIMIT = 6000  
```
- GEN_IMGS: Capture and generate paper images
- GEN_EQUATIONS: Capture and generate paper equations
- **USE_PDFFIGURE2**: Use PDFFIGURE2 to capture paper images **(Requires Java environment; set to False if Java environment is not installed)**
- SNAP_WITH_CAPTION: When USE_PDFFIGURE2 is True, capture images and tables along with captions
- TEXT2LIST_MAX_NUM (Currently ineffective)
- TEXT2TREE_MAX_NUM (Currently ineffective)
- FAKE_GPT_RESPONSE: Pseudo GPT response when not using ChatGPT
- **GPT_ENABLE**: Whether to use GPT
  - If not using ChatGPT to generate text summaries and only generating the table of contents and images/equations, set it to False
- **THREAD_RATE_LIMIT**: Number of requests per minute for a single thread (single API key)
  - OpenAI has frequency limits on requests; typically 3/min for standard packages

**PDF Parser: Regular Expression Settings**
```
"""PDF Parser - Regular Expression"""
# Special title
ABS_MATCHSTR = "ABSTRACT|Abstract|abstract"
INTRO_MATCHSTR = "I.[\s]{1,3}(INTRODUCTION|Introduction|introduction)"
REF_MATCHSTR = "Reference|REFERENCE|Bibliography"
APD_MATCHSTR = "APPENDIX|Appendix"  # Not used for now
# General title
# FIXME: Misidentification exists
SECTION_TITLE_MATCHSTR = ["[IVX1-9]{1,4}[\.\s][\sA-Za-z]{1,}|[1-9]{1,2}[\s\.\n][\sA-Za-z]{1,}",  # Level 1
                          "[A-M]{1}\.[\sA-Za-z]{1,}|[1-9]\.[1-9]\.[\sA-Za-z]{1,}"]  # Level 2
# Equation & Image
EQUATION_MATCHSTR = '[\s]{0,}\([\d]{1,}[a-zA-Z]{0,1}\)'
IMG_MATCHSTR = 'Fig.[\s]{1,3}[\d]{1,2}|Figure[\s]{1,3}[\d]{1,2}|Tab.[\s]{1,3}[\dIVX]{1,3}|Table[\s]{1,3}[\dIVX]{1,3}'  # Figure & Table
```

**Xmind Sytle Template**
```
"""Xmind Sytle Template"""
TEMPLATE_XMIND_PATH = 'template.xmind'
```

**Debug Info**
```
"""Debuging"""
DEBUG_MODE = False
```

### 3. Getting Started

Convert PDF papers to XMind
```
cd <root-dir>
python paper2xmind.py --path <pdf_path_or_folder_path>
```
Run the demo
```
python paper2xmind.py
```

## Common Errors
### 1. 'PDFFigure2PaperParser' object has no attribute 'pdf'
```
FileNotFoundError: [WinError 2] The system cannot find the file specified.
Exception ignored in: <function PDFPaperParser.del at 0x000001F4388C2C00>
Traceback (most recent call last):
File "D:\git\ChatPaper2Xmind\pdf_parser.py", line 31, in __del__
self.pdf.close()
^^^^^^^^
AttributeError: 'PDFFigure2PaperParser' object has no attribute 'pdf'
```
- Incorrect PDF input path
  - PDF file doesn't exist
  - Input path contains spaces and is not enclosed in double quotes
- Java environment not installed and using PDFFIGURE2 to generate images
  - Set USE_PDFFIGURE2=False or install Java environment and add it to the system PATH environment variable

### 2. ImportError: cannot import name 'xmind' from 'XmindCopilot' (unknown location)
```
Traceback (most recent call last):
File "D:\academic chatgpt series\ChatPaper2Xmind-main\paper2xmind.py", line 3, in <module>
from XmindCopilot import xmind, fileshrink
ImportError: cannot import name 'xmind' from 'XmindCopilot' (unknown location)
```
- Git repository XmindCopilot not cloned properly
  - Need to properly execute environment setup
```
git clone --recursive https://github.com/MasterYip/ChatPaper2Xmind.git
cd <work-dir>
pip install -r requirements.txt
pip install -r ./XmindCopilot/requirements.txt
```

## Future Work
- Reduce GPT requests to speed up XMind generation.
- Add metadata and resource parsing capabilities.
- Add functionality for generating Markdown notes.
- Optimize formula detection (boundary detection).

## Acknowledgements

Thanks to the following projects for their valuable contributions to this project:

- [PDFfigures 2.0](https://github.com/allenai/pdffigures2)
- [Chatpaper](https://github.com/kaixindelele/ChatPaper)
- [xmind](https://github.com/zhuifengshen/xmind)

And all other projects that might have been inadvertently overlooked :)

Special thanks to the open-source community and all contributors who have contributed to this project.

## License
This project is released under the MIT License. For more information, see the [LICENSE](LICENSE) file.

## Author
Master Yip

Email: 2205929492@qq.com

GitHub: [Master Yip](https://github.com/MasterYip)

QQ Group：
![QQ](doc/QQ.jpg)