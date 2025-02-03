import os
import glob
import json
import xml.etree.cElementTree as ET
from ui.enter_name import Ui_Dialog as EnterName
from ui.import_data import Ui_ImportData as ImportData
from PyQt5.QtWidgets import QTreeWidget, QMenu, QAction, QDialog, QFileDialog
from PyQt5.QtCore import Qt, QThread, pyqtSignal


class LoadJsonTask(QThread):
    progressUpdated = pyqtSignal(int)
    finishedSignal = pyqtSignal(str)

    def __init__(self, image_path, label_path):
        super().__init__()
        self.image_path = image_path
        self.label_path = label_path
        self.progress_value = 0

    def get_label_image_from_json(self, images, jsons):
        labeled = []
        total = len(jsons)
        for index, item in enumerate(jsons):
            base_json = os.path.basename(item)
            json_name = base_json.split('.')[0]
            for i in images:
                base_image = os.path.basename(i)
                image_name = base_image.split('.')[0]
                if json_name == image_name:
                    labeled.append(i)
            self.progress_value = int(50 * (index + 1) / total)
            self.progressUpdated.emit(self.progress_value)
        set1 = set(labeled)
        set2 = set(images)
        unlabeled = list(set2 - set1)
        return labeled, unlabeled

    def get_num_classes_from_json(self, jsons):
        labels = []
        total = len(jsons)
        for index, item in enumerate(jsons):
            with open(item, 'r', encoding='utf-8') as fd:
                content = json.load(fd)
                shapes = content.get('shapes')
                if shapes is None:
                    continue
                else:
                    for shape in shapes:
                        label = shape.get('label')
                        labels.append(label)
            progress = int(50 * (index + 1) / total)
            self.progress_value += progress
            self.progressUpdated.emit(self.progress_value)
        return list(set(labels))

    def run(self) -> None:
        jsons = glob.glob(os.path.join(self.label_path, "*.json"))
        total_labels = len(jsons)
        images = []
        for ext in ["*.bmp", "*.png", "*.jpg", "*.jpeg"]:
            images.extend(glob.glob(os.path.join(self.image_path, ext)))
        labeled, unlabeled = self.get_label_image_from_json(images, jsons)
        labeled_images = len(labeled)
        unlabeled_images = len(unlabeled)
        num_cls = self.get_num_classes_from_json(jsons)
        num_classes = len(num_cls)
        info = "找到{}个标签文件,对应{}张已标注的图像,总共{}类别,{}张图像未标注!"\
            .format(total_labels, labeled_images, num_classes, unlabeled_images)
        self.finishedSignal.emit(info)


class LoadTxtTask(QThread):
    progressUpdated = pyqtSignal(int)
    finishedSignal = pyqtSignal(str)

    def __init__(self, image_path, label_path):
        super().__init__()
        self.image_path = image_path
        self.label_path = label_path
        self.progress_value = 0

    def get_label_image_from_txt(self, images, txts):
        labeled = []
        total = len(txts)
        for index, item in enumerate(txts):
            base_txt = os.path.basename(item)
            txt_name = base_txt.split('.')[0]
            for i in images:
                base_image = os.path.basename(i)
                image_name = base_image.split('.')[0]
                if txt_name == image_name:
                    labeled.append(i)
            self.progress_value = int(50 * (index + 1) / total)
            self.progressUpdated.emit(self.progress_value)
        set1 = set(labeled)
        set2 = set(images)
        unlabeled = list(set2 - set1)
        return labeled, unlabeled

    def get_num_classes_from_txt(self, txts):
        labels = []
        total = len(txts)
        for index, item in enumerate(txts):
            with open(item) as fd:
                lines = fd.readlines()
                for line in lines:
                    data = line.split(' ')
                    labels.append(data[0])
            progress = int(50 * (index + 1) / total)
            self.progress_value += progress
            self.progressUpdated.emit(self.progress_value)
        return list(set(labels))

    def run(self):
        txts = glob.glob(os.path.join(self.label_path, "*.txt"))
        total_labels = len(txts)
        images = []
        for ext in ["*.bmp", "*.png", "*.jpg", "*.jpeg"]:
            images.extend(glob.glob(os.path.join(self.image_path, ext)))
        labeled, unlabeled = self.get_label_image_from_txt(images, txts)  # 假设你有这个方法
        labeled_images = len(labeled)
        unlabeled_images = len(unlabeled)
        num_cls = self.get_num_classes_from_txt(txts)
        num_classes = len(num_cls)
        info = "找到{}个标签文件,对应{}张已标注的图像,总共{}类别,{}张图像未标注!"\
            .format(total_labels, labeled_images, num_classes, unlabeled_images)
        self.finishedSignal.emit(info)


