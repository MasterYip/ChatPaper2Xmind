![Logo](doc/logo.png)
# ChatPaper2XMind

[中文](README.md)|**English**

Paper XMind Notes Generator: Convert PDF to Concise XMind Notes with Images and Formulas Using ChatGPT for Enhanced Reading Efficiency

# Features
![PaperConvertion](doc/feature-Paper2Xmind.png)

# Installation & Usage
1. Environment Setup
```
pip install -r requirements.txt
git submodule update --init --recursive
```
2. Set OpenAI APIKEY
Add your API keys to `config.py` (supports multi-threaded requests).

3. Getting Started

Convert PDF papers to XMind
```
cd <root-dir>
python paper2xmind.py --path <pdf-path or pdf-folder-path>
```
Run Demo
```
python paper2xmind.py
```

# Future work
 - Decrease request numbers to speed up xmind generation
 - Add Meta data & resources parser
 - Implement figure detect using PDFfigures 2.0.
 - Imporve image locating method (there are images dropped out because of section match failure).
 - Add markdown notes generation feature.
 - Optimize equation dectection (border detection).
 - Handle OpenAI Proxy problem

# Acknowledgements

I would like to acknowledge the following projects for their valuable contributions to this project:

- [PDFfigures 2.0](https://github.com/allenai/pdffigures2)
- [Chatpaper](https://github.com/kaixindelele/ChatPaper)
- [xmind](https://github.com/zhuifengshen/xmind)

And other projects that are carelessly ignored:)

Special thanks to the open-source community and all the contributors who helped make this project possible.
