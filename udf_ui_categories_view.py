# -*- Coding: utf-8 -*-
# Created by Diablo76 on 04/01/2024 -- 00:44:10.

from PyQt6.QtCore import QRect, pyqtSignal
from PyQt6.QtWidgets import QCheckBox, QGridLayout, QPushButton, QWidget


class UbuntuDesktopFileCategoriesView(QWidget):
    """Manage the Ubuntu Desktop File Categories View.

    This class represents the dialog window for selecting categories.
    It provides checkboxes for predefined categories and emits a signal with the selected categories.

    Attributes:
        categories_selected: A signal emitted when categories are selected."""

    categories_selected = pyqtSignal(list)

    # Predefined categories
    CATEGORIES = [
        "AudioVideo",
        "Audio",
        "Building",
        "DesktopSettings",
        "Development",
        "Education",
        "Game",
        "Graphics",
        "Network",
        "Office",
        "Qt",
        "Settings",
        "System",
        "TextEditor",
        "Utility",
    ]

    def __init__(self) -> None:
        super().__init__()

        # Set window title and size
        self.setWindowTitle("Select your categories")
        self.setFixedSize(602, 207)

        # Create a grid layout to hold the checkboxes
        self.gridLayoutWidget = QWidget(self)
        self.gridLayoutWidget.setGeometry(QRect(8, 8, 585, 165))
        self.gridLayout = QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)

        # Add checkboxes for each category to the grid layout
        for index, category in enumerate(self.CATEGORIES):
            row, col = divmod(index, 5)
            checkbox = QCheckBox(self.gridLayoutWidget)
            checkbox.setText(category)
            self.gridLayout.addWidget(checkbox, row, col, 1, 1)

        # Create an "Ok" button and connect its clicked signal to the get_type_categories method
        self.pushButton = QPushButton(self)
        self.pushButton.setText("Ok")
        button_x = int((self.width() / 2) - 34)
        button_y = 168
        button_width = 68
        button_height = 32
        self.pushButton.setGeometry(
            QRect(button_x, button_y, button_width, button_height)
        )
        self.pushButton.clicked.connect(self.emit_categories_and_close)

    def _get_type_categories(self) -> list[str]:
        # Retrieve the selected categories from the checkboxes
        return [
            check_box.text()
            for check_box in self.gridLayoutWidget.findChildren(QCheckBox)
            if check_box.isChecked()
        ]

    def emit_categories_and_close(self) -> None:
        list_categories = self._get_type_categories()
        # Emit the selected categories as a signal
        self.categories_selected.emit(list_categories)
        super().close()
