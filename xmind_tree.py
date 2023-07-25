from XmindCopilot import xmind
from XmindCopilot.xmind.core.topic import TopicElement
from XmindCopilot.search import topic_search
from XmindCopilot.fileshrink import xmind_shrink
from gpt_interface import GPTInterface, GPTRequest
from pdf_extract import get_objpixmap
import re


class Xmindtree(TopicElement):

    def __init__(self, stem_node, paper, title='') -> None:
        # Set root node to itself
        self.__dict__ = stem_node.__dict__

        if title:
            self.setTitle(title)
        self.paper = paper
        self.gpt = GPTInterface()

        # Meta Data
        # self.meta_node = self.addSubTopicbyTitle("Meta")
        # self.meta_node.addSubTopicbyTitle('Title:' + self.paper.title)
        # self.meta_node.addSubTopicbyTitle('Url:' + self.paper.url)
        # self.meta_node.addSubTopicbyTitle('Paper_info:' + self.paper.section_text_dict['paper_info'])

    def gen_table_of_content(self):
        # Note: only support sections named with specified numbering
        ptr = self
        section_list = self.paper.get_section_titles(withlevel=True)
        for title in section_list:
            if title[1] == 1:
                ptr = self.addSubTopicbyTitle(title[0])
            else:
                ptr.addSubTopicbyTitle(title[0])

    def gen_textbrief(self):
        """
        Generate textbrief for each section in xmind
        `Note: This might be time consuming`
        """
        # Add Request Tasks
        content_dict = self.paper.get_section_textdict()
        section_names = self.paper.get_section_titles()
        
        # Abstract
        self.gpt.addRequest(GPTRequest(self.paper.abstract).para2list(), section_names[0])
        # Introduction Summary
        summary_text = '\n'.join(["Title:" + self.paper.title,
                                  "URL:" + self.paper.url,
                                  "Ahthor:" + ' '.join(self.paper.authors),
                                  "Abstract:" + self.paper.abstract,
                                  self.paper.introduction])
        self.gpt.addRequest(GPTRequest(summary_text).introSummary(), section_names[1])
        for name in section_names[2:-1]:
            self.gpt.addRequest(GPTRequest(content_dict[name]).para2tree(), name)
        # Start GPT req
        self.gpt.gptMultitask()
        # Add to xmind
        for name in section_names[:-1]:
            content_ls = self.gpt.getResponse(name)
            topic_search(self, name).addSubTopicbyIndentedList(
                [content for content in content_ls], 0)
                # [content for content in content_ls if len(content) > self.minlength], 0)

    def gen_equation(self, legacy=True):
        """
        Generate equation for each section in xmind

        :param legacy: if True, use legacy method to extract\
            equation, else use new method.
        `NOTE` It seems that legacy method is more accurate.
        """
        section_names = self.paper.get_section_titles()
        eqa_dict = self.paper.get_section_equationdict(legacy=legacy)
        for name in section_names[:-1]:
            eqa_ls = eqa_dict.get(name)
            if eqa_ls:
                for eqa in eqa_ls:
                    eqa_tempdir = get_objpixmap(self.paper.pdf, eqa)
                    topic_search(self, name).addSubTopicbyImage(
                        eqa_tempdir, eqa_ls.index(eqa))

    def gen_image(self):
        """
        Generate image for each section in xmind
        """
        section_names = self.paper.get_section_titles()
        img_dict = self.paper.get_section_imagedict()
        for name in section_names[:-1]:
            img_ls = img_dict.get(name)
            # if img_ls: print(name, img_ls)
            if img_ls:
                for img in img_ls:
                    img_tempdir = get_objpixmap(self.paper.pdf, img)
                    topic_search(self, name).addSubTopicbyImage(
                        img_tempdir, img_ls.index(img))

    def gen_summary(self, folded=True):
        self.gen_table_of_content()
        print("\033[94mChatGPT Requesting...\033[97m")
        self.gen_textbrief()
        print("\033[94mImages Generating...")
        self.gen_equation(legacy=False)
        self.gen_image()
        if folded:
            self.setFolded(True)

    def save_xmind(self, path=None, img_compress=False):
        """Not recommanded yet"""
        xmind.save(self.getOwnerWorkbook(), path=path)
        if img_compress:
            xmind_shrink(self.getOwnerWorkbook().get_path())
