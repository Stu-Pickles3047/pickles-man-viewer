import subprocess
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QListWidget,
    QListWidgetItem, QLabel, QPushButton, QCompleter
)
from PyQt6.QtCore import Qt, pyqtSignal, QStringListModel

class SearchWidget(QWidget):
    man_page_selected = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(20, 20, 20, 20)
        self.layout.setSpacing(10)

        # Title
        title_label = QLabel("Search Man Pages")
        font = title_label.font()
        font.setPointSize(18)
        font.setBold(True)
        title_label.setFont(font)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(title_label)

        # Search Input
        search_input_layout = QHBoxLayout()
        self.search_line_edit = QLineEdit()
        self.search_line_edit.setPlaceholderText("Type to search man pages...")
        self.search_line_edit.textChanged.connect(self._update_suggestions)
        search_input_layout.addWidget(self.search_line_edit)

        search_button = QPushButton("Search")
        search_button.clicked.connect(self._perform_search)
        search_input_layout.addWidget(search_button)

        self.layout.addLayout(search_input_layout)

        # Suggestions/Results List
        self.results_list_widget = QListWidget()
        self.results_list_widget.itemClicked.connect(self._on_item_clicked)
        self.layout.addWidget(self.results_list_widget)

        # QCompleter for real-time suggestions in the QLineEdit
        self.completer_model = QStringListModel()
        self.completer = QCompleter(self.completer_model, self)
        self.completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        self.search_line_edit.setCompleter(self.completer)

        # Store a list of (man_page_name, full_apropos_line) tuples
        self._all_man_pages_data = []
        self._load_all_man_pages_for_search()

    def _load_all_man_pages_for_search(self):
        try:
            result = subprocess.run(['apropos', '.'], capture_output=True, text=True, check=True)
            lines = result.stdout.splitlines()
            names_for_completer = []
            for line in lines:
                if '(' in line and ')' in line:
                    name_section = line.split('(')[0].strip()
                    name = name_section.split(',')[0].strip()
                    if name:
                        # Store unique names and their full apropos line
                        if name not in [item[0] for item in self._all_man_pages_data]:
                            self._all_man_pages_data.append((name, line))
                            names_for_completer.append(name)

            self._all_man_pages_data.sort(key=lambda x: x[0].lower()) # Sort by name
            names_for_completer.sort()
            self.completer_model.setStringList(names_for_completer)

        except subprocess.CalledProcessError as e:
            print(f"Error loading all man pages for search: {e.stderr}")
        except FileNotFoundError:
            print("Error: 'apropos' command not found for search.")

    def _update_suggestions(self, query):
        self.results_list_widget.clear()
        if not query:
            # Optionally display a default list or nothing when query is empty
            return

        query_lower = query.lower()

        exact_matches = []
        starts_with_matches = []
        contains_matches = [] # This will include partial and keyword matches

        # First pass: categorize all matches
        for name, full_apropos_line in self._all_man_pages_data:
            name_lower = name.lower()
            if name_lower == query_lower:
                exact_matches.append(name)
            elif name_lower.startswith(query_lower):
                starts_with_matches.append(name)
            elif query_lower in name_lower: # Check if query is anywhere in the name
                contains_matches.append(name)

        # Sort each category
        exact_matches.sort()
        starts_with_matches.sort()
        contains_matches.sort()

        # Add to list widget with delineation
        if exact_matches:
            self._add_section_header("Exact Matches")
            for name in exact_matches:
                self.results_list_widget.addItem(name)

        if starts_with_matches:
            # Filter out any exact matches that might have also been in starts_with
            starts_with_matches = [name for name in starts_with_matches if name not in exact_matches]
            if starts_with_matches: # Check again after filtering
                self._add_section_header("Starts With")
                for name in starts_with_matches:
                    self.results_list_widget.addItem(name)

        if contains_matches:
            # Filter out any matches already covered by exact or starts_with
            contains_matches = [name for name in contains_matches if name not in exact_matches and name not in starts_with_matches]
            if contains_matches: # Check again after filtering
                self._add_section_header("Contains (Partial/Keyword)")
                for name in contains_matches:
                    self.results_list_widget.addItem(name)

    def _perform_search(self):
        # For now, this just triggers the same filtering as typing
        self._update_suggestions(self.search_line_edit.text())

    def _on_item_clicked(self, item):
        # Ensure we don't emit a signal for section headers
        if item.flags() & Qt.ItemFlag.ItemIsSelectable:
            self.man_page_selected.emit(item.text())

    def _add_section_header(self, text):
        header_item = QListWidgetItem(text)
        header_item.setFlags(header_item.flags() & ~Qt.ItemFlag.ItemIsSelectable) # Make header non-selectable
        header_item.setForeground(Qt.GlobalColor.darkBlue) # Optional: style header
        font = header_item.font()
        font.setBold(True)
        header_item.setFont(font)
        self.results_list_widget.addItem(header_item)
