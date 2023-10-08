from config import *
import openai
from threading import Thread
import time
from tqdm import trange
import tiktoken


def countTokens(string: str, encoding_name: str) -> int:
    """
    Get the number of tokens in a string, using the given encoding.
    :param string: The string to count tokens in.
    :param encoding_name: The name of the encoding to use, e.g. gpt-3.5-turbo.
    :note: Make sure `pip install --upgrade tiktoken`
    """
    encoding = tiktoken.encoding_for_model(encoding_name)
    num_tokens = len(encoding.encode(string))
    return num_tokens


def autoCutoff(string: str, encoding_name: str, max_tokens: int) -> str:
    """
    Automatically cut off a string to a maximum number of tokens, using the given encoding.
    :param string: The string to cut off.
    :param encoding_name: The name of the encoding to use, e.g. gpt-3.5-turbo.
    :param max_tokens: The maximum number of tokens to allow.
    """
    encoding = tiktoken.encoding_for_model(encoding_name)
    tokens = encoding.encode(string)
    if len(tokens) > max_tokens:
        tokens = tokens[:max_tokens]
        string = encoding.decode(tokens)
    return string


def messageAutoCutoff(message: list, encoding_name: str, max_tokens: int):
    token_cnt = 0
    for item in message:
        token_cnt += countTokens(item['content'], encoding_name)
    if token_cnt > max_tokens:
        for item in message:
            if item['role'] == 'user':
                item['content'] = autoCutoff(item['content'], encoding_name, countTokens(
                    item['content'], encoding_name) + max_tokens - token_cnt)
                break
    return message


class GPTRequest(object):
    # TODO: other model support?
    def __init__(self, content, model=MODEL, language=LANGUAGE, keyword=KEYWORD, maxtoken=MAXTOKEN,
                 gpt_enable=GPT_ENABLE, fake_response=FAKE_GPT_RESPONSE):
        """
        Initialize GPTRequest.\\
        Note that request message has not been generated yet.

        :param content: text content
        :param model: OpenAI model name
        :param language: language
        :param keyword: keyword of the field the content belongs to
        """
        self.model = model
        self.content = content
        self.language = language
        self.keyword = keyword
        self.maxtoken = maxtoken
        self.gpt_enable = gpt_enable
        self.fake_response = fake_response
        
        self.ret = None
        self.success = False
        # TODO: Nontype problem?
        self.postprocess = None

    # Messages Generation
    def para2list(self, maxnum=TEXT2LIST_MAX_NUM):
        """
        para2list task
        :param maxnum: max number of items in list
        :postprocess return: self.ret (List)
        """
        self.message = [
            {"role": "system",
             "content": "You are a researcher in the field of [" + self.keyword + "] who is good at summarizing papers using concise statements"},
            {"role": "assistant",
             "content": f"Sumarize and simplify in list up to {maxnum} items. Every item are splited by '\n'"},
            {"role": "user", "content": "Please summarize it:" + self.content}
        ]
        self.postprocess = self.para2list_postprocess
        return self

    def para2tree(self, maxnum=TEXT2TREE_MAX_NUM):
        """
        para2tree task
        :param maxnum: max number of items in tree
        :postprocess return: self.ret (List, depth is represented by '\t' prefix)
        """
        self.message = [
            {"role": "system",
                "content": "You are a researcher in the field of [" + self.keyword + "] who is good at summarizing papers using concise statements"},
            {"role": "assistant",
                "content": f"""
                    Your mission is to summarize paragraphs.
                    Requirements:
                    1. Summarize in multi-level list in markdown style.
                    2. Total number of items in the list must not exceed {maxnum}.
                    3. Sumarize in {LANGUAGE}.
                    4. Ignore the irregular text that probably belong to math equations.
                """},
            {"role": "user", "content": "Content:" + self.content}
        ]
        self.postprocess = self.para2tree_postprocess
        return self

    def introSummary(self):
        self.message = [
            {"role": "system",
                "content": "You are a researcher in the field of [" + self.keyword + "] who is good at summarizing papers using concise statements"},
            {"role": "assistant",
                "content": "This is the title, author, link, abstract and introduction of an English document. I need your help to read and summarize the following questions: " + self.content},
            {"role": "user", "content": """                 
                    1. Mark the title of the paper (with Chinese translation)
                    2. list all the authors' names (use English)
                    3. mark the first author's affiliation (output {} translation only)                 
                    4. mark the keywords of this article (use English)
                    5. link to the paper, Github code link (if available, fill in Github:None if not)
                    6. summarize according to the following four points.Be sure to use {} answers (proper nouns need to be marked in English)
                    - (1):What is the research background of this article?
                    - (2):What are the past methods? What are the problems with them? Is the approach well motivated?
                    - (3):What is the research methodology proposed in this paper?
                    - (4):On what task and what performance is achieved by the methods in this paper? Can the performance support their goals?
                    Follow the format of the output that follows:                  
                    1. Title: xxx\n\n
                    2. Authors: xxx\n\n
                    3. Affiliation: xxx\n\n                 
                    4. Keywords: xxx\n\n   
                    5. Urls: xxx or xxx , xxx \n\n      
                    6. Summary: \n\n
                    - (1):xxx;\n 
                    - (2):xxx;\n 
                    - (3):xxx;\n  
                    - (4):xxx.\n\n     
                    
                    Be sure to use {} answers (proper nouns need to be marked in English), statements as concise and academic as possible, do not have too much repetitive information, numerical values using the original numbers, be sure to strictly follow the format, the corresponding content output to xxx, in accordance with \n line feed.                 
                    """.format(self.language, self.language, self.language)},
        ]
        self.postprocess = self.introSummary_postprocess
        return self

    # Postprocess
    def para2list_postprocess(self):
        # self.ret = re.sub('- ', '', self.ret)
        # self.ret = self.ret.split("\n")
        pass

    def para2tree_postprocess(self):
        # self.ret = re.sub('- ', '', self.ret)
        # self.ret = self.ret.split("\n")
        pass

    def introSummary_postprocess(self):
        # self.ret = self.ret.split("\n")
        pass

    # Run
    def run(self, errsleep=20):
        """
        Run a GPT request
        :param errsleep: sleep time when error occurs
        FIXME: this sleep is not controlled by the GPTThread
        """
        completions = None
        if self.gpt_enable:
            while completions is None:
                try:
                    completions = openai.ChatCompletion.create(
                        model=self.model,
                        messages=messageAutoCutoff(self.message, self.model, self.maxtoken),
                    )
                except Exception as e:
                    print(e)
                    try:
                        time.sleep(errsleep)
                    except KeyboardInterrupt:
                        exit()
                except KeyboardInterrupt:
                    exit()
            # Output to self.ret
            self.ret = completions['choices'][0]['message']['content']
            self.postprocess()
        else:
            self.ret = self.fake_response
            self.postprocess()
        self.success = True

    def isSuccess(self):
        return self.success


