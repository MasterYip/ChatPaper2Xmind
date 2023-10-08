# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'user_interface.ui'
##
## Created by: Qt User Interface Compiler version 6.5.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QFormLayout,
    QGroupBox, QHBoxLayout, QLabel, QLineEdit,
    QMainWindow, QMenuBar, QPushButton, QSizePolicy,
    QSpinBox, QStatusBar, QTextBrowser, QTextEdit,
    QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(737, 553)
        MainWindow.setAcceptDrops(True)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.groupBox = QGroupBox(self.centralwidget)
        self.groupBox.setObjectName(u"groupBox")
        self.groupBox.setGeometry(QRect(10, 10, 351, 341))
        self.formLayoutWidget = QWidget(self.groupBox)
        self.formLayoutWidget.setObjectName(u"formLayoutWidget")
        self.formLayoutWidget.setGeometry(QRect(20, 30, 311, 291))
        self.formLayout = QFormLayout(self.formLayoutWidget)
        self.formLayout.setObjectName(u"formLayout")
        self.formLayout.setContentsMargins(0, 0, 0, 0)
        self.label = QLabel(self.formLayoutWidget)
        self.label.setObjectName(u"label")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.label)

        self.lineEdit_APIBASE = QLineEdit(self.formLayoutWidget)
        self.lineEdit_APIBASE.setObjectName(u"lineEdit_APIBASE")

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.lineEdit_APIBASE)

        self.label_2 = QLabel(self.formLayoutWidget)
        self.label_2.setObjectName(u"label_2")

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.label_2)

        self.label_7 = QLabel(self.formLayoutWidget)
        self.label_7.setObjectName(u"label_7")

        self.formLayout.setWidget(9, QFormLayout.LabelRole, self.label_7)

        self.lineEdit_PROXY = QLineEdit(self.formLayoutWidget)
        self.lineEdit_PROXY.setObjectName(u"lineEdit_PROXY")

        self.formLayout.setWidget(9, QFormLayout.FieldRole, self.lineEdit_PROXY)

        self.label_6 = QLabel(self.formLayoutWidget)
        self.label_6.setObjectName(u"label_6")

        self.formLayout.setWidget(8, QFormLayout.LabelRole, self.label_6)

        self.lineEdit_KEYWORD = QLineEdit(self.formLayoutWidget)
        self.lineEdit_KEYWORD.setObjectName(u"lineEdit_KEYWORD")

        self.formLayout.setWidget(8, QFormLayout.FieldRole, self.lineEdit_KEYWORD)

        self.label_4 = QLabel(self.formLayoutWidget)
        self.label_4.setObjectName(u"label_4")

        self.formLayout.setWidget(7, QFormLayout.LabelRole, self.label_4)

        self.spinBox_MAXTOKEN = QSpinBox(self.formLayoutWidget)
        self.spinBox_MAXTOKEN.setObjectName(u"spinBox_MAXTOKEN")
        self.spinBox_MAXTOKEN.setMaximum(99999)

        self.formLayout.setWidget(7, QFormLayout.FieldRole, self.spinBox_MAXTOKEN)

        self.label_3 = QLabel(self.formLayoutWidget)
        self.label_3.setObjectName(u"label_3")

        self.formLayout.setWidget(6, QFormLayout.LabelRole, self.label_3)

        self.comboBox_MODEL = QComboBox(self.formLayoutWidget)
        self.comboBox_MODEL.setObjectName(u"comboBox_MODEL")

        self.formLayout.setWidget(6, QFormLayout.FieldRole, self.comboBox_MODEL)

        self.label_5 = QLabel(self.formLayoutWidget)
        self.label_5.setObjectName(u"label_5")

        self.formLayout.setWidget(5, QFormLayout.LabelRole, self.label_5)

        self.comboBox_LANGUAGE = QComboBox(self.formLayoutWidget)
        self.comboBox_LANGUAGE.setObjectName(u"comboBox_LANGUAGE")

        self.formLayout.setWidget(5, QFormLayout.FieldRole, self.comboBox_LANGUAGE)

        self.textEdit_APIKEYS = QTextEdit(self.formLayoutWidget)
        self.textEdit_APIKEYS.setObjectName(u"textEdit_APIKEYS")

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.textEdit_APIKEYS)

        self.groupBox_2 = QGroupBox(self.centralwidget)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.groupBox_2.setGeometry(QRect(380, 10, 351, 261))
        self.formLayoutWidget_2 = QWidget(self.groupBox_2)
        self.formLayoutWidget_2.setObjectName(u"formLayoutWidget_2")
        self.formLayoutWidget_2.setGeometry(QRect(20, 30, 321, 211))
        self.formLayout_2 = QFormLayout(self.formLayoutWidget_2)
        self.formLayout_2.setObjectName(u"formLayout_2")
        self.formLayout_2.setContentsMargins(0, 0, 0, 0)
        self.label_8 = QLabel(self.formLayoutWidget_2)
        self.label_8.setObjectName(u"label_8")

        self.formLayout_2.setWidget(0, QFormLayout.LabelRole, self.label_8)

        self.checkBox_GEN_IMGS = QCheckBox(self.formLayoutWidget_2)
        self.checkBox_GEN_IMGS.setObjectName(u"checkBox_GEN_IMGS")

        self.formLayout_2.setWidget(0, QFormLayout.FieldRole, self.checkBox_GEN_IMGS)

        self.label_9 = QLabel(self.formLayoutWidget_2)
        self.label_9.setObjectName(u"label_9")

        self.formLayout_2.setWidget(1, QFormLayout.LabelRole, self.label_9)

        self.checkBox_GEN_EQUATIONS = QCheckBox(self.formLayoutWidget_2)
        self.checkBox_GEN_EQUATIONS.setObjectName(u"checkBox_GEN_EQUATIONS")

        self.formLayout_2.setWidget(1, QFormLayout.FieldRole, self.checkBox_GEN_EQUATIONS)

        self.label_10 = QLabel(self.formLayoutWidget_2)
        self.label_10.setObjectName(u"label_10")

        self.formLayout_2.setWidget(2, QFormLayout.LabelRole, self.label_10)

        self.checkBox_USE_PDFFIGURE2 = QCheckBox(self.formLayoutWidget_2)
        self.checkBox_USE_PDFFIGURE2.setObjectName(u"checkBox_USE_PDFFIGURE2")

        self.formLayout_2.setWidget(2, QFormLayout.FieldRole, self.checkBox_USE_PDFFIGURE2)

        self.label_11 = QLabel(self.formLayoutWidget_2)
        self.label_11.setObjectName(u"label_11")

        self.formLayout_2.setWidget(3, QFormLayout.LabelRole, self.label_11)

        self.checkBox_SNAP_WITH_CAPTION = QCheckBox(self.formLayoutWidget_2)
        self.checkBox_SNAP_WITH_CAPTION.setObjectName(u"checkBox_SNAP_WITH_CAPTION")

        self.formLayout_2.setWidget(3, QFormLayout.FieldRole, self.checkBox_SNAP_WITH_CAPTION)

        self.label_13 = QLabel(self.formLayoutWidget_2)
        self.label_13.setObjectName(u"label_13")

        self.formLayout_2.setWidget(4, QFormLayout.LabelRole, self.label_13)

        self.lineEdit_FAKE_GPT_RESPONSE = QLineEdit(self.formLayoutWidget_2)
        self.lineEdit_FAKE_GPT_RESPONSE.setObjectName(u"lineEdit_FAKE_GPT_RESPONSE")

        self.formLayout_2.setWidget(4, QFormLayout.FieldRole, self.lineEdit_FAKE_GPT_RESPONSE)

        self.label_20 = QLabel(self.formLayoutWidget_2)
        self.label_20.setObjectName(u"label_20")

        self.formLayout_2.setWidget(5, QFormLayout.LabelRole, self.label_20)

        self.checkBox_GPT_ENABLE = QCheckBox(self.formLayoutWidget_2)
        self.checkBox_GPT_ENABLE.setObjectName(u"checkBox_GPT_ENABLE")

        self.formLayout_2.setWidget(5, QFormLayout.FieldRole, self.checkBox_GPT_ENABLE)

        self.label_21 = QLabel(self.formLayoutWidget_2)
        self.label_21.setObjectName(u"label_21")
        self.label_21.setScaledContents(False)
        self.label_21.setWordWrap(False)

        self.formLayout_2.setWidget(6, QFormLayout.LabelRole, self.label_21)

        self.spinBox_TEXT2LIST_MAX_NUM = QSpinBox(self.formLayoutWidget_2)
        self.spinBox_TEXT2LIST_MAX_NUM.setObjectName(u"spinBox_TEXT2LIST_MAX_NUM")

        self.formLayout_2.setWidget(6, QFormLayout.FieldRole, self.spinBox_TEXT2LIST_MAX_NUM)

        self.label_22 = QLabel(self.formLayoutWidget_2)
        self.label_22.setObjectName(u"label_22")

        self.formLayout_2.setWidget(7, QFormLayout.LabelRole, self.label_22)

        self.spinBox_TEXT2TREE_MAX_NUM = QSpinBox(self.formLayoutWidget_2)
        self.spinBox_TEXT2TREE_MAX_NUM.setObjectName(u"spinBox_TEXT2TREE_MAX_NUM")

        self.formLayout_2.setWidget(7, QFormLayout.FieldRole, self.spinBox_TEXT2TREE_MAX_NUM)

        self.label_23 = QLabel(self.formLayoutWidget_2)
        self.label_23.setObjectName(u"label_23")

        self.formLayout_2.setWidget(8, QFormLayout.LabelRole, self.label_23)

        self.spinBox_THREAD_RATE_LIMIT = QSpinBox(self.formLayoutWidget_2)
        self.spinBox_THREAD_RATE_LIMIT.setObjectName(u"spinBox_THREAD_RATE_LIMIT")
        self.spinBox_THREAD_RATE_LIMIT.setMaximum(999)

        self.formLayout_2.setWidget(8, QFormLayout.FieldRole, self.spinBox_THREAD_RATE_LIMIT)

        self.groupBox_3 = QGroupBox(self.centralwidget)
        self.groupBox_3.setObjectName(u"groupBox_3")
        self.groupBox_3.setGeometry(QRect(380, 270, 351, 81))
        self.horizontalLayoutWidget = QWidget(self.groupBox_3)
        self.horizontalLayoutWidget.setObjectName(u"horizontalLayoutWidget")
        self.horizontalLayoutWidget.setGeometry(QRect(20, 40, 311, 31))
        self.horizontalLayout = QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.pushButton_SAVE_CONFIG = QPushButton(self.horizontalLayoutWidget)
        self.pushButton_SAVE_CONFIG.setObjectName(u"pushButton_SAVE_CONFIG")

        self.horizontalLayout.addWidget(self.pushButton_SAVE_CONFIG)

        self.pushButton_GENERATE = QPushButton(self.horizontalLayoutWidget)
        self.pushButton_GENERATE.setObjectName(u"pushButton_GENERATE")

        self.horizontalLayout.addWidget(self.pushButton_GENERATE)

        self.pushButton_STOP = QPushButton(self.horizontalLayoutWidget)
        self.pushButton_STOP.setObjectName(u"pushButton_STOP")

        self.horizontalLayout.addWidget(self.pushButton_STOP)

        self.textBrowser_Terminal = QTextBrowser(self.centralwidget)
        self.textBrowser_Terminal.setObjectName(u"textBrowser_Terminal")
        self.textBrowser_Terminal.setGeometry(QRect(30, 360, 681, 131))
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 737, 22))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"ChatPaper2Xmind", None))
#if QT_CONFIG(statustip)
        MainWindow.setStatusTip(QCoreApplication.translate("MainWindow", u"Authored by MasterYip", None))
