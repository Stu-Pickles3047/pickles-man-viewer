#!/usr/bin/env python
import sys
import os
# sys.path.insert(0, '/etc/pickles-linux/pickles-man-viewer')  # Commented out for development

from PyQt6.QtWidgets import QApplication, QMainWindow, QStackedWidget, QMessageBox, QDialog, QVBoxLayout, QLabel
from PyQt6.QtGui import QIcon
from PyQt6.QtPrintSupport import QPrinter, QPrintDialog

from menu_bar import create_main_menu_bar
from welcome_widget import WelcomeWidget
from man_page_list_widget import ManPageListWidget
from search_widget import SearchWidget
from man_page_viewer_widget import ManPageViewerWidget

import os

version_file = os.path.join(os.path.dirname(__file__), 'version.txt')
try:
    with open(version_file, 'r') as f:
        VERSION = f.read().strip()
except FileNotFoundError:
    VERSION = "2.0.0"  # fallback for development


class AboutDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("About Pickles Man Page Viewer")
        self.setModal(True)
        layout = QVBoxLayout(self)
        label = QLabel(
            "Pickles Man Page Viewer\n\n"
            f"Version {VERSION}\n\n"
            "Author: Stu-Pickles3047\n\n"
            'Website: <a href="https://github.com/Stu-Pickles3047">https://github.com/Stu-Pickles3047</a>\n\n'
            "A simple GUI application for viewing Linux man pages.\n\n"
            "Built with Python & PyQt6. for Pickles Linux"
        )
        label.setStyleSheet("font-size: 12px;")
        label.setOpenExternalLinks(True)
        layout.addWidget(label)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Pickles Man Page Viewer")
        self.setWindowIcon(QIcon('/etc/pickles-linux/pickles-man-viewer/pickle-logo.ico'))
        self.resize(900, 700)

        # --- Central stacked widget ---
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        # --- Pages ---
        self.welcome_widget = WelcomeWidget()
        self.man_list_widget = ManPageListWidget()
        self.search_widget = SearchWidget()
        self.man_viewer_widget = ManPageViewerWidget()

        # Add pages to stack
        self.stacked_widget.addWidget(self.welcome_widget)    # index 0
        self.stacked_widget.addWidget(self.man_list_widget)   # index 1
        self.stacked_widget.addWidget(self.search_widget)     # index 2
        self.stacked_widget.addWidget(self.man_viewer_widget) # index 3

        # Menu bar
        self.menu_bar = create_main_menu_bar(self)
        self.setMenuBar(self.menu_bar)

        # --- Signal wiring ---
        # From Welcome screen
        self.welcome_widget.show_man_list_requested.connect(
            lambda: self.stacked_widget.setCurrentWidget(self.man_list_widget)
        )
        self.welcome_widget.show_search_requested.connect(
            lambda: self.stacked_widget.setCurrentWidget(self.search_widget)
        )
        self.welcome_widget.show_random_man_page_requested.connect(
            self.open_man_page
        )

        # From list + search
        self.man_list_widget.man_page_selected.connect(self.open_man_page)
        self.search_widget.man_page_selected.connect(self.open_man_page)

        # From viewer back button
        self.man_viewer_widget.back_to_main.connect(self._switch_to_welcome)

        # Start at welcome screen
        self.stacked_widget.setCurrentWidget(self.welcome_widget)

        # Zoom level for reset
        self.zoom_level = 0

    def print_current_page(self):
        if self.stacked_widget.currentWidget() == self.man_viewer_widget:
            printer = QPrinter()
            dialog = QPrintDialog(printer, self)
            if dialog.exec():
                self.man_viewer_widget.viewer.print(printer)
        else:
            QMessageBox.information(self, "Print", "Please open a man page to print.")

    def select_all_text(self):
        current = self.stacked_widget.currentWidget()
        if hasattr(current, 'viewer') and hasattr(current.viewer, 'selectAll'):
            current.viewer.selectAll()
        elif hasattr(current, 'selectAll'):
            current.selectAll()

    def copy_text(self):
        current = self.stacked_widget.currentWidget()
        if hasattr(current, 'viewer') and hasattr(current.viewer, 'copy'):
            current.viewer.copy()
        elif hasattr(current, 'copy'):
            current.copy()

    def set_light_theme(self):
        self.setStyleSheet("")
        for widget in [self.welcome_widget, self.man_list_widget, self.search_widget, self.man_viewer_widget]:
            widget.setStyleSheet("")

    def set_dark_theme(self):
        dark_stylesheet = """
        QWidget { background-color: #2b2b2b; color: #ffffff; }
        QListWidget { background-color: #1e1e1e; color: #ffffff; }
        QLineEdit { background-color: #1e1e1e; color: #ffffff; }
        QTextBrowser { background-color: #1e1e1e; color: #ffffff; }
        QPushButton { background-color: #404040; color: #ffffff; }
        QLabel { color: #ffffff; }
        """
        self.setStyleSheet(dark_stylesheet)
        for widget in [self.welcome_widget, self.man_list_widget, self.search_widget, self.man_viewer_widget]:
            widget.setStyleSheet(dark_stylesheet)

    def zoom_in(self):
        if self.stacked_widget.currentWidget() == self.man_viewer_widget:
            self.man_viewer_widget.viewer.zoomIn(1)
            self.zoom_level += 1

    def zoom_out(self):
        if self.stacked_widget.currentWidget() == self.man_viewer_widget:
            self.man_viewer_widget.viewer.zoomOut(1)
            self.zoom_level -= 1

    def zoom_reset(self):
        if self.stacked_widget.currentWidget() == self.man_viewer_widget:
            if self.zoom_level > 0:
                for _ in range(self.zoom_level):
                    self.man_viewer_widget.viewer.zoomOut(1)
            elif self.zoom_level < 0:
                for _ in range(-self.zoom_level):
                    self.man_viewer_widget.viewer.zoomIn(1)
            self.zoom_level = 0

    def show_about(self):
        dialog = AboutDialog(self)
        dialog.exec()

    def _switch_to_welcome(self):
        """Switch to welcome widget and refresh random man page."""
        self.stacked_widget.setCurrentWidget(self.welcome_widget)
        self.welcome_widget.refresh_random()

    def open_man_page(self, page_name):
        """Load a man page into the viewer and switch to it."""
        self.man_viewer_widget.load_man_page(page_name)
        self.stacked_widget.setCurrentWidget(self.man_viewer_widget)


def main():
    print(f"Running Pickles Man Viewer - Version: {VERSION}")
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
