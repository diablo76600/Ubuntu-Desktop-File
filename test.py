
#!/usr/bin/env python
from pathlib import PurePath
from textwrap import dedent
import sys
try:
    from PySide6.QtWidgets import (
        QApplication, QMainWindow, QDialogButtonBox,
        QGroupBox, QLineEdit, QFormLayout,
        QDataWidgetMapper, QVBoxLayout, QHBoxLayout,
        QWidget, QComboBox
    )
    from PySide6.QtGui import QStandardItemModel, QIcon
    from PySide6.QtCore import Qt, QObject, Signal, QModelIndex, QCoreApplication, QLibraryInfo, QTranslator
except ImportError:
    print("ERREUR: installez pyside 6 !")
    exit(13)
 
"""
https://specifications.freedesktop.org/desktop-entry-spec/desktop-entry-spec-latest.html#recognized-keys
"""

TEMPLATE = {
    "exec" : {
        "msg": "Le fichier à exécuter",
        "type": 1
    },
    "name" : {
        "msg": "bruno",
        "type": 1
    },
    "icon": {
        "msg": "Fichier .png ou nom d'une icone dans notre thème",
        "type": 1
    },
    "comment": {
        "msg": "",
        "type": 1
    },
    "type" : {
        "msg": ("Application","Link","Directory"),
        "type": 2
    },
    "path" : {
        "msg": "",
        "type": 1
    },
    "categories" : {
        "msg": ["Development","System", "Utility"],
        "type": 3
    },
}

"""
voir la fonction test() pour l'écrire/mini test de cette classe (app -t)
"""
class Work(QObject):
 
    onchange = Signal(int, str)  # pour GUI refresh
 
    def __init__(self) -> None:
        super().__init__()
        self.error = ""
        self._exec = ""
        self.type = ""
        self.name = ""
        self.comment = ""
        self._icon = ""
        self.path = ""
        self.categories = []
        self.type = "Application"
 
    @property
    def exec(self):
        return self._exec
    @exec.setter
    def exec(self, value):
        self.error = ""
        self._exec = value
        path = None
        if not self.name:
            path = PurePath(self.exec)
            self.name = path.stem
            self.onchange.emit(self.key_to_int("name"), "name")
        if not self.icon and self.name:
            self.icon = self.name
 
    @property
    def icon(self):
        return self._icon
    @icon.setter
    def icon(self, value):
        self.error = ""
        if value:
            ico = QIcon.fromTheme(value)
            if ico.isNull():
                self.error = "icone non trouvée dans le theme courant"
                return
        self._icon = value
        self.onchange.emit(self.key_to_int("icon"), "icon")
 
    def __str__(self) -> str:
        return dedent(
            f"""
                [Desktop Entry]
                Type={self.type}
                Name={self.name}
                Comment={self.comment}
                Exec={self.exec}
                Icon={self.icon}
 
                # erreur: {self.error}
            """
        )
 
    @staticmethod
    def key_to_int(key):
        return list(TEMPLATE.keys()).index(key)
 
 
class FormModel(QStandardItemModel):
    """ interface QT liée a mon métier """
    cols = tuple(k for k in TEMPLATE)
    error = Signal(str)
 
    def __init__(self, parent):
        super().__init__(1, len(TEMPLATE), parent=parent)
        self._datas = Work()
        self._datas.onchange.connect(self.onUpdate)
 
    def data(self , index , role):
        if not index.isValid():
            return
        if role in (Qt.EditRole, Qt.DisplayRole):
            """ texte par défaut à l'édition """
            key = self.cols[index.column()]
            return getattr(self._datas, key)
        if role == Qt.UserRole:
            return self.cols[index.column()]
        return super().data(index, role)
 
    def setData(self, index, value, role) -> bool:
        if not index.isValid():
            return
        if role == Qt.EditRole:
            self._datas.error = "" #puisque un seul setter existe dans la classe Work
            key = self.cols[index.column()]
            setattr(self._datas, key, value)
            self.error.emit(self._datas.error or "")
            return True
        return False
 
    def onUpdate(self, col, key):
        self.beginResetModel()
        index = self.index(0, col, QModelIndex())
        self.dataChanged.emit(index, index, Qt.DisplayRole)
        self.endResetModel()
 
 
class MainWin(QMainWindow):
    """ fenetre principale """
 
    def __init__(self):
        super().__init__()
        self.resize(790, 50)
        self.setWindowTitle("model Qt lié a model classique python")
        self.edits = {}
        for key in TEMPLATE.keys():
            if TEMPLATE[key]["type"] != 2:
                self.edits[key] = QLineEdit()
            else:
                self.edits[key] = QComboBox()
                self.edits[key].addItems(TEMPLATE[key]["msg"])
            self.edits[key].setPlaceholderText(str(TEMPLATE[key]["msg"]))

        btnWidget = QWidget()
        layout = QHBoxLayout()
        savetBtn = QDialogButtonBox(QDialogButtonBox.StandardButton.Save)
        exitBtn = QDialogButtonBox(QDialogButtonBox.StandardButton.Close)
        savetBtn.clicked.connect(self.save_file)
        exitBtn.clicked.connect(self.close)
        layout.addWidget(savetBtn, stretch=1, alignment=Qt.AlignmentFlag.AlignRight)
        layout.addWidget(exitBtn)
        btnWidget.setLayout(layout)

        self.formGroupBox = QGroupBox("Données")
        self.form = QFormLayout()
        for key in TEMPLATE.keys():
            self.form.addRow(
                f"{key.capitalize()} :",
                self.edits[key]
            )
        self.formGroupBox.setLayout(self.form)

        mainLayout = QVBoxLayout()
        mainLayout.addWidget(self.formGroupBox)
        mainLayout.addWidget(btnWidget)

        widget = QWidget()
        widget.setLayout(mainLayout)
        self.setCentralWidget(widget)
        self.statusBar()
        self._setupModel()

    def _setupModel(self):
        self.model = FormModel(self)
        self.model.error.connect(self.onError)
        self.model.dataChanged.connect(self.onDataChanged)
        self.mapper = QDataWidgetMapper()
        self.mapper.setModel(self.model)
        self.model.modelReset.connect(self.mapper.toFirst)
        for i, key in enumerate(TEMPLATE.keys()):
            self.mapper.addMapping(self.edits[key], i)
        self.mapper.toFirst()

    def onError(self, msg):
        self.statusBar().showMessage(msg)

    def onDataChanged(self, item, _):
        print("maj de", item.data(Qt.UserRole))
        if item.column() == 2:
            ico = item.data(Qt.DisplayRole)
            if ico:
                QApplication.setWindowIcon(QIcon.fromTheme(item.data(Qt.DisplayRole)))
 
    def save_file(self):
        print(self.model._datas)
 
app = None
def run():
    """gui"""
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon.fromTheme("desktop"))
    trans = QTranslator()
    trans.load('qt_fr', QLibraryInfo.path(QLibraryInfo.LibraryPath.TranslationsPath))
    QCoreApplication.installTranslator(trans)    # dialogues/btn en fr
 
    win = MainWin()
    win.show()
    sys.exit(app.exec())
 
 
def test():
    """ si on ne travaille que sur la classe métier """
    work = Work()
    work.exec = "pacman"
    print(work)
    work.exec = "/usr/bin/pacman.sh"
    print(work)
    exit(0)
 
if __name__ == "__main__":
    if "-t" in sys.argv:
        test()
    run()