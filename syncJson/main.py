import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import uic
import pandas as pd
import json

form_class = uic.loadUiType("sync_json.ui")[0]
app_name = "Sync Json Manager"
version = " ver. 1.0.0"


class WindowClass(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle(app_name + version)  # 프로그램 이름 설정
        self.initUI()
        self.json_src = {}
        self.json_tar = {}
        self.df = None

    def initUI(self):
        # Buttons
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
        self.tableWidget_cmp.setColumnCount(3)  # 두 개의 컬럼을 설정 (Key, Value)
        self.tableWidget_cmp.setHorizontalHeaderLabels(["Key", "Before", "After"])
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

    def saveFileDialog(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save JSON File",
            "",
            "JSON Files (*.json);;All Files (*)",
            options=options,
        )
        return file_path

    def update_common_keys(self, src, tar, df=None):
        # Initialize df only if it's the top-level call
        if self.df is None:
            self.df = pd.DataFrame(columns=["Key", "Before", "After"])

        try:
            for key, value in src.items():
                if key in tar:
                    if isinstance(value, dict) and isinstance(tar[key], dict):
                        # Recursive call with df passed along to accumulate results
                        self.update_common_keys(value, tar[key], df)
                    else:
                        # Append the change to df
                        self.df = pd.concat(
                            [
                                self.df,
                                pd.DataFrame(
                                    [{"Key": key, "Before": tar[key], "After": value}]
                                ),
                            ],
                            ignore_index=True,
                        )
                        print(f"Match: {key}: {tar[key]} -> {value}")
                        tar[key] = value  # Update target value
        except Exception as e:
            print(f"Exception occurred: {e}")

    def clear(self):
        self.label_src.setText("")
        self.label_tar.setText("")
        self.tableWidget_cmp.clear()
        self.df.drop(self.df.index, inplace=True)
        self.json_src = []
        self.json_tar = []

    def saveHandler(self):
        path = self.saveFileDialog()
        with open(path, "w") as outfile:
            json.dump(self.json_tar, outfile, indent=4)

    def compare(self):
        self.load_json_to_dict()
        self.update_common_keys(self.json_src, self.json_tar)
        self.display_table()

    def display_table(self):
        self.tableWidget_cmp.setRowCount(0)  # reset
        self.tableWidget_cmp.setHorizontalHeaderLabels(
            ["TuneKey Name", "Before Value", "After Value"]
        )

        if self.df is not None:
            for i in range(len(self.df)):
                self.tableWidget_cmp.insertRow(i)

                # Key Column
                item_key = QTableWidgetItem(str(self.df.at[i, "Key"]))
                item_key.setTextAlignment(Qt.AlignRight)
                self.tableWidget_cmp.setItem(i, 0, item_key)

                # Before Column
                item_before = QTableWidgetItem(str(self.df.at[i, "Before"]))
                item_before.setTextAlignment(Qt.AlignRight)
                self.tableWidget_cmp.setItem(i, 1, item_before)

                # After Column
                item_after = QTableWidgetItem(str(self.df.at[i, "After"]))
                item_after.setTextAlignment(Qt.AlignRight)
                self.tableWidget_cmp.setItem(i, 2, item_after)
        else:
            print("dataframe is None!")

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
