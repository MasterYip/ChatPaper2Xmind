![Logo](doc/logo.png)
# ChatPaper2XMind

**中文**|[English](README_en.md)

ChatPaper2XMind论文XMind笔记生成工具：使用ChatGPT将PDF转换为带有图片和公式的简洁XMind笔记，提高阅读效率。

**注意：受限于ChatGPT生成模型准确性，生成的Xmind笔记更适合作为笔记草稿，在此基础上制作阅读笔记，而不能直接将其当做论文阅读。**

## 功能展示
![文档转换](doc/feature-Paper2Xmind.png)

## 安装与使用
### 1. 环境设置
```
cd <root-dir>
pip install -r requirements.txt
git submodule update --init --recursive
```
### 2. Config配置

基本设置

- **APIKEY设置(必须配置)**：在`config.py`中加入APIKEYs（支持多线程请求）
- GPT模型选择：在`config.py`中设置MODEL变量为所需的模型，目前提供"GPT-3.5-turbo"模型可选。
- 语言设置：在`config.py`中设置LANGUAGE变量以选择模型的语言，默认为英语，但部分支持中文。
- 领域关键词：在`config.py`中设置KEYWORD变量以指定模型关注的领域关键词。
- 代理设置：在`config.py`中设置PROXY变量以指定代理地址，**如果您的系统已经设置了全局代理，可以保留为None**。
- 线程请求速率限制：在`config.py`中设置THREAD_RATE_LIMIT变量以指定每个APIKEY在一分钟内可以发送的请求次数，由于OpenAI的限制，每个APIKEY最多支持3次请求。

生成设置

- 最大生成项数：在`config.py`中设置TEXT2LIST_MAX_NUM和TEXT2TREE_MAX_NUM变量，分别表示文本转列表和文本转树结构的最大生成项数。
- 使用真实GPT模型：在`config.py`中设置GPT_ENABLE变量以使用真实GPT/伪GPT
- 伪GPT模型响应：在`config.py`中设置FAKE_GPT_RESPONSE变量以指定伪GPT模型的响应内容。

标题正则匹配
- 标题正则匹配字符串：在`config.py`中设置SECTIONNUM_MATCHSTR进行对应标题匹配

文件保存
- Xmind风格模板文件：在`config.py`中设置TEMPLATE_XMIND_PATH选择风格模板（模板应为空）

### 3. 开箱使用

将PDF论文转换为XMind
```
cd <root-dir>
python paper2xmind.py --path <pdf路径或pdf文件夹路径>
```
运行演示
```
python paper2xmind.py
```

## 未来工作
- 减少GPT请求次数以加快XMind生成速度
- 添加元数据和资源解析功能
- 使用PDFfigures 2.0实现图片检测
- 改进图像定位方法（由于部分匹配失败导致的图像丢失）
- 添加Markdown笔记生成功能
- 优化公式检测（边界检测）

## 鸣谢

感谢以下项目对本项目的宝贵贡献：

- [PDFfigures 2.0](https://github.com/allenai/pdffigures2)
- [Chatpaper](https://github.com/kaixindelele/ChatPaper)
- [xmind](https://github.com/zhuifengshen/xmind)

以及其他不小心被忽略的项目 :)

特别感谢开源社区和所有为该项目作出贡献的贡献者。

## 许可证
本项目在MIT许可下发布。有关详细信息，请参阅[LICENSE](LICENSE)文件。

## 作者
Master Yip

电子邮件：2205929492@qq.com

GitHub：[Master Yip](https://github.com/MasterYip)