class LoadXmlTask(QThread):
    progressUpdated = pyqtSignal(int)
    finishedSignal = pyqtSignal(str)

    def __init__(self, image_path, label_path):
        super().__init__()
        self.image_path = image_path
        self.label_path = label_path
        self.progress_value = 0

    def get_label_image_from_xml(self, images, xmls):
        labeled = []
        total = len(xmls)
        for index, item in enumerate(xmls):
            base_txt = os.path.basename(item)
            txt_name = base_txt.split('.')[0]
            for i in images:
                base_image = os.path.basename(i)
                image_name = base_image.split('.')[0]
                if txt_name == image_name:
                    labeled.append(i)
            self.progress_value = int(50 * (index + 1) / total)
            self.progressUpdated.emit(self.progress_value)
        set1 = set(labeled)
        set2 = set(images)
        unlabeled = list(set2 - set1)
        return labeled, unlabeled

    def get_num_classes_from_xml(self, xmls):
        labels = []
        total = len(xmls)
        for index, item in enumerate(xmls):
            tree = ET.ElementTree(file=item)
            root = tree.getroot()
            objects = root.findall('object')
            for obj in objects:
                label = obj.find('name').text
                labels.append(label)
            progress = int(50 * (index + 1) / total)
            self.progress_value += progress
            self.progressUpdated.emit(self.progress_value)
        return list(set(labels))

    def run(self):
        xmls = glob.glob(os.path.join(self.label_path, "*.xml"))
        total_labels = len(xmls)
        images = []
        for ext in ["*.bmp", "*.png", "*.jpg", "*.jpeg"]:
            images.extend(glob.glob(os.path.join(self.image_path, ext)))
        labeled, unlabeled = self.get_label_image_from_xml(images, xmls)  # 假设你有这个方法
        labeled_images = len(labeled)
        unlabeled_images = len(unlabeled)
        num_cls = self.get_num_classes_from_xml(xmls)
        num_classes = len(num_cls)
        info = "找到{}个标签文件,对应{}张已标注的图像,总共{}类别,{}张图像未标注!"\
            .format(total_labels, labeled_images, num_classes, unlabeled_images)
        self.finishedSignal.emit(info)


