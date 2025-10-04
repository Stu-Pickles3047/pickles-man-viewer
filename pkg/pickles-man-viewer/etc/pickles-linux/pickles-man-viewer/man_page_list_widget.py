import subprocess
from PyQt6.QtWidgets import QTreeWidget, QTreeWidgetItem, QWidget, QVBoxLayout, QLineEdit, QLabel
from PyQt6.QtCore import pyqtSignal

class ManPageListWidget(QWidget):
    man_page_selected = pyqtSignal(str)

    SECTION_NAMES = {
        '1': 'User Commands',
        '8': 'System Administration',
        '3': 'Library Functions',
        '2': 'System Calls',
        '4': 'Device Files',
        '5': 'File Formats',
        '6': 'Games',
        '7': 'Miscellaneous',
        '9': 'Kernel Routines',
        'n': 'New',
        'l': 'Local',
        'p': 'Public',
        'o': 'Old',
        't': 'TeX',
    }

    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)

        # Search box
        search_label = QLabel("Search:")
        self.layout.addWidget(search_label)
        self.search_edit = QLineEdit()
        self.search_edit.setPlaceholderText("Type to filter man pages...")
        self.search_edit.textChanged.connect(self._filter_list)
        self.layout.addWidget(self.search_edit)

        self.tree_widget = QTreeWidget()
        self.tree_widget.setHeaderHidden(True)
        self.layout.addWidget(self.tree_widget)
        self.tree_widget.itemClicked.connect(self._on_item_clicked)

        self.all_man_pages = {}  # section to list of names
        self.load_man_pages()

    def load_man_pages(self):
        try:
            result = subprocess.run(['apropos', '.'], capture_output=True, text=True, check=True)
            lines = result.stdout.splitlines()
            self.all_man_pages = {}
            for line in lines:
                if '(' in line and ')' in line:
                    parts = line.split('(')
                    name_section = parts[0].strip()
                    section_part = parts[1].split(')')[0].strip()
                    name = name_section.split(',')[0].strip()
                    if name:
                        if section_part not in self.all_man_pages:
                            self.all_man_pages[section_part] = []
                        if name not in self.all_man_pages[section_part]:
                            self.all_man_pages[section_part].append(name)
            # Sort names in each section
            for section in self.all_man_pages:
                self.all_man_pages[section].sort()
            self._update_list()
        except subprocess.CalledProcessError as e:
            self.all_man_pages = {}
            error_item = QTreeWidgetItem([f"Error loading man pages: {e.stderr}"])
            self.tree_widget.addTopLevelItem(error_item)
        except FileNotFoundError:
            self.all_man_pages = {}
            error_item = QTreeWidgetItem(["Error: 'apropos' command not found."])
            self.tree_widget.addTopLevelItem(error_item)

    def _update_list(self):
        self.tree_widget.clear()
        for section in sorted(self.all_man_pages.keys()):
            section_name = self.SECTION_NAMES.get(section, f"Section {section}")
            section_item = QTreeWidgetItem([section_name])
            self.tree_widget.addTopLevelItem(section_item)
            for name in self.all_man_pages[section]:
                name_item = QTreeWidgetItem([name])
                section_item.addChild(name_item)
        # Start collapsed

    def _filter_list(self, text):
        self.tree_widget.clear()
        if not text:
            self._update_list()
        else:
            filtered = {}
            for section, names in self.all_man_pages.items():
                filtered_names = [n for n in names if text.lower() in n.lower()]
                if filtered_names:
                    filtered[section] = filtered_names
            for section in sorted(filtered.keys()):
                section_name = self.SECTION_NAMES.get(section, f"Section {section}")
                section_item = QTreeWidgetItem([section_name])
                self.tree_widget.addTopLevelItem(section_item)
                for name in filtered[section]:
                    name_item = QTreeWidgetItem([name])
                    section_item.addChild(name_item)
            # Start collapsed

    def _on_item_clicked(self, item, column):
        if item.parent():  # it's a name item, not section
            self.man_page_selected.emit(item.text(0))