#endif // QT_CONFIG(statustip)
        self.groupBox.setTitle(QCoreApplication.translate("MainWindow", u"OpenAI API", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"APIBASE", None))
        self.lineEdit_APIBASE.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Default is \"https://api.openai.com/v1\"", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"APIKEYS", None))
        self.label_7.setText(QCoreApplication.translate("MainWindow", u"PROXY", None))
#if QT_CONFIG(statustip)
        self.lineEdit_PROXY.setStatusTip(QCoreApplication.translate("MainWindow", u"[NOTE] The program will NOT follow system proxy! Please enter the proxy if you are using it!", None))
#endif // QT_CONFIG(statustip)
        self.lineEdit_PROXY.setText("")
        self.lineEdit_PROXY.setPlaceholderText(QCoreApplication.translate("MainWindow", u"e.g. http://127.0.0.1:7890", None))
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"KEYWORD", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"MAXTOKEN", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"MODEL", None))
        self.comboBox_MODEL.setCurrentText("")
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"LANGUAGE", None))
        self.comboBox_LANGUAGE.setCurrentText("")
#if QT_CONFIG(statustip)
        self.textEdit_APIKEYS.setStatusTip(QCoreApplication.translate("MainWindow", u"Your APIKEYs splitted in lines", None))
#endif // QT_CONFIG(statustip)
        self.textEdit_APIKEYS.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Should not be empty (No thread will be running)", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("MainWindow", u"Generation", None))
        self.label_8.setText(QCoreApplication.translate("MainWindow", u"GEN_IMGS", None))
        self.checkBox_GEN_IMGS.setText("")
        self.label_9.setText(QCoreApplication.translate("MainWindow", u"GEN_EQUATIONS", None))
        self.checkBox_GEN_EQUATIONS.setText("")
        self.label_10.setText(QCoreApplication.translate("MainWindow", u"USE_PDFFIGURE2", None))
        self.checkBox_USE_PDFFIGURE2.setText("")
        self.label_11.setText(QCoreApplication.translate("MainWindow", u"SNAP_WITH_CAPTION", None))
        self.checkBox_SNAP_WITH_CAPTION.setText("")
        self.label_13.setText(QCoreApplication.translate("MainWindow", u"FAKE_GPT_RESPONSE", None))
        self.label_20.setText(QCoreApplication.translate("MainWindow", u"GPT_ENABLE", None))
        self.checkBox_GPT_ENABLE.setText("")
        self.label_21.setText(QCoreApplication.translate("MainWindow", u"TEXT2LIST_MAX_NUM", None))
        self.label_22.setText(QCoreApplication.translate("MainWindow", u"TEXT2TREE_MAX_NUM", None))
        self.label_23.setText(QCoreApplication.translate("MainWindow", u"THREAD_RATE_LIMIT", None))
        self.groupBox_3.setTitle("")
        self.pushButton_SAVE_CONFIG.setText(QCoreApplication.translate("MainWindow", u"Save Config", None))
        self.pushButton_GENERATE.setText(QCoreApplication.translate("MainWindow", u"Generate", None))
        self.pushButton_STOP.setText(QCoreApplication.translate("MainWindow", u"Stop", None))
    # retranslateUi