class MyTreeWidget(QTreeWidget):
    def __init__(self, name, parent=None):
        super(MyTreeWidget, self).__init__(parent)
        self.parent = parent
        self.name = name
        self.load_thread = None
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.show_context_menu)

    def show_context_menu(self, position):
        item_at = self.itemAt(position)
        if item_at.parent() is None:
            self.show_tree_menu(position)
        else:
            self.show_item_menu(position, item_at.text(0))

    def show_item_menu(self, position, item_name):
        menu = QMenu(self)
        action1 = QAction("导入", self)
        action2 = QAction("导出", self)
        menu.addAction(action1)
        menu.addAction(action2)
        action1.triggered.connect(lambda: self.dataset_import_triggered(item_name))
        action2.triggered.connect(lambda: self.dataset_export_triggered(item_name))
        menu.exec_(self.viewport().mapToGlobal(position))

    def show_tree_menu(self, position):
        menu = QMenu()
        action1 = QAction("删除", self)
        action2 = QAction("重命名", self)
        menu.addAction(action1)
        menu.addAction(action2)
        action1.triggered.connect(lambda: self.project_delete_triggered())
        action2.triggered.connect(lambda: self.project_rename_triggered())
        menu.exec_(self.viewport().mapToGlobal(position))

    def project_delete_triggered(self):
        layout = self.parent.train_layout
        for i in range(layout.count()):
            widget = layout.itemAt(i).widget()
            if isinstance(widget, MyTreeWidget):
                my_name = widget.name
                if my_name == self.name:
                    layout.removeWidget(widget)
                    widget.deleteLater()
                    msg = '删除项目={},成功!'.format(self.name)
                    self.parent.write_log(msg)
                    break

    def project_rename_triggered(self):
        layout = self.parent.train_layout
        for i in range(layout.count()):
            widget = layout.itemAt(i).widget()
            if isinstance(widget, MyTreeWidget):
                my_name = widget.name
                if my_name == self.name:
                    dialog = QDialog(self.parent)
                    enter_name = EnterName()
                    enter_name.setupUi(dialog)
                    enter_name.project_name_txt.setPlaceholderText('新项目名称')
                    enter_name.enter_name_lbl.setVisible(False)
                    dialog.setWindowFlags(
                        self.parent.windowFlags() & ~Qt.WindowContextHelpButtonHint & ~Qt.WindowMinMaxButtonsHint)
                    enter_name.done_enter_name_btn.clicked.connect(
                        lambda _, w=widget: self.rename_project_name(enter_name.project_name_txt.text(), w, dialog)
                    )
                    dialog.show()

    def rename_project_name(self, new_name, widget, dialog):
        top_item_count = widget.topLevelItemCount()
        for j in range(top_item_count):
            item = widget.topLevelItem(j)
            item.setText(0, new_name)
            msg = '项目={},重命名为={},成功!'.format(self.name, new_name)
            self.parent.write_log(msg)
            break
        dialog.close()

    def dataset_import_triggered(self, item_name):
        dialog = QDialog(self.parent)
        import_data = ImportData()
        import_data.setupUi(dialog)
        import_data.tips_lbl.setVisible(False)
        import_data.progress_bar.setValue(0)
        import_data.progress_bar.setVisible(False)
        import_data.image_path_txt.setEnabled(False)
        import_data.label_path_txt.setEnabled(False)
        import_data.done_import_btn.setEnabled(False)
        dialog.setWindowFlags(
            self.parent.windowFlags() & ~Qt.WindowContextHelpButtonHint & ~Qt.WindowMinMaxButtonsHint)
        import_data.choose_image_dir_btn.clicked.connect(lambda: self.choose_folder(import_data, '图像'))
        import_data.choose_label_dir_btn.clicked.connect(lambda: self.choose_folder(import_data, '标签'))
        import_data.done_import_btn.clicked.connect(lambda: self.do_import_data(dialog))
        dialog.show()
        msg = '项目={},数据集={},导入数据'.format(self.name, item_name)
        self.parent.write_log(msg)

    def choose_folder(self, dialog, operator_name):
        folder_path = QFileDialog.getExistingDirectory(self, "选择文件夹")
        if folder_path:
            if operator_name == '图像':
                dialog.image_path_txt.setEnabled(True)
                dialog.image_path_txt.setText(folder_path)
            else:
                dialog.label_path_txt.setEnabled(True)
                dialog.label_path_txt.setText(folder_path)
            if dialog.image_path_txt.isEnabled() and dialog.label_path_txt.isEnabled():
                self.get_label_info(dialog)
                dialog.done_import_btn.setEnabled(True)
        else:
            return None

    @staticmethod
    def load_dataset_finished(widget, info):
        widget.progress_bar.setVisible(False)
        widget.tips_lbl.setText(info)
        widget.tips_lbl.setVisible(True)

    def get_label_info(self, widget):
        image_path = widget.image_path_txt.text()
        label_path = widget.label_path_txt.text()
        labelme_fmt = widget.labelme_fmt.isChecked()
        yolo_fmt = widget.yolo_fmt.isChecked()
        labelimg_fmt = widget.labelImg_fmt.isChecked()
        images = []
        image_bmp = glob.glob(os.path.join(image_path, "*.bmp"))
        image_png = glob.glob(os.path.join(image_path, "*.png"))
        image_jpg = glob.glob(os.path.join(image_path, "*.jpg"))
        image_jpeg = glob.glob(os.path.join(image_path, "*.jpeg"))
        images.extend(image_bmp)
        images.extend(image_png)
        images.extend(image_jpg)
        images.extend(image_jpeg)
        if labelme_fmt:
            widget.progress_bar.setVisible(True)
            self.load_thread = LoadJsonTask(image_path, label_path)
            self.load_thread.progressUpdated.connect(widget.progress_bar.setValue)
            self.load_thread.finishedSignal.connect(lambda info0: self.load_dataset_finished(widget, info0))
            self.load_thread.start()
        elif yolo_fmt:
            widget.progress_bar.setVisible(True)
            self.load_thread = LoadTxtTask(image_path, label_path)
            self.load_thread.progressUpdated.connect(widget.progress_bar.setValue)
            self.load_thread.finishedSignal.connect(lambda info0: self.load_dataset_finished(widget, info0))
            self.load_thread.start()
        else:
            widget.progress_bar.setVisible(True)
            self.load_thread = LoadXmlTask(image_path, label_path)
            self.load_thread.progressUpdated.connect(widget.progress_bar.setValue)
            self.load_thread.finishedSignal.connect(lambda info0: self.load_dataset_finished(widget, info0))
            self.load_thread.start()

    def do_import_data(self, dialog):
        msg = '开始导入'
        self.parent.write_log(msg)

    def dataset_export_triggered(self, item_name):
        print("导出数据集 --->{},{}".format(self.name, item_name))
