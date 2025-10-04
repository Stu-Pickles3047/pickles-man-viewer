import subprocess
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QTextBrowser,
    QPushButton,
    QHBoxLayout,
)
from PyQt6.QtCore import Qt, pyqtSignal


class ManPageViewerWidget(QWidget):
    # Signal that parent can connect to for "back to main"
    back_to_main = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)

        # --- Navigation row (Back button to main) ---
        nav_layout = QHBoxLayout()
        self.back_button = QPushButton("← Back to Main")
        self.back_button.clicked.connect(self._emit_back_to_main)
        nav_layout.addWidget(self.back_button)
        nav_layout.addStretch()
        self.layout.addLayout(nav_layout)

        # --- Viewer ---
        self.viewer = QTextBrowser()
        self.viewer.setReadOnly(True)
        self.layout.addWidget(self.viewer)

        # --- Error label ---
        self.error_label = QLabel("Select a man page to view.")
        self.error_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.error_label.setStyleSheet("QLabel { color: gray; font-size: 16px; }")
        self.layout.addWidget(self.error_label)
        self.error_label.hide()

    def _emit_back_to_main(self):
        """Emit signal to tell parent to go back to main view."""
        self.back_to_main.emit()

    def load_man_page(self, page_name):
        """Load and display the requested man page."""
        self.error_label.hide()
        self.viewer.show()

        html_content = self._get_man_page_html(page_name)
        if html_content.startswith("<h1>Error"):
            self.viewer.hide()
            self.error_label.setText(
                html_content.replace("<h1>", "").replace("</h1>", "")
            )
            self.error_label.show()
        else:
            self.viewer.setHtml(html_content)

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