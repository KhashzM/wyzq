import os
import json
import winreg
import warnings
from PyQt5 import QtCore, QtGui, QtWidgets
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QMessageBox, QRadioButton, QWidget
from PyQt5.QtCore import Qt  # 导入 Qt 模块

# 忽略弃用警告
warnings.filterwarnings("ignore", category=DeprecationWarning, message="sipPyTypeDict\(\) is deprecated")

def get_key_name(path):
    """
    生成键名，直接使用文件名（不带后缀）。
    """
    file_name = os.path.basename(path)  # 例如：IDMan.exe
    file_name_without_ext = os.path.splitext(file_name)[0]  # 例如：IDMan
    return f"WYZQ_{file_name_without_ext}"

# 自定义对话框类
class AddDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("添加条目")
        self.setModal(True)  # 设置为模态对话框
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)  # 移除问号按钮
        self.init_ui()

    def init_ui(self):
        # 第一行：文本框 + 按钮
        self.line_edit1 = QLineEdit(self)
        self.line_edit1.setPlaceholderText("请输入路径或点击浏览选择文件")  # 添加内容提示
        self.button1 = QPushButton("浏览", self)
        self.button1.clicked.connect(self.on_browse_clicked)

        hbox1 = QHBoxLayout()
        hbox1.addWidget(self.line_edit1)
        hbox1.addWidget(self.button1)

        # 第二行：文本框
        self.line_edit2 = QLineEdit(self)
        self.line_edit2.setPlaceholderText("请输入备注信息（可选）")  # 添加内容提示

        # 第三行：确认和取消按钮
        self.confirm_button = QPushButton("确认", self)
        self.confirm_button.setDefault(True)  # 将确认按钮设置为默认按钮
        self.cancel_button = QPushButton("取消", self)
        self.confirm_button.clicked.connect(self.on_confirm_clicked)
        self.cancel_button.clicked.connect(self.on_cancel_clicked)

        hbox2 = QHBoxLayout()
        hbox2.addWidget(self.confirm_button)
        hbox2.addWidget(self.cancel_button)

        # 整体布局
        layout = QVBoxLayout()
        layout.addLayout(hbox1)
        layout.addWidget(self.line_edit2)
        layout.addLayout(hbox2)
        self.setLayout(layout)

    def on_browse_clicked(self):
        # 点击“浏览”按钮时，弹出文件选择对话框
        file_path, _ = QtWidgets.QFileDialog.getOpenFileName(self, "选择文件", "", "All Files (*)")
        if file_path:
            self.line_edit1.setText(file_path)

    def on_confirm_clicked(self):
        # 点击“确认”按钮时，检查路径是否为空
        if not self.line_edit1.text():
            QMessageBox.warning(self, "警告", "路径不能为空！")
        else:
            self.accept()  # 关闭对话框并返回 QDialog.Accepted

    def on_cancel_clicked(self):
        self.reject()  # 关闭对话框并返回 QDialog.Rejected

    def get_inputs(self):
        # 返回用户输入的内容
        return self.line_edit1.text(), self.line_edit2.text()

