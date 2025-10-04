from PyQt6.QtWidgets import QMenuBar, QMenu
from PyQt6.QtGui import QAction

def create_main_menu_bar(parent_window):
    menu_bar = QMenuBar(parent_window)

    # File Menu
    file_menu = QMenu("&File", parent_window)
    menu_bar.addMenu(file_menu)

    print_action = QAction("&Print", parent_window)
    print_action.triggered.connect(parent_window.print_current_page)
    file_menu.addAction(print_action)

    close_action = QAction("&Close", parent_window)
    close_action.triggered.connect(parent_window.close)
    file_menu.addAction(close_action)

    # Edit Menu
    edit_menu = QMenu("&Edit", parent_window)
    menu_bar.addMenu(edit_menu)

    select_all_action = QAction("Select &All", parent_window)
    select_all_action.triggered.connect(parent_window.select_all_text)
    edit_menu.addAction(select_all_action)

    copy_action = QAction("&Copy", parent_window)
    copy_action.triggered.connect(parent_window.copy_text)
    edit_menu.addAction(copy_action)

    # View Menu
    view_menu = QMenu("&View", parent_window)
    menu_bar.addMenu(view_menu)

    light_action = QAction("&Light", parent_window)
    light_action.triggered.connect(parent_window.set_light_theme)
    view_menu.addAction(light_action)

    dark_action = QAction("&Dark", parent_window)
    dark_action.triggered.connect(parent_window.set_dark_theme)
    view_menu.addAction(dark_action)

    view_menu.addSeparator()

    zoom_in_action = QAction("Zoom &In", parent_window)
    zoom_in_action.setShortcut("Ctrl++")
    zoom_in_action.triggered.connect(parent_window.zoom_in)
    view_menu.addAction(zoom_in_action)

    zoom_out_action = QAction("Zoom &Out", parent_window)
    zoom_out_action.setShortcut("Ctrl+-")
    zoom_out_action.triggered.connect(parent_window.zoom_out)
    view_menu.addAction(zoom_out_action)

    zoom_reset_action = QAction("Zoom &Reset", parent_window)
    zoom_reset_action.setShortcut("Ctrl+0")
    zoom_reset_action.triggered.connect(parent_window.zoom_reset)
    view_menu.addAction(zoom_reset_action)

    # Help Menu
    help_menu = QMenu("&Help", parent_window)
    menu_bar.addMenu(help_menu)

    about_action = QAction("&About", parent_window)
    about_action.triggered.connect(parent_window.show_about)
    help_menu.addAction(about_action)

    return menu_bar
