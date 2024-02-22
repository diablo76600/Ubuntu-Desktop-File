# -*- Coding: utf-8 -*-
# Created by Diablo76 on 06/01/2024 -- 12:23:10.


import os

from udf_ui_view import UbuntuDesktopFileView as UdfView
from udf_ui_categories_view import UbuntuDesktopFileCategoriesView as UdfCategoriesView
from udf_model import UbuntuDesktopFileModel as UdfModel

from PyQt6.QtWidgets import QMessageBox, QCheckBox, QLineEdit, QFileDialog, QApplication
from PyQt6.QtGui import QPixmap, QFontMetrics
from PyQt6.QtCore import Qt

class UbuntuDesktopFileController:
    """Controller class for managing the Ubuntu Desktop File.

    This class provides methods for handling user interactions
    and managing the data flow between the view
    and model components of the Ubuntu Desktop File application.

    Args:
        udf_view: The view component for the Ubuntu Desktop File.
        udf_categories_view: The view component for the Ubuntu Desktop File Categories.
        udf_model: The model component for the Ubuntu Desktop File."""

    def __init__(self, app: QApplication,  udf_view: UdfView, udf_categories_view: UdfCategoriesView, udf_model: UdfModel) -> None:
        self.app = app
        self.udf_view = udf_view
        self.udf_categories_view = udf_categories_view
        self.udf_model = udf_model
        self.udf_categories_view.categories_selected.connect(self.update_categories)
        self.udf_view.lineEdit_exec.textChanged.connect(self.update_application_name)

    def connect_signals(self):
        """Connect signals to their respective slots."""
        signal_connections = {
            self.udf_view.pushButton_exec: self.select_executable_or_python_file,
            self.udf_view.pushButton_icon: self.set_icon,
            self.udf_view.pushButton_save: self.save_desktop_file,
            self.udf_view.pushButton_quit: self.app.exit,
            self.udf_view.pushButton_categories: self.udf_categories_view.exec,
            self.udf_view.checkBox_directory: self.update_checkbox_text,
            self.udf_view.checkBox_terminal: self.update_checkbox_text,
            self.udf_view.checkBox_startup: self.update_checkbox_text,
            self.udf_view.checkBox_python: self.update_python_label,
        }
        for signal, slot in signal_connections.items():
            signal.clicked.connect(slot)
        self.udf_view.lineEdit_exec.textChanged.connect(
            self.update_checkbox_label_directory
        )

    def get_entered_data(self) -> dict:
        """Get all the entered data from the widgets."""
        return {
            "Categories": self.udf_view.lineEdit_categories.text(),
            "Comment": self.udf_view.lineEdit_comment.text(),
            "Exec": self.udf_view.lineEdit_exec.property("original_text"),
            "GenericName": self.udf_view.lineEdit_generic_name.text(),
            "Icon": self.udf_view.lineEdit_icon.property("original_text"),
            "Name": self.udf_view.lineEdit_name.text(),
            "Path": (
                os.path.dirname(self.udf_view.lineEdit_exec.property("original_text"))
                if self.udf_view.checkBox_directory.isChecked()
                else ""
            ),
            "StartupNotify": str(self.udf_view.checkBox_startup.isChecked()).lower(),
            "Terminal": str(self.udf_view.checkBox_terminal.isChecked()).lower(),
            "Type": self.udf_view.lineEdit_type.text(),
            "Version": self.udf_view.lineEdit_version.text(),
        }

    def update_categories(self, list_categories: list) -> None:
        """Update the categories in the view based on the selected categories."""
        self.udf_view.lineEdit_categories.setText(";".join(list_categories))

    @staticmethod
    def display_message(title: str, text: str, type_message: str) -> None:
        """Display a message box with the specified title, text, and type."""
        if type_message == "warning":
            QMessageBox.warning(None, title, text)
        else:
            QMessageBox.information(None, title, text)

    @staticmethod
    def get_application_name(exec_path: str) -> str:
        """Extract the application name from the provided executable path."""
        return os.path.splitext(os.path.basename(exec_path))[0]

    def update_application_name(self) -> None:
        """Update the application name based on the entered executable path."""
        if self.udf_view.lineEdit_name.text():
            return
        application_name: str = self.get_application_name(
            self.udf_view.lineEdit_exec.text()
        )
        self.udf_view.lineEdit_name.setText(application_name)

    def check_widgets(self) -> bool:
        """Check if all required widgets have valid values."""
        if not self.udf_view.lineEdit_name.text():
            self.display_message(
                self.udf_view.title, "Please enter an Application Name.", "information"
            )
            return False
        if not self.udf_view.lineEdit_exec.text():
            message = (
                "Please select Python file."
                if self.udf_view.checkBox_python.isChecked()
                else "Please select Executable file."
            )
            self.display_message(self.udf_view.title, message, "information")
            return False
        return True

    def update_checkbox_text(self) -> None:
        """Update the text of the checkbox based on its state."""
        checkbox: QCheckBox = self.udf_view.sender()
        if checkbox == self.udf_view.checkBox_directory:
            checkbox.setText(
                os.path.dirname(self.udf_view.lineEdit_exec.text())
                if checkbox.isChecked()
                else ""
            )
        else:
            checkbox.setText(str(checkbox.isChecked()))

    def select_file_dialog(self, caption: str, filter: str) -> str | None:
        """Open a file dialog to select a file."""
        if file := QFileDialog.getOpenFileName(parent=self.udf_view, caption=caption, filter=filter)[0]:
            return file
        return None

    def select_executable_or_python_file(self) -> None:
        """Open a file dialog to select the executable or Python file."""
        self.udf_view.lineEdit_exec.clear()
        if is_python := self.udf_view.checkBox_python.isChecked():
            caption = "Select a Python file."
            file_ext = "*.py"
        else:
            caption = "Select an Executable file."
            file_ext = ""
        if file_path := self.select_file_dialog(caption=caption, filter=file_ext):
            if not is_python and not os.access(file_path, os.X_OK):
                self.display_message(
                    self.udf_view.title,
                    f"{file_path} <font color='red'>is not executable</font>.",
                    "information",
                )
            else:
                self.udf_view.lineEdit_exec.setProperty("original_text", file_path)
                file_path = self.truncate_text(self.udf_view.lineEdit_exec, file_path)
                self.udf_view.lineEdit_exec.setText(file_path)

    def update_checkbox_label_directory(self):
        if self.udf_view.checkBox_directory.isChecked():
            self.udf_view.checkBox_directory.setText(os.path.dirname(self.udf_view.lineEdit_exec.text()))

    def truncate_text(self, widget: QLineEdit, file_path: str) -> str:
        """Truncates text to fit within the width of QLineEdit, 
            adding ellipsis if text is longer."""
        font_metrics = QFontMetrics(widget.font())
        return font_metrics.elidedText(
            file_path, Qt.TextElideMode.ElideMiddle, widget.width()
        )

    def set_icon(self) -> None:
        """Open a file dialog to select the icon file and display it."""
        if icon_file := self.select_file_dialog(caption="Select Icon file.", filter=""):
            pixmap = QPixmap(icon_file)
            if pixmap.isNull():
                self.display_message(
                    self.udf_view.title,
                    f"{icon_file} <font color='red'>is not recognized</font>.",
                    "information",
                )
                self.udf_view.lineEdit_icon.clear()
            else:
                self.udf_view.lineEdit_icon.setProperty("original_text", icon_file)
                icon_file = self.truncate_text(self.udf_view.lineEdit_icon, icon_file)
                self.udf_view.lineEdit_icon.setText(icon_file)
                self.udf_view.label_icon_application.setPixmap(pixmap)

    def exec_categories(self) -> None:
        """Execute the categories view."""
        self.udf_categories_view.exec()

    def save_desktop_file(self) -> None:
        """Save the desktop file with the entered data."""
        if not self.check_widgets():
            return
        dict_data = self.get_entered_data()
        self.modify_exec_value(dict_data)
        if destination := self.choose_destination():
            desktop_file_data = self.udf_model.generate_desktop_file_data(dict_data)
            state, message = self.udf_model.write_desktop_file(destination, desktop_file_data)
            message_type = "information" if state else "warning"
            self.display_message(self.udf_view.title, message, message_type)

    def modify_exec_value(self, data: dict) -> None:
        """Modify the 'Exec' value in the data dictionary if the checkbox is checked."""
        if self.udf_view.checkBox_python.isChecked():
            data["Exec"] = f"python3 {data['Exec']}"

    def choose_destination(self) -> str:
        """Prompt the user to choose a destination to save the file."""
        file_name = f"{self.udf_view.lineEdit_name.text()}.desktop"
        destination, _ = QFileDialog.getSaveFileName(
            self.udf_view,
            "Save Desktop file",
            file_name,
            filter="*.desktop"
        )
        return destination

    def update_python_label(self) -> None:
        """Update the label and style based on the Python checkbox state."""
        self.udf_view.lineEdit_exec.clear()
        if self.udf_view.checkBox_python.isChecked():
            self.udf_view.label_exec.setText("Python File :")
            self.udf_view.label_exec.setStyleSheet("color : red;")
        else:
            self.udf_view.label_exec.setText("Exec :")
            self.udf_view.label_exec.setStyleSheet("color : None;")
