import re
from typing_extensions import override
import fitz
from pdf_extract import *
from config import *
import os
# import arxiv


class PDFPaperParser:

    def __init__(self, path, title='', url='', authors=[]):
        # Args
        self.path = path
        self.url = url
        self.authors = authors

        # PDF parse
        self.pdf = fitz.open(self.path)
        self.title = self.get_title() if (title == '' and self.get_title()) else title
        # self.all_text = "".join([page.get_text() for page in self.pdf])
        self.all_text = self.get_all_text()
        self.section_textdict = self.get_section_textdict()
        self.abstract = self.get_abstract()
        self.introduction = self.get_introduction()

        # Used in get_title()
        self.title_page = 0

    def __del__(self):
        self.pdf.close()

    def save_pdf(self, path=None, debug=True):
        """For debug use"""
        path = path if path else self.path
        if debug:
            path = os.path.splitext(path)[0]+"_debug.pdf"
        self.pdf.save(path)

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

    def get_all_text(self):
        """Get all text in the pdf file.
        TODO: Higher performance is needed.
        """
        all_text = ""
        for page in self.pdf:
            for block in page.get_text("dict", flags=0)["blocks"]:
                for line in block["lines"]:
                    for span in line["spans"]:
                        all_text = all_text + span["text"]
                    all_text = all_text + "\n"
        return all_text

    def get_abstract(self):
        for item in self.get_section_textdict().items():
            if 'abstract' in item[0].lower():
                return item[1]

    def get_introduction(self):
        for item in self.get_section_textdict().items():
            if 'introduction' in item[0].lower():
                return item[1]
        return ''

    # Section Dict Extract
    def get_section_titles(self, withlevel=False, verbose=False):
        section_title = []
        # ref_break_flag = False
        level1_matchstr = SECTION_TITLE_MATCHSTR[0]
        level2_matchstr = SECTION_TITLE_MATCHSTR[1]
        for page in self.pdf:
            blocks = page.get_text("dict", flags=0)["blocks"]
            for block in blocks:
                # Assume: Section title is the first "Line" or multiple "Lines" that have the same y position in one "block"
                is_equation = False
                lines = block["lines"]
                pos_y = block["lines"][0]["bbox"][1]
                tol = 1
                line_text = ""
                for line in lines:
                    if abs(pos_y-line["bbox"][1]) < tol:
                        line_text = line_text + "".join([span["text"] for span in line["spans"]]) + "\n"
                    for span in line["spans"]:
                        if span['font'].startswith('CM') or span['font'].startswith('MSBM'):
                            is_equation = True
                            break
                    else:
                        break
                if is_inbox(block['bbox'][0:2], get_bounding_box(getColumnRectLegacy(page)))\
                   and is_inbox(block['bbox'][2:4], get_bounding_box(getColumnRectLegacy(page))) and not is_equation:
                    if re.match(level2_matchstr, line_text):
                        if line_text.startswith('I.') and len(section_title) < 7:  # Considering I. i.e. ABCDEFGHI
                            section_title.append((line_text, 1))
                        else:
                            section_title.append((line_text, 2))
                    elif re.match(level1_matchstr, line_text):
                        section_title.append((line_text, 1))
                # if re.match(REF_MATCHSTR, line_text):
                #     ref_break_flag = True
                #     break
            #     if ref_break_flag:
            #         break
            # if ref_break_flag:
            #     break
        section_title = [(re.search(ABS_MATCHSTR, self.all_text).group(), 1)]\
            + section_title\
            + [(re.search(REF_MATCHSTR, self.all_text).group(), 1)]
        return section_title if withlevel else [t[0] for t in section_title]

    def get_section_textposdict(self):
        section_title = self.get_section_titles()
        section_dict = {}
        for i in range(0, len(section_title)-1):
            title = section_title[i]
            latter_title = section_title[i+1]
            begin_pos = self.all_text.find(title)
            end_pos = self.all_text.find(latter_title)
            section_dict[title] = (begin_pos, end_pos)
            if begin_pos == -1:
                print(f"Warning: {title} not found in all_text.")
        return section_dict
            
    def get_section_textdict(self):
        """
        Get section text dict of the paper.
        :return: Dict of section titles with text content
        FIXME: This will not get Reference content
        """
        section_title = self.get_section_titles(withlevel=False)
        pos_dict = self.get_section_textposdict()
        section_dict = {}
        for title in section_title[:-1]:
            section_dict[title] = self.all_text[pos_dict[title][0]:pos_dict[title][1]]
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
        pos_dict = self.get_section_textposdict()
        section_dict = {}
        for title in section_title[:-1]:
            section_dict[title] = []
            for eqa in eqa_ls:
                if eqa[0] > pos_dict[title][0] and eqa[0] <= pos_dict[title][0]:
                    section_dict[title].append(eqa)
                elif section_dict[title]:
                    break
        return section_dict

    def get_section_imagedict(self, verbose=False):
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
        if verbose:
            print('Total images found:', len(img_ls))
        section_title = self.get_section_titles()
        pos_dict = self.get_section_textposdict()
        section_dict = {}
        match_cnt = 0
        for title in section_title[:-1]:
            for img in img_ls:
                if img[0] > pos_dict[title][0] and img[0] < pos_dict[title][1]:
                    section_dict[title].append(img)
                    match_cnt += 1
                # elif section_dict[title]:
                #     break
        if verbose:
            print('Images match the content:', match_cnt)
        return section_dict


