import os
import argparse
from XmindCopilot import XmindCopilot
from XmindCopilot.XmindCopilot.file_shrink import xmind_shrink
from pdf_parser import PDFFigure2PaperParser, PDFPaperParser
from pdf_extract import *
from xmind_tree import Xmindtree
from config import *
from glob import glob


def pdf_processing(pdf_file_path, xmind_file_path, usePDFFigure2=USE_PDFFIGURE2, debug=DEBUG_MODE,
                   apibase=APIBASE, apikeys=APIKEYS, model=MODEL, keyword=KEYWORD,
                   gpt_enable=GPT_ENABLE, openai_proxy=PROXY, rate_limit=THREAD_RATE_LIMIT,
                   fake_response=FAKE_GPT_RESPONSE, maxtoken=MAXTOKEN, language=LANGUAGE):
    if usePDFFigure2:
        paper = PDFFigure2PaperParser(pdf_file_path)
    else:
        paper = PDFPaperParser(pdf_file_path)
    if os.path.isfile(xmind_file_path):
        workbook = XmindCopilot.load(xmind_file_path)
    else:
        workbook = XmindCopilot.load(TEMPLATE_XMIND_PATH)
    sheet = workbook.getPrimarySheet()
    root_topic = sheet.getRootTopic()
    paper_topic = root_topic.addSubTopicbyTitle(paper.title[:15])
    tree = Xmindtree(paper_topic, paper, paper.title[:15],
                     apibase=apibase, apikeys=apikeys, model=model, keyword=keyword,
                     gpt_enable=gpt_enable, openai_proxy=openai_proxy, rate_limit=rate_limit,
                     fake_response=fake_response, maxtoken=maxtoken, language=language)
    tree.gen_summary(verbose=debug)
    tree.save_xmind(xmind_file_path)
    if debug:
        paper.save_pdf(debug=True)


def pdf_batch_processing(path, usePDFFigure2=USE_PDFFIGURE2, debug=DEBUG_MODE,
                         apibase=APIBASE, apikeys=APIKEYS, model=MODEL, keyword=KEYWORD,
                         gpt_enable=GPT_ENABLE, openai_proxy=PROXY, rate_limit=THREAD_RATE_LIMIT,
                         fake_response=FAKE_GPT_RESPONSE, maxtoken=MAXTOKEN, language=LANGUAGE):
    if os.path.isdir(path):
        xmind_path = os.path.join(path, "summary.xmind")
        for pdf_path in glob(os.path.join(path, '**/*.pdf'), recursive=True):
            if pdf_path.endswith('.pdf') and not pdf_path.endswith('_debug.pdf'):
                print("\033[92m" + pdf_path)
                pdf_processing(pdf_path, xmind_path, usePDFFigure2=usePDFFigure2, debug=debug,
                               apibase=apibase, apikeys=apikeys, model=model, keyword=keyword,
                               gpt_enable=gpt_enable, openai_proxy=openai_proxy, rate_limit=rate_limit,
                               fake_response=fake_response, maxtoken=maxtoken, language=language)
        print("\033[95mXmind size shrinking...")
        xmind_shrink(xmind_path)
    elif os.path.isfile(path) and path.endswith('.pdf'):
        pdf_path = path
        xmind_path = os.path.splitext(pdf_path)[0] + ".xmind"
        pdf_processing(pdf_path, xmind_path, usePDFFigure2=usePDFFigure2, debug=debug,
                       apibase=apibase, apikeys=apikeys, model=model, keyword=keyword,
                       gpt_enable=gpt_enable, openai_proxy=openai_proxy, rate_limit=rate_limit)
        print("\033[95mXmind size shrinking...")
        xmind_shrink(xmind_path)
    else:
        print(
            "\033[91m" + "Invalid path! Please input a pdf file or a folder containing pdf files.")
        return


if __name__ == "__main__":
    argparser = argparse.ArgumentParser()
    argparser.add_argument("--path", type=str, default=r'./PDFexample',
                           help="Pdf file or a folder containing pdf files.")
    pdf_batch_processing(argparser.parse_args().path)
