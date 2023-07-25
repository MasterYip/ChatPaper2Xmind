import re
import fitz
from pdf_extract import get_eqbox, getEqRect, get_box_textpos, getFigRect
from config import *
# import arxiv


class PDFPaperParser:

    def __init__(self, path, title='', url='', authors=[]):
        # Args
        self.path = path
        self.url = url
        self.authors = authors
        
        # PDF parse
        self.pdf = fitz.open(self.path)
        self.title = title if title != '' else self.get_title()
        self.all_text = chr(12).join([page.get_text() for page in self.pdf])
        self.section_textdict = self.get_section_textdict()
        self.abstract = self.get_abstract()
        self.introduction = self.get_introduction()
        
        # Used in get_title()
        self.title_page = 0

    def __del__(self):
        self.pdf.close()

    def get_title(self):
        doc = self.pdf  # 打开pdf文件
        max_font_size = 0  # 初始化最大字体大小为0
        max_string = ""  # 初始化最大字体大小对应的字符串为空
        max_font_sizes = [0]
        for page_index, page in enumerate(doc):  # 遍历每一页
            text = page.get_text("dict")  # 获取页面上的文本信息
            blocks = text["blocks"]  # 获取文本块列表
            for block in blocks:  # 遍历每个文本块
                if block["type"] == 0 and len(block['lines']):  # 如果是文字类型
                    if len(block["lines"][0]["spans"]):
                        # 获取第一行第一段文字的字体大小
                        font_size = block["lines"][0]["spans"][0]["size"]
                        max_font_sizes.append(font_size)
                        if font_size > max_font_size:  # 如果字体大小大于当前最大值
                            max_font_size = font_size  # 更新最大值
                            # 更新最大值对应的字符串
                            max_string = block["lines"][0]["spans"][0]["text"]
        max_font_sizes.sort()
        # print("max_font_sizes", max_font_sizes[-10:])
        cur_title = ''
        for page_index, page in enumerate(doc):  # 遍历每一页
            text = page.get_text("dict")  # 获取页面上的文本信息
            blocks = text["blocks"]  # 获取文本块列表
            for block in blocks:  # 遍历每个文本块
                if block["type"] == 0 and len(block['lines']):  # 如果是文字类型
                    if len(block["lines"][0]["spans"]):
                        # 更新最大值对应的字符串
                        cur_string = block["lines"][0]["spans"][0]["text"]
                        # 获取第一行第一段文字的字体特征
                        font_flags = block["lines"][0]["spans"][0]["flags"]
                        # 获取第一行第一段文字的字体大小
                        font_size = block["lines"][0]["spans"][0]["size"]
                        # print(font_size)
                        if abs(font_size - max_font_sizes[-1]) < 0.3 or abs(font_size - max_font_sizes[-2]) < 0.3:
                            # print("The string is bold.", max_string, "font_size:", font_size, "font_flags:", font_flags)
                            if len(cur_string) > 4 and "arXiv" not in cur_string:
                                # print("The string is bold.", max_string, "font_size:", font_size, "font_flags:", font_flags)
                                if cur_title == '':
                                    cur_title += cur_string
                                else:
                                    cur_title += ' ' + cur_string
                            self.title_page = page_index
                            # break
        title = cur_title.replace('\n', ' ')
        return title

    def get_outlines(self):
        """
        Outline of the pdf file.\\
        Note: The outline is not all the same as the section title.
        """
        return self.pdf.get_toc(simple=True)

    def get_abstract(self):
        for item in self.get_section_textdict().items():
            if 'abstract' in item[0].lower():
                return item[1]

    def get_introduction(self):
        for item in self.get_section_textdict().items():
            if 'introduction' in item[0].lower():
                return item[1]

    # Section Dict Extract
    # Deprecated
    def get_section_titles_legacy(self):
        text = self.all_text
        match_str = '\n('+'|'.join(
            self.section_numbering[0]+self.section_numbering[1])+')(\s.*)'
        # clip the reference part
        ref_match = re.search(self.ref_matchstr, text)
        refpos = ref_match.span()[0] if ref_match else len(text)
        # search for all sections
        numbering_match = re.findall(match_str, text[:refpos])
        section_title = [re.search(self.abstrct_matchstr, text).group()]\
            + [m[0]+m[1] for m in numbering_match]\
            + [ref_match.group()]
        # TODO: ref?
        return section_title

    def get_section_titles(self, withlevel=False):
        section_title = []
        ref_break_flag = False
        level1_matchstr = '('+'|'.join(SECTIONNUM_MATCHSTR[0])+')(\s.*)'
        level2_matchstr = '('+'|'.join(SECTIONNUM_MATCHSTR[1])+')(\s.*)'
        for page in self.pdf:
            blocks = page.get_text("dict", flags=0)["blocks"]
            for block in blocks:
                lines = block["lines"]
                for line in lines:
                    line_text = "".join([span["text"] for span in line["spans"]])
                    if re.match(level2_matchstr, line_text) and len(section_title)>0:
                        section_title.append((line_text, 2))
                    elif re.match(level1_matchstr, line_text):
                        section_title.append((line_text, 1))
                    if re.match(REF_MATCHSTR, line_text):
                        ref_break_flag = True
                        break
                if ref_break_flag:
                    break
            if ref_break_flag:
                break
        section_title = [(re.search(ABS_MATCHSTR, self.all_text).group(), 1)]\
            + section_title\
            + [(re.search(REF_MATCHSTR, self.all_text).group(), 1)]
        return section_title if withlevel else [t[0] for t in section_title]

    def get_section_textdict(self):
        """
        Get section text dict of the paper.
        :return: Dict of section titles with text content
        FIXME: This will not get Reference content
        """
        section_title = self.get_section_titles(withlevel=False)
        section_dict = {}
        for i in range(0, len(section_title)-1):
            title = section_title[i]
            latter_title = section_title[i+1]
            begin_pos = self.all_text.find(title)+len(title)
            end_pos = self.all_text.find(latter_title)
            section_dict[title] = self.all_text[begin_pos:end_pos]
        return section_dict

    def get_section_equationdict(self, legacy=False):
        """
        Get equation dict of each section
        
        :param legacy: True for legacy equation extraction method
        :return: Dict of section titles with tuple item list 
        (equation_text_pos, page_number, equation_bbox)
        """
        eqa_ls = []
        for i in range(len(self.pdf)):
            page = self.pdf[i]
            if legacy:
                eq_box = get_eqbox(page)
            else:
                eq_box = getEqRect(page)
            if eq_box:
                for box in eq_box:
                    eqa_ls.append((get_box_textpos(page, box, self.all_text),
                                   i, box))
        section_title = self.get_section_titles()
        section_dict = {}
        for i in range(0, len(section_title)-1):
            title = section_title[i]
            section_dict[title] = []
            latter_title = section_title[i+1]
            begin_pos = self.all_text.find(title)+len(title)
            end_pos = self.all_text.find(latter_title)
            for eqa in eqa_ls:
                if eqa[0] > begin_pos and eqa[0] < end_pos:
                    section_dict[title].append(eqa)
                elif section_dict[title]:
                    break
        return section_dict

    def get_section_imagedict(self):
        """
        Get image dict of each section
        
        :return: Dict of section titles with tuple item list 
        (img_text_pos, page_number, img_bbox)
        """
        img_ls = []
        for i in range(len(self.pdf)):
            page = self.pdf[i]
            img_box = getFigRect(page)
            if img_box:
                for box in img_box:
                    img_ls.append((get_box_textpos(page, box, self.all_text),
                                   i, box))
        section_title = self.get_section_titles()
        section_dict = {}
        for i in range(0, len(section_title)-1):
            title = section_title[i]
            section_dict[title] = []
            latter_title = section_title[i+1]
            begin_pos = self.all_text.find(title)+len(title)
            end_pos = self.all_text.find(latter_title)
            for img in img_ls:
                if img[0] > begin_pos and img[0] < end_pos:
                    section_dict[title].append(img)
                # elif section_dict[title]:
                #     break
        return section_dict