class GPTThread(object):

    def __init__(self, apikey, rate_limit, gpt_enable):
        self.apikey = apikey
        self.thread = None
        # FIXME: Should not use global variable
        if gpt_enable:
            self.cooling_time = 60 / rate_limit
        else:
            self.cooling_time = 0
        self.last_request_time = None
        self.thread = None

    def run(self, gptreq: GPTRequest):
        """ 
        Run a GPT request
        :param gptreq: GPTRequest
        :return: GPT response or None if failed
        """
        openai.api_key = self.apikey
        self.last_request_time = time.time()
        self.thread = Thread(target=gptreq.run)
        self.thread.start()

    def isAvailable(self):
        if self.last_request_time:
            if time.time() - self.last_request_time < self.cooling_time:
                return False
        if self.thread and self.thread.is_alive():
            return False
        return True


class GPTInterface(object):
    def __init__(self, apibase, apikeys, model, keyword,
                 gpt_enable, openai_proxy, rate_limit) -> None:
        if openai_proxy:
            openai.proxy = openai_proxy
        if apibase:
            openai.api_base = apibase
        self.apikeys = apikeys
        self.model = model
        self.keyword = keyword
        self.gpt_enable = gpt_enable
        self.request_list = []
        self.thread_list = [GPTThread(apikey, rate_limit, gpt_enable) for apikey in self.apikeys]
        self.request_index = {}

    def gptMultitask(self, interval=0):
        ptr = 0
        progress = trange(len(self.request_list))
        try:
            while self.checkSuccessNum() < len(self.request_list):
                for thread in self.thread_list:
                    if thread.isAvailable() and ptr < len(self.request_list):
                        thread.run(self.request_list[ptr])
                        ptr += 1
                progress.update(self.checkSuccessNum() - progress.n)
                time.sleep(interval)
        except KeyboardInterrupt:
            progress.close()
            exit()

    def checkSuccessNum(self):
        return [req.isSuccess() for req in self.request_list].count(True)

    def addRequest(self, gptreq: GPTRequest, index=None):
        self.request_list.append(gptreq)
        if index:
            self.request_index[index] = gptreq

    def getResponse(self, index):
        return self.request_index[index].ret
