import os
from XmindCopilot import xmind, search
from pdf_parser import PDFFigure2PaperParser, PDFPaperParser
from pdf_extract import *
from xmind_tree import Xmindtree
from matplotlib.pyplot import plot
import json

def pdf2xmind():
    # file_dir = "E:\\Temp\\pdf_process\\SFD2 Semantic-guided Feature Detection and Description.pdf"
    file_dir = "E:\\CodeTestFile\\comprehensive-coding\\Python\\GPT_PDF2Xmind\\PDFexample\\2019_Passive Whole-body Control for Quadruped Robots.pdf"
    file_dir = "E:\\CodeTestFile\\Github-opensource-repo\\ChatPaper2Xmind\\PDFexample\\2022_Perceptive Locomotion through Nonlinear Model Predictive Control_debug.pdf"

    # paper = PDFFigure2PaperParser(file_dir)
    paper = PDFPaperParser(file_dir)
    workbook = xmind.load("E:\\Temp\\Test.xmind")
    sheet = workbook.getPrimarySheet()
    root_topic = sheet.getRootTopic()
    tree = Xmindtree(root_topic, paper, paper.title[:10])
    tree.gen_summary(verbose=True)
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
    # file_dir = "E:\\CodeTestFile\\Github-opensource-repo\\ChatPaper2Xmind\\PDFexample\\2021_A Unified MPC Framework for Whole-Body Dynamic Locomotion and Manipulation.pdf"
    # file_dir = "E:\\CodeTestFile\\Github-opensource-repo\\ChatPaper2Xmind\\PDFexample\\2022_Perceptive Locomotion through Nonlinear Model Predictive Control.pdf"
    # paper = PDFPaperParser(file_dir)
    paper = PDFFigure2PaperParser(file_dir)
    # page = paper.pdf[4]
    # content_dict = paper.get_section_textdict()
    section_names = paper.get_section_titles(verbose=True)
    for name in section_names:
        print(name)
    # draw_all_textbbox(paper.pdf)
    # rects = getEqRect(page, True)
    # for rect in rects:
    #     print(rect)
    # paper.pdf.save(os.path.splitext(file_dir)[0]+"_debug.pdf")


if __name__ == "__main__":
    # pdf2xmind()
    pdfTest()




    

