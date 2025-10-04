import subprocess
import random
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QSpacerItem, QSizePolicy, QTextBrowser
from PyQt6.QtCore import Qt, pyqtSignal
import html

class WelcomeWidget(QWidget):
    show_man_list_requested = pyqtSignal()
    show_search_requested = pyqtSignal()
    show_random_man_page_requested = pyqtSignal(str) # Signal to request viewing a random man page

    def __init__(self, parent=None):
        super().__init__(parent)

        # Main vertical layout for the entire widget
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20) # Add some padding
        main_layout.setSpacing(20) # Spacing between elements

        # --- Title ---
        title_label = QLabel("Welcome to Pickles Man Viewer!")
        font = title_label.font()
        font.setPointSize(24)
        font.setBold(True)
        title_label.setFont(font)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(title_label)

        # --- Content Area (Horizontal Layout for Left Panel and Right Panel) ---
        content_layout = QHBoxLayout()
        content_layout.setSpacing(20)

        # Left Panel for Buttons (Vertical Layout)
        left_panel_layout = QVBoxLayout()
        left_panel_layout.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft) # Align buttons to top-left
        left_panel_layout.setSpacing(10) # Spacing between buttons

        search_button = QPushButton("Search Man Pages")
        search_button.setFixedSize(200, 50)
        search_button.clicked.connect(self.show_search_requested.emit)
        left_panel_layout.addWidget(search_button)

        man_list_button = QPushButton("View All Man Pages")
        man_list_button.setFixedSize(200, 50) # Fixed size for consistency
        man_list_button.clicked.connect(self.show_man_list_requested.emit)
        left_panel_layout.addWidget(man_list_button)

        # Add a spacer to push buttons to the top-left if the layout has extra vertical space
        left_panel_layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))

        content_layout.addLayout(left_panel_layout)

        # --- Right Panel for Random Man Page ---
        right_panel_layout = QVBoxLayout()
        right_panel_layout.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        right_panel_layout.setSpacing(10)

        random_title_label = QLabel("Random Man Page:")
        font = random_title_label.font()
        font.setPointSize(14)
        font.setBold(True)
        random_title_label.setFont(font)
        right_panel_layout.addWidget(random_title_label)

        self.random_man_page_name_button = QPushButton("Loading...")
        self.random_man_page_name_button.setFlat(True)
        self.random_man_page_name_button.setStyleSheet("border: none; text-align: left; font-size: 16px; font-weight: bold; color: blue; text-decoration: underline;")
        self.random_man_page_name_button.clicked.connect(lambda: self.show_random_man_page_requested.emit(self.current_random_man_page))
        right_panel_layout.addWidget(self.random_man_page_name_button)

        self.random_man_page_browser = QTextBrowser()
        right_panel_layout.addWidget(self.random_man_page_browser, 1)  # Allow it to expand

        content_layout.addLayout(right_panel_layout)

        main_layout.addLayout(content_layout)

        # Add a final spacer to push content to the top if the window is very tall
        main_layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))

        self.setLayout(main_layout)

        self._all_man_page_names = []
        self._load_all_man_page_names()
        self._select_random_man_page_and_view() # Select and view on startup

    def _load_all_man_page_names(self):
        try:
            result = subprocess.run(['apropos', '.'], capture_output=True, text=True, check=True)
            lines = result.stdout.splitlines()
            unique_names = set()
            for line in lines:
                if '(' in line and ')' in line:
                    name_section = line.split('(')[0].strip()
                    name = name_section.split(',')[0].strip()
                    if name:
                        unique_names.add(name)
            self._all_man_page_names = sorted(list(unique_names))
        except subprocess.CalledProcessError as e:
            print(f"Error loading all man page names for random selection: {e.stderr}")
            self.random_man_page_name_button.setText("Error loading pages.")
            # self.view_random_button.setEnabled(False) # Removed button
        except FileNotFoundError:
            print("Error: 'apropos' command not found for random selection.")
            self.random_man_page_name_button.setText("Error: apropos not found.")
            # self.view_random_button.setEnabled(False) # Removed button

    def _select_random_man_page_and_view(self):
        if self._all_man_page_names:
            self.current_random_man_page = random.choice(self._all_man_page_names)
            self.random_man_page_name_button.setText(self.current_random_man_page)
            # Load and display the man page description or full content
            desc = self._get_man_page_description(self.current_random_man_page)
            if desc:
                self.random_man_page_browser.setHtml(f"<p>{desc}</p>")
            else:
                html_content = self._get_man_page_html(self.current_random_man_page)
                self.random_man_page_browser.setHtml(html_content)
            # No longer emit signal to auto-open viewer
        else:
            self.random_man_page_name_button.setText("No man pages found.")
            self.random_man_page_browser.setHtml("<p>No man pages available.</p>")
            # self.view_random_button.setEnabled(False) # Removed button

    def _get_man_page_description(self, page_name):
        """Retrieve the description of a man page using apropos."""
        try:
            result = subprocess.run(['apropos', page_name], capture_output=True, text=True, check=True)
            lines = result.stdout.strip().split('\n')
            for line in lines:
                if ' - ' in line:
                    desc = line.split(' - ', 1)[1]
                    return html.escape(desc)
            return None
        except subprocess.CalledProcessError:
            return None

    def _get_man_page_html(self, page_name):
        """Retrieve a man page as HTML or plain text wrapped in <pre> tags."""
        try:
            result = subprocess.run(
                ["man", "-Thtml", page_name],
                capture_output=True,
                text=True,
                check=True,
            )
            if result.stdout:
                return result.stdout
        except subprocess.CalledProcessError as e:
            print(f"Error getting HTML man page for {page_name} with -Thtml: {e}")
            print(f"Stderr: {e.stderr}")
            try:
                result = subprocess.run(
                    ["man", page_name], capture_output=True, text=True, check=True
                )
                return f"<pre>{result.stdout}</pre>"
            except subprocess.CalledProcessError as e_plain:
                print(f"Error getting plain text man page for {page_name}: {e_plain}")
                print(f"Stderr: {e_plain.stderr}")
                return f"<h1>Error: Man page for '{page_name}' not found or could not be rendered.</h1>"

        return f"<h1>Error: Man page for '{page_name}' not found or could not be rendered.</h1>"

    def refresh_random(self):
        """Refresh the random man page selection."""
        self._select_random_man_page_and_view()

    # Removed _on_view_random_clicked as it's no longer needed