class PDFFigure2PaperParser(PDFPaperParser):
    """
    Parse paper from PDF file with figure2paper
    """
    @override
    def __init__(self, path, title='', url='', authors=[]):
        self.PDFF2data = parsePDF_PDFFigures2(path)
        super().__init__(path, title, url, authors)

    # # FIXME: Doesn't perform well
    # @override
    # def get_section_titles(self, withlevel=False, verbose=False):
    #     PDFFTitles = [(re.search(ABS_MATCHSTR, self.all_text).group(), 1),
    #                   (re.search(INTRO_MATCHSTR, self.all_text).group(), 1)]
    #     for d in self.PDFF2data['sections'][1:]:
    #         if d.get('title'):
    #             title = d['title']['text']
    #         else:
    #             title = d['paragraphs'][0]['text']
    #         if re.match(SECTION_TITLE_MATCHSTR[1], title) and len(PDFFTitles) > 0:  # Considering I. i.e. ABCDEFGHI
    #             PDFFTitles.append((title, 2))
    #         else:
    #             PDFFTitles.append((title, 1))
                
    #     matchStrTitles = super().get_section_titles(withlevel=True)
    #     # TODO: merge it rather than len compare
    #     # titles = PDFFTitles
    #     titles = matchStrTitles
    #     # titles = PDFFTitles if len(PDFFTitles) > len(matchStrTitles) else matchStrTitles
    #     return titles if withlevel else [t[0] for t in titles]

    # @override
    # def get_section_textdict(self):
        # pass

    @override
    def get_abstract(self):
        """
        Get abstract of the paper.
        :return: Abstract text, None if not found
        """
        return self.PDFF2data.get('abstractText').get('text')

    @override
    def get_section_imagedict(self, snapWithCap=SNAP_WITH_CAPTION, verbose=False):
        """
        Get image dict of each section
        :return: Dict of section titles with tuple item list
        (img_text_pos, page_number, img_bbox, img_caption)
        """
        img_ls = []
        for d in self.PDFF2data['figures']:
            if snapWithCap:
                box = get_bounding_box([
                    (d['regionBoundary']['x1'], d['regionBoundary']['y1'],
                     d['regionBoundary']['x2'], d['regionBoundary']['y2']),
                    (d['captionBoundary']['x1'], d['captionBoundary']['y1'],
                     d['captionBoundary']['x2'], d['captionBoundary']['y2'])])
                img_ls.append((get_box_textpos(self.pdf[d['page']], box, self.all_text),
                               d['page'], box))
            else:
                box = (d['regionBoundary']['x1'], d['regionBoundary']['y1'],
                       d['regionBoundary']['x2'], d['regionBoundary']['y2'])
                img_ls.append((get_box_textpos(self.pdf[d['page']], box, self.all_text),
                               d['page'], box, d['caption']))
        if verbose:
            print('Total images found:', len(img_ls))
        section_title = self.get_section_titles()
        pos_dict = self.get_section_textposdict()
        section_dict = {}
        match_cnt = 0
        for title in section_title[:-1]:
            section_dict[title] = []
            if verbose:
                print('Title:', title, 'Begin pos:',
                      pos_dict[title][0], 'End pos:', pos_dict[title][1])
            for img in img_ls:
                if img[0] > pos_dict[title][0] and img[0] < pos_dict[title][1]:
                    section_dict[title].append(img)
                    match_cnt += 1
                # elif section_dict[title]:
                #     break
        if verbose:
            print('Images match the content:', match_cnt)
        return section_dict
