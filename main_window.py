'''
Author: MasterYip 2205929492@qq.com
Date: 2023-10-08 09:23:35
LastEditors: MasterYip
LastEditTime: 2023-10-08 15:10:14
FilePath: \ChatPaper2Xmind\main_window.py
Description: file content
'''

import os
import sys
import json
from config import *
from paper2xmind import pdf_batch_processing
from user_interface_ui_pyqt5 import *
from PyQt5.QtCore import QThread, pyqtSignal, QRect
from PyQt5.QtWidgets import QApplication, QMainWindow, QLineEdit

# Directory Management
try:
    # Run in Terminal
    ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
except:
    # Run in ipykernel & interactive
    ROOT_DIR = os.getcwd()


class OutputRedirectThread(QThread):
    signalForText = pyqtSignal(str)

    def __init__(self, data=None, parent=None):
        super(OutputRedirectThread, self).__init__(parent)
        self.data = data

    def write(self, text):
        self.signalForText.emit(str(text))


class FileEdit(QLineEdit):
    def __init__(self, parent):
        super(FileEdit, self).__init__(parent)

        self.setDragEnabled(True)

    def dragEnterEvent(self, event):
        data = event.mimeData()
        urls = data.urls()
        if (urls and urls[0].scheme() == 'file'):
            event.acceptProposedAction()

    def dragMoveEvent(self, event):
        data = event.mimeData()
        urls = data.urls()
        if (urls and urls[0].scheme() == 'file'):
            event.acceptProposedAction()

    def dropEvent(self, event):
        data = event.mimeData()
        urls = data.urls()
        if (urls and urls[0].scheme() == 'file'):
            # for some reason, this doubles up the intro slash
            filepath = str(urls[0].path())[1:]
            self.setText(filepath)


