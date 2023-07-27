import os
from XmindCopilot import xmind, search
from pdf_parser import PDFPaperParser
from pdf_extract import *
from xmind_tree import Xmindtree
from matplotlib.pyplot import plot


def pdf2xmind():
    # file_dir = "E:\\Temp\\pdf_process\\SFD2 Semantic-guided Feature Detection and Description.pdf"
    file_dir = "E:\\CodeTestFile\\comprehensive-coding\\Python\\GPT_PDF2Xmind\\PDFexample\\2019_Passive Whole-body Control for Quadruped Robots.pdf"

    paper = PDFPaperParser(file_dir)
    workbook = xmind.load("E:\\Temp\\Fahmi.xmind")
    sheet = workbook.getPrimarySheet()
    root_topic = sheet.getRootTopic()
    tree = Xmindtree(root_topic, paper, paper.title[:10])
    tree.gen_summary()
    tree.save_xmind()


def xmindTest():
    workbook = xmind.load("E:\\Temp\\Fahmi.xmind")
    sheet = workbook.getPrimarySheet()
    root_topic = sheet.getRootTopic()
    topic = search.topic_search(root_topic, "test")
    print(workbook.reference_dir)
    print(topic.getImageAttr())
    xmind.save(workbook)


def pdfTest():
    file_dir = "E:\\SFTRDatapool2\\人工智能核心550篇论文汇总\\1.自然语言处理\\1.语言建模\\1.Semi-supervised Sequence Learning\\1511.01432v1.pdf"
    # file_dir = "E:\\Temp\\pdf_process\\2019_Passive Whole-body Control for Quadruped Robots.pdf"
    # file_dir = "E:\\CodeTestFile\\comprehensive-coding\\Python\\GPT_PDF2Xmind\\PDFexample\\2016_ANYmal - a highly mobile and dynamic quadrupedal robot.pdf"
    paper = PDFPaperParser(file_dir)
    # page = paper.pdf[4]
    content_dict = paper.get_section_textdict()
    section_names = paper.get_section_titles()
    for name in section_names[:-1]:
        print(name, len(content_dict[name]))
    draw_all_textbbox(paper.pdf)
    # rects = getEqRect(page, True)
    # for rect in rects:
    #     print(rect)
    paper.pdf.save(os.path.splitext(file_dir)[0]+"_processed.pdf")


if __name__ == "__main__":
    # pdfTest()
    # pdf2xmind()
    pdfTest()



    

