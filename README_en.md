![Logo](doc/logo.png)
# ChatPaper2XMind

[中文](README.md) | **English**

ChatPaper2XMind is a tool for generating concise XMind notes from PDF papers using ChatGPT, including images and formulas, to improve reading efficiency.

**Note: Due to the limitations of the ChatGPT generation model's accuracy, the generated XMind notes are more suitable as note drafts, which can be used as a basis for creating reading notes, rather than directly using them for paper reading.**

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

### 2. Config Configuration

Basic Settings

- **APIKEY Configuration (Required)**: Add your API keys in `config.py`.
  - Supports multi-threaded requests.
  - **For those without an API key, you can refer to [ChatGPT_API_NoKey](https://github.com/MasterYip/ChatGPT_API_NoKey) for configuring a mock API server and modify `openai.api_base` to achieve mock API access.** In this case, the API key must be set to any value (cannot be empty).
- GPT Model Selection: Set the MODEL variable in `config.py` to the desired model. Currently, "GPT-3.5-turbo" model is available.
- Language Setting: Set the LANGUAGE variable in `config.py` to select the language of the model. The default is English, but partial support for Chinese is available.
- Domain Keyword: Set the KEYWORD variable in `config.py` to specify the domain keyword that the model should focus on.
- Proxy Setup: Set the PROXY variable in `config.py` to specify the proxy address. **If your system has a global proxy set, you can leave it as None**.
- Thread Request Rate Limit: Set the THREAD_RATE_LIMIT variable in `config.py` to specify the number of requests each APIKEY can send per minute. Due to OpenAI's limitations, each APIKEY can support up to 3 requests.

Generation Settings

- Max Generation Items: Set the TEXT2LIST_MAX_NUM and TEXT2TREE_MAX_NUM variables in `config.py` to specify the maximum number of items for text-to-list and text-to-tree conversions, respectively.
- Enable Real GPT Model: Set the GPT_ENABLE variable in `config.py` to use real GPT/fake GPT.
- Fake GPT Model Response: Set the FAKE_GPT_RESPONSE variable in `config.py` to specify the response content of the fake GPT model.

Title Regex Matching
- Title Regex Matching String: Set the SECTIONNUM_MATCHSTR variable in `config.py` for corresponding title matching.

File Saving
- XMind Style Template File: Set the TEMPLATE_XMIND_PATH variable in `config.py` to select the style template (the template should be empty).

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

## Future Work
- Reduce GPT requests to speed up XMind generation.
- Add metadata and resource parsing capabilities.
- Implement image detection using PDFfigures 2.0.
- Improve image positioning methods (to address image loss due to partial matching failures).
- Add functionality for generating Markdown notes.
- Optimize formula detection (boundary detection).
- Table Detection

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