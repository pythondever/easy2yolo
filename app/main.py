import datetime
import sys
import ctypes
from ui.main import Ui_Trainer as MainUI
from ui.enter_name import Ui_Dialog as EnterName
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from app.train_widget import MyTreeWidget
from PyQt5.QtWidgets import QWidget, QApplication, QDialog, \
    QTreeWidgetItem, QVBoxLayout, QSpacerItem, QSizePolicy
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("trainer")


class App(QWidget, MainUI):
    def __init__(self):
        super().__init__()
        self.train_widget = None
        self.train_layout = None
        self.init_widget()
        self.register_event()

    def init_widget(self):
        self.setupUi(self)
        self.setWindowIcon(QIcon("../resources/favicon.ico"))
        self.train_widget = QWidget(self)
        self.train_layout = QVBoxLayout(self.train_widget)
        self.setWindowFlags(Qt.WindowMinMaxButtonsHint | Qt.WindowCloseButtonHint)
        self.tabWidget.setCurrentIndex(0)

    def register_event(self):
        self.add_train_btn.clicked.connect(lambda: self.add_project_train())

    def add_project_train(self):
        dialog = QDialog(self)
        enter_name = EnterName()
        enter_name.setupUi(dialog)
        enter_name.enter_name_lbl.setVisible(False)
        dialog.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint & ~Qt.WindowMinMaxButtonsHint)
        enter_name.done_enter_name_btn.clicked.connect(lambda: self.add_train_widget(
            enter_name.project_name_txt.text(), dialog))
        dialog.show()

    def show_ui(self):
        self.showMaximized()

    def remove_spacer(self):
        layout = self.train_layout
        for i in range(layout.count()):
            item = layout.itemAt(i)
            spacer = item.spacerItem()
            if spacer is not None:
                layout.removeItem(item)

    def write_log(self, msg, level='info'):
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log = timestamp + '>>' + msg
        self.log_area.append(log)

    def add_train_widget(self, project_name, dialog):
        self.remove_spacer()
        tree = MyTreeWidget(project_name, self)
        tree.setStyleSheet("border: none;")
        tree.setColumnCount(2)
        tree.setColumnWidth(0, 200)
        tree.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        root = QTreeWidgetItem(tree)
        root.setText(0, project_name)
        root.setIcon(0, QIcon("../resources/项目.ico"))
        tree.setMaximumWidth(300)
        tree.setMaximumHeight(80)
        tree.setHeaderHidden(True)
        train_set = QTreeWidgetItem(root)
        train_set.setText(0, '训练集')
        train_set.setText(1, '0')
        train_set.setIcon(0, QIcon("../resources/训练集.ico"))
        train_set.setCheckState(0, Qt.Checked)
        valid_set = QTreeWidgetItem(root)
        valid_set.setText(0, '验证集')
        valid_set.setText(1, '0')
        valid_set.setIcon(0, QIcon("../resources/验证集.ico"))
        valid_set.setCheckState(0, Qt.Checked)
        spacerItem = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.train_layout.addWidget(tree)
        self.train_layout.addItem(spacerItem)
        self.train_scroll_area.setWidget(self.train_widget)
        msg = '创建项目={},成功!'.format(project_name)
        self.write_log(msg)
        dialog.close()


if __name__ == '__main__':
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    myapp = QApplication(sys.argv)
    ui = App()
    ui.show_ui()
    sys.exit(myapp.exec_())