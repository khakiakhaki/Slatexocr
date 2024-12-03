# coding:utf-8
import sys
import base64
import requests
import json
import PyQt5.QtGui
import PyQt5.QtCore
from PyQt5.QtWidgets import (
    QApplication,
    QLabel,
    QPushButton,
    QWidget,
    QGridLayout,
    QLineEdit,
    QSystemTrayIcon,
    QMenu,
    QAction,
)
from PyQt5.QtCore import Qt
from PIL import ImageGrab
import pyperclip
import datetime
from random import Random
import hashlib
import qrimg
from io import BytesIO

global G_config
G_config = {}


def loadconfig():
    global G_config
    if G_config:
        return True
    try:
        with open("config.json", "r") as f:
            G_config = json.load(f)
            return True
    except FileNotFoundError:
        return False


copy_icon_url = ":img/img/copy.png"
edit_icon_url = ":img/img/edit.png"
copied_icon_url = ":img/img/copied.png"
app_icon_url = ":img/img/icon.png"


class Img2Latex(QWidget):
    imagedata = None

    def __init__(self):
        super().__init__()
        self.initUI()
        self.createTrayIcon()

    def initUI(self):
        self.setGeometry(300, 300, 800, 700)
        self.setWindowTitle("Slatexocr")

        # Determine the base path for resources
        # Set window icon
        self.setWindowIcon(PyQt5.QtGui.QIcon(app_icon_url))
        # copy latex
        self.Latex1copyBtn = QPushButton()
        self.Latex2copyBtn = QPushButton()
        self.Latex3copyBtn = QPushButton()
        # set copy btn icon
        self.Latex1copyBtn.setIcon(PyQt5.QtGui.QIcon(copy_icon_url))
        self.Latex2copyBtn.setIcon(PyQt5.QtGui.QIcon(copy_icon_url))
        self.Latex3copyBtn.setIcon(PyQt5.QtGui.QIcon(copy_icon_url))

        # edit latex
        self.Latex1EditBtn = QPushButton()
        self.Latex2EditBtn = QPushButton()
        self.Latex3EditBtn = QPushButton()
        # set edit btn icon
        self.Latex1EditBtn.setIcon(PyQt5.QtGui.QIcon(edit_icon_url))
        self.Latex2EditBtn.setIcon(PyQt5.QtGui.QIcon(edit_icon_url))
        self.Latex3EditBtn.setIcon(PyQt5.QtGui.QIcon(edit_icon_url))

        # img to latex convert btn
        self.img2latexBtn = QPushButton("convert")

        # show the picture on clipboard
        self.imgLable = QLabel()

        # show the formula in latex
        self.Latex1Edit = QLineEdit()
        self.Latex2Edit = QLineEdit()
        self.Latex3Edit = QLineEdit()
        self.Latex1Edit.setEnabled(False)
        self.Latex2Edit.setEnabled(False)
        self.Latex3Edit.setEnabled(False)
        grid = QGridLayout()
        grid.setSpacing(20)

        # 排版
        grid.addWidget(self.imgLable, 1, 0, 5, 3)

        grid.addWidget(self.img2latexBtn, 6, 0, 1, 2)

        grid.addWidget(self.Latex1Edit, 7, 0)
        grid.addWidget(self.Latex1copyBtn, 7, 1)

        grid.addWidget(self.Latex2copyBtn, 8, 1)
        grid.addWidget(self.Latex2Edit, 8, 0)

        grid.addWidget(self.Latex3copyBtn, 9, 1)
        grid.addWidget(self.Latex3Edit, 9, 0)

        self.setLayout(grid)

        # sign and slot

        # img to latex convert
        self.img2latexBtn.clicked.connect(self.convert)

        # copy latex
        self.Latex1copyBtn.clicked.connect(self.copyLatex1)
        self.Latex2copyBtn.clicked.connect(self.copyLatex2)
        self.Latex3copyBtn.clicked.connect(self.copyLatex3)

        # beautify the window
        self.Beautify()
        self.show()

    def Beautify(self):
        self.setWindowOpacity(1)  # 设置窗口透明度
        pe = PyQt5.QtGui.QPalette()
        self.setAutoFillBackground(True)
        pe.setColor(PyQt5.QtGui.QPalette.Background, Qt.black)
        self.setPalette(pe)
        self.imgLable.setStyleSheet(
            """ QLabel{
                border: 2px solid red;
                border-radius:15px;
                padding:2px 4px;
                background-color:#aaa;
            }"""
        )
        self.Latex1Edit.setStyleSheet(
            """QLineEdit{
            border:1px solid gray;
            border-radius:10px;
            padding:2px 4px;
            background-color:#ddd;
            height:35px;
            color:#000000;
            font-weight:400;
            font-size:24px;
            font-family: Consolas;
            }"""
        )
        self.Latex2Edit.setStyleSheet(
            """QLineEdit{
            border:1px solid gray;
            border-radius:10px;
            padding:2px 4px;
            background-color:#ddd;
            height:35px;
            color:#000000;
            font-weight:400;
            font-size:24px;
            font-family: Consolas;
            }"""
        )
        self.Latex3Edit.setStyleSheet(
            """QLineEdit{
            border:1px solid gray;
            border-radius:10px;
            padding:2px 4px;
            background-color:#ddd;
            height:35px;
            color:#000000;
            font-weight:400;
            font-size:24px;
            font-family: Consolas;
            }"""
        )

        self.Latex1copyBtn.setStyleSheet(
            """QPushButton{
                border:1px solid gray;
                border-radius:4px;
                padding:5px 5px;
                height:35px
            }"""
        )
        self.Latex2copyBtn.setStyleSheet(
            """QPushButton{
                border:1px solid gray;
                border-radius:4px;
                padding:5px 5px;
                height:35px
            }"""
        )
        self.Latex3copyBtn.setStyleSheet(
            """QPushButton{
                border:1px solid gray;
                border-radius:4px;
                padding:5px 5px;
                height:35px
            }"""
        )

        self.img2latexBtn.setStyleSheet(
            """QPushButton{
                border:2px solid gray;
                border-radius:10px;
                padding:5px 5px;
                background-color:#555;
                font-size:24px;
                color:#fff;
                font-weight:700;
                font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
            }"""
        )

    def createTrayIcon(self):
        self.trayIcon = QSystemTrayIcon(self)
        self.trayIcon.setIcon(PyQt5.QtGui.QIcon(app_icon_url))

        trayMenu = QMenu(self)
        restoreAction = QAction("Restore", self)
        quitAction = QAction("Exit", self)

        restoreAction.triggered.connect(self.showNormal)
        quitAction.triggered.connect(QApplication.instance().quit)

        trayMenu.addAction(restoreAction)
        trayMenu.addAction(quitAction)

        self.trayIcon.setContextMenu(trayMenu)
        self.trayIcon.activated.connect(self.onTrayIconActivated)
        self.trayIcon.show()

    def onTrayIconActivated(self, reason):
        if reason == QSystemTrayIcon.Trigger:
            self.showNormal()

    def closeEvent(self, event):
        event.ignore()
        self.hide()
        self.trayIcon.showMessage(
            "Img2Latex",
            "Application was minimized to tray.",
            QSystemTrayIcon.Information,
            2000,
        )

    def image_uri(self, filename):
        return "data:image/jpg;base64," + base64.b64encode(self.image_data).decode()

    def latex(self):
        if not G_config:
            if not loadconfig():
                return {"res": {"latex": "config file not found!"}}

        def get_req_data(req_data, appid, secret):
            global G_config

            def random_str(randomlength=16):
                str = ""
                chars = "AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789"
                length = len(chars) - 1
                random = Random()
                for i in range(randomlength):
                    str += chars[random.randint(0, length)]
                return str

            header = {}
            header["timestamp"] = str(int(datetime.datetime.now().timestamp()))
            header["random-str"] = random_str(16)
            header["app-id"] = appid
            pre_sign_string = ""
            sorted_keys = list(req_data.keys()) + list(header)
            sorted_keys.sort()
            for key in sorted_keys:
                if pre_sign_string:
                    pre_sign_string += "&"
                if key in header:
                    pre_sign_string += key + "=" + str(header[key])
                else:
                    pre_sign_string += key + "=" + str(req_data[key])

            pre_sign_string += "&secret=" + secret
            header["sign"] = hashlib.md5(pre_sign_string.encode()).hexdigest()
            return header, req_data

        img_file = img_file = {"file": ("1.png", self.imagedata, "1.png")}
        data = {}
        header, data = get_req_data(data, G_config["appid"], G_config["appsecret"])
        res = requests.post(
            G_config["url"],
            files=img_file,
            data=data,
            headers=header,
        )
        if res.status_code != 200:
            return {
                "res": {
                    "latex": "error: " + json.loads(res.text)["err_info"]["err_msg"]
                }
            }
        return json.loads(res.text)

    def grapclipboard(self):
        im = ImageGrab.grabclipboard()
        if im:
            buffered = BytesIO()
            im.save(buffered, format="PNG")
            buffered.seek(0)
            self.imagedata = buffered.read()
            self.adjust_image_size()
            # self.imgLable.setPixmap(PyQt5.QtGui.QPixmap(r'.\img\equa.png'))
        else:
            self.Latex1Edit.setText("No image found in clipboard")

    def adjust_image_size(self):
        pixmap = PyQt5.QtGui.QPixmap()
        pixmap.loadFromData(self.imagedata)
        if pixmap.width() > self.width():
            pixmap = pixmap.scaledToWidth(self.width(), Qt.SmoothTransformation)
        self.imgLable.setPixmap(pixmap)
        QApplication.processEvents()

    def keyPressEvent(self, event):
        global G_config
        if (event.key() == Qt.Key_V) and (event.modifiers() == Qt.ControlModifier):
            self.convert()
        if (event.key() == Qt.Key_C) and (event.modifiers() == Qt.ControlModifier):
            if G_config["copywhich"] == 1:
                self.copyLatex1()
            elif G_config["copywhich"] == 2:
                self.copyLatex2()
            else:
                self.copyLatex3()

    def convert(self):
        try:
            self.grapclipboard()
            r = self.latex()
            latex1 = r["res"]["latex"]
        except Exception:
            latex1 = "img to latex failed, please retry again!"
            self.Latex1Edit.setText(latex1)
        else:
            latex2 = "$" + latex1 + "$"
            latex3 = "$$" + latex1 + "$$"
            self.Latex1Edit.setText(latex1)
            self.Latex2Edit.setText(latex2)
            self.Latex3Edit.setText(latex3)
            self.Latex1copyBtn.setIcon(PyQt5.QtGui.QIcon(copy_icon_url))
            self.Latex2copyBtn.setIcon(PyQt5.QtGui.QIcon(copy_icon_url))
            self.Latex3copyBtn.setIcon(PyQt5.QtGui.QIcon(copy_icon_url))

    def copyLatex1(self):
        text = self.Latex1Edit.text()
        pyperclip.copy(text)
        self.Latex1copyBtn.setIcon(PyQt5.QtGui.QIcon(copied_icon_url))

    def copyLatex2(self):
        text = self.Latex2Edit.text()
        pyperclip.copy(text)
        self.Latex2copyBtn.setIcon(PyQt5.QtGui.QIcon(copied_icon_url))

    def copyLatex3(self):
        text = self.Latex3Edit.text()
        pyperclip.copy(text)
        self.Latex3copyBtn.setIcon(PyQt5.QtGui.QIcon(copied_icon_url))

    # def resizeEvent(self, event):
    #     if self.imagedata:
    #         self.adjust_image_size()
    #     super().resizeEvent(event)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = Img2Latex()
    sys.exit(app.exec_())
