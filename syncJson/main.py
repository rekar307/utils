import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import uic
import pandas as pd
import json

form_class = uic.loadUiType("sync_json.ui")[0]


class WindowClass(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.initUI()
        self.json_src = {}
        self.json_tar = {}
        self.df = pd.DataFrame(columns=["Key", "Value"])

    def initUI(self):
        # Buttons
        self.pushButton_apply.clicked.connect(lambda: self.apply())
        self.pushButton_clear.clicked.connect(lambda: self.clear())
        self.pushButton_save.clicked.connect(lambda: self.saveHandler())
        self.pushButton_cmp.clicked.connect(lambda: self.compare())
        self.pushButton_src.clicked.connect(
            lambda: self.openFileHandler(self.label_src)
        )
        self.pushButton_tar.clicked.connect(
            lambda: self.openFileHandler(self.label_tar)
        )

        # Labels
        self.label_src.setText("")
        self.label_tar.setText("")

        # Menu
        self.actionExit.triggered.connect(self.close)

        # tableWidget
        self.tableWidget_cmp.setColumnCount(2)  # 두 개의 컬럼을 설정 (Key, Value)
        self.tableWidget_cmp.setHorizontalHeaderLabels(["Key", "Value"])
        self.tableWidget_cmp.clear()

    def openFileHandler(self, label):
        file_path = self.openFileDialog()
        if file_path:
            label.setText(file_path)

    def openFileDialog(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(
            self, "File Choose", "", "Json File (*.json)", options=options
        )
        return file_path

    def update_common_keys(self, src, tar):
        # 이 함수에서 DataFrame에 데이터를 추가
        for key, value in src.items():
            if key in tar:
                if isinstance(value, dict) and isinstance(tar[key], dict):
                    self.update_common_keys(value, tar[key])  # 재귀적으로 비교
                else:
                    # DataFrame에 key와 value 추가
                    self.df = self.df.append(
                        {"Key": key, "Value": value}, ignore_index=True
                    )
                    tar[key] = value  # 값을 덮어쓰기
        return tar

    def apply(self):
        pass

    def clear(self):
        self.label_src.setText("")
        self.label_tar.setText("")
        self.tableWidget_cmp.clear()
        self.df.reset()
        self.json_src = []
        self.json_tar = []

    def saveHandler(self):
        path = self.openFileDialog()
        if path:
            pass

    def compare(self):
        self.load_json_to_dict()
        # updated_data = self.update_common_keys(self.json_src, self.json_tar)
        # print(json.dumps(updated_data, indent=4))
        # self.display_table()
        with open("self.label_src") as f:
            data = json.load(f)
        df = json_normalize(data, "products", ["store_info"])
        print(df)

    def display_table(self):
        # pandas DataFrame에서 QTableWidget으로 데이터 추가
        self.tableWidget_cmp.setRowCount(0)  # 기존 데이터 초기화
        for i in range(len(self.df)):
            self.tableWidget_cmp.insertRow(i)
            self.tableWidget_cmp.setItem(
                i, 0, QTableWidgetItem(str(self.df.at[i, "Key"]))
            )  # Key
            self.tableWidget_cmp.setItem(
                i, 1, QTableWidgetItem(str(self.df.at[i, "Value"]))
            )  # Value

    def load_json_to_dict(self):
        with open(self.label_src.text(), "r") as src_file:
            self.json_src = json.load(src_file)
        with open(self.label_tar.text(), "r") as tar_file:
            self.json_tar = json.load(tar_file)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = WindowClass()
    myWindow.show()
    app.exec_()
