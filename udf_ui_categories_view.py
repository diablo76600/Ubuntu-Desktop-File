# -*- Coding: utf-8 -*-
# Created by Diablo76 on 04/01/2024 -- 00:44:10.

from PyQt6.QtCore import QRect, pyqtSignal
from PyQt6.QtWidgets import QCheckBox, QGridLayout, QVBoxLayout, QDialogButtonBox, QWidget, QDialog


class UbuntuDesktopFileCategoriesView(QDialog):
    """Manage the Ubuntu Desktop File Categories View.

    This class represents the dialog window for selecting categories.
    It provides checkboxes for predefined categories and emits a signal with the selected categories.

    Attributes:
        categories_selected: A signal emitted when categories are selected."""

    # Defines a signal categories_selected 
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
        self.setFixedSize(512, 150)
        # Ceate central widget
        self.centralWidget = QWidget(self)
        self.centralWidget.setGeometry(QRect(0, 0, 502, 150))
        self.verticalLayout = QVBoxLayout(self.centralWidget)
        self.gridLayout_checkbox = QGridLayout()
        # Create checkboxes for each predefined category
        for index, category in enumerate(self.CATEGORIES):
            row, col = divmod(index, 5)
            checkbox = QCheckBox(self.centralWidget)
            checkbox.setText(category)
            self.gridLayout_checkbox.addWidget(checkbox, row, col, 1, 1)
        # Add the grid layout to the vertical layout
        self.verticalLayout.addLayout(self.gridLayout_checkbox)
        # Create and connect the "Ok" button
        self.buttonBox = QDialogButtonBox(self.centralWidget)
        self.buttonBox.setStandardButtons(QDialogButtonBox.StandardButton.Ok)
        self.buttonBox.setCenterButtons(True)
        self.buttonBox.accepted.connect(self.emit_categories_and_close)
        self.verticalLayout.addWidget(self.buttonBox)

    def _get_type_categories(self) -> list[str]:
        # Retrieve the selected categories from the checkboxes
        return [
            check_box.text()
            for check_box in self.centralWidget.findChildren(QCheckBox)
            if check_box.isChecked()
        ]

    def emit_categories_and_close(self) -> None:
        # Get the selected categories using _get_type_categories
        list_categories = self._get_type_categories()
        # Emit the selected categories as a signal
        self.categories_selected.emit(list_categories)
        # Close the dialog window
        super().close()
