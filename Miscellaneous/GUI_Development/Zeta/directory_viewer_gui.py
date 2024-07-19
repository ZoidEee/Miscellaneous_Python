# directory_viewer_gui.py
import sys
import os
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QIcon, QPixmap, QAction, QFileSystemModel
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QGridLayout,
    QMenuBar, QTreeView, QFileDialog,
    QComboBox, QLabel, QHBoxLayout, QVBoxLayout, QPushButton, QHeaderView, QGroupBox, QFormLayout, QSplitter
)
from directory_viewer_logic import DirectoryViewerLogic


class DirectoryViewerGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.logic = DirectoryViewerLogic()
        self.init_ui()
        self.setup_main_window()

    def init_ui(self):
        self.setWindowTitle('Video File Metadata Viewer')
        self.setMinimumSize(1250, 750)

    def setup_main_window(self):
        self.setup_menu_bar()

        self.dir_combo = QComboBox()
        self.dir_combo.setEditable(True)
        self.dir_combo.setInsertPolicy(QComboBox.InsertPolicy.InsertAtTop)
        self.dir_combo.activated.connect(self.on_combo_activated)

        dir_label = QLabel("Select Directory:")

        dir_button = QPushButton()
        dir_button.setIcon(QIcon(QPixmap("images/opened-folder-100.png")))
        dir_button.setIconSize(QSize(20, 20))
        dir_button.setFixedSize(30, 30)
        dir_button.clicked.connect(self.open_directory)

        combo_layout = QHBoxLayout()
        combo_layout.addWidget(dir_label)
        combo_layout.addWidget(self.dir_combo,Qt.AlignmentFlag.AlignCenter)
        combo_layout.addWidget(dir_button)

        splitter = QSplitter(Qt.Orientation.Horizontal)


        self.treeview = QTreeView()
        self.treeview.setMinimumWidth(300)
        self.model = QFileSystemModel()
        self.treeview.setModel(self.model)

        # Hide columns 1 and 3
        for i in range(self.model.columnCount()):
            if i not in [0]:
                self.treeview.hideColumn(i)

        self.treeview.selectionModel().selectionChanged.connect(self.on_selection_changed)
        splitter.addWidget(self.treeview)

        # File Metadata
        self.f_groupbox = QGroupBox("File Metadata")
        self.fQbox_layout = QVBoxLayout()

        file_fields = ['Name', 'Size', 'Duration', 'Overall Bitrate']
        self.file_labels = {}

        for field in file_fields:
            hbox = QHBoxLayout()
            label = QLabel(f"{field}:")
            value = QLabel()
            hbox.addWidget(label)
            hbox.addWidget(value)
            self.fQbox_layout.addLayout(hbox)
            self.file_labels[field] = value

        self.f_groupbox.setLayout(self.fQbox_layout)

        # Video Metadata
        self.v_groupbox = QGroupBox("Video Metadata")
        self.vQbox_layout = QVBoxLayout()

        video_fields = ['Format', 'Profile', 'Resolution', 'Aspect Ratio', 'FPS', 'Bit Depth', 'Pixel Format',
                        'Bitrate']
        self.video_labels = {}

        for field in video_fields:
            hbox = QHBoxLayout()
            label = QLabel(f"{field}:")
            value = QLabel()
            hbox.addWidget(label)
            hbox.addWidget(value)
            self.vQbox_layout.addLayout(hbox)
            self.video_labels[field] = value

        self.v_groupbox.setLayout(self.vQbox_layout)

        # Audio Metadata
        self.a_groupbox = QGroupBox("Audio Metadata")
        self.aQbox_layout = QVBoxLayout()

        audio_fields = ['Format', 'Profile', 'Audio Channels', 'Sample Rate', 'Bit Depth', 'Bitrate']
        self.audio_labels = {}

        for field in audio_fields:
            hbox = QHBoxLayout()
            label = QLabel(f"{field}:")
            value = QLabel()
            hbox.addWidget(label)
            hbox.addWidget(value)
            self.aQbox_layout.addLayout(hbox)
            self.audio_labels[field] = value

        self.a_groupbox.setLayout(self.aQbox_layout)
        self.setup_directory_metadata()

        # Create a widget for metadata and add it to the splitter
        metadata_widget = QWidget()
        metadata_layout = QVBoxLayout(metadata_widget)
        metadata_layout.addWidget(self.f_groupbox)
        metadata_layout.addWidget(self.v_groupbox)
        metadata_layout.addWidget(self.a_groupbox)
        metadata_layout.addWidget(self.dir_groupbox)
        metadata_layout.addStretch()
        metadata_widget.setMinimumWidth(350)  # Set a minimum width for metadata
        splitter.addWidget(metadata_widget)

        # Set initial sizes for splitter
        splitter.setSizes([550, 450])  # Adjust these values as needed

        main_layout = QVBoxLayout()
        main_layout.addLayout(combo_layout)
        main_layout.addWidget(splitter)

        wid = QWidget()
        wid.setLayout(main_layout)
        self.setCentralWidget(wid)

    def setup_directory_metadata(self):
        self.dir_groupbox = QGroupBox("Directory Metadata")
        self.dir_layout = QVBoxLayout()
        dir_fields = ['Name', 'Size', 'Created', 'Modified', 'Subdirectories', 'Files']
        self.dir_labels = {}
        for field in dir_fields:
            hbox = QHBoxLayout()
            label = QLabel(f"{field}:")
            value = QLabel()
            hbox.addWidget(label)
            hbox.addWidget(value)
            self.dir_layout.addLayout(hbox)
            self.dir_labels[field] = value
        self.dir_groupbox.setLayout(self.dir_layout)
        self.dir_groupbox.hide()  # Initially hidden

    def setup_menu_bar(self):
        menubar = QMenuBar(self)
        self.setMenuBar(menubar)

        file_menu = menubar.addMenu("File")
        file_menu.addAction(self.create_action("Minimize", self.showMinimized))
        file_menu.addAction(self.create_action("Exit", self.close))

        menubar.addMenu("Edit")

    def create_action(self, text, slot):
        action = QAction(text, self)
        action.triggered.connect(slot)
        return action

    def open_directory(self):
        dir_path = QFileDialog.getExistingDirectory(self, "Select Directory")
        if dir_path:
            self.update_tree_view(dir_path)

    def update_tree_view(self, dir_path):
        self.model.setRootPath(dir_path)
        self.treeview.setRootIndex(self.model.index(dir_path))

        header = self.treeview.header()
        for i in range(header.count()):
            if header.sectionSize(i) < 250:
                header.resizeSection(i, 250)

        self.logic.update_recent_dirs(dir_path)
        self.update_combo_box()

    def update_combo_box(self):
        self.dir_combo.clear()
        self.dir_combo.addItems(self.logic.recent_dirs)
        self.dir_combo.setCurrentIndex(0)

    def on_combo_activated(self, index):
        selected_dir = self.dir_combo.itemText(index)
        self.update_tree_view(selected_dir)

    def on_selection_changed(self, selected, deselected):
        indexes = selected.indexes()
        if indexes:
            file_path = self.model.filePath(indexes[0])
            if os.path.isfile(file_path):
                self.update_file_metadata(file_path)
                self.show_file_metadata()
            else:
                self.update_directory_metadata(file_path)
                self.show_directory_metadata()

    def show_file_metadata(self):
        self.f_groupbox.show()
        self.v_groupbox.show()
        self.a_groupbox.show()
        self.dir_groupbox.hide()

    def show_directory_metadata(self):
        self.f_groupbox.hide()
        self.v_groupbox.hide()
        self.a_groupbox.hide()
        self.dir_groupbox.show()

    def update_directory_metadata(self, dir_path):
        dir_info = self.logic.get_directory_info(dir_path)
        if dir_info:
            self.dir_labels['Name'].setText(dir_info['name'])
            self.dir_labels['Size'].setText(dir_info['size'])
            self.dir_labels['Created'].setText(dir_info['created'])
            self.dir_labels['Modified'].setText(dir_info['modified'])
            self.dir_labels['Subdirectories'].setText(str(dir_info['subdirs']))
            self.dir_labels['Files'].setText(str(dir_info['files']))
        else:
            for label in self.dir_labels.values():
                label.setText("N/A")

    def update_file_metadata(self, file_path):
        _, ext = os.path.splitext(file_path)
        if ext.lower() in ['.mkv', '.avi', '.mp4', '.mov', '.flv']:
            metadata = self.logic.get_video_metadata(file_path)
            if metadata:
                # Update file metadata
                self.file_labels['Name'].setText(metadata['filename'])
                self.file_labels['Size'].setText(metadata['size'])
                self.file_labels['Duration'].setText(
                    self.logic.format_duration(metadata['duration']) if metadata.get('duration') else 'N/A')
                self.file_labels['Overall Bitrate'].setText(
                    self.logic.format_bitrate(metadata['overall_bitrate']) if metadata.get(
                        'overall_bitrate') else 'N/A')

                # Update video metadata
                if 'video_format' in metadata:
                    self.video_labels['Format'].setText(metadata['video_format'])
                    self.video_labels['Profile'].setText(metadata.get('video_profile', 'N/A'))
                    self.video_labels['Resolution'].setText(f"{metadata['width']}x{metadata['height']}")
                    self.video_labels['Aspect Ratio'].setText(
                        self.logic.format_aspect_ratio(metadata['aspect_ratio']) if metadata.get(
                            'aspect_ratio') else 'N/A')
                    self.video_labels['FPS'].setText(f"{metadata['fps']:.2f}" if metadata.get('fps') else 'N/A')
                    self.video_labels['Bit Depth'].setText(
                        str(metadata['bit_depth']) if metadata.get('bit_depth') else 'N/A')
                    self.video_labels['Pixel Format'].setText(metadata.get('pixel_format', 'N/A'))
                    self.video_labels['Bitrate'].setText(
                        self.logic.format_bitrate(metadata['video_bitrate']) if metadata.get(
                            'video_bitrate') else 'N/A')
                else:
                    self.clear_labels(self.video_labels)

                # Update audio metadata
                if 'audio_format' in metadata:
                    self.audio_labels['Format'].setText(metadata['audio_format'])
                    self.audio_labels['Profile'].setText(metadata.get('audio_profile', 'N/A'))
                    self.audio_labels['Audio Channels'].setText(str(metadata['channels']))
                    self.audio_labels['Sample Rate'].setText(f"{metadata['sample_rate']} Hz")
                    self.audio_labels['Bit Depth'].setText(
                        str(metadata['bit_depth']) if metadata.get('bit_depth') else 'N/A')
                    self.audio_labels['Bitrate'].setText(
                        self.logic.format_bitrate(metadata['audio_bitrate']) if metadata.get(
                            'audio_bitrate') else 'N/A')
                else:
                    self.clear_labels(self.audio_labels)
            else:
                self.clear_all_labels()
                self.file_labels['Name'].setText("Unable to extract metadata")
        else:
            self.clear_all_labels()
            self.file_labels['Name'].setText(os.path.basename(file_path))
            self.file_labels['Size'].setText(self.logic.format_size(os.path.getsize(file_path)))
            self.file_labels['Duration'].setText("N/A")
            self.file_labels['Overall Bitrate'].setText("N/A")
            self.clear_labels(self.video_labels)
            self.clear_labels(self.audio_labels)

    def clear_labels(self, label_dict):
        for label in label_dict.values():
            label.setText('N/A')

    def clear_all_labels(self):
        self.clear_labels(self.file_labels)
        self.clear_labels(self.video_labels)
        self.clear_labels(self.audio_labels)


def main():
    app = QApplication(sys.argv)
    window = DirectoryViewerGUI()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