class MainWindow(QMainWindow, Ui_MainWindow):
    textColors = ['FF5C5C', '398AD9', '5BEC8D',
                  'FD42AC', 'FF33FF', '4B8200', 'DE87B8']
    config_dir = os.path.join(ROOT_DIR, "config.json")

    def __init__(self, parent=None):
        super().__init__()
        self.setupUi(self)
        # TODO: Redirecting stdout and stderr to MainWindow leads to non-responding
        # self.th = OutputRedirectThread()
        # self.th.signalForText.connect(self.onUpdateTerminal)
        # sys.stdout = self.th
        # sys.stderr = self.th
        self.config = {}
        self.comboBox_LANGUAGE.addItems(["English", "Chinese"])
        self.comboBox_MODEL.addItems(["gpt-3.5-turbo"])
        # Default config
        self.lineEdit_APIBASE.setText(APIBASE)
        self.textEdit_APIKEYS.setText("\n".join(APIKEYS))
        self.comboBox_LANGUAGE.setCurrentText(LANGUAGE)
        self.comboBox_MODEL.setCurrentText(MODEL)
        self.spinBox_MAXTOKEN.setValue(MAXTOKEN)
        self.lineEdit_KEYWORD.setText(KEYWORD)
        self.lineEdit_PROXY.setText(PROXY)

        self.checkBox_GEN_IMGS.setChecked(GEN_IMGS)
        self.checkBox_GEN_EQUATIONS.setChecked(GEN_EQUATIONS)
        self.checkBox_USE_PDFFIGURE2.setChecked(USE_PDFFIGURE2)
        self.checkBox_SNAP_WITH_CAPTION.setChecked(SNAP_WITH_CAPTION)
        self.lineEdit_FAKE_GPT_RESPONSE.setText(FAKE_GPT_RESPONSE)
        self.checkBox_GPT_ENABLE.setChecked(GPT_ENABLE)
        self.spinBox_TEXT2LIST_MAX_NUM.setValue(TEXT2LIST_MAX_NUM)
        self.spinBox_TEXT2TREE_MAX_NUM.setValue(TEXT2TREE_MAX_NUM)
        self.spinBox_THREAD_RATE_LIMIT.setValue(THREAD_RATE_LIMIT)

        self.load_config()

        # Path drag and drop
        self.lineEdit_PATH = FileEdit(self.groupBox_3)
        self.lineEdit_PATH.setObjectName(u"lineEdit_PATH")
        self.lineEdit_PATH.setGeometry(QRect(20, 10, 311, 20))

        self.pushButton_GENERATE.clicked.connect(self.generate_xmind)
        self.pushButton_SAVE_CONFIG.clicked.connect(self.save_config)

    def load_config(self):
        if os.path.isfile(self.config_dir):
            with open(self.config_dir, 'r') as f:
                config = json.load(f)
            self.lineEdit_APIBASE.setText(config['APIBASE'])
            self.textEdit_APIKEYS.setText("\n".join(config['APIKEYS']))
            self.comboBox_LANGUAGE.setCurrentText(config['LANGUAGE'])
            self.comboBox_MODEL.setCurrentText(config['MODEL'])
            self.spinBox_MAXTOKEN.setValue(config['MAXTOKEN'])
            self.lineEdit_KEYWORD.setText(config['KEYWORD'])
            self.lineEdit_PROXY.setText(config['PROXY'])

            self.checkBox_GEN_IMGS.setChecked(config['GEN_IMGS'])
            self.checkBox_GEN_EQUATIONS.setChecked(config['GEN_EQUATIONS'])
            self.checkBox_USE_PDFFIGURE2.setChecked(config['USE_PDFFIGURE2'])
            self.checkBox_SNAP_WITH_CAPTION.setChecked(
                config['SNAP_WITH_CAPTION'])
            self.lineEdit_FAKE_GPT_RESPONSE.setText(
                config['FAKE_GPT_RESPONSE'])
            self.checkBox_GPT_ENABLE.setChecked(config['GPT_ENABLE'])
            self.spinBox_TEXT2LIST_MAX_NUM.setValue(
                config['TEXT2LIST_MAX_NUM'])
            self.spinBox_TEXT2TREE_MAX_NUM.setValue(
                config['TEXT2TREE_MAX_NUM'])
            self.spinBox_THREAD_RATE_LIMIT.setValue(
                config['THREAD_RATE_LIMIT'])
            self.config = config

    def update_config(self):
        self.config['APIBASE'] = self.lineEdit_APIBASE.text()
        self.config['APIKEYS'] = self.textEdit_APIKEYS.toPlainText().splitlines()
        self.config['LANGUAGE'] = self.comboBox_LANGUAGE.currentText()
        self.config['MODEL'] = self.comboBox_MODEL.currentText()
        self.config['MAXTOKEN'] = self.spinBox_MAXTOKEN.value()
        self.config['KEYWORD'] = self.lineEdit_KEYWORD.text()
        self.config['PROXY'] = self.lineEdit_PROXY.text()

        self.config['GEN_IMGS'] = self.checkBox_GEN_IMGS.isChecked()
        self.config['GEN_EQUATIONS'] = self.checkBox_GEN_EQUATIONS.isChecked()
        self.config['USE_PDFFIGURE2'] = self.checkBox_USE_PDFFIGURE2.isChecked()
        self.config['SNAP_WITH_CAPTION'] = self.checkBox_SNAP_WITH_CAPTION.isChecked()
        self.config['FAKE_GPT_RESPONSE'] = self.lineEdit_FAKE_GPT_RESPONSE.text()
        self.config['GPT_ENABLE'] = self.checkBox_GPT_ENABLE.isChecked()
        self.config['TEXT2LIST_MAX_NUM'] = self.spinBox_TEXT2LIST_MAX_NUM.value()
        self.config['TEXT2TREE_MAX_NUM'] = self.spinBox_TEXT2TREE_MAX_NUM.value()
        self.config['THREAD_RATE_LIMIT'] = self.spinBox_THREAD_RATE_LIMIT.value()

    def save_config(self):
        self.update_config()
        with open(self.config_dir, 'w') as f:
            json.dump(self.config, f, indent=4)

    def generate_xmind(self):
        self.update_config()
        pdf_batch_processing(self.lineEdit_PATH.text(), usePDFFigure2=self.config['USE_PDFFIGURE2'],
                             apibase=self.config['APIBASE'], apikeys=self.config['APIKEYS'],
                             model=self.config['MODEL'], keyword=self.config['KEYWORD'],
                             gpt_enable=self.config['GPT_ENABLE'], openai_proxy=self.config['PROXY'],
                             rate_limit=self.config['THREAD_RATE_LIMIT'])

    # def onUpdateTerminal(self, text):
    #     self.textBrowser_Terminal.moveCursor(QTextCursor.End)
    #     text = re.sub(r'\033\[\d+m', '', text)
    #     self.textBrowser_Terminal.insertPlainText(text)
    #     # FIXME: Insert colored text
    #     # for line in text.splitlines():
    #     #     if line.startswith("\033[91m"):
    #     #         self.textBrowser_Terminal.setTextColor(
    #     #             QColor(self.textColors[0]))
    #     #         self.textBrowser_Terminal.insertPlainText(line[5:])
    #     #     elif line.startswith("\033[92m"):
    #     #         self.textBrowser_Terminal.setTextColor(
    #     #             QColor(self.textColors[1]))
    #     #         self.textBrowser_Terminal.insertPlainText(line[5:])
    #     #     else:
    #     #         # self.textBrowser_Terminal.setTextColor(
    #     #         #     QColor(self.textColors[2]))
    #     #         self.textBrowser_Terminal.insertPlainText(line)
    #     self.textBrowser_Terminal.moveCursor(QTextCursor.End)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    myWin = MainWindow()
    myWin.show()

    sys.exit(app.exec())
