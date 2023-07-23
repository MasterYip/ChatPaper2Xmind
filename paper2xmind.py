import os
import argparse
from XmindCopilot import xmind, fileshrink
from pdf_parser import PDFPaperParser
from pdf_extract import *
from xmind_tree import Xmindtree

TEMPLATE_XMIND_PATH = 'template.xmind'


def pdf_processing(pdf_file_path, xmind_file_path):
    paper = PDFPaperParser(pdf_file_path)
    if os.path.isfile(xmind_file_path):
        workbook = xmind.load(xmind_file_path)
    else:
        workbook = xmind.load(TEMPLATE_XMIND_PATH)
    sheet = workbook.getPrimarySheet()
    root_topic = sheet.getRootTopic()
    paper_topic = root_topic.addSubTopicbyTitle(paper.title[:15])
    tree = Xmindtree(paper_topic, paper, paper.title[:15])
    tree.gen_summary()
    tree.save_xmind(xmind_file_path)


def pdf_batch_processing(path):
    if os.path.isdir(path):
        xmind_path = os.path.join(path, "summary.xmind")
        for pdf_path in os.listdir(path):
            if pdf_path.endswith('.pdf') and not pdf_path.endswith('_processed.pdf'):
                print("\033[92m" + pdf_path)
                pdf_processing(os.path.join(path, pdf_path), xmind_path)
        print("\033[95mXmind size shrinking...")
        fileshrink.xmind_shrink(xmind_path)
    elif os.path.isfile(path) and path.endswith('.pdf'):
        pdf_path = path
        xmind_path = os.path.splitext(pdf_path)[0] + ".xmind"
        pdf_processing(pdf_path, xmind_path)
        print("\033[95mXmind size shrinking...")
        fileshrink.xmind_shrink(xmind_path)
    else:
        print("\033[91m" + "Invalid path! Please input a pdf file or a folder containing pdf files.")
        return


if __name__ == "__main__":
    argparser = argparse.ArgumentParser()
    argparser.add_argument("--path", type=str, default=r'./PDFexample',
                           help="Pdf file or a folder containing pdf files.")
    pdf_batch_processing(argparser.parse_args().path)