# 主窗口类
class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(768, 487)
        self.verticalLayoutWidget = QtWidgets.QWidget(Form)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(10, 10, 751, 471))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pushButton = QtWidgets.QPushButton(self.verticalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.pushButton.sizePolicy().hasHeightForWidth())
        self.pushButton.setSizePolicy(sizePolicy)
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout.addWidget(self.pushButton)
        self.pushButton_2 = QtWidgets.QPushButton(self.verticalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.pushButton_2.sizePolicy().hasHeightForWidth())
        self.pushButton_2.setSizePolicy(sizePolicy)
        self.pushButton_2.setObjectName("pushButton_2")
        self.horizontalLayout.addWidget(self.pushButton_2)
        self.pushButton_3 = QtWidgets.QPushButton(self.verticalLayoutWidget)  # 新增“应用”按钮
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.pushButton_3.sizePolicy().hasHeightForWidth())
        self.pushButton_3.setSizePolicy(sizePolicy)
        self.pushButton_3.setObjectName("pushButton_3")
        self.horizontalLayout.addWidget(self.pushButton_3)
        spacerItem = QtWidgets.QSpacerItem(300, 40, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.label = QtWidgets.QLabel(self.verticalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(3)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.tableWidget = QtWidgets.QTableWidget(self.verticalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(5)
        sizePolicy.setHeightForWidth(self.tableWidget.sizePolicy().hasHeightForWidth())
        self.tableWidget.setSizePolicy(sizePolicy)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(3)
        self.tableWidget.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.tableWidget.setHorizontalHeaderItem(2, item)
        self.horizontalLayout_2.addWidget(self.tableWidget)
        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.pushButton.setText(_translate("Form", "添加"))
        self.pushButton_2.setText(_translate("Form", "删除"))
        self.pushButton_3.setText(_translate("Form", "应用"))  # 设置“应用”按钮的文本
        self.label.setText(_translate("Form", "TextLabel"))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("Form", "启用"))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("Form", "路径"))
        item = self.tableWidget.horizontalHeaderItem(2)
        item.setText(_translate("Form", "备注"))

# 主窗口逻辑类
class MainWindow(QMainWindow, Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.on_add_clicked)
        self.pushButton_2.clicked.connect(self.on_delete_clicked)
        self.pushButton_3.clicked.connect(self.on_apply_clicked)  # 绑定“应用”按钮的点击事件

        # 设置列宽
        self.tableWidget.setColumnWidth(0, 100)  # 第 0 列（启用）宽度为 100
        self.tableWidget.setColumnWidth(1, 400)  # 第 1 列（路径）宽度为 400
        self.tableWidget.setColumnWidth(2, 150)  # 第 2 列（备注）宽度为 150

        # 启动时加载配置文件
        self.load_config()

    def load_config(self):
        """
        加载配置文件并显示到列表中。
        """
        save_path = os.path.join(os.getenv("LOCALAPPDATA"), "Iwzq")
        json_file = os.path.join(save_path, "data.json")
        if os.path.exists(json_file):
            try:
                with open(json_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                for item in data:
                    self.add_table_row(item["enabled"], item["path"], item["remark"])
            except Exception as e:
                print(f"加载配置文件失败：{e}")

    def add_table_row(self, enabled, path, remark):
        """
        向表格中添加一行数据。
        """
        row_position = self.tableWidget.rowCount()
        self.tableWidget.insertRow(row_position)

        # 在第一列添加单选框
        radio_button_widget = QWidget()
        radio_button_layout = QHBoxLayout(radio_button_widget)
        radio_button_layout.setAlignment(Qt.AlignCenter)  # 居中对齐
        radio_button_layout.setContentsMargins(0, 0, 0, 0)
        radio_button = QRadioButton()
        radio_button.setChecked(enabled)  # 设置单选框状态
        radio_button_layout.addWidget(radio_button)
        self.tableWidget.setCellWidget(row_position, 0, radio_button_widget)

        # 在第二列和第三列添加路径和备注
        self.tableWidget.setItem(row_position, 1, QtWidgets.QTableWidgetItem(path))
        self.tableWidget.setItem(row_position, 2, QtWidgets.QTableWidgetItem(remark))

    def on_add_clicked(self):
        # 弹出添加对话框
        dialog = AddDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            path, remark = dialog.get_inputs()
            # 将用户输入添加到表格中
            self.add_table_row(False, path, remark)  # 默认不启用

    def on_delete_clicked(self):
        # 删除当前选中的行
        current_row = self.tableWidget.currentRow()
        if current_row >= 0:
            self.tableWidget.removeRow(current_row)

    def on_apply_clicked(self):
        # 读取表格中的数据
        data = []
        for row in range(self.tableWidget.rowCount()):
            enabled = self.tableWidget.cellWidget(row, 0).findChild(QRadioButton).isChecked()  # 获取单选框状态
            path = self.tableWidget.item(row, 1).text()  # 获取路径
            remark = self.tableWidget.item(row, 2).text()  # 获取备注
            data.append({
                "enabled": enabled,
                "path": path,
                "remark": remark
            })

        # 保存为 JSON 文件
        save_path = os.path.join(os.getenv("LOCALAPPDATA"), "Iwzq")
        os.makedirs(save_path, exist_ok=True)  # 创建目录（如果不存在）
        json_file = os.path.join(save_path, "data.json")
        with open(json_file, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

        # 编辑注册表
        reg_path = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Run"
        try:
            reg_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, reg_path, 0, winreg.KEY_ALL_ACCESS)
        except FileNotFoundError:
            reg_key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, reg_path)

        # 先处理需要删除的键值对
        for item in data:
            key_name = get_key_name(item["path"])  # 生成键名
            if not item["enabled"]:
                try:
                    winreg.DeleteValue(reg_key, key_name)
                    print(f"删除注册表键值对：{key_name}")
                except FileNotFoundError:
                    print(f"注册表键值对不存在：{key_name}")
                except Exception as e:
                    print(f"删除注册表键值对失败：{e}")

        # 再处理需要创建或更新的键值对
        for item in data:
            item_path = item["path"].replace("/", "\\")  # 路径中不能有斜杠
            working_directory = os.path.dirname(item_path) + "\\"  # 工作目录为路径所在目录
            # 生成键值

            # key_value = f'"{item_path}" "{working_directory}"'  # 键值格式为：“python.exe 路径”
            key_value = f'"{item_path}"'  # 仅用双引号包裹路径
            print('程序路径：',item_path)
            print('工作目录：',working_directory)
            print('键值：',key_value)

            key_name = get_key_name(item_path)  # 生成键名
            if item["enabled"]:
                try:
                    # winreg.SetValueEx(reg_key, key_name, 0, winreg.REG_SZ, item_path)
                    winreg.SetValueEx(reg_key, key_name, 0, winreg.REG_SZ, key_value)
                    print(f"创建/更新注册表键值对：{key_name} = {item_path}")
                except Exception as e:
                    print(f"创建/更新注册表键值对失败：{e}")

        winreg.CloseKey(reg_key)
        QMessageBox.information(self, "提示", "应用成功！")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())