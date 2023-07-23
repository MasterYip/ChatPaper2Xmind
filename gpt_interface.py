import openai
import re
from threading import Thread
import time
from tqdm import trange
from config import *
# import openai
# import requests
# import tenacity
# import tiktoken

class GPTRequest(object):
    # TODO: other model support?
    def __init__(self, content, model=MODEL, language=LANGUAGE, keyword=KEYWORD):
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
            "content": f"Sumarize and simplify in list up to {maxnum} items. Every item are splited by '\n'. Children item has one more '\t' prefix then their father item."},
            {"role": "user", "content": "Please summarize it:" + self.content}
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
        self.ret = re.sub('- ', '', self.ret)
        self.ret = self.ret.split("\n")
    
    def para2tree_postprocess(self):
        self.ret = re.sub('- ', '', self.ret)
        self.ret = self.ret.split("\n")
    
    def introSummary_postprocess(self):
        self.ret = self.ret.split("\n")
        pass
    
    # Run
    def run(self, errsleep=20):
        """
        Run a GPT request
        :param errsleep: sleep time when error occurs
        FIXME: this sleep is not controlled by the GPTThread
        """
        completions = None
        if GPT_ENABLE:
            while completions is None:
                try:
                    completions = openai.ChatCompletion.create(
                        model=self.model,
                        messages=self.message,
                    )
                except Exception as e:
                    print(e)
                    time.sleep(errsleep)
                except KeyboardInterrupt:
                    exit()
            # Output to self.ret
            self.ret = completions['choices'][0]['message']['content']
            self.postprocess()
        else:
            self.ret = FAKE_GPT_RESPONSE
            self.postprocess()
        self.success = True
    
    def isSuccess(self):
        return self.success


class GPTThread(object):
    
    def __init__(self, apikey, rate_limit=THREAD_RATE_LIMIT):
        self.apikey = apikey
        self.thread = None
        self.cooling_time = 60 / rate_limit
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
    def __init__(self, apikeys=APIKEYS, model=MODEL, keyword=KEYWORD, gpt_enable=GPT_ENABLE) -> None:
        self.apikeys = apikeys
        self.model = model
        self.keyword = keyword
        self.gpt_enable = gpt_enable
        self.request_list = []
        self.thread_list = [GPTThread(apikey) for apikey in self.apikeys]
        self.request_index = {}

    # Legacy
    def content2list(self, content, write=False, name="DEFAULT", max_num=4, err_sleep=25):
        """
        Convert content to list
        """
        # 调用接口
        if self.gpt_enable:
            completions = None
            if self.model == "gpt-3.5-turbo":
                while not completions:
                    try:
                        completions = openai.ChatCompletion.create(
                            model="gpt-3.5-turbo",
                            messages=[
                                {"role": "system",
                                "content": "You are a researcher in the field of [" + self.keyword + "] who is good at summarizing papers using concise statements"},
                                {"role": "assistant",
                                "content": f"Sumarize and simplify in list up to {max_num} items. Every item are splited by '\n'. Children item has one more '\t' prefix then their father item."},
                                {"role": "user", "content": "Please summarize it:" + content}
                            ]
                        )
                    except KeyboardInterrupt:
                        exit()
                    except Exception as e:
                        print(e)
                        time.sleep(err_sleep)
                        

                # 输出结果
                message = completions['choices'][0]['message']['content']
            elif self.model == "text-davinci-003":
                prompt = f"Sumarize and simplify in list up to {max_num} items. Every item are splited by '\n'." + content
                
                while not completions:
                    try:
                        # 调用接口
                        completions = openai.Completion.create(
                            engine="text-davinci-003",
                            prompt=prompt,
                            max_tokens=1024,
                            n=1,
                            stop=None,
                            temperature=0.5,
                        )
                    except Exception as e:
                        print(e)
                        time.sleep(err_sleep)
                # 输出结果
                message = completions.choices[0].text
                
            message = re.sub('- ', '', message)
            
        else:  # Fake GPT to save time for testing
            message = re.sub('\.', '.\n', content)
        if write:
            self.list_dict[name] = message.split("\n")
        return message.split("\n")
    # Legacy
    def content2list_multitask(self, list_dict, section_text_dict, section_names, thread_num=1):
        
        self.section_names = section_names
        self.list_dict = list_dict
        self.section_text_dict = section_text_dict
        for name in self.section_names[:-1]:
            self.thread_ls.append(Thread(target=self.content2list, args=(
                self.section_text_dict[name], True, name)))

        ptr = trange(len(self.thread_ls))
        ptr.desc = self.section_names[ptr.n][0:15]
        ptr.update(0)
        self.ptr = ptr
        while True:
            if self.get_alive_thread_num() < thread_num and ptr.n < len(self.thread_ls):
                self.thread_ls[ptr.n].start()
                ptr.desc = self.section_names[ptr.n][0:15]
                ptr.update()
            if not any([thread.is_alive() for thread in self.thread_ls]) and ptr.n >= len(self.thread_ls):
                break
    
    def gptMultitask(self, interval=0):
        ptr = 0
        progress = trange(len(self.request_list))
        while self.checkSuccessNum() < len(self.request_list):
            for thread in self.thread_list:
                if thread.isAvailable() and ptr < len(self.request_list):
                    thread.run(self.request_list[ptr])
                    ptr += 1
            progress.update(self.checkSuccessNum() - progress.n)
            time.sleep(interval)
    
    def checkSuccessNum(self):
        return [req.isSuccess() for req in self.request_list].count(True)
    
    def addRequest(self, gptreq: GPTRequest, index=None):
        self.request_list.append(gptreq)
        if index:
            self.request_index[index] = gptreq
            
    def getResponse(self, index):
        return self.request_index[index].ret

    # Legacy
    def get_alive_thread_num(self):
        return sum([thread.is_alive() for thread in self.thread_ls])
    



