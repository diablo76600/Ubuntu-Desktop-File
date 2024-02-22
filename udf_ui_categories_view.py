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
        self.verticalLayoutWidget = QWidget(self)
        self.verticalLayoutWidget.setGeometry(QRect(0, 0, 602, 207))
        self.verticalLayout = QVBoxLayout(self.verticalLayoutWidget)
        self.gridLayout_checkbox = QGridLayout()
        #
        for index, category in enumerate(self.CATEGORIES):
            row, col = divmod(index, 5)
            checkbox = QCheckBox(self.verticalLayoutWidget)
            checkbox.setText(category)
            self.gridLayout_checkbox.addWidget(checkbox, row, col, 1, 1)
        #
        self.verticalLayout.addLayout(self.gridLayout_checkbox)
        self.buttonBox = QDialogButtonBox(self.verticalLayoutWidget)
        self.buttonBox.setStandardButtons(QDialogButtonBox.StandardButton.Ok)
        self.buttonBox.setCenterButtons(True)
        self.buttonBox.accepted.connect(self.emit_categories_and_close)
        self.verticalLayout.addWidget(self.buttonBox)

    def _get_type_categories(self) -> list[str]:
        # Retrieve the selected categories from the checkboxes
        return [
            check_box.text()
            for check_box in self.verticalLayoutWidget.findChildren(QCheckBox)
            if check_box.isChecked()
        ]

    def emit_categories_and_close(self) -> None:
        list_categories = self._get_type_categories()
        # Emit the selected categories as a signal
        self.categories_selected.emit(list_categories)
        super().close()